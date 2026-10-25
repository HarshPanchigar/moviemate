import uuid
import hashlib
import datetime
import time
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Customer
from admin_panel.models import Movie, Cinema, Showtime, Booking, AdminActivityLog, SeatHold

def signup(request):
    if request.session.get("customer_id"):
        return redirect("dashboard")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        mobile = request.POST.get("mobile", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        ctx = {"full_name": full_name, "email": email, "mobile": mobile}

        if not full_name:
            messages.error(request, "Please enter your full name.")
            return render(request, "signup.html", ctx)

        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, "signup.html", ctx)

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "signup.html", ctx)

        if not mobile:
            messages.error(request, "Please enter your mobile number.")
            return render(request, "signup.html", ctx)

        if not password1:
            messages.error(request, "Please enter a password.")
            return render(request, "signup.html", ctx)

        if len(password1) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
            return render(request, "signup.html", ctx)

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html", ctx)

        customer = Customer.objects.create(
            full_name=full_name,
            email=email,
            mobile=mobile,
            password=make_password(password1),
            role='client'
        )
        request.session["customer_id"] = customer.id
        return redirect("dashboard")

    return render(request, "signup.html")

def login_view(request):
    if request.session.get("customer_id"):
        customer = Customer.objects.filter(id=request.session.get("customer_id")).first()
        if customer and customer.role == 'admin':
            return redirect("admin_panel:dashboard")
        return redirect("dashboard")

    login_error = None
    if request.method == "POST":
        email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        try:
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                request.session["customer_id"] = customer.id
                if customer.role == 'admin':
                    return redirect("admin_panel:dashboard")
                return redirect("dashboard")
            else:
                login_error = "Invalid email or password."
        except Customer.DoesNotExist:
            login_error = "Invalid email or password."

    return render(request, "login.html", {"login_error": login_error})

def logout_view(request):
    request.session.flush()
    return redirect("login")

def dashboard(request):
    customer_id = request.session.get("customer_id")
    customer = Customer.objects.filter(id=customer_id).first() if customer_id else None
    
    # 1. Hero Movies: Selected by admin (is_hero=True), fallback to latest active
    hero_movies = Movie.objects.filter(status='active', is_hero=True)
    if not hero_movies.exists():
        hero_movies = Movie.objects.filter(status='active').order_by('-created_at')[:3]

    # 2. This Week's Releases: Only movies added in the past 1 week (7 days)
    one_week_ago = timezone.now() - datetime.timedelta(days=7)
    this_week_movies = Movie.objects.filter(status='active', created_at__gte=one_week_ago).order_by('-created_at')

    # 3. All Movies: Complete active catalog
    all_movies = Movie.objects.filter(status='active').order_by('-created_at')

    context = {
        "customer": customer,
        "hero_movies": hero_movies,
        "this_week_movies": this_week_movies,
        "all_movies": all_movies
    }
    return render(request, "dashboard.html", context)


def movie_search_api(request):
    from django.http import JsonResponse
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'movies': []})
    
    matches = Movie.objects.filter(status='active', title__icontains=query)[:6]
    data = []
    for m in matches:
        data.append({
            'id': m.id,
            'title': m.title,
            'genre': m.genre,
            'rating': float(m.rating),
            'poster_url': m.poster_url or 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba',
            'display_tag': m.get_display_tag_display(),
        })
    return JsonResponse({'movies': data})

# --- Booking System Flow ---

