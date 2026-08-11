# MovieMate — Complete Project Context

> **IMPORTANT:** This document is the single-context file for AI assistants working on MovieMate.
>
> Before making any code changes, read this entire file and understand the current architecture, requirements, database design, rules, development phases, UI design, and current project status.
>
> Do not invent requirements or change the architecture without approval.

---

# 1. Project Overview

## Project Name

**MovieMate**

## Main Goal

MovieMate is an **online movie ticket booking system**.

It allows customers to:

* Create an account.
* Login/logout.
* Manage their profile.
* Search movies.
* Select a city.
* View available cinemas.
* Select a cinema/theater.
* Select a showtime.
* Select seats.
* Pay for the booking.
* Receive a digital movie ticket.
* Download the ticket as a PDF.
* Use a QR code on the ticket for verification.

MovieMate also provides an administrative system where administrators can manage:

* Movies.
* Cinemas.
* Screens.
* Seats.
* Movie allocations.
* Shows.
* Bookings.
* Payments.
* Tickets.
* Users.
* Analytics.

---

# 2. Target Users

MovieMate has two primary user types:

```text
CUSTOMER
ADMIN
```

### Customer

The customer uses the client-facing MovieMate application to discover movies and book tickets.

### Admin

The administrator manages the MovieMate platform and its booking-related data.

---

# 3. Technology Stack

The approved technology stack is:

```text
Frontend:
HTML
CSS
JavaScript

Backend:
Python
Django

Database:
PostgreSQL

Movie API:
OMDb API
```

Do not replace the stack with React, Next.js, Vue, Angular, Node.js, Express, Laravel, PHP, MongoDB, etc. unless explicitly approved.

MovieMate should remain a **Django-based modular monolith**.

---

# 4. Application Architecture

Recommended high-level structure:

```text
MovieMate/
│
├── manage.py
│
├── moviemate/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── client/
│
├── admin_panel/
│
├── core/
│
├── services/
│
├── templates/
│
├── static/
│
├── media/
│
├── docs/
│
└── .env
```

---

# 5. Django Apps

MovieMate should use three main Django apps.

## `client`

Handles customer-facing functionality.

```text
client/
```

Responsibilities:

* Signup.
* Login.
* Logout.
* Profile.
* Movie browsing.
* Movie search.
* Movie details.
* City selection.
* Cinema selection.
* Show selection.
* Seat selection.
* Checkout.
* Payment UI.
* Booking history.
* Ticket download.

---

## `admin_panel`

Handles the custom MovieMate administration system.

```text
admin_panel/
```

Responsibilities:

* Dashboard.
* Movie management.
* Cinema management.
* Screen management.
* Seat management.
* Movie allocation.
* Show management.
* Booking management.
* Payment management.
* Ticket verification.
* User management.
* Analytics.

The admin side uses the MovieMate **dark + blue** theme.

---

## `core`

Contains shared database models and data used by both the client and admin.

The main models belong here because the same data is used by both sides.

Examples:

```text
User
City
Cinema
Screen
Seat
Movie
MovieAllocation
Show
ShowSeatPrice
Booking
BookingSeat
Payment
Ticket
SeatLock
```

---

# 6. Services

Complex reusable business logic should be placed in:

```text
services/
```

Possible services:

```text
services/
├── omdb.py
├── booking.py
├── payment.py
├── ticket.py
├── qr.py
└── pdf.py
```

Services are responsible for complex operations such as:

* OMDb movie importing.
* Booking creation.
* Seat locking.
* Payment processing/verification.
* Ticket generation.
* QR generation/verification.
* PDF ticket generation.

Do not put large amounts of business logic directly inside Django views.

---

# 7. Client-Side Flow

The main customer journey is:

```text
Signup
   ↓
Login
   ↓
Select City
   ↓
Search/Browse Movie
   ↓
Select Movie
   ↓
Select Cinema
   ↓
Select Show
   ↓
Select Seats
   ↓
Checkout
   ↓
Payment
   ↓
Booking Confirmation
   ↓
Download Ticket PDF
   ↓
Ticket QR Verification
```

---

# 8. Customer Authentication

Customers must be able to:

