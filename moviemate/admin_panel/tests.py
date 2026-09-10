from django.test import TestCase, Client
from accounts.models import Customer
from admin_panel.models import Movie, Cinema, Showtime

class AdminPanelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = Customer.objects.create(
            full_name="Admin Test",
            email="admin@moviemate.com",
            mobile="9999999999",
            password="adminpassword",
            role="admin"
        )
        # Log in session
        session = self.client.session
        session['customer_id'] = self.admin_user.id
        session.save()

        self.movie = Movie.objects.create(
            title="Test Action Movie",
            genre="Action",
            duration_minutes=140,
            rating=8.8,
            display_tag="hot",
            status="active"
        )
        self.cinema = Cinema.objects.create(
            name="Test Cinema Hall",
            city="Ahmedabad",
            address="CG Road",
            total_screens=4
        )

    def test_dashboard_view(self):
        response = self.client.get('/admin-panel/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_movies_view(self):
        response = self.client.get('/admin-panel/movies/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Action Movie")

    def test_cinemas_view(self):
        response = self.client.get('/admin-panel/cinemas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Cinema Hall")

    def test_allocations_view(self):
        response = self.client.get('/admin-panel/allocations/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Show Allocations")

    def test_activity_logs_view(self):
        response = self.client.get('/admin-panel/activity-logs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "System Activity & Audit Logs")

    def test_clear_activity_logs(self):
        response = self.client.post('/admin-panel/activity-logs/clear/', {'duration': 'all'})
        self.assertEqual(response.status_code, 302)