def select_theater(request, movie_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        messages.info(request, "Please log in to book tickets.")
        return redirect("login")
    
    from django.utils import timezone
    now = timezone.localtime()
    current_date = now.date()
    current_time = now.time()

    movie = get_object_or_404(Movie, id=movie_id)
    # Fetch all showtimes from today onwards
    raw_showtimes = Showtime.objects.filter(movie=movie, show_date__gte=current_date).select_related('cinema').order_by('show_date', 'start_time')
    
    # Filter out shows that have already ended today (or in the past)
    upcoming_showtimes = [
        st for st in raw_showtimes
        if st.show_date > current_date or (st.show_date == current_date and st.start_time > current_time)
    ]
    
    # Extract distinct show dates that have upcoming shows
    available_dates = sorted(list(set(st.show_date for st in upcoming_showtimes)))
    
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        from datetime import datetime
        try:
            sel_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            showtimes = [st for st in upcoming_showtimes if st.show_date == sel_date]
        except ValueError:
            showtimes = upcoming_showtimes
    else:
        selected_date_str = str(available_dates[0]) if available_dates else str(current_date)
        showtimes = [st for st in upcoming_showtimes if str(st.show_date) == selected_date_str]

    # Extract unique cinemas available for this movie on the selected date
    unique_cinemas = []
    seen_ids = set()
    for st in showtimes:
        if st.cinema.id not in seen_ids:
            seen_ids.add(st.cinema.id)
            cinema_obj = st.cinema
            cinema_obj.showtime_list = [s for s in showtimes if s.cinema_id == st.cinema.id]
            unique_cinemas.append(cinema_obj)

    context = {
        'movie': movie,
        'cinemas': unique_cinemas,
        'available_dates': available_dates,
        'selected_date_str': selected_date_str,
        'has_ended_today': (selected_date_str == str(current_date) and len(showtimes) == 0)
    }
    return render(request, "select_theater.html", context)

def select_showtime(request, movie_id, cinema_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    movie = get_object_or_404(Movie, id=movie_id)
    cinema = get_object_or_404(Cinema, id=cinema_id)
    
    from django.utils import timezone
    now = timezone.localtime()
    current_date = now.date()
    current_time = now.time()

    selected_date_str = request.GET.get('date')
    raw_showtimes = Showtime.objects.filter(movie=movie, cinema=cinema, show_date__gte=current_date).order_by('show_date', 'start_time')
    
    # Filter out expired showtimes
    showtimes = [
        st for st in raw_showtimes
        if st.show_date > current_date or (st.show_date == current_date and st.start_time > current_time)
    ]
    
    if selected_date_str:
        from datetime import datetime
        try:
            sel_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            showtimes = [st for st in showtimes if st.show_date == sel_date]
        except ValueError:
            pass

    context = {
        'movie': movie,
        'cinema': cinema,
        'showtimes': showtimes,
        'selected_date_str': selected_date_str
    }
    return render(request, "select_showtime.html", context)

def get_booked_seats(showtime_id):
    """Return set of uppercase seat codes confirmed in Bookings for this showtime."""
    bookings = Booking.objects.filter(showtime_id=showtime_id).values_list('seats', flat=True)
    booked = set()
    for s_str in bookings:
        if s_str:
            for s in s_str.split(','):
                clean_s = s.strip().upper()
                if clean_s:
                    booked.add(clean_s)
    return booked

def clean_expired_holds():
    """Remove expired seat holds across the system."""
    SeatHold.objects.filter(expires_at__lte=timezone.now()).delete()

def get_active_holds(showtime_id, exclude_customer_id=None):
    """Return set of uppercase seat codes currently held by other customers."""
    clean_expired_holds()
    qs = SeatHold.objects.filter(showtime_id=showtime_id, expires_at__gt=timezone.now())
    if exclude_customer_id:
        qs = qs.exclude(customer_id=exclude_customer_id)
    return set(s.upper() for s in qs.values_list('seat_code', flat=True))

def select_seats(request, showtime_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    # Block access if showtime has already ended or started
    now = timezone.localtime()
    if showtime.show_date < now.date() or (showtime.show_date == now.date() and showtime.start_time <= now.time()):
        messages.error(request, "This showtime has already ended or started. Please choose an upcoming showtime.")
        return redirect("select_theater", movie_id=showtime.movie.id)
    
    clean_expired_holds()
    confirmed_seats = get_booked_seats(showtime.id)
    other_held_seats = get_active_holds(showtime.id, exclude_customer_id=customer_id)
    unavailable_seats = list(confirmed_seats | other_held_seats)

    # Construct clean, proportional, symmetric seat rows with center aisle
    platinum_rows = [
        {'row': 'A', 'left_seats': ['A1', 'A2', 'A3', 'A4'], 'right_seats': ['A5', 'A6', 'A7', 'A8']},
        {'row': 'B', 'left_seats': ['B1', 'B2', 'B3', 'B4'], 'right_seats': ['B5', 'B6', 'B7', 'B8']},
    ]
    gold_rows = [
        {'row': 'C', 'left_seats': ['C1', 'C2', 'C3', 'C4', 'C5'], 'right_seats': ['C6', 'C7', 'C8', 'C9', 'C10']},
        {'row': 'D', 'left_seats': ['D1', 'D2', 'D3', 'D4', 'D5'], 'right_seats': ['D6', 'D7', 'D8', 'D9', 'D10']},
        {'row': 'E', 'left_seats': ['E1', 'E2', 'E3', 'E4', 'E5'], 'right_seats': ['E6', 'E7', 'E8', 'E9', 'E10']},
    ]
    silver_rows = [
        {'row': 'F', 'left_seats': ['F1', 'F2', 'F3', 'F4', 'F5'], 'right_seats': ['F6', 'F7', 'F8', 'F9', 'F10']},
        {'row': 'G', 'left_seats': ['G1', 'G2', 'G3', 'G4', 'G5'], 'right_seats': ['G6', 'G7', 'G8', 'G9', 'G10']},
    ]

    context = {
        'showtime': showtime,
        'booked_seats': unavailable_seats,
        'confirmed_seats': list(confirmed_seats),
        'held_seats': list(other_held_seats),
        'platinum_rows': platinum_rows,
        'gold_rows': gold_rows,
        'silver_rows': silver_rows,
    }
    return render(request, "select_seats.html", context)

def seat_status_api(request, showtime_id):
    """
    Real-time API endpoint returning booked and currently held seats for a showtime.
    Polled periodically by select_seats.js to update seat availability live.
    """
    customer_id = request.session.get("customer_id")
    clean_expired_holds()
    confirmed = list(get_booked_seats(showtime_id))
    other_held = list(get_active_holds(showtime_id, exclude_customer_id=customer_id))
    unavailable = list(set(confirmed) | set(other_held))
    return JsonResponse({
        "status": "success",
        "confirmed_seats": confirmed,
        "held_seats": other_held,
        "unavailable_seats": unavailable
    })

def release_seat_hold(request, showtime_id):
    """Release active seat holds when customer changes seats or cancels checkout."""
    customer_id = request.session.get("customer_id")
    if customer_id:
        SeatHold.objects.filter(customer_id=customer_id, showtime_id=showtime_id).delete()
    return redirect("select_seats", showtime_id=showtime_id)

def process_payment(request, showtime_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = get_object_or_404(Customer, id=customer_id)
    showtime = get_object_or_404(Showtime, id=showtime_id)

    def calc_seats_total(seats_str, fallback_tier):
        seat_list = [s.strip().upper() for s in seats_str.split(',') if s.strip()]
        if not seat_list:
            return 0, fallback_tier
        
        total = 0
        primary_tier = fallback_tier
        for seat in seat_list:
            row = seat[0] if len(seat) > 0 else ''
            if row in ('A', 'B'):
                total += float(showtime.platinum_price)
                primary_tier = 'platinum'
            elif row in ('C', 'D', 'E'):
                total += float(showtime.gold_price)
                primary_tier = 'gold'
            elif row in ('F', 'G'):
                total += float(showtime.silver_price)
                primary_tier = 'silver'
            else:
                if fallback_tier == 'platinum':
                    total += float(showtime.platinum_price)
                elif fallback_tier == 'silver':
                    total += float(showtime.silver_price)
                else:
                    total += float(showtime.gold_price)
        return total, primary_tier

    HOLD_MINUTES = 8

    if request.method == "POST":
        raw_tier = request.POST.get("seat_tier") or request.POST.get("tier", "gold")
        seats = request.POST.get("seats", "").strip()
        seat_list = [s.strip().upper() for s in seats.split(',') if s.strip()]

        if not seat_list:
            messages.error(request, "No seats selected. Please select at least one seat.")
            return redirect("select_seats", showtime_id=showtime.id)

        # ATOMIC TRANSACTION LOCKING TO PREVENT DOUBLE BOOKING RACE CONDITIONS
        with transaction.atomic():
            locked_showtime = Showtime.objects.select_for_update().get(id=showtime.id)
            clean_expired_holds()

            # 1. Verify none of the seats are already booked
            confirmed_booked = get_booked_seats(locked_showtime.id)
            booked_conflicts = [s for s in seat_list if s in confirmed_booked]
            if booked_conflicts:
                SeatHold.objects.filter(customer=customer, showtime=locked_showtime).delete()
                conflict_names = ", ".join(booked_conflicts)
                messages.error(request, f"Seat collision detected! Seat(s) {conflict_names} were already booked by another customer. Please choose different seats.")
                return redirect("select_seats", showtime_id=showtime.id)

            # 2. Verify none of the seats are held by ANOTHER customer
            other_holds = get_active_holds(locked_showtime.id, exclude_customer_id=customer.id)
            hold_conflicts = [s for s in seat_list if s in other_holds]
            if hold_conflicts:
                conflict_names = ", ".join(hold_conflicts)
                messages.error(request, f"Seat(s) {conflict_names} are currently on hold for another customer completing payment. Please choose different seats.")
                return redirect("select_seats", showtime_id=showtime.id)

            # 3. Passed all checks - proceed with booking creation
            clean_seats_str = ", ".join(seat_list)
            total_amount, seat_tier = calc_seats_total(clean_seats_str, raw_tier)

            raw_payload = f"MM-{customer.id}-{locked_showtime.id}-{uuid.uuid4().hex[:8]}"
            qr_hash = hashlib.sha256(raw_payload.encode()).hexdigest()[:16].upper()

            booking = Booking.objects.create(
                customer=customer,
                showtime=locked_showtime,
                seats=clean_seats_str,
                seat_tier=seat_tier,
                total_amount=total_amount,
                payment_status='paid',
                qr_code_hash=qr_hash
            )

            # Release all temporary holds for this customer on this showtime
            SeatHold.objects.filter(customer=customer, showtime=locked_showtime).delete()

            AdminActivityLog.objects.create(
                action=f"Client '{customer.full_name}' booked {clean_seats_str} for '{locked_showtime.movie.title}' (₹{total_amount})",
                performed_by=customer.full_name
            )

        messages.success(request, "Payment successful! Your tickets have been confirmed.")
        return redirect("booking_confirmation", booking_id=booking.booking_id)

    # GET request: User navigated from seat selection to checkout page
    raw_tier = request.GET.get("seat_tier") or request.GET.get("tier", "gold")
    seats_str = request.GET.get("seats", "").strip()
    seat_list = [s.strip().upper() for s in seats_str.split(',') if s.strip()]

    if not seat_list:
        messages.error(request, "Please select at least one seat before proceeding to payment.")
        return redirect("select_seats", showtime_id=showtime.id)

    with transaction.atomic():
        locked_showtime = Showtime.objects.select_for_update().get(id=showtime.id)

        # Check if customer previously held these seats and they already expired
        expired_user_holds = SeatHold.objects.filter(
            customer=customer,
            showtime=locked_showtime,
            seat_code__in=seat_list,
            expires_at__lte=timezone.now()
        )
        had_expired_user_holds = expired_user_holds.exists()

        clean_expired_holds()

        # Check if already booked
        confirmed_booked = get_booked_seats(locked_showtime.id)
        booked_conflicts = [s for s in seat_list if s in confirmed_booked]
        if booked_conflicts:
            conflict_names = ", ".join(booked_conflicts)
            messages.error(request, f"Sorry, seat(s) {conflict_names} have already been booked. Please choose different seats.")
            return redirect("select_seats", showtime_id=showtime.id)

        # Check if held by someone else
        other_holds = get_active_holds(locked_showtime.id, exclude_customer_id=customer.id)
        hold_conflicts = [s for s in seat_list if s in other_holds]
        if hold_conflicts:
            conflict_names = ", ".join(hold_conflicts)
            messages.error(request, f"Seat(s) {conflict_names} are currently reserved by another customer. Please choose different seats.")
            return redirect("select_seats", showtime_id=showtime.id)

        # Check for active holds for this customer on these requested seats
        existing_customer_holds = list(SeatHold.objects.filter(
            customer=customer,
            showtime=locked_showtime,
            seat_code__in=seat_list,
            expires_at__gt=timezone.now()
        ))

        existing_held_seats = {h.seat_code.upper() for h in existing_customer_holds}
        requested_seat_set = set(seat_list)

        if existing_customer_holds and requested_seat_set.issubset(existing_held_seats):
            # Page refresh / revisit during an active reservation:
            # Preserve the existing expiry so the timer continues and does NOT restart!
            min_expiry = min(h.expires_at for h in existing_customer_holds)
            remaining_seconds = int((min_expiry - timezone.now()).total_seconds())

            if remaining_seconds <= 0:
                SeatHold.objects.filter(customer=customer, showtime=locked_showtime).delete()
                messages.error(request, "Your seat reservation session has expired. Please select your seats again.")
                return redirect("select_seats", showtime_id=showtime.id)
        elif had_expired_user_holds and not existing_customer_holds:
            # The reservation expired
            messages.error(request, "Your seat reservation session has expired. Please select your seats again.")
            return redirect("select_seats", showtime_id=showtime.id)
        else:
            # New reservation or modified seat selection
            # Release any previous holds on other seats for this showtime
            SeatHold.objects.filter(customer=customer, showtime=locked_showtime).exclude(seat_code__in=seat_list).delete()

            # If customer already had an ongoing active reservation session for this showtime,
            # preserve the remaining time from that session so changing seats doesn't grant a fresh 8 min:
            active_holds = list(SeatHold.objects.filter(
                customer=customer,
                showtime=locked_showtime,
                expires_at__gt=timezone.now()
            ))
            if active_holds:
                min_expiry = min(h.expires_at for h in active_holds)
                remaining_seconds = int((min_expiry - timezone.now()).total_seconds())
                if remaining_seconds <= 0:
                    SeatHold.objects.filter(customer=customer, showtime=locked_showtime).delete()
                    messages.error(request, "Your seat reservation session has expired. Please select your seats again.")
                    return redirect("select_seats", showtime_id=showtime.id)
            else:
                min_expiry = timezone.now() + datetime.timedelta(minutes=HOLD_MINUTES)
                remaining_seconds = HOLD_MINUTES * 60

            for seat_code in seat_list:
                SeatHold.objects.update_or_create(
                    showtime=locked_showtime,
                    seat_code=seat_code,
                    defaults={'customer': customer, 'expires_at': min_expiry}
                )

    clean_seats_str = ", ".join(seat_list)
    total_amount, tier = calc_seats_total(clean_seats_str, raw_tier)

    mins = max(0, remaining_seconds) // 60
    secs = max(0, remaining_seconds) % 60
    timer_display = f"{mins:02d}:{secs:02d}"

    context = {
        'customer': customer,
        'showtime': showtime,
        'tier': tier,
        'seats': clean_seats_str,
        'total_amount': total_amount,
        'hold_expires_in_seconds': max(0, remaining_seconds),
        'timer_display': timer_display,
    }
    return render(request, "payment.html", context)

def booking_confirmation(request, booking_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    
    booking = get_object_or_404(Booking, booking_id=booking_id, customer__id=customer_id)
    return render(request, "booking_confirmation.html", {"booking": booking})

def my_bookings(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    
    customer = get_object_or_404(Customer, id=customer_id)
    all_bookings = Booking.objects.filter(customer=customer).select_related('showtime__movie', 'showtime__cinema').order_by('-created_at')
    
    upcoming_bookings = [b for b in all_bookings if not b.is_past]
    past_bookings = [b for b in all_bookings if b.is_past]

    return render(request, "my_bookings.html", {
        "upcoming_bookings": upcoming_bookings,
        "past_bookings": past_bookings,
        "all_bookings": all_bookings,
        "customer": customer
    })

# --- Profile Management ---

def profile_view(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")
    
    # Fetch logged-in user's personal booking notifications
    user_bookings = Booking.objects.filter(customer=customer).select_related('showtime__movie', 'showtime__cinema').order_by('-created_at')[:6]

    return render(request, "profile.html", {
        "customer": customer,
        "user_bookings": user_bookings
    })

def edit_profile(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")

        if Customer.objects.filter(email=email).exclude(id=customer.id).exists():
            messages.error(request, "This email address is already registered.")
            return render(request, "edit_profile.html", {"customer": customer})

        customer.full_name = full_name
        customer.email = email
        customer.mobile = mobile
        customer.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect("profile")

    return render(request, "edit_profile.html", {"customer": customer})

def mask_email(email):
    """Returns a masked version of email, e.g. ha*****ar@gmail.com"""
    if not email or "@" not in email:
        return email
    name_part, domain_part = email.split("@", 1)
    if len(name_part) <= 2:
        masked_name = name_part[0] + "*"
    elif len(name_part) <= 4:
        masked_name = name_part[0] + "**" + name_part[-1]
    else:
        masked_name = name_part[:2] + ("*" * (len(name_part) - 4)) + name_part[-2:]
    return f"{masked_name}@{domain_part}"

def send_password_change_otp_email(customer, otp_code, expires_minutes=10, request=None):
    """
    Sends a sleek, minimalist Apple Dark Theme verification email via Gmail SMTP.
    Returns (success: bool, message: str)
    """
    subject = f"{otp_code} is your MovieMate verification code"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'MovieMate Security <harshpanchigar@gmail.com>')
    to_email = customer.email

    app_pwd = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    is_placeholder = not app_pwd or 'PASTE_YOUR_16' in app_pwd

    if request:
        action_url = request.build_absolute_uri(f"/profile/change-password/?code={otp_code}")
    else:
        action_url = f"http://127.0.0.1:8000/profile/change-password/?code={otp_code}"

    # Clean, authentic, minimalist Apple Dark Theme HTML email
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your MovieMate Verification Code</title>
</head>
<body style="margin: 0; padding: 0; background-color: #000000; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #ffffff; -webkit-font-smoothing: antialiased;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #000000; padding: 48px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width: 460px; background-color: #0c0c0e; border: 1px solid #232328; border-radius: 16px; padding: 32px 28px; text-align: left; box-shadow: 0 16px 36px rgba(0,0,0,0.6);">
          <!-- Logo -->
          <tr>
            <td style="padding-bottom: 22px;">
              <span style="font-size: 18px; font-weight: 900; letter-spacing: 0.5px; color: #ffffff;">
                MOVIE<span style="color: #10b981;">MATE</span>
              </span>
            </td>
          </tr>

          <!-- Heading -->
          <tr>
            <td style="padding-bottom: 12px;">
              <h1 style="margin: 0; font-size: 21px; font-weight: 700; color: #ffffff; letter-spacing: -0.3px;">
                Verification code
              </h1>
            </td>
          </tr>

          <!-- Body Text -->
          <tr>
            <td style="padding-bottom: 22px;">
              <p style="margin: 0; font-size: 14px; line-height: 1.55; color: #a1a1aa;">
                Hi {customer.full_name},<br>
                Use this one-time code to complete your password change:
              </p>
            </td>
          </tr>

          <!-- Code Box with Copy Button -->
          <tr>
            <td style="padding-bottom: 24px;">
              <div style="background-color: #141418; border: 1px solid #27272f; border-radius: 12px; padding: 18px 20px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                  <tr>
                    <td style="vertical-align: middle;">
                      <span id="codeToCopy" style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 32px; font-weight: 800; letter-spacing: 6px; color: #10b981; -webkit-user-select: all; user-select: all; display: inline-block;">
                        {otp_code}
                      </span>
                    </td>
                    <td align="right" style="vertical-align: middle;">
                      <a href="{action_url}" onclick="if(navigator.clipboard){{navigator.clipboard.writeText('{otp_code}');alert('Verification code copied!');}}" style="display: inline-block; background-color: #10b981; color: #000000; font-size: 13px; font-weight: 700; text-decoration: none; padding: 9px 16px; border-radius: 8px; white-space: nowrap;">
                        Copy Code
                      </a>
                    </td>
                  </tr>
                </table>
              </div>
            </td>
          </tr>

          <!-- Expiry Notice -->
          <tr>
            <td style="padding-bottom: 28px; border-bottom: 1px solid #1c1c21;">
              <p style="margin: 0 0 8px; font-size: 13px; color: #71717a; line-height: 1.5;">
                This code will expire in <strong style="color: #d4d4d8;">{expires_minutes} minutes</strong>.
              </p>
              <p style="margin: 0; font-size: 13px; color: #52525b; line-height: 1.5;">
                If you didn't request a password change, you can safely ignore this email.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding-top: 20px;">
              <p style="margin: 0; font-size: 12px; color: #52525b;">
                MovieMate Cinemas &bull; Automated Security
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    plain_content = f"""Hi {customer.full_name},

Your MovieMate password verification code is:

{otp_code}

This code will expire in {expires_minutes} minutes.
If you didn't request this change, you can safely ignore this email.

— MovieMate Team
"""

    if is_placeholder:
        print("\n" + "="*70)
        print("[MOVIEMATE EMAIL NOTIFICATION] Google App Password not configured yet.")
        print(f"Recipient: {customer.email}")
        print(f"Verification OTP Code: {otp_code} (Valid for {expires_minutes} minutes)")
        print("To send real emails, paste your 16-character Google App Password in settings.py or .env")
        print("="*70 + "\n")
        return (True, "dev_mode")

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_content,
            from_email=from_email,
            to=[to_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        return (True, "sent")
    except Exception as exc:
        print(f"[MOVIEMATE EMAIL ERROR] Failed to send email to {customer.email}: {exc}")
        return (False, str(exc))

def send_password_change_otp(request):
    """
    AJAX / POST endpoint to validate credentials and send an OTP to the customer's email.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed."}, status=405)

    customer_id = request.session.get("customer_id")
    if not customer_id:
        return JsonResponse({"success": False, "message": "Please log in to continue."}, status=401)

    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        return JsonResponse({"success": False, "message": "Customer record not found."}, status=404)

    current_password = request.POST.get("current_password", "").strip()
    new_password = request.POST.get("new_password", "").strip()
    confirm_password = request.POST.get("confirm_password", "").strip()

    # Pre-validation: User must enter their current password first
    if not current_password:
        return JsonResponse({"success": False, "message": "Please enter your current password first."}, status=400)

    if not check_password(current_password, customer.password):
        return JsonResponse({"success": False, "message": "Your current password is incorrect."}, status=400)

    # Validate new password rules if already entered
    if new_password:
        if len(new_password) < 8:
            return JsonResponse({"success": False, "message": "New password must be at least 8 characters long."}, status=400)
        if confirm_password and new_password != confirm_password:
            return JsonResponse({"success": False, "message": "New passwords do not match."}, status=400)
        if check_password(new_password, customer.password):
            return JsonResponse({"success": False, "message": "New password must be different from your current password."}, status=400)

    # 60-second cooldown protection against spamming
    now = time.time()
    existing_otp = request.session.get("password_change_otp")
    if existing_otp and (now - existing_otp.get("last_sent_at", 0) < 60):
        wait_seconds = int(60 - (now - existing_otp["last_sent_at"]))
        return JsonResponse({
            "success": False,
            "message": f"Please wait {wait_seconds} seconds before requesting another code.",
            "cooldown": wait_seconds
        }, status=429)

    # Generate secure 6-digit OTP
    otp_code = str(secrets.randbelow(900000) + 100000)
    expires_minutes = 10
    expires_at = now + (expires_minutes * 60)

    # Save to session
    request.session["password_change_otp"] = {
        "code": otp_code,
        "created_at": now,
        "expires_at": expires_at,
        "last_sent_at": now,
        "attempts": 0,
        "customer_id": customer.id,
        "email": customer.email,
    }
    request.session.modified = True

    # Send email
    sent_ok, result = send_password_change_otp_email(customer, otp_code, expires_minutes=expires_minutes, request=request)
    masked = mask_email(customer.email)

    if not sent_ok:
        return JsonResponse({
            "success": False,
            "message": f"Unable to send verification email. Please check your Gmail App Password configuration in settings.py: {result}"
        }, status=500)

    message = f"A 6-digit verification code has been sent to {masked}."
    if result == "dev_mode":
        message += " (Check your terminal console for the development code)"

    return JsonResponse({
        "success": True,
        "message": message,
        "masked_email": masked,
        "cooldown": 60,
        "expires_in": expires_minutes * 60
    })

def change_password(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")

    masked = mask_email(customer.email)
    session_otp = request.session.get("password_change_otp")
    now = time.time()
    otp_active = bool(session_otp and session_otp.get("customer_id") == customer.id and now < session_otp.get("expires_at", 0))

    if request.method == "POST":
        current_password = request.POST.get("current_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        entered_otp = request.POST.get("otp", "").strip()

        # 1. Validate inputs
        if not current_password or not new_password or not confirm_password:
            messages.error(request, "Please fill in all required password fields.")
            return redirect("change_password")

        if not check_password(current_password, customer.password):
            messages.error(request, "Your current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("change_password")

        if check_password(new_password, customer.password):
            messages.error(request, "New password must be different from your current password.")
            return redirect("change_password")

        # 2. Validate OTP presence
        if not session_otp or session_otp.get("customer_id") != customer.id:
            messages.error(request, f"Please click 'Send Verification Code' to authenticate your email ({masked}) before changing password.")
            return redirect("change_password")

        # 3. Check OTP expiration (10 minutes)
        if now > session_otp.get("expires_at", 0):
            if "password_change_otp" in request.session:
                del request.session["password_change_otp"]
                request.session.modified = True
            messages.error(request, "The verification code has expired. Please request a new code.")
            return redirect("change_password")

        # 4. Check brute-force attempts (limit to 5 attempts)
        attempts = session_otp.get("attempts", 0)
        if attempts >= 5:
            if "password_change_otp" in request.session:
                del request.session["password_change_otp"]
                request.session.modified = True
            messages.error(request, "Too many incorrect code attempts. For security, this code was invalidated. Please request a new code.")
            return redirect("change_password")

        # 5. Check OTP match
        if not entered_otp:
            messages.error(request, "Please enter the 6-digit verification code sent to your email.")
            return redirect("change_password")

        if entered_otp != str(session_otp.get("code")):
            session_otp["attempts"] = attempts + 1
            request.session.modified = True
            remaining = 5 - session_otp["attempts"]
            if remaining <= 0:
                del request.session["password_change_otp"]
                request.session.modified = True
                messages.error(request, "Too many incorrect attempts. Code invalidated. Please request a new code.")
            else:
                messages.error(request, f"Invalid verification code. {remaining} attempt{'s' if remaining > 1 else ''} remaining.")
            return redirect("change_password")

        # 6. All authentications passed - update password
        customer.password = make_password(new_password)
        customer.save()

        # Invalidate OTP from session
        if "password_change_otp" in request.session:
            del request.session["password_change_otp"]
            request.session.modified = True

        # Log to activity log
        try:
            AdminActivityLog.objects.create(
                action=f"Client '{customer.full_name}' changed password with email OTP verification",
                performed_by=customer.full_name
            )
        except Exception:
            pass

        messages.success(request, "Your password has been changed successfully. You can now use your new password.")
        return redirect("profile")

    return render(request, "change_password.html", {
        "customer": customer,
        "masked_email": masked,
        "otp_active": otp_active,
        "otp_expires_in": max(0, int(session_otp.get("expires_at", 0) - now)) if otp_active else 0,
        "prefilled_otp": request.GET.get("code") or request.GET.get("otp") or ""
    })

def delete_account(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")

    if request.method == "POST":
        customer.delete()
        request.session.flush()
        return redirect("login")

    return render(request, "delete_account.html", {"customer": customer})