* Signup.
* Login.
* Logout.
* Change password.
* View profile.
* Edit profile.

The custom Django User model should use **email as the login identifier**.

No user profile picture is required.

Profile information should include:

```text
First Name
Last Name
Email
Phone
Password
```

Passwords must never be stored as plain text.

---

# 9. Movie System

MovieMate uses the **OMDb API** to fetch movie information.

The admin workflow is:

```text
Search OMDb
     ↓
Select Movie
     ↓
Review Movie
     ↓
Save Movie
```

OMDb should primarily be used by the admin to register movies.

Client-side movie searching should use MovieMate's own PostgreSQL database instead of calling OMDb for every customer search.

The OMDb API key must be stored in `.env`.

Never expose the OMDb API key to the browser.

---

# 10. Movie Categories

MovieMate initially supports:

```text
HOT
TRENDING
RATING
NEW
```

These categories can be used to dynamically populate homepage sections and the hero section.

A movie may need multiple categories in the future. If that requirement is implemented, use a proper relational structure rather than storing multiple categories incorrectly inside one field.

---

# 11. Cinema Structure

The cinema hierarchy is:

```text
City
 ↓
Cinema
 ↓
Screen
 ↓
Seat
```

Example:

```text
Ahmedabad
   ↓
PVR Ahmedabad
   ↓
Screen 1
   ↓
A1, A2, A3...
```

A cinema belongs to one city.

A cinema can contain multiple screens.

A screen can contain multiple physical seats.

---

# 12. Movie Allocation

A movie must be allocated to a cinema before it can be shown there.

The allocation contains:

```text
Movie
Cinema
Start Date
End Date
Active Status
```

Example:

```text
Movie:
Avengers

Cinema:
PVR Ahmedabad

Start:
15 August

End:
30 August
```

The same movie can be allocated to multiple cinemas.

There should be an option for the admin to allocate a movie to all active cinemas.

---

# 13. Show System

A Show represents one actual movie screening.

A Show contains:

```text
Movie
Cinema
Screen
Date
Start Time
End Time
Status
```

Show statuses:

```text
UPCOMING
ACTIVE
COMPLETED
CANCELLED
```

A show must not be created for a movie/cinema combination that is not properly allocated.

A show must not overlap another show on the same screen.

Completed shows must not accept new bookings.

Historical bookings must remain available.

---

# 14. Seat System

Seat categories are:

```text
SILVER
GOLD
PLATINUM
```

A physical seat belongs to a screen.

Example:

```text
A1 → SILVER
A2 → SILVER

B1 → GOLD
B2 → GOLD

C1 → PLATINUM
C2 → PLATINUM
```

Do **not** add a global:

```text
is_booked
```

field to the Seat model.

The same physical seat can be booked for one show and available for another.

---

# 15. Seat Pricing

Seat prices are stored per show using `ShowSeatPrice`.

Example:

```text
Show: Avengers — 6:30 PM

SILVER     ₹150
GOLD       ₹200
PLATINUM   ₹300
```

This allows different shows to have different prices.

The frontend can display prices, but Django must calculate and validate the final price.

---

# 16. Seat Locking

Seat locking is required to prevent two customers from booking the same seat simultaneously.

The lifecycle is:

```text
AVAILABLE
    ↓
LOCKED
    ↓
PAYMENT
    ↓
CONFIRMED
```

If payment fails:

```text
LOCKED
    ↓
AVAILABLE
```

If the lock expires:

```text
LOCKED
    ↓
AVAILABLE
```

A `SeatLock` contains:

```text
Show
Seat
User
Expires At
Created At
```

The backend must use transactions/appropriate database locking to prevent double booking.

---

# 17. Booking System

A Booking represents the customer's complete booking.

A booking contains:

```text
User
Show
Booking Code
Total Amount
Status
Booked At
```

Booking statuses:

```text
PENDING
CONFIRMED
CANCELLED
EXPIRED
```

A booking can contain multiple seats through `BookingSeat`.

Example:

```text
Booking #1001

A1 → ₹150
A2 → ₹150
B1 → ₹200

Total → ₹500
```

The actual price paid must be stored in `BookingSeat`.

This preserves historical prices if the current show price changes later.

