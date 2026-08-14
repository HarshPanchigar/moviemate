import uuid
from django.db import models
from accounts.models import Customer

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Movie(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    )
    
    TAG_CHOICES = (
        ('hot', 'Hot'),
        ('trending', 'Trending'),
        ('top_rated', 'Top Rated'),
        ('new_release', 'New Release'),
    )

    imdb_id = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')
    genre = models.CharField(max_length=100)
    duration_minutes = models.IntegerField(default=120)
    release_year = models.IntegerField(default=2026)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=8.5)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    backdrop_url = models.URLField(max_length=500, blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    display_tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='trending')
    is_hero = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cinema(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, default='Ahmedabad')
    address = models.TextField()
    total_screens = models.IntegerField(default=4)
    facilities = models.CharField(max_length=255, default='4K Dolby Atmos, Recliners, Food Court')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='showtimes')
    show_date = models.DateField()
    start_time = models.TimeField()
    platinum_price = models.DecimalField(max_digits=7, decimal_places=2, default=350.00)
    gold_price = models.DecimalField(max_digits=7, decimal_places=2, default=250.00)
    silver_price = models.DecimalField(max_digits=7, decimal_places=2, default=180.00)

    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} - {self.show_date} {self.start_time}"


class Booking(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    seats = models.CharField(max_length=255) # e.g. "A1, A2"
    seat_tier = models.CharField(max_length=20, choices=(('platinum', 'Platinum'), ('gold', 'Gold'), ('silver', 'Silver')))
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='paid')
    qr_code_hash = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{str(self.booking_id)[:8]} - {self.customer.full_name}"


class AdminActivityLog(models.Model):
    action = models.CharField(max_length=255)
    performed_by = models.CharField(max_length=100, default='Admin')
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.performed_by} - {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
