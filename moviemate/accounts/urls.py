from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("search-api/", views.movie_search_api, name="movie_search_api"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path("profile/delete/", views.delete_account, name="delete_account"),
    
    # Booking Engine Routes
    path("movie/<int:movie_id>/theaters/", views.select_theater, name="select_theater"),
    path("movie/<int:movie_id>/cinema/<int:cinema_id>/showtimes/", views.select_showtime, name="select_showtime"),
    path("showtime/<int:showtime_id>/seats/", views.select_seats, name="select_seats"),
    path("showtime/<int:showtime_id>/payment/", views.process_payment, name="process_payment"),
    path("booking/<uuid:booking_id>/confirmation/", views.booking_confirmation, name="booking_confirmation"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
]