---

# 18. Payment System

Payment belongs to a booking.

Payment statuses:

```text
PENDING
SUCCESS
FAILED
REFUNDED
```

Important:

```text
Payment QR ≠ Ticket QR
```

They are separate systems.

The payment process should be:

```text
Pending Booking
      ↓
Checkout
      ↓
Payment QR / Payment Mechanism
      ↓
Payment Verification
      ↓
SUCCESS
      ↓
Booking CONFIRMED
```

Never trust the browser to simply send:

```text
payment_success = true
```

Payment success must be verified by the backend/payment mechanism.

For an academic/demo implementation, a controlled payment simulation can be used if a real payment gateway is not available, while keeping the architecture replaceable for a real provider later.

---

# 19. Ticket System

After successful payment and booking confirmation, MovieMate generates a ticket.

Ticket information should include:

```text
Movie
Cinema
Screen
Date
Time
Seats
Seat Category
Amount
Booking ID
Ticket ID
QR Code
```

The ticket should have a unique:

```text
ticket_code
```

and secure:

```text
qr_token
```

---

# 20. Ticket QR Verification

The ticket QR is used to verify whether a ticket is valid.

The flow is:

```text
Ticket PDF
    ↓
QR Code
    ↓
Scanner
    ↓
QR Token
    ↓
Django
    ↓
Ticket Validation
```

Possible results:

```text
VALID
ALREADY USED
INVALID
CANCELLED
EXPIRED
```

A valid ticket can only be used once.

The lifecycle is:

```text
VALID
  ↓
USED
```

A second scan must return:

```text
ALREADY USED
```

The backend, not the frontend, decides whether a ticket is valid.

---

# 21. PDF Ticket

After successful booking confirmation, the customer can download a PDF ticket.

The PDF should contain:

```text
MovieMate Branding
Movie
Cinema
Screen
Date
Time
Seats
Amount
Booking ID
Ticket QR
```

The PDF should follow the MovieMate ticket-inspired design.

PDF generation should be handled by a dedicated service.

---

# 22. Database Tables

MovieMate uses these 14 primary tables:

```text
1. User
2. City
3. Cinema
4. Screen
5. Seat
6. Movie
7. MovieAllocation
8. Show
9. ShowSeatPrice
10. Booking
11. BookingSeat
12. Payment
13. Ticket
14. SeatLock
```

---

# 23. Database Relationships

The major relationships are:

```text
User
 │
 └──< Booking
          │
          ├──< BookingSeat >── Seat
          │
          ├── Payment
          │
          └── Ticket
```

Cinema hierarchy:

```text
City
 │
 └──< Cinema
          │
          └──< Screen
                   │
                   └──< Seat
```

Movie hierarchy:

```text
Movie
 │
 ├──< MovieAllocation >── Cinema
 │
 └──< Show >── Cinema
             │
             └── Screen
```

Show pricing:

```text
Show
 │
 └──< ShowSeatPrice
```

Seat locking:

```text
SeatLock
 ├── Show
 ├── Seat
 └── User
```

---

# 24. Foreign Key Map

```text
Cinema.city_id
    → City.id

Screen.cinema_id
    → Cinema.id

Seat.screen_id
    → Screen.id

MovieAllocation.movie_id
    → Movie.id

MovieAllocation.cinema_id
    → Cinema.id

Show.movie_id
    → Movie.id

Show.cinema_id
    → Cinema.id

Show.screen_id
    → Screen.id

ShowSeatPrice.show_id
    → Show.id

Booking.user_id
    → User.id

Booking.show_id
    → Show.id

BookingSeat.booking_id
    → Booking.id

BookingSeat.seat_id
    → Seat.id

Payment.booking_id
    → Booking.id

Ticket.booking_id
    → Booking.id

SeatLock.show_id
    → Show.id

SeatLock.seat_id
    → Seat.id

SeatLock.user_id
    → User.id
```

---

# 25. Client UI Design

The client uses:

```text
DARK + RED
```

Primary red:

```text
#E8283F
```

Primary client colors:

```text
Background:
#111018

Surface:
#1A1823

Elevated:
#232030

Border:
#332F42

Primary Red:
#E8283F

Dark Red:
#8A1C2C

Primary Text:
#F3F1EC

Muted Text:
#9C97AC

Faint Text:
#6B6779
```

---

# 26. Typography

MovieMate uses:

```text
Bebas Neue
Plus Jakarta Sans
Space Mono
```

### Bebas Neue

Use for:

* Large headings.
* Movie titles.
* Hero titles.
* Section headings.
* Branding.

### Plus Jakarta Sans

Use for:

* Body text.
* Navigation.
* Buttons.
* Forms.
* General UI.

### Space Mono

Use for:

* Ticket information.
* Booking IDs.
* Metadata.
* Technical labels.
* Small uppercase information.

Do not randomly introduce additional fonts.

---

# 27. Client Design Language

MovieMate should feel like:

```text
Modern Cinema
+
Premium Ticket Experience
+
Dark Theme
+
Strong Red Accent
```

The UI should use:

* Rounded cards.
* Rounded buttons.
* Pill-shaped filters.
* Dark surfaces.
* Subtle borders.
* Strong typography.
* Movie posters.
* Ticket/perforation motifs.
* Cinematic hero sections.

Do not make the client UI look like a generic e-commerce website.

---

# 28. Navbar

The client navbar should be:

```text
Sticky
Dark
Semi-transparent
Blurred
Bordered
```

It should include:

```text
MovieMate Logo
City Selector
Search
Movies
My Bookings
Offers
Login/Signup
```

The logo should use `Bebas Neue`.

`MATE` should use the primary red accent.

---

# 29. Hero Section

The hero section should include:

```text
Movie Information
Movie Title
Description
Metadata
Tags
Book Now
Watch Trailer
Movie Poster
Slider Controls
Slider Indicators
```

The hero can dynamically display movies from:

```text
HOT
TRENDING
RATING
NEW
```

The hero should use a dark cinematic background with subtle red atmospheric effects.

Do not use excessive gradients.

---

# 30. Movie Cards

Movie cards should have a cinematic ticket-stub style.

Structure:

```text
Poster
   ↓
Perforated Divider
   ↓
Movie Metadata
   ↓
Book Tickets
```

Cards should have:

```text
Rounded corners
Dark surfaces
Subtle borders
2:3 poster ratio
```

Hover behavior should be subtle.

Do not use excessive animations.

---

# 31. Ticket Design

Ticket-related UI should use:

```text
Dark background
Red accent
Perforated divider
Bebas Neue
Space Mono
QR code
```

The ticket should feel like a premium cinema ticket rather than a normal invoice.

---

# 32. Authentication Design

Desktop authentication can use a split-screen layout:

```text
LEFT:
MovieMate cinematic/ticket visual

RIGHT:
Login/Signup form
```

The form should use:

```text
Dark surface
Thin border
Rounded inputs
Red focus state
Clear labels
```

On mobile, the decorative visual panel can be hidden and the form can occupy the screen.

---

# 33. Seat Selection UI

Seat selection should clearly display:

```text
SILVER
GOLD
PLATINUM
```

Seat states:

```text
AVAILABLE
SELECTED
LOCKED
BOOKED
```

Do not rely only on color to communicate state.

The actual seat layout must come from the configured screen and database.

Do not hardcode seat layouts into the frontend.

---

# 34. Booking UI

The booking flow should visually communicate:

```text
Movie
 ↓
Cinema
 ↓
Show
 ↓
Seats
 ↓
Checkout
 ↓
Payment
 ↓
Confirmation
```

The current step should use the primary accent.

---

# 35. Admin UI Design

The custom admin interface uses:

```text
DARK + BLUE
```

It should still feel like MovieMate.

Structure:

```text
Sidebar
   ↓
Top Navigation
   ↓
Dashboard Content
```

Sidebar sections may include:

```text
Dashboard

Movies
Cinemas
Screens
Seats
Movie Allocation
Shows

Bookings
Payments
Tickets

Users

Analytics

Settings
```

The exact admin blue palette should remain consistent throughout the admin interface.

---

# 36. Admin Dashboard

Dashboard should display useful metrics such as:

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

Analytics may include:

```text
Bookings by Date
Revenue by Date
Tickets Sold by Movie
Most Booked Movies
Cinema Performance
```

Do not add meaningless charts simply to make the dashboard look complex.

---

# 37. Responsive Design

MovieMate must work on:

```text
Desktop
Laptop
Tablet
Mobile
```

Responsive behavior is required for:

* Navbar.
* Hero.
* Movie grids.
* Movie cards.
* Authentication.
* Cinema selection.
* Seat selection.
* Checkout.
* Ticket.
* Admin dashboard.

Mobile layouts should remain usable rather than simply shrinking desktop layouts.

---

# 38. Security Rules

Security is a priority.

The following must be protected:

```text
Authentication
Authorization
Admin Access
Bookings
Seats
Payments
Tickets
API Keys
User Data
```

Use Django's authentication and authorization system.

CSRF protection must remain enabled.

Never expose:

```text
SECRET_KEY
DATABASE_PASSWORD
OMDB_API_KEY
PAYMENT_SECRET
```

to the browser.

Store secrets in `.env`.

Never commit `.env`.

---

# 39. Backend Rules

Django handles:

* Authentication.
* Authorization.
* Validation.
* Business logic.
* Database operations.
* Booking logic.
* Seat availability.
* Seat locking.
* Payment verification.
* Ticket verification.
* Price calculation.

Critical business logic must never depend only on JavaScript.

---

# 40. Frontend Rules

Frontend uses:

```text
HTML
CSS
JavaScript
```

JavaScript may handle:

* Dynamic UI.
* AJAX/fetch.
* Seat selection.
* Filters.
* Search interactions.
* Hero slider.
* QR scanner interface.

JavaScript must not be the source of truth for:

```text
Price
Seat availability
Payment status
Booking status
Ticket validity
Permissions
```

---

# 41. Database Rules

Use PostgreSQL.

Use proper:

* Foreign keys.
* Unique constraints.
* Indexes where appropriate.
* Transactions.
* Validation.

Do not duplicate information unnecessarily.

Do not use SQLite as the final database.

---

# 42. Booking Integrity Rules

Double booking must be prevented at the backend/database level.

The system must handle:

```text
Two users selecting the same seat
Expired seat locks
Payment failure
Duplicate requests
Concurrent booking requests
```

Use database transactions and appropriate locking.

Never rely only on:

```javascript
if (seat.available) {
    bookSeat();
}
```

---

# 43. Price Integrity

The frontend may display:

```text
Silver ₹150
Gold ₹200
Platinum ₹300
```

but Django must calculate the actual amount.

Never trust a client-provided total.

The historical amount paid must be stored with the booking.

---

# 44. AI Coding Rules

Any AI working on MovieMate must:

1. Read this document completely before coding.
2. Inspect the existing code before modifying it.
3. Follow the documented architecture.
4. Follow the database relationships.
5. Follow the UI design.
6. Follow the current development phase.
7. Avoid inventing features.
8. Avoid changing the stack.
9. Avoid blindly replacing complete files.
10. Preserve working functionality.
11. Test significant changes.
12. Update the project memory after meaningful progress.

---

# 45. AI Must Not Assume

The AI must not assume:

* A package is installed.
* A model exists.
* A migration exists.
* A URL exists.
* A file contains specific code.
* A payment provider is configured.
* A feature has already been implemented.

If the project can be inspected, inspect it first.

---

# 46. AI Error-Fixing Workflow

When an error occurs:

```text
Read Error
    ↓
Identify Root Cause
    ↓
Inspect Relevant Code
    ↓
Apply Minimal Correct Fix
    ↓
Test
```

Do not randomly modify multiple files.

Do not hide errors using:

```python
try:
    ...
except:
    pass
```

---

# 47. Development Phases

MovieMate must be built incrementally.

The official development order is:

```text
Phase 0 — Project Setup
        ↓
Phase 1 — Database + Authentication Foundation
        ↓
Phase 2 — Movie/Cinema/Screen/Seat/Show Data
        ↓
Phase 3 — Client Movie Discovery
        ↓
Phase 4 — Cinema + Show + Seat Selection
        ↓
Phase 5 — Booking + Seat Locking
        ↓
Phase 6 — Payment
        ↓
Phase 7 — Ticket PDF + QR Verification
        ↓
Phase 8 — Custom Admin Dashboard
        ↓
Phase 9 — Analytics
        ↓
Phase 10 — UI Polish + Responsive Design
        ↓
Phase 11 — Testing + Security
        ↓
Phase 12 — Deployment
```

