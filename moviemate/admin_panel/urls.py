from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users_list, name='users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('movies/', views.movies_list, name='movies'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('movies/toggle-hero/<int:movie_id>/', views.toggle_hero_movie, name='toggle_hero_movie'),
    path('movies/omdb-search/', views.omdb_search_api, name='omdb_search'),
    path('movies/import-omdb/', views.import_omdb_movie, name='import_omdb'),
    path('movies/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('cinemas/', views.cinemas_list, name='cinemas'),
    path('cinemas/add/', views.add_cinema, name='add_cinema'),
    path('cinemas/edit/<int:cinema_id>/', views.edit_cinema, name='edit_cinema'),
    path('cinemas/delete/<int:cinema_id>/', views.delete_cinema, name='delete_cinema'),
    path('allocations/', views.allocations_list, name='allocations'),
    path('allocations/add/', views.add_allocation, name='add_allocation'),
    path('allocations/edit-group/<int:movie_id>/<int:cinema_id>/', views.edit_allocation_group, name='edit_allocation_group'),
    path('allocations/delete/<int:showtime_id>/', views.delete_allocation, name='delete_allocation'),
    path('allocations/delete-group/<int:movie_id>/<int:cinema_id>/', views.delete_allocation_group, name='delete_allocation_group'),
    path('verifier/', views.ticket_verifier, name='verifier'),
    path('api/verify-ticket/', views.api_verify_ticket, name='api_verify_ticket'),
]
