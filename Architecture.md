# MovieMate — Architecture Document

## 1. Project Overview

MovieMate is a web-based online movie ticket booking platform.

The system has two major sides:

1. **Client Side** — used by customers to discover movies and book tickets.
2. **Admin Side** — used by administrators to manage movies, cinemas, shows, bookings, payments, users, and analytics.

The application will use:

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Django
* **Database:** PostgreSQL
* **Movie Data:** OMDb API
* **Authentication:** Django Authentication System
* **PDF Generation:** Python PDF library
* **QR Generation:** Python QR-code library
* **Payment:** QR-based payment flow
* **Styling:** Custom HTML/CSS/JavaScript UI

---

# 2. Overall Architecture

```text
                           MOVIEMATE
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
          CLIENT SIDE                    ADMIN SIDE
                │                             │
                ▼                             ▼
           Customers                    Administrators
                │                             │
                └──────────────┬──────────────┘
                               ▼
                        Django Backend
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
             Services                    PostgreSQL
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
     OMDb      QR Code     PDF
```

Django is the central source of truth for all important business operations.

The frontend must never be trusted for:

* Seat availability.
* Ticket validity.
* Payment confirmation.
* Booking price.
* User permissions.
* Booking status.

---

# 3. Technology Stack

## Frontend

```text
HTML
CSS
JavaScript
```

No frontend framework is required for the initial version.

The frontend should use reusable HTML components and JavaScript for dynamic interactions.

---

## Backend

```text
Python
Django
```

Django will handle:

* Routing.
* Authentication.
* Authorization.
* Forms.
* Validation.
* Business logic.
* Database operations.
* Booking system.
* Payment handling.
* Ticket generation.
* Ticket verification.

---

## Database

```text
PostgreSQL
```

PostgreSQL will store:

* Users.
* Cities.
* Cinemas.
* Screens.
* Seats.
* Movies.
* Movie allocations.
* Shows.
* Prices.
* Bookings.
* Booking seats.
* Payments.
* Tickets.

---

# 4. UI Architecture

MovieMate uses a **dark premium cinema theme**.

The client-side design uses:

```text
Background:
#111018

Surface:
#1A1823

Elevated Surface:
#232030

Border:
#332F42

Primary Accent:
#E8283F

Primary Text:
#F3F1EC

Muted Text:
#9C97AC

Faint Text:
#6B6779
```

These values are based on the provided MovieMate UI design.

---

# 5. Client-Side Theme

The client side will use:

```text
Primary Accent:
Red #E8283F
```

The red accent is used for:

* Primary buttons.
* Active navigation items.
* Active filters.
* MovieMate logo accent.
* Hero highlights.
* Ratings.
* Links.
* Important UI states.
* Ticket accents.
* Focus states.

The existing design uses `#E8283F` for the main accent and a darker `#8A1C2C` as the dim accent.

---

# 6. Admin-Side Theme

The admin side will use the same overall visual language:

```text
Dark background
Dark surfaces
Rounded components
Premium cinema-style UI
Same typography
Same spacing philosophy
Same component structure
```

However, the primary accent will change:

```text
Client:
RED

Admin:
BLUE
```

Where the client uses the red accent, the admin interface should use the corresponding blue accent.

The exact admin blue color will be finalized in `Design.md`.

The admin side should feel like the same MovieMate product rather than a completely different application.

---

# 7. Typography

The provided design uses three main fonts:

### Bebas Neue

Used for:

* Large movie titles.
* Section titles.
* MovieMate branding.
* Display headings.

### Plus Jakarta Sans

Used for:

* Body text.
* Buttons.
* Navigation.
* Forms.
* General UI.

### Space Mono

Used for:

* Ticket information.
* Small labels.
* Eyebrows.
* Technical information.
* Ticket numbers.
* Metadata.

## These fonts are part of the provided UI design.

# 8. Client-Side Visual Language

The client UI should maintain these characteristics:

