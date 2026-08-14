from django.contrib import admin
from .models import Movie, Category, AdminActivityLog

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'rating', 'views_count', 'status', 'created_at')
    list_filter = ('status', 'genre')
    search_fields = ('title', 'genre')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'performed_by', 'timestamp')
    readonly_fields = ('timestamp',)