Do not attempt to build the entire application in one step.

---

# 48. Phase 0 — Project Setup

Tasks:

* Create virtual environment.
* Install Django.
* Configure PostgreSQL.
* Configure `.env`.
* Configure `.env.example`.
* Configure `.gitignore`.
* Create Django project.
* Create Django apps.
* Configure templates.
* Configure static files.
* Configure media.
* Configure URLs.
* Initialize Git.

---

# 49. Phase 1 — Authentication

Build:

```text
Signup
Login
Logout
Profile
Edit Profile
Password Change
```

Use a custom User model from the beginning.

---

# 50. Phase 2 — Core Data

Build:

```text
City
Cinema
Screen
Seat
Movie
MovieAllocation
Show
ShowSeatPrice
```

During this phase, Django's built-in admin may be used to create test data.

The complete custom admin dashboard does not need to be built yet.

---

# 51. Phase 3 — Client Movie Discovery

Build:

```text
Homepage
Hero
Movie Search
Movie Listing
Movie Details
City Selection
Categories
Movie Cards
```

Use the client red theme.

---

# 52. Phase 4 — Cinema + Shows + Seats

Build:

```text
Cinema Selection
Show Selection
Date Selection
Seat Layout
Seat Categories
Dynamic Pricing
Booking Summary
```

The seat layout must come from the database.

---

# 53. Phase 5 — Booking

Build:

```text
Booking
BookingSeat
SeatLock
Booking History
```

Implement:

* Transactions.
* Double-booking protection.
* Seat expiration.
* Backend price validation.

---

# 54. Phase 6 — Payment

Build:

```text
Payment
Payment UI
Payment Verification
Success/Failure Handling
```

Payment QR and ticket QR must remain separate.

---

# 55. Phase 7 — Ticket

Build:

```text
Ticket
Ticket QR
QR Verification
PDF Ticket
Download Ticket
Used Ticket State
```

---

# 56. Phase 8 — Custom Admin

Build the full custom admin dashboard after the core customer booking flow works.

Admin can manage:

```text
Movies
Cinemas
Screens
Seats
Movie Allocation
Shows
Bookings
Payments
Tickets
Users
```

Admin theme:

```text
Dark + Blue
```

---

# 57. Phase 9 — Analytics

Build useful metrics:

```text
Users
Movies
Cinemas
Shows
Bookings
Revenue
Tickets Sold
Movie Performance
Cinema Performance
```

---

# 58. Phase 10 — UI Polish

Review the complete application:

* Client.
* Authentication.
* Movie pages.
* Cinema pages.
* Show pages.
* Seat selection.
* Checkout.
* Payment.
* Confirmation.
* Ticket.
* Admin dashboard.

Ensure consistent design and responsiveness.

---

# 59. Phase 11 — Testing

Test:

### Authentication

```text
Signup
Duplicate email
Invalid login
Logout
Protected pages
Profile update
```

### Movies

```text
OMDb search
Movie import
Categories
Inactive movies
```

### Shows

```text
Valid show
Invalid allocation
Screen conflicts
Cancelled show
Completed show
```

### Booking

```text
Single seat
Multiple seats
Same seat by two users
Expired lock
Payment failure
Successful payment
Cancelled booking
```

### Ticket

```text
Valid QR
Invalid QR
Used QR
Cancelled ticket
Expired ticket
```

---

# 60. Phase 12 — Deployment

Production architecture:

```text
Internet
   ↓
Nginx
   ↓
Gunicorn
   ↓
Django
   ↓
PostgreSQL
```

External integrations:

```text
Django
 ├── OMDb
 └── Payment Provider
```

Before deployment:

* `DEBUG=False`.
* Configure allowed hosts.
* Configure production database.
* Configure HTTPS.
* Secure secrets.
* Configure static files.
* Configure media.
* Configure backups.