* Dark cinema atmosphere.
* Premium but simple appearance.
* Rounded buttons.
* Rounded cards.
* Pill-shaped filters.
* Strong typography.
* Large movie titles.
* Movie poster cards.
* Ticket-inspired visual elements.
* Subtle borders.
* Minimal shadows.
* Smooth hover states.
* No excessive gradients.
* No unnecessary visual clutter.

The current design uses rounded buttons with strong primary actions and a subtle shadow rather than a bright glow.

---

# 9. Navigation Architecture

The client navigation should contain:

```text
MOVIEMATE

Movies
My Bookings
Offers

[City]
[Search]

Log in
Sign up
```

The current UI places the city selector, search field, navigation links, and authentication buttons inside the main navigation.

The navigation should be sticky on desktop.

On smaller screens, search/navigation elements can collapse according to the responsive design.

---

# 10. Client Homepage

The homepage should contain:

```text
Navigation
     ↓
Hero Slider
     ↓
Now Showing
     ↓
Movie Filters
     ↓
Movie Cards
     ↓
This Week's Releases
     ↓
Footer
```

The provided design already follows this structure.

---

# 11. Hero Section

The hero section should dynamically display movies selected by the administrator.

Movies can be categorized as:

```text
HOT
TRENDING
RATING
NEW
```

The homepage can randomly or dynamically select movies from these categories.

Each hero slide can display:

```text
Movie Title
Description
Certification
Genre
Runtime
Category/Rating
Poster
Book Now
Watch Trailer
```

The current design uses a multi-slide hero with navigation arrows and dots.

---

# 12. Movie Cards

Movie cards should follow the existing ticket-inspired design.

Each movie card can contain:

```text
Poster
Certification
Rating
Movie Title
Genre
Languages
Book Tickets
```

The current design uses movie poster cards with ratings, certification labels, perforated ticket-style separators, and a booking button.

---

# 13. Filters

Movie filtering should support options such as:

```text
All
Hindi
English
Gujarati
2D
3D
4DX
Action
Romance
```

Additional filters can be introduced later.

The UI should use rounded pill-style filter chips.

The active filter uses the primary accent color.

---

# 14. Authentication UI

The authentication pages should follow the provided split-screen design.

Desktop:

```text
┌──────────────────────┬─────────────────────┐
│                      │                     │
│   Visual / Ticket    │    Login / Signup   │
│       Section        │       Form          │
│                      │                     │
└──────────────────────┴─────────────────────┘
```

Mobile:

```text
┌─────────────────────┐
│                     │
│     Login/Signup    │
│        Form         │
│                     │
└─────────────────────┘
```

The visual side is hidden on smaller screens in the existing design.

---

# 15. Authentication Features

Customers can:

* Sign up.
* Log in.
* Log out.
* Reset password.
* Change password.
* Edit profile.
* View profile.

Signup information should include:

```text
Full Name
Email
Mobile Number
Password
Confirm Password
```

There should be no profile picture functionality.

The provided signup UI already follows this structure.

---

# 16. Accounts App

The `accounts` Django app handles:

```text
Authentication
User Model
Signup
Login
Logout
Profile
Edit Profile
Password Management
User Roles
Permissions
```

A custom User model should be created before the first migration.

---

# 17. User Model

Recommended structure:

```text
User
├── id
├── email
├── password
├── first_name
├── last_name
├── phone
├── role
├── is_active
├── is_staff
├── date_joined
└── updated_at
```

Email should be the primary login identifier.

No profile image field should exist.

---

# 18. User Roles

Initial roles:

```text
CUSTOMER
ADMIN
```

### Customer

Can:

* Browse movies.
* Search movies.
* Select city.
* Select cinema.
* Select show.
* Select seats.
* Make bookings.
* Make payments.
* Download tickets.
* View booking history.
* Manage profile.

### Admin

Can:

* Manage movies.
* Manage cinemas.
* Manage screens.
* Manage seats.
* Allocate movies.
* Manage shows.
* Manage prices.
* Manage bookings.
* Manage users.
* View payments.
* View analytics.
* Verify tickets.

---

# 19. Django Application Structure

The project should be divided into focused Django apps:

