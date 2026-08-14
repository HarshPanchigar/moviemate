import uuid
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer
from admin_panel.models import Movie, Cinema, Showtime, Booking, AdminActivityLog

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

    # 2. This Week's Releases: new_release tag or recent created
    this_week_movies = Movie.objects.filter(status='active', display_tag='new_release').order_by('-created_at')
    if not this_week_movies.exists():
        this_week_movies = Movie.objects.filter(status='active').order_by('-created_at')

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
    
    from datetime import date
    today = date.today()

    movie = get_object_or_404(Movie, id=movie_id)
    all_showtimes = Showtime.objects.filter(movie=movie, show_date__gte=today).select_related('cinema').order_by('show_date', 'start_time')
    
    # Extract distinct show dates available (today & future only)
    available_dates = sorted(list(set(st.show_date for st in all_showtimes)))
    
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        from datetime import datetime
        try:
            sel_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            showtimes = all_showtimes.filter(show_date=sel_date)
        except ValueError:
            showtimes = all_showtimes
    else:
        selected_date_str = str(available_dates[0]) if available_dates else None
        showtimes = all_showtimes.filter(show_date=available_dates[0]) if available_dates else all_showtimes

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
        'selected_date_str': selected_date_str
    }
    return render(request, "select_theater.html", context)

def select_showtime(request, movie_id, cinema_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    movie = get_object_or_404(Movie, id=movie_id)
    cinema = get_object_or_404(Cinema, id=cinema_id)
    
    selected_date_str = request.GET.get('date')
    showtimes = Showtime.objects.filter(movie=movie, cinema=cinema).order_by('show_date', 'start_time')
    if selected_date_str:
        from datetime import datetime
        try:
            sel_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            showtimes = showtimes.filter(show_date=sel_date)
        except ValueError:
            pass

    context = {
        'movie': movie,
        'cinema': cinema,
        'showtimes': showtimes,
        'selected_date_str': selected_date_str
    }
    return render(request, "select_showtime.html", context)

def select_seats(request, showtime_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    
    showtime = get_object_or_404(Showtime, id=showtime_id)
    
    # Existing booked seats for this showtime
    existing_bookings = Booking.objects.filter(showtime=showtime)
    booked_seats_list = []
    for b in existing_bookings:
        booked_seats_list.extend([s.strip() for s in b.seats.split(',') if s.strip()])

    # Construct clean seat matrix data
    platinum_rows = [
        {'row': 'A', 'seats': [f'A{i}' for i in range(1, 11)]},
        {'row': 'B', 'seats': [f'B{i}' for i in range(1, 11)]},
    ]
    gold_rows = [
        {'row': 'C', 'seats': [f'C{i}' for i in range(1, 13)]},
        {'row': 'D', 'seats': [f'D{i}' for i in range(1, 13)]},
        {'row': 'E', 'seats': [f'E{i}' for i in range(1, 13)]},
    ]
    silver_rows = [
        {'row': 'F', 'seats': [f'F{i}' for i in range(1, 13)]},
        {'row': 'G', 'seats': [f'G{i}' for i in range(1, 13)]},
    ]

    context = {
        'showtime': showtime,
        'booked_seats': booked_seats_list,
        'platinum_rows': platinum_rows,
        'gold_rows': gold_rows,
        'silver_rows': silver_rows,
    }
    return render(request, "select_seats.html", context)

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

    if request.method == "POST":
        raw_tier = request.POST.get("seat_tier") or request.POST.get("tier", "gold")
        seats = request.POST.get("seats", "A1, A2")
        total_amount, seat_tier = calc_seats_total(seats, raw_tier)

        # Generate unique verification hash payload for QR code
        raw_payload = f"MM-{customer.id}-{showtime.id}-{uuid.uuid4().hex[:8]}"
        qr_hash = hashlib.sha256(raw_payload.encode()).hexdigest()[:16].upper()

        booking = Booking.objects.create(
            customer=customer,
            showtime=showtime,
            seats=seats,
            seat_tier=seat_tier,
            total_amount=total_amount,
            payment_status='paid',
            qr_code_hash=qr_hash
        )

        AdminActivityLog.objects.create(
            action=f"Client '{customer.full_name}' booked {seats} for '{showtime.movie.title}' (₹{total_amount})",
            performed_by=customer.full_name
        )

        messages.success(request, "Payment successful! Ticket booked.")
        return redirect("booking_confirmation", booking_id=booking.booking_id)

    # GET request: Render payment gateway preview
    raw_tier = request.GET.get("seat_tier") or request.GET.get("tier", "gold")
    seats_str = request.GET.get("seats", "A1, A2")
    total_amount, tier = calc_seats_total(seats_str, raw_tier)

    context = {
        'customer': customer,
        'showtime': showtime,
        'tier': tier,
        'seats': seats_str,
        'total_amount': total_amount
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
    bookings = Booking.objects.filter(customer=customer).select_related('showtime__movie', 'showtime__cinema').order_by('-created_at')
    return render(request, "my_bookings.html", {"bookings": bookings, "customer": customer})

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

def change_password(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        request.session.flush()
        return redirect("login")

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

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

        customer.password = make_password(new_password)
        customer.save()
        messages.success(request, "Your password has been changed successfully.")
        return redirect("profile")

    return render(request, "change_password.html", {"customer": customer})

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