---

# 61. Documentation Files

MovieMate documentation consists of:

```text
PRD.md
Architecture.md
Rules.md
Phases.md
Design.md
Database.md
Memory.md
PROJECT_CONTEXT.md
```

This file, `PROJECT_CONTEXT.md`, is the **single file intended to be given to a new AI** when only one file can be shared.

---

# 62. Current Project Status

At the beginning of development:

```text
Documentation:
COMPLETE

Coding:
NOT STARTED
```

Documentation completed:

```text
PRD.md
Architecture.md
Rules.md
Phases.md
Design.md
Database.md
Memory.md
PROJECT_CONTEXT.md
```

Current development phase:

```text
Phase 0 — Project Setup
```

---

# 63. Current Technical Decisions

The following decisions are already approved:

```text
Frontend:
HTML + CSS + JavaScript

Backend:
Django

Database:
PostgreSQL

Movie API:
OMDb

Client Theme:
Dark + #E8283F Red

Admin Theme:
Dark + Blue

Authentication:
Custom Django User

Profile Images:
Not required

Architecture:
Modular Django Monolith

Django Apps:
client
admin_panel
core

Business Logic:
services/
```

---

# 64. Important Non-Requirements

Do not add these unless explicitly requested:

```text
Social Login
User Profile Pictures
Reviews
Watchlists
Favorites
Food Ordering
Loyalty Programs
Subscriptions
Coupons
AI Recommendations
Chat System
Unrequested APIs
Unrequested Frameworks
```

---

# 65. Important Architecture Principle

MovieMate should remain:

```text
Simple
Modular
Secure
Maintainable
```

Do not create unnecessary complexity.

Do not introduce microservices.

Do not split every model into its own Django application.

Do not change the approved technology stack without approval.

---

# 66. Final System Architecture

```text
                         MOVIEMATE
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           CLIENT        ADMIN PANEL       SERVICES
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                            CORE
                             │
                             ▼
                         PostgreSQL
```

---

# 67. Final Customer Flow

```text
Customer
   ↓
Signup/Login
   ↓
Select City
   ↓
Search Movie
   ↓
Select Movie
   ↓
Select Cinema
   ↓
Select Show
   ↓
Select Seats
   ↓
Seat Lock
   ↓
Checkout
   ↓
Payment
   ↓
Payment Verification
   ↓
Booking Confirmation
   ↓
Ticket Generation
   ↓
PDF Download
   ↓
QR Ticket Verification
```

---

# 68. Final Admin Flow

```text
Admin
   ↓
Dashboard
   │
   ├── Movies
   │     ↓
   │   OMDb Search
   │     ↓
   │   Movie Registration
   │
   ├── Cinemas
   │     ↓
   │   Screens
   │     ↓
   │   Seats
   │
   ├── Movie Allocation
   │
   ├── Shows
   │
   ├── Bookings
   │
   ├── Payments
   │
   ├── Ticket Verification
   │
   └── Analytics
```

---

# 69. Final Rule for AI

Before writing code, always follow:

```text
Read Context
     ↓
Understand Current Phase
     ↓
Inspect Existing Project
     ↓
Plan the Requested Change
     ↓
Implement Only What Is Required
     ↓
Test
     ↓
Fix Problems
     ↓
Update Memory
```

### Most Important Rule

> **Do not make MovieMate work by breaking its architecture, database integrity, security, or approved design.**

When uncertain about a requirement, do not invent a solution. Identify the uncertainty and ask for clarification.

MovieMate must be built incrementally and must remain consistent with this document throughout development.
<!--  -->

moviemate/
│
├── manage.py
├── requirements.txt
│
├── moviemate/                 # project config folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py                # main urls, includes app urls
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # signup/login/profile (shared)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/accounts/
│
├── movies/                    # client-side: browse movies, book tickets
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/movies/
│
├── bookings/                  # client-side: ticket booking, seat selection
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/bookings/
│
├── dashboard/                 # your custom admin panel (staff only)
│   ├── views.py
│   ├── urls.py
│   └── templates/dashboard/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                 # base.html, shared layout
│   └── base.html
│
└── media/                     # uploaded posters etc.