```text
apps/
│
├── accounts/
├── movies/
├── cinemas/
├── shows/
├── bookings/
├── payments/
└── dashboard/
```

Each app should have a clear responsibility.

---

# 20. Project Structure

```text
moviemate/
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── PRD.md
├── Architecture.md
├── Rules.md
├── Phases.md
├── Design.md
├── Memory.md
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── movies/
│   ├── cinemas/
│   ├── shows/
│   ├── bookings/
│   ├── payments/
│   └── dashboard/
│
├── services/
│   ├── omdb.py
│   ├── pdf.py
│   └── qr.py
│
├── templates/
│   ├── base.html
│   ├── components/
│   ├── client/
│   └── admin/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── media/
```

---

# 21. Movies App

The `movies` app handles:

* Movie registration.
* Movie details.
* Movie search.
* OMDb API integration.
* Movie categories.
* Movie status.

---

# 22. Movie Model

Recommended structure:

```text
Movie
├── id
├── omdb_id
├── title
├── year
├── rated
├── released
├── runtime
├── genre
├── director
├── actors
├── plot
├── language
├── poster
├── imdb_rating
├── status
├── created_at
└── updated_at
```

Status:

```text
ACTIVE
INACTIVE
ARCHIVED
```

---

# 23. Movie Categories

Movies can have multiple homepage categories:

```text
HOT
TRENDING
RATING
NEW
```

A many-to-many relationship should be used.

Example:

```text
Movie
 ├── HOT
 ├── TRENDING
 └── RATING
```

---

# 24. OMDb Architecture

Movie registration should work like:

```text
Admin Dashboard
      ↓
Add Movie
      ↓
Search OMDb
      ↓
OMDb Service
      ↓
OMDb API
      ↓
Movie Results
      ↓
Admin Selects Movie
      ↓
Review Details
      ↓
Save Movie
      ↓
PostgreSQL
```

The OMDb API key must be stored in `.env`.

```text
OMDB_API_KEY=
```

It must never be hardcoded.

---

# 25. Cinema Architecture

Cinema hierarchy:

```text
City
 │
 └── Cinema
       │
       ├── Screen
       │    └── Seats
       │
       ├── Screen
       │    └── Seats
       │
       └── Screen
            └── Seats
```

---

# 26. City Model

```text
City
├── id
├── name
├── state
├── is_active
├── created_at
└── updated_at
```

---

# 27. Cinema Model

```text
Cinema
├── id
├── name
├── city
├── address
├── state
├── pincode
├── phone
├── description
├── is_active
├── created_at
└── updated_at
```

Relationship:

```text
City 1 ─────── N Cinema
```

---

# 28. Screen Model

```text
Screen
├── id
├── cinema
├── name
├── screen_number
├── is_active
├── created_at
└── updated_at
```

Relationship:

```text
Cinema 1 ─────── N Screen
```

---

# 29. Seat Model

```text
Seat
├── id
├── screen
├── row
├── number
├── category
├── is_active
└── created_at
```

Seat categories:

```text
SILVER
GOLD
PLATINUM
```

The seat's permanent database record should not contain a global `is_booked` value.

Seat availability belongs to a specific show.

---

# 30. Movie Allocation

Movies must be allocated to cinemas before customers can book them.

```text
Movie
   │
   └── MovieAllocation
          │
          ├── Cinema
          ├── Start Date
          ├── End Date
          └── Status
```

Recommended model:

```text
MovieAllocation
├── id
├── movie
├── cinema
├── start_date
├── end_date
├── is_active
├── created_at
└── updated_at
```

This allows:

```text
Avengers
│
├── Cinema A → 15 Aug - 30 Aug
├── Cinema B → 15 Aug - 25 Aug
└── Cinema C → 18 Aug - 30 Aug
```

---

# 31. Show Architecture

A Show represents one actual screening.

A show connects:

```text
Movie
Cinema
Screen
Date
Start Time
End Time
```

Recommended model:

```text
Show
├── id
├── movie
├── cinema
├── screen
├── start_time
├── end_time
├── status
├── created_at
└── updated_at
```

