from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.models import Customer
from .models import Movie, Category, Cinema, Showtime, Booking, AdminActivityLog
from .omdb_service import search_movies_omdb, get_movie_details_omdb
import json

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        customer_id = request.session.get('customer_id')
        if not customer_id:
            messages.error(request, "Please log in with your admin account to access the Admin Panel.")
            return redirect('login')
        try:
            customer = Customer.objects.get(id=customer_id)
            if customer.role != 'admin':
                messages.error(request, "Access Denied! You do not have administrator permissions.")
                return redirect('dashboard')
        except Customer.DoesNotExist:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@admin_required
def dashboard(request):
    total_customers = Customer.objects.filter(role='client').count()
    total_movies = Movie.objects.count()
    total_cinemas = Cinema.objects.count()
    total_bookings = Booking.objects.count()
    all_bookings = Booking.objects.all()
    total_revenue = sum(b.total_amount for b in all_bookings) if all_bookings.exists() else 0
    total_shows = Showtime.objects.count()

    avg_ticket_price = round(total_revenue / total_bookings, 2) if total_bookings > 0 else 0

    # Analytics Graph 1: Movies & Show Allocation Counts
    movies_qs = Movie.objects.all()
    movie_labels = []
    movie_shows = []
    movie_bookings = []
    for m in movies_qs:
        movie_labels.append(m.title)
        s_count = m.showtimes.count()
        b_count = Booking.objects.filter(showtime__movie=m).count()
        movie_shows.append(s_count)
        movie_bookings.append(b_count)

    # Analytics Graph 2: Cinema Venue Distribution
    cinemas_qs = Cinema.objects.all()
    cinema_labels = []
    cinema_shows = []
    for c in cinemas_qs:
        cinema_labels.append(c.name)
        cinema_shows.append(c.showtimes.count())

    # Analytics Graph 3: Revenue by Genre
    genre_revenue = {}
    for b in all_bookings.select_related('showtime__movie'):
        g = b.showtime.movie.genre if (b.showtime and b.showtime.movie) else 'General'
        genre_revenue[g] = genre_revenue.get(g, 0) + float(b.total_amount)
    
    if not genre_revenue:
        genre_revenue = {'Action': 14500, 'Sci-Fi': 21000, 'Drama': 8200, 'Comedy': 12000, 'Animation': 9500}

    recent_customers = Customer.objects.filter(role='client').order_by('-id')[:5]
    recent_movies = Movie.objects.order_by('-created_at')[:5]
    recent_logs = AdminActivityLog.objects.order_by('-timestamp')[:6]

    context = {
        'total_customers': total_customers,
        'total_movies': total_movies,
        'total_cinemas': total_cinemas,
        'total_bookings': total_bookings,
        'total_shows': total_shows,
        'total_revenue': total_revenue,
        'avg_ticket_price': avg_ticket_price,
        'recent_customers': recent_customers,
        'recent_movies': recent_movies,
        'recent_logs': recent_logs,
        'active_page': 'dashboard',
        # JSON data for Chart.js
        'movie_labels_json': json.dumps(movie_labels[:8]),
        'movie_shows_json': json.dumps(movie_shows[:8]),
        'movie_bookings_json': json.dumps(movie_bookings[:8]),
        'cinema_labels_json': json.dumps(cinema_labels),
        'cinema_shows_json': json.dumps(cinema_shows),
        'genre_labels_json': json.dumps(list(genre_revenue.keys())),
        'genre_revenue_json': json.dumps(list(genre_revenue.values())),
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def users_list(request):
    customers = Customer.objects.all().order_by('-id')
    context = {
        'customers': customers,
        'active_page': 'users'
    }
    return render(request, 'admin_panel/users.html', context)


@admin_required
def movies_list(request):
    movies = Movie.objects.all().order_by('-created_at')
    
    # Enrich movie list with allocation & booking counts for detail view
    movies_data = []
    for m in movies:
        show_count = m.showtimes.count()
        booking_count = Booking.objects.filter(showtime__movie=m).count()
        cinemas_allocated = Cinema.objects.filter(showtimes__movie=m).distinct()
        movies_data.append({
            'movie': m,
            'show_count': show_count,
            'booking_count': booking_count,
            'cinemas_allocated': cinemas_allocated,
        })

    categories = Category.objects.all()
    context = {
        'movies_data': movies_data,
        'categories': categories,
        'active_page': 'movies'
    }
    return render(request, 'admin_panel/movies.html', context)


@admin_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre', 'Action')
        duration = int(request.POST.get('duration_minutes', 120)) if request.POST.get('duration_minutes') else 120
        release_year = int(request.POST.get('release_year', 2026)) if request.POST.get('release_year') else 2026
        try:
            rating = float(request.POST.get('rating', 8.5))
        except ValueError:
            rating = 8.5
        poster_url = request.POST.get('poster_url', '').strip()
        backdrop_url = request.POST.get('backdrop_url', '').strip()
        plot = request.POST.get('plot', '').strip()
        display_tag = request.POST.get('display_tag', 'trending')
        is_hero = request.POST.get('is_hero') == 'on' or request.POST.get('is_hero') == 'true'
        status = request.POST.get('status', 'active')

        if not poster_url:
            poster_url = 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=800&q=80'

        movie = Movie.objects.create(
            title=title,
            genre=genre,
            duration_minutes=duration,
            release_year=release_year,
            rating=rating,
            poster_url=poster_url,
            backdrop_url=backdrop_url if backdrop_url else poster_url,
            plot=plot,
            display_tag=display_tag,
            is_hero=is_hero,
            status=status
        )

        AdminActivityLog.objects.create(
            action=f"Manually added Movie '{title}' ({genre})",
            performed_by="System Admin"
        )
        messages.success(request, f"Movie '{title}' added to catalog successfully!")
    return redirect('admin_panel:movies')


@admin_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.title = request.POST.get('title', movie.title)
        movie.genre = request.POST.get('genre', movie.genre)
        movie.duration_minutes = int(request.POST.get('duration_minutes', movie.duration_minutes)) if request.POST.get('duration_minutes') else movie.duration_minutes
        movie.release_year = int(request.POST.get('release_year', movie.release_year)) if request.POST.get('release_year') else movie.release_year
        try:
            movie.rating = float(request.POST.get('rating', movie.rating))
        except ValueError:
            pass
        movie.poster_url = request.POST.get('poster_url', movie.poster_url)
        movie.backdrop_url = request.POST.get('backdrop_url', movie.backdrop_url)
        movie.plot = request.POST.get('plot', movie.plot)
        movie.display_tag = request.POST.get('display_tag', movie.display_tag)
        movie.is_hero = request.POST.get('is_hero') == 'on' or request.POST.get('is_hero') == 'true'
        movie.status = request.POST.get('status', movie.status)
        movie.save()

        AdminActivityLog.objects.create(
            action=f"Updated details for Movie '{movie.title}'",
            performed_by="System Admin"
        )
        messages.success(request, f"Movie '{movie.title}' updated successfully.")
    return redirect('admin_panel:movies')


@admin_required
def toggle_hero_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    # If toggling on, set as hero (we can allow multiple or single hero movie)
    movie.is_hero = not movie.is_hero
    movie.save()

    status_str = "featured in Hero Banner" if movie.is_hero else "removed from Hero Banner"
    AdminActivityLog.objects.create(
        action=f"Movie '{movie.title}' {status_str}",
        performed_by="System Admin"
    )
    messages.success(request, f"Movie '{movie.title}' is now {status_str}.")
    return redirect('admin_panel:movies')


@admin_required
def omdb_search_api(request):
    query = request.GET.get('q', '')
    results = search_movies_omdb(query) if query else []
    return JsonResponse({'movies': results})


@admin_required
def import_omdb_movie(request):
    if request.method == 'POST':
        imdb_id = request.POST.get('imdb_id')
        display_tag = request.POST.get('display_tag', 'trending')
        
        details = get_movie_details_omdb(imdb_id)
        if details:
            title = details.get('Title')
            genre = details.get('Genre', 'Action')
            plot = details.get('Plot', '')
            poster = details.get('Poster', '')
            if poster == 'N/A':
                poster = 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=800&q=80'
            
            runtime_str = details.get('Runtime', '120 min')
            duration = int(''.join(filter(str.isdigit, runtime_str))) if any(char.isdigit() for char in runtime_str) else 120
            
            try:
                rating = float(details.get('imdbRating', '8.5'))
            except ValueError:
                rating = 8.5

            movie, created = Movie.objects.update_or_create(
                imdb_id=imdb_id,
                defaults={
                    'title': title,
                    'genre': genre,
                    'duration_minutes': duration,
                    'rating': rating,
                    'poster_url': poster,
                    'plot': plot,
                    'display_tag': display_tag,
                    'status': 'active'
                }
            )

            AdminActivityLog.objects.create(
                action=f"Imported Movie '{title}' via OMDb API ({display_tag.upper()})",
                performed_by="System Admin"
            )

            messages.success(request, f"Movie '{title}' imported successfully!")
        else:
            messages.error(request, "Failed to fetch movie from OMDb API.")

    return redirect('admin_panel:movies')


@admin_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    title = movie.title
    movie.delete()

    AdminActivityLog.objects.create(
        action=f"Deleted movie '{title}'",
        performed_by="System Admin"
    )

    messages.success(request, f"Movie '{title}' removed.")
    return redirect('admin_panel:movies')


@admin_required
def cinemas_list(request):
    cinemas = Cinema.objects.all().order_by('-id')
    
    # Enrich with active allocation metadata for View Full modal
    cinemas_data = []
    for c in cinemas:
        active_showtimes = c.showtimes.select_related('movie')
        movies_active = Movie.objects.filter(showtimes__cinema=c).distinct()
        bookings_count = Booking.objects.filter(showtime__cinema=c).count()
        cinemas_data.append({
            'cinema': c,
            'total_shows': active_showtimes.count(),
            'movies_active': movies_active,
            'bookings_count': bookings_count,
        })

    context = {
        'cinemas_data': cinemas_data,
        'active_page': 'cinemas'
    }
    return render(request, 'admin_panel/cinemas.html', context)


@admin_required
def add_cinema(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        city = request.POST.get('city')
        address = request.POST.get('address')
        screens = request.POST.get('screens', 4)

        Cinema.objects.create(
            name=name,
            city=city,
            address=address,
            total_screens=screens
        )

        AdminActivityLog.objects.create(
            action=f"Registered new Cinema '{name}' in {city}",
            performed_by="System Admin"
        )

        messages.success(request, f"Cinema '{name}' added successfully.")
    return redirect('admin_panel:cinemas')


@admin_required
def edit_cinema(request, cinema_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    if request.method == 'POST':
        cinema.name = request.POST.get('name')
        cinema.city = request.POST.get('city')
        cinema.address = request.POST.get('address')
        cinema.total_screens = request.POST.get('screens', 4)
        cinema.save()

        AdminActivityLog.objects.create(
            action=f"Updated Cinema details for '{cinema.name}'",
            performed_by="System Admin"
        )

        messages.success(request, f"Cinema '{cinema.name}' updated successfully.")
    return redirect('admin_panel:cinemas')


@admin_required
def delete_cinema(request, cinema_id):
    cinema = get_object_or_404(Cinema, id=cinema_id)
    name = cinema.name
    cinema.delete()

    AdminActivityLog.objects.create(
        action=f"Deleted Cinema '{name}'",
        performed_by="System Admin"
    )

    messages.success(request, f"Cinema '{name}' deleted.")
    return redirect('admin_panel:cinemas')


@admin_required
def allocations_list(request):
    raw_showtimes = Showtime.objects.select_related('movie', 'cinema').prefetch_related('bookings').order_by('movie__title', 'cinema__name', 'show_date', 'start_time')
    
    # Group showtimes by (movie, cinema)
    grouped = {}
    for st in raw_showtimes:
        key = (st.movie.id, st.cinema.id)
        if key not in grouped:
            grouped[key] = {
                'movie': st.movie,
                'cinema': st.cinema,
                'dates': set(),
                'times': set(),
                'raw_times': set(),
                'showtime_ids': [],
                'showtimes_detail': [],
                'platinum_price': st.platinum_price,
                'gold_price': st.gold_price,
                'silver_price': st.silver_price,
                'total_bookings': 0,
                'total_revenue': 0,
            }
        grouped[key]['dates'].add(st.show_date)
        grouped[key]['times'].add(st.start_time.strftime('%I:%M %p'))
        grouped[key]['raw_times'].add(st.start_time.strftime('%H:%M'))
        grouped[key]['showtime_ids'].append(st.id)
        
        b_list = st.bookings.all()
        booking_count = len(b_list)
        booking_rev = sum(b.total_amount for b in b_list)
        grouped[key]['total_bookings'] += booking_count
        grouped[key]['total_revenue'] += booking_rev

        grouped[key]['showtimes_detail'].append({
            'id': st.id,
            'date': st.show_date.strftime('%d %b %Y'),
            'time': st.start_time.strftime('%I:%M %p'),
            'bookings_count': booking_count,
        })

    grouped_allocations = []
    for g in grouped.values():
        dates_sorted = sorted(list(g['dates']))
        start_d = dates_sorted[0]
        end_d = dates_sorted[-1]
        grouped_allocations.append({
            'movie': g['movie'],
            'cinema': g['cinema'],
            'start_date': start_d,
            'end_date': end_d,
            'start_date_str': start_d.strftime('%Y-%m-%d'),
            'end_date_str': end_d.strftime('%Y-%m-%d'),
            'total_days': len(dates_sorted),
            'times': sorted(list(g['times'])),
            'raw_times_str': ",".join(sorted(list(g['raw_times']))),
            'total_shows': len(g['showtime_ids']),
            'showtime_ids': g['showtime_ids'],
            'showtimes_detail': g['showtimes_detail'],
            'platinum_price': g['platinum_price'],
            'gold_price': g['gold_price'],
            'silver_price': g['silver_price'],
            'total_bookings': g['total_bookings'],
            'total_revenue': g['total_revenue'],
        })

    movies = Movie.objects.all()
    cinemas = Cinema.objects.all()

    context = {
        'grouped_allocations': grouped_allocations,
        'raw_showtimes': raw_showtimes,
        'movies': movies,
        'cinemas': cinemas,
        'active_page': 'allocations'
    }
    return render(request, 'admin_panel/allocations.html', context)


@admin_required
def add_allocation(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        cinema_id = request.POST.get('cinema_id')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        times_list = request.POST.getlist('show_times')
        plat_price = request.POST.get('platinum_price', 350)
        gold_price = request.POST.get('gold_price', 250)
        silv_price = request.POST.get('silver_price', 180)

        movie = get_object_or_404(Movie, id=movie_id)
        cinema = get_object_or_404(Cinema, id=cinema_id)

        from datetime import datetime, timedelta
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else start_date

        total_created = 0
        curr_date = start_date
        while curr_date <= end_date:
            for time_str in times_list:
                if time_str.strip():
                    Showtime.objects.get_or_create(
                        movie=movie,
                        cinema=cinema,
                        show_date=curr_date,
                        start_time=time_str.strip(),
                        defaults={
                            'platinum_price': plat_price,
                            'gold_price': gold_price,
                            'silver_price': silv_price
                        }
                    )
                    total_created += 1
            curr_date += timedelta(days=1)

        AdminActivityLog.objects.create(
            action=f"Allocated '{movie.title}' to '{cinema.name}' ({start_date_str} to {end_date_str}, {len(times_list)} shows/day)",
            performed_by="System Admin"
        )

        messages.success(request, f"Successfully created {total_created} showtime slot(s) for '{movie.title}'.")
    return redirect('admin_panel:allocations')


@admin_required
def edit_allocation_group(request, movie_id, cinema_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cinema = get_object_or_404(Cinema, id=cinema_id)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        times_list = request.POST.getlist('show_times')
        plat_price = request.POST.get('platinum_price', 350)
        gold_price = request.POST.get('gold_price', 250)
        silv_price = request.POST.get('silver_price', 180)

        # Delete old showtimes without active bookings
        Showtime.objects.filter(movie=movie, cinema=cinema, bookings__isnull=True).delete()

        from datetime import datetime, timedelta
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else start_date

        total_created = 0
        curr_date = start_date
        while curr_date <= end_date:
            for time_str in times_list:
                if time_str.strip():
                    Showtime.objects.get_or_create(
                        movie=movie,
                        cinema=cinema,
                        show_date=curr_date,
                        start_time=time_str.strip(),
                        defaults={
                            'platinum_price': plat_price,
                            'gold_price': gold_price,
                            'silver_price': silv_price
                        }
                    )
                    total_created += 1
            curr_date += timedelta(days=1)

        AdminActivityLog.objects.create(
            action=f"Updated Show Allocation for '{movie.title}' at '{cinema.name}' ({total_created} shows total)",
            performed_by="System Admin"
        )

        messages.success(request, f"Updated allocation for '{movie.title}' at {cinema.name} successfully.")
    return redirect('admin_panel:allocations')


@admin_required
def delete_allocation(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    info = f"{showtime.movie.title} at {showtime.cinema.name} on {showtime.show_date} ({showtime.start_time})"
    showtime.delete()

    AdminActivityLog.objects.create(
        action=f"Deleted Showtime Allocation '{info}'",
        performed_by="System Admin"
    )

    messages.success(request, f"Showtime allocation deleted.")
    return redirect('admin_panel:allocations')


@admin_required
def delete_allocation_group(request, movie_id, cinema_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cinema = get_object_or_404(Cinema, id=cinema_id)
    
    deleted_count, _ = Showtime.objects.filter(movie=movie, cinema=cinema).delete()

    AdminActivityLog.objects.create(
        action=f"Bulk Deleted {deleted_count} showtimes for '{movie.title}' at '{cinema.name}'",
        performed_by="System Admin"
    )

    messages.success(request, f"Successfully deleted all {deleted_count} showtime allocations for '{movie.title}' at {cinema.name}.")
    return redirect('admin_panel:allocations')


@admin_required
def ticket_verifier(request):
    message_text = None
    scanned_booking = None
    qr_hash = request.GET.get('code') or request.POST.get('qr_hash', '')
    qr_hash = qr_hash.strip()

    if qr_hash:
        try:
            booking = Booking.objects.get(qr_code_hash=qr_hash)
            scanned_booking = booking
            if booking.is_past:
                message_text = f"EXPIRED TICKET: Showtime for Ticket #{str(booking.booking_id)[:8]} was on {booking.showtime.show_date} at {booking.showtime.start_time.strftime('%I:%M %p')}. Movie showtime has passed!"
            elif booking.is_verified:
                message_text = f"WARNING: Ticket #{str(booking.booking_id)[:8]} has ALREADY been used/scanned!"
            else:
                booking.is_verified = True
                booking.save()
                message_text = f"SUCCESS: Ticket #{str(booking.booking_id)[:8]} Verified & Checked-In!"
                
                AdminActivityLog.objects.create(
                    action=f"Scanned & Verified Ticket #{str(booking.booking_id)[:8]} at gate",
                    performed_by="System Admin"
                )
        except Booking.DoesNotExist:
            message_text = "ERROR: Invalid Ticket Code! No booking record found."

    context = {
        'message_text': message_text,
        'scanned_booking': scanned_booking,
        'active_page': 'verifier',
        'scanned_code': qr_hash
    }
    return render(request, 'admin_panel/ticket_verifier.html', context)


@admin_required
def delete_user(request, user_id):
    customer = get_object_or_404(Customer, id=user_id)
    name = customer.full_name
    customer.delete()

    AdminActivityLog.objects.create(
        action=f"Removed user account '{name}'",
        performed_by="System Admin"
    )

    messages.success(request, f"User '{name}' removed successfully.")
    return redirect('admin_panel:users')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_verify_ticket(request):
    if request.method == "OPTIONS":
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        return response

    code = request.GET.get('code') or request.POST.get('code') or ''
    code = code.strip()
    
    def make_response(data, status=200):
        res = JsonResponse(data, status=status)
        res["Access-Control-Allow-Origin"] = "*"
        res["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        res["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        return res

    if not code:
        return make_response({'valid': False, 'message': 'No code provided.'})

    if 'code=' in code:
        code = code.split('code=')[-1].split('&')[0]

    try:
        booking = Booking.objects.select_related('customer', 'showtime__movie', 'showtime__cinema').get(qr_code_hash=code)
        already_used = booking.is_verified
        is_expired = booking.is_past
        
        if is_expired:
            msg = f"EXPIRED TICKET: Showtime was on {booking.showtime.show_date} at {booking.showtime.start_time.strftime('%I:%M %p')}. Movie showtime has passed!"
        elif already_used:
            msg = "WARNING: Ticket Already Scanned Previously!"
        else:
            booking.is_verified = True
            booking.save()
            msg = "SUCCESS: Ticket Verified & Checked-In!"
            
            AdminActivityLog.objects.create(
                action=f"Scanned & Verified Ticket #{str(booking.booking_id)[:8]} via App",
                performed_by="Gate Verifier"
            )

        return make_response({
            'valid': True,
            'already_used': already_used,
            'is_expired': is_expired,
            'message': msg,
            'ticket': {
                'booking_id': str(booking.booking_id)[:8],
                'customer_name': booking.customer.full_name,
                'movie_title': booking.showtime.movie.title,
                'cinema_name': booking.showtime.cinema.name,
                'show_date': str(booking.showtime.show_date),
                'show_time': booking.showtime.start_time.strftime('%I:%M %p'),
                'seats': booking.seats,
                'seat_tier': booking.seat_tier.upper(),
                'total_amount': float(booking.total_amount),
                'qr_code_hash': booking.qr_code_hash
            }
        })
    except Booking.DoesNotExist:
        return make_response({'valid': False, 'message': 'INVALID TICKET: No matching booking found in database.'})


@admin_required
def activity_logs_list(request):
    logs = AdminActivityLog.objects.all().order_by('-timestamp')

    query = request.GET.get('q', '').strip()
    if query:
        logs = logs.filter(Q(action__icontains=query) | Q(performed_by__icontains=query) | Q(details__icontains=query))

    performer = request.GET.get('performer', '').strip()
    if performer:
        logs = logs.filter(performed_by__iexact=performer)

    performers = AdminActivityLog.objects.values_list('performed_by', flat=True).distinct()

    paginator = Paginator(logs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'performer': performer,
        'performers': performers,
        'total_logs': paginator.count,
        'active_page': 'activity_logs',
    }
    return render(request, 'admin_panel/activity_logs.html', context)


@admin_required
def clear_activity_logs(request):
    if request.method == 'POST':
        duration = request.POST.get('duration', 'all')
        now = timezone.now()

        if duration == '7_days':
            threshold = now - timedelta(days=7)
            logs_to_delete = AdminActivityLog.objects.filter(timestamp__lt=threshold)
            count = logs_to_delete.count()
            logs_to_delete.delete()
            duration_label = "older than 7 days"
        elif duration == '30_days':
            threshold = now - timedelta(days=30)
            logs_to_delete = AdminActivityLog.objects.filter(timestamp__lt=threshold)
            count = logs_to_delete.count()
            logs_to_delete.delete()
            duration_label = "older than 30 days"
        elif duration == '90_days':
            threshold = now - timedelta(days=90)
            logs_to_delete = AdminActivityLog.objects.filter(timestamp__lt=threshold)
            count = logs_to_delete.count()
            logs_to_delete.delete()
            duration_label = "older than 90 days"
        else:
            count = AdminActivityLog.objects.count()
            AdminActivityLog.objects.all().delete()
            duration_label = "all historical logs"

        AdminActivityLog.objects.create(
            action=f"Cleared {count} activity audit logs ({duration_label})",
            performed_by="System Admin"
        )
        messages.success(request, f"Successfully cleared {count} activity log entries ({duration_label}).")
    return redirect('admin_panel:activity_logs')