---

# 32. Show Creation

Admin can configure:

```text
Movie
Cinema
Screen
Start Date
End Date
Showtimes
Silver Price
Gold Price
Platinum Price
```

The system generates individual shows.

Example:

```text
15 Aug
10:00 AM
02:00 PM
06:00 PM
09:00 PM

16 Aug
10:00 AM
02:00 PM
06:00 PM
09:00 PM
```

Every show is independently bookable.

---

# 33. Show Validation

Before creating a show, Django must verify:

1. Movie exists.
2. Cinema exists.
3. Screen belongs to selected cinema.
4. Movie is allocated to cinema.
5. Show date is within allocation period.
6. Show does not overlap another show on the same screen.

---

# 34. Show Status

```text
UPCOMING
ACTIVE
COMPLETED
CANCELLED
```

The system should automatically determine the appropriate status based on date/time where possible.

---

# 35. Pricing Architecture

Pricing belongs to a show.

```text
Show
 │
 └── ShowSeatPrice
       ├── SILVER
       ├── GOLD
       └── PLATINUM
```

Example:

```text
Silver   → ₹150
Gold     → ₹200
Platinum → ₹300
```

Prices should be copied into the booking when the booking is confirmed so historical tickets do not change when future prices are modified.

---

# 36. Client Booking Flow

```text
Home
 ↓
Search / Browse Movie
 ↓
Select City
 ↓
Select Movie
 ↓
Select Cinema
 ↓
Select Date
 ↓
Select Show
 ↓
View Seats
 ↓
Select Seats
 ↓
Checkout
 ↓
Payment
 ↓
Payment Verification
 ↓
Booking Confirmation
 ↓
Generate Ticket
 ↓
Generate Ticket QR
 ↓
Generate PDF
 ↓
Download Ticket
```

---

# 37. Seat Availability

A physical seat belongs to a screen.

Its booking state belongs to a show.

Example:

```text
Seat A1

Show 1 → BOOKED
Show 2 → AVAILABLE
Show 3 → BOOKED
Show 4 → AVAILABLE
```

This prevents one booking from incorrectly blocking the seat for every show.

---

# 38. Temporary Seat Locking

When a customer selects seats:

```text
AVAILABLE
    ↓
LOCKED
    ↓
PAYMENT
    ↓
CONFIRMED
```

If payment fails or the lock expires:

```text
LOCKED
    ↓
AVAILABLE
```

The lock must have an expiration timestamp.

The backend must prevent another user from selecting a currently locked seat.

---

# 39. Booking Architecture

The booking system contains:

```text
Booking
BookingSeat
Ticket
```

Recommended Booking model:

```text
Booking
├── id
├── booking_id
├── user
├── show
├── total_amount
├── status
├── payment_status
├── ticket_status
├── created_at
└── updated_at
```

Statuses:

```text
PENDING
CONFIRMED
CANCELLED
EXPIRED
```

---

# 40. BookingSeat

```text
BookingSeat
├── id
├── booking
├── seat
├── category
├── price
└── created_at
```

A booking can contain multiple seats.

Example:

```text
Booking MM10025

G12
G13
P04
```

---

# 41. Double Booking Prevention

The backend must guarantee:

> One physical seat cannot be confirmed for two bookings of the same show.

The implementation should use:

* Database constraints.
* Transactions.
* Row-level locking where necessary.
* Proper seat-lock logic.

The system must handle concurrent booking requests safely.

---

# 42. Payment Architecture

The `payments` app handles:

* Payment creation.
* Payment status.
* Transaction ID.
* Payment verification.
* Payment success.
* Payment failure.

Recommended model:

```text
Payment
├── id
├── booking
├── transaction_id
├── amount
├── payment_method
├── status
├── created_at
└── updated_at
```

Statuses:

```text
PENDING
SUCCESS
FAILED
REFUNDED
```

---

# 43. QR Payment

Payment flow:

```text
Checkout
   ↓
Create Pending Booking
   ↓
Calculate Amount
   ↓
Display Payment QR
   ↓
Customer Scans QR
   ↓
Payment
   ↓
Payment Verification
   ↓
SUCCESS
   ↓
Confirm Booking
```

The payment QR is separate from the ticket QR.

---

# 44. Payment Security

The browser must never be trusted to declare payment success.

For example, Django must not accept:

```text
payment_success=true
```

as proof of payment.

The backend must verify payment using the actual payment mechanism.

For an academic/demo implementation, a controlled payment simulation can be used if a real payment gateway is not integrated.

The payment architecture should remain isolated so a real gateway can be added later.

---

# 45. Ticket Architecture

After successful payment:

```text
Payment SUCCESS
       ↓
Booking CONFIRMED
       ↓
Generate Ticket ID
       ↓
Generate Ticket QR
       ↓
Generate PDF
       ↓
Allow Download
```

Ticket information:

```text
Booking ID
Movie
Cinema
Screen
Date
Time
Seats
Seat Category
Amount
Ticket QR
```

---

# 46. Ticket QR

The ticket QR should contain a secure ticket identifier rather than sensitive booking information.

Example:

```text
MM-TICKET-8f92a1c4...
```

Verification:

```text
QR Scanner
     ↓
Ticket Token
     ↓
Django
     ↓
Find Ticket
     ↓
Validate
     ↓
Return Result
```

The frontend must never determine ticket validity itself.

---

# 47. Ticket Verification

Possible verification results:

```text
VALID
ALREADY USED
INVALID
CANCELLED
EXPIRED
```

Verification flow:

```text
Scan QR
   ↓
Extract Token
   ↓
Send Token to Django
   ↓
Find Ticket
   ↓
Check Booking
   ↓
Check Ticket Status
   ↓
Check Show
   ↓
Return Result
```

---

# 48. Ticket Usage

A valid ticket starts as:

```text
NOT_USED
```

After successful entry:

```text
NOT_USED
    ↓
USED
```

A second scan returns:

```text
ALREADY USED
```

The status update must be atomic.

---

# 49. Show Completion

After the show ends:

```text
Show
06:30 PM → 09:00 PM

Before 06:30 PM
→ Booking Available

After 06:30 PM
→ Booking Closed

After 09:00 PM
→ COMPLETED
```

After completion:

* No new bookings.
* Show becomes `COMPLETED`.
* Existing bookings remain.
* Tickets remain downloadable.
* Booking history remains.
* Historical data is not automatically deleted.

---

# 50. PDF Generation

PDF generation should be isolated:

```text
services/
└── pdf.py
```

Flow:

```text
Booking
   ↓
PDF Service
   ↓
Ticket Template
   ↓
Ticket QR
   ↓
PDF
   ↓
Download
```

The generated PDF should match MovieMate's visual ticket style.

---

# 51. QR Generation

QR generation should be isolated:

```text
services/
└── qr.py
```

The service receives the secure ticket identifier and generates the QR image.

---

# 52. Admin Dashboard

The admin dashboard will use the same MovieMate design system but with a **blue primary accent instead of the client-side red accent**.

The admin dashboard should contain:

```text
Dashboard
Movies
Cinemas
Screens
Seats
Shows
Bookings
Payments
Users
Ticket Verification
Analytics
Settings
```

The admin UI should maintain the same:

* Dark backgrounds.
* Dark surfaces.
* Typography.
* Rounded cards.
* Rounded buttons.
* Borders.
* Spacing.
* Responsive behavior.

Only the primary accent system changes from red to blue.

---

# 53. Admin Movie Flow

```text
Admin Dashboard
      ↓
Movies
      ↓
Add Movie
      ↓
Search OMDb
      ↓
Select Movie
      ↓
Review Details
      ↓
Select Category
      ↓
Save
```

---

# 54. Admin Cinema Flow

```text
Admin Dashboard
      ↓
Cinemas
      ↓
Add Cinema
      ↓
Cinema Details
      ↓
Save Cinema
      ↓
Add Screens
      ↓
Configure Seats
      ↓
Set Seat Categories
```

---

# 55. Admin Allocation Flow

```text
Movie
   ↓
Allocate Movie
   ↓
Select Cinema(s)
   ↓
Set Start Date
   ↓
Set End Date
   ↓
Configure Shows
   ↓
Set Prices
   ↓
Publish
```

There should be an option to allocate a movie to all active cinemas.

---

# 56. Admin Analytics

The dashboard should display:

```text
Total Users
Total Movies
Total Cinemas
Total Shows
Total Bookings
Total Tickets Sold
Total Revenue
Today's Bookings
Upcoming Shows
Completed Shows
```

Additional analytics can include:

```text
Most Booked Movies
Most Popular Cinemas
Revenue by Date
Bookings by Date
Tickets Sold by Movie
Cinema Performance
```

---

# 57. Client Pages

```text
Home
│
├── Login
├── Signup
│
├── Movies
│   └── Movie Details
│
├── City Selection
│
├── Theater Selection
│
├── Show Selection
│
├── Seat Selection
│
├── Checkout
│
├── Payment
│
├── Booking Confirmation
│
├── My Bookings
│   └── Booking Details
│
└── Profile
    ├── Edit Profile
    └── Change Password
```

---

# 58. Admin Pages

```text
Admin Dashboard
│
├── Dashboard
│
├── Movies
│   ├── All Movies
│   ├── Add Movie
│   └── Categories
│
├── Cinemas
│   ├── All Cinemas
│   ├── Add Cinema
│   ├── Screens
│   └── Seats
│
├── Shows
│   ├── All Shows
│   ├── Create Show
│   └── Manage Shows
│
├── Bookings
│   ├── All Bookings
│   └── Ticket Verification
│
├── Payments
│
├── Users
│
├── Analytics
│
└── Settings
```

---

# 59. URL Architecture

Client URLs:

```text
/
 /login/
 /signup/
 /movies/
 /movies/<id>/
 /cities/
 /theaters/
 /shows/
 /seats/<show_id>/
 /checkout/<show_id>/
 /payment/<booking_id>/
 /booking/<booking_id>/
 /my-bookings/
 /profile/
```

Admin URLs:

```text
/admin-dashboard/
 /admin-dashboard/movies/
 /admin-dashboard/movies/add/
 /admin-dashboard/cinemas/
 /admin-dashboard/cinemas/add/
 /admin-dashboard/screens/
 /admin-dashboard/seats/
 /admin-dashboard/shows/
 /admin-dashboard/bookings/
 /admin-dashboard/payments/
 /admin-dashboard/users/
 /admin-dashboard/analytics/
 /admin-dashboard/verify-ticket/
```

Exact URLs can be changed during implementation if required.

---

# 60. Database Relationships

Core relationships:

```text
User
 │
 └── Booking
       │
       ├── Show
       │     ├── Movie
       │     ├── Cinema
       │     └── Screen
       │           └── Seat
       │
       └── BookingSeat
              └── Seat

Movie
 │
 └── MovieAllocation
       └── Cinema

Booking
 │
 └── Payment
```

---

# 61. Relationship Summary

```text
User 1 ─────── N Booking

Movie 1 ─────── N Show

Cinema 1 ─────── N Screen

Screen 1 ─────── N Seat

Movie 1 ─────── N MovieAllocation

Cinema 1 ─────── N MovieAllocation

Show 1 ─────── N Booking

Booking 1 ─────── N BookingSeat

Seat 1 ─────── N BookingSeat

Booking 1 ─────── 1 Payment
```

---

# 62. Service Layer

Complex business logic should not be placed directly inside views.

Recommended services:

```text
movies/services.py
    search_omdb()
    import_movie()

shows/services.py
    create_show_schedule()
    validate_show_conflict()

bookings/services.py
    lock_seats()
    create_booking()
    confirm_booking()
    cancel_booking()
    verify_ticket()

payments/services.py
    create_payment()
    verify_payment()
```

Global services:

```text
services/
├── omdb.py
├── pdf.py
└── qr.py
```

---

# 63. Environment Variables

Sensitive information must be stored in `.env`.

```text
SECRET_KEY=
DEBUG=True

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

OMDB_API_KEY=

PAYMENT_KEY=
PAYMENT_SECRET=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_USER=
EMAIL_PASSWORD=
```

`.env` must never be committed to Git.

`.env.example` should contain the variable names without real credentials.

---

# 64. Static and Media Files

Static:

```text
static/
├── css/
├── js/
└── images/
```

Media:

```text
media/
├── movie_posters/
└── tickets/
```

No profile-image directory is required because MovieMate does not support user profile pictures.

---

# 65. Security Architecture

MovieMate must use:

* Django password hashing.
* CSRF protection.
* Authentication.
* Authorization.
* Permission checks.
* Server-side validation.
* Server-side price calculation.
* Server-side payment verification.
* Server-side ticket verification.
* Database constraints.
* Transactions.
* Secure environment variables.

The client must never be trusted for critical business decisions.

---

# 66. Transaction-Sensitive Operations

The following operations should use database transactions where necessary.

### Booking

```text
Check Availability
       ↓
Lock Seats
       ↓
Create Booking
```

### Payment Confirmation

```text
Verify Payment
       ↓
Confirm Booking
       ↓
Confirm Seats
```

### Ticket Verification

```text
Check Ticket
       ↓
Check Status
       ↓
Mark Ticket Used
```

These operations should be atomic wherever possible.

---

# 67. Testing Architecture

Tests should cover critical business logic.

### Authentication

* Signup.
* Login.
* Invalid login.
* Protected pages.
* Profile update.
* Password change.

### Movies

* OMDb search.
* Movie registration.
* Movie categories.

### Cinemas

* Cinema creation.
* Screen creation.
* Seat creation.
* Seat categories.

### Shows

* Show creation.
* Movie allocation validation.
* Screen conflict validation.
* Expired show handling.

### Bookings

* Seat availability.
* Double booking prevention.
* Booking creation.
* Payment failure.
* Payment success.
* Ticket generation.

### Ticket Verification

* Valid ticket.
* Invalid ticket.
* Cancelled ticket.
* Already-used ticket.
* Completed show.

---

# 68. Complete MovieMate Flow

```text
                         MOVIEMATE
                             │
             ┌───────────────┴───────────────┐
             │                               │
             ▼                               ▼
        CLIENT SIDE                     ADMIN SIDE
             │                               │
             ▼                               ▼
          Homepage                       Dashboard
             │                               │
             ▼                               ├── Movies
        Search Movie                        ├── Cinemas
             │                               ├── Screens
             ▼                               ├── Seats
        Select City                         ├── Shows
             │                               ├── Bookings
             ▼                               ├── Payments
        Select Movie                        ├── Users
             │                               ├── Analytics
             ▼                               └── Verify Ticket
       Select Cinema
             │
             ▼
        Select Show
             │
             ▼
        Select Seats
             │
             ▼
         Checkout
             │
             ▼
          Payment
             │
             ▼
     Payment Verification
             │
             ▼
      Confirm Booking
             │
             ▼
       Generate Ticket
             │
             ├──────────► QR
             │
             └──────────► PDF
                         │
                         ▼
                  Download Ticket
                         │
                         ▼
                    Visit Cinema
                         │
                         ▼
                    Scan Ticket
                         │
                         ▼
                 Verify Ticket
```

---

# 69. Final Architecture Principles

MovieMate should always follow these core principles:

```text
Frontend = User Experience

Django = Business Logic + Security

PostgreSQL = Source of Truth

OMDb = External Movie Data

QR = Payment / Ticket Identification

PDF = Downloadable Ticket

Admin = Platform Management
```

The client side and admin side should feel like two interfaces of the same MovieMate product.

The client side uses:

```text
DARK + RED
```

The admin side uses:

```text
DARK + BLUE
```

Both sides share the same typography, spacing, component philosophy, rounded UI, and premium cinema identity.

The provided UI design is the visual reference that the implementation should follow.
