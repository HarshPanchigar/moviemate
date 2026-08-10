Phase 0 → Project Setup
Phase 1 → Authentication
Phase 2 → Movies + OMDb
Phase 3 → Cities + Cinemas + Screens + Seats
Phase 4 → Movie Allocation + Shows
Phase 5 → Seat Selection + Booking
Phase 6 → Payment
Phase 7 → Ticket PDF + QR Verification
Phase 8 → Admin Dashboard + Analytics
Phase 9 → UI Polish + Responsive Design
Phase 10 → Testing + Security + Deployment

# MovieMate — Development Phases

## 1. Purpose

This document divides MovieMate development into manageable phases.

The project must **not** be built all at once.

Each phase should be completed, tested, and stable before moving to the next phase.

The AI/developer must not start future phases prematurely unless a dependency requires a small amount of preparation.

---

# 2. Development Strategy

MovieMate will follow this development order:

```text
Phase 0
Project Setup
      ↓
Phase 1
Database + Authentication Foundation
      ↓
Phase 2
Basic Movie/Cinema/Show Data Management
      ↓
Phase 3
Client Movie Discovery
      ↓
Phase 4
Cinema + Show + Seat Selection
      ↓
Phase 5
Booking + Seat Locking
      ↓
Phase 6
Payment
      ↓
Phase 7
Ticket PDF + QR Verification
      ↓
Phase 8
Custom Admin Dashboard
      ↓
Phase 9
Analytics + Advanced Admin Features
      ↓
Phase 10
Testing + Security + Optimization
      ↓
Phase 11
Deployment
```

---

# 3. Important Development Rule

The complete custom admin dashboard should **not** be built before the client booking system.

During early development, Django's built-in admin can be used to create and manage test data.

This allows the client-side booking system to be developed and tested without spending early development time on the complete custom admin interface.

The custom MovieMate admin dashboard will be developed later.

---

# Phase 0 — Project Setup

## Goal

Create the basic Django project and development environment.

## Tasks

* Create Django project.
* Create virtual environment.
* Install Django.
* Configure PostgreSQL.
* Configure environment variables.
* Create `.env`.
* Create `.env.example`.
* Create `.gitignore`.
* Configure static files.
* Configure media files.
* Configure templates.
* Configure Django apps structure.
* Configure base URL routing.
* Create initial Git repository.
* Create initial project documentation.

## Apps

Create:

```text
accounts
movies
cinemas
shows
bookings
payments
dashboard
```

## Expected Structure

```text
moviemate/
├── manage.py
├── config/
├── apps/
├── services/
├── templates/
├── static/
└── media/
```

## Completion Criteria

Phase 0 is complete when:

* Django runs successfully.
* PostgreSQL connection works.
* Environment variables load correctly.
* Static files work.
* Templates work.
* All initial apps are registered.
* Git repository is configured.
* `.env` is ignored.

---

# Phase 1 — Database + Authentication Foundation

## Goal

Create the database foundation and customer authentication system.

## Tasks

### Custom User

Implement:

* Custom User model.
* Email-based login.
* Password hashing.
* Customer role.
* Admin role.

### Authentication

Implement:

* Signup.
* Login.
* Logout.
* Password change.
* Profile page.
* Edit profile.

## Profile Fields

```text
First Name
Last Name
Email
Phone
Password
```

No profile image.

## Database

Create and apply migrations.

## UI

Implement:

* Login page.
* Signup page.
* Profile page.
* Edit profile page.

Use the approved MovieMate client design:

```text
Dark + Red
```

## Testing

Test:

* Valid signup.
* Duplicate email.
* Invalid password.
* Valid login.
* Invalid login.
* Logout.
* Protected pages.
* Profile editing.
* Password change.

## Completion Criteria

A customer can:

```text
Signup
  ↓
Login
  ↓
View Profile
  ↓
Edit Profile
  ↓
Logout
```

---

# Phase 2 — Core Movie, Cinema, Screen and Show Data

## Goal

Create the data foundation required for movie booking.

This phase does **not** require the complete custom admin dashboard.

Django's built-in admin can be used for initial management and testing.

---

## 2.1 Movie Management

Implement:

* Movie model.
* Movie categories.
* Movie status.
* OMDb integration.
* OMDb search.
* Movie import.

Categories:

```text
HOT
TRENDING
RATING
NEW
```

Admin should be able to:

```text
Search OMDb
    ↓
Select Movie
    ↓
Save Movie
```

---

## 2.2 City Management

Create:

```text
City
```

with:

* Name.
* State.
* Active status.

---

## 2.3 Cinema Management

Create:

```text
Cinema
```

with:

* Name.
* City.
* Address.
* State.
* Pincode.
* Phone.
* Description.
* Active status.

---

## 2.4 Screen Management

Create:

```text
Screen
```

with:

* Cinema.
* Screen name.
* Screen number.
* Active status.

---

## 2.5 Seat Management

Create:

```text
Seat
```

with:

* Screen.
* Row.
* Number.
* Category.
* Active status.

Categories:

```text
SILVER
GOLD
PLATINUM
```

---

## 2.6 Movie Allocation

Create:

```text
MovieAllocation
```

containing:

* Movie.
* Cinema.
* Start date.
* End date.
* Active status.

---

## 2.7 Shows

Create:

```text
Show
```

with:

* Movie.
* Cinema.
* Screen.
* Start time.
* End time.
* Status.

Also create:

```text
ShowSeatPrice
```

for:

```text
Silver
Gold
Platinum
```

---

## Completion Criteria

The developer can create this data:

```text
City
 ↓
Cinema
 ↓
Screen
 ↓
Seats

Movie
 ↓
Movie Allocation
 ↓
Show
 ↓
Seat Prices
```

At this point, the database contains enough information for the client booking flow.

---

# Phase 3 — Client Movie Discovery

## Goal

Build the customer-facing movie browsing experience.

## Tasks

Implement:

* Homepage.
* Navigation.
* City selection.
* Movie search.
* Movie listing.
* Movie details.
* Movie categories.
* Hero section.
* Movie cards.
* Featured movies.
* Trending movies.
* New movies.
* Rating-based movies.

---

## Homepage Flow

```text
Navbar
   ↓
Hero Section
   ↓
Now Showing
   ↓
Filters
   ↓
Movie Cards
   ↓
Upcoming / Weekly Movies
   ↓
Footer
```

---

## Hero Section

The hero should dynamically display movies from:

```text
HOT
TRENDING
RATING
NEW
```

The movies can be randomly selected from eligible movies.

Implement:

* Hero slider.
* Previous/next controls.
* Slide indicators.
* Movie information.
* Book Now button.

---

## Search

Implement:

```text
Search Movie
```

Search by movie title.

Search results should come from the MovieMate database.

Do not call OMDb for every client-side search.

OMDb is primarily used by the admin when registering movies.

---

## Completion Criteria

Customer can:

```text
Open Home
   ↓
Select City
   ↓
Search Movie
   ↓
Browse Movies
   ↓
Open Movie
```

---

# Phase 4 — Cinema, Show and Seat Selection

## Goal

Allow customers to choose where and when they want to watch a movie.

---

## 4.1 Theater Selection

After selecting a movie and city:

```text
Movie
 ↓
City
 ↓
Available Cinemas
```

Only cinemas with an active movie allocation and valid shows should appear.

---

## 4.2 Show Selection

After selecting a cinema:

```text
Cinema
 ↓
Available Dates
 ↓
Available Shows
```

Example:

```text
10:00 AM
01:30 PM
06:30 PM
09:30 PM
```

Only valid upcoming shows should be displayed.

---

## 4.3 Seat Selection

Display the actual screen layout.

Categories:

```text
PLATINUM
GOLD
SILVER
```

Seat states:

```text
AVAILABLE
SELECTED
LOCKED
BOOKED
```

---

## 4.4 Dynamic Pricing

Display the price for each category.

Example:

```text
Silver   ₹150
Gold     ₹200
Platinum ₹300
```

Calculate the selected-seat total.

The final amount must be recalculated by Django.

---

## Completion Criteria

Customer can:

```text
Select Movie
   ↓
Select City
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
See Total
```

No payment or confirmed booking is required yet.

---

# Phase 5 — Booking + Seat Locking

## Goal

Implement the actual booking system.

This is one of the most important phases.

---

## 5.1 Booking Model

Implement:

```text
Booking
BookingSeat
```

Booking statuses:

```text
PENDING
CONFIRMED
CANCELLED
EXPIRED
```

---

## 5.2 Seat Locking

When the customer selects seats:

```text
AVAILABLE
    ↓
LOCKED
```

The lock must have an expiration time.

Example:

```text
Seat A1
Locked for User A
Expires in 10 minutes
```

---

## 5.3 Booking Creation

Flow:

```text
Select Seats
    ↓
Validate Seats
    ↓
Lock Seats
    ↓
Create Pending Booking
    ↓
Calculate Total
    ↓
Checkout
```

---

## 5.4 Double Booking Protection

Implement:

* Transactions.
* Database constraints.
* Proper locking.
* Concurrent request protection.

Test two users attempting to reserve the same seat.

Only one should succeed.

---

## 5.5 Booking History

Create:

```text
My Bookings
```

with:

```text
Upcoming
Completed
Cancelled
```

---

## Completion Criteria

The system can:

```text
Select Seat
   ↓
Lock Seat
   ↓
Create Booking
   ↓
Prevent Duplicate Booking
   ↓
Expire Failed/Abandoned Booking
```

---

# Phase 6 — Payment

## Goal

Implement the payment stage.

---

## 6.1 Payment Model

Create:

```text
Payment
```

Statuses:

```text
PENDING
SUCCESS
FAILED
REFUNDED
```

---

## 6.2 Payment Flow

```text
Pending Booking
      ↓
Checkout
      ↓
Payment QR
      ↓
Payment
      ↓
Payment Verification
      ↓
SUCCESS
      ↓
Confirm Booking
```

---

## 6.3 Payment QR

Display the payment QR to the customer.

Important:

```text
Payment QR ≠ Ticket QR
```

They must remain separate.

---

## 6.4 Payment Security

Never trust:

```text
payment_success=true
```

sent from the browser.

The backend must verify payment through the configured payment mechanism.

If a real payment gateway is not available for the academic version, use a controlled payment simulation while keeping the architecture ready for a real gateway.

---

## Completion Criteria

A successful payment produces:

```text
Payment SUCCESS
      ↓
Booking CONFIRMED
      ↓
Seats CONFIRMED
```

A failed payment produces:

```text
Payment FAILED
      ↓
Booking NOT CONFIRMED
      ↓
Seats Released
```

---

# Phase 7 — Ticket PDF + QR Verification

## Goal

Generate the final ticket and implement ticket verification.

---

## 7.1 Ticket Generation

After confirmed booking:

```text
Booking
   ↓
Ticket ID
   ↓
Ticket QR
   ↓
PDF
```

---

## 7.2 Ticket Information

The ticket must contain:

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
QR Code
```

---

## 7.3 Ticket PDF

Create a downloadable PDF.

The PDF should follow the MovieMate ticket-inspired design.

---

## 7.4 Ticket QR

Generate a secure ticket identifier.

Example:

```text
MM-TICKET-8f92a1c4...
```

Do not put sensitive data directly into the QR.

---

## 7.5 Ticket Verification

Implement:

```text
Scan QR
   ↓
Send Token to Django
   ↓
Find Ticket
   ↓
Validate
   ↓
Return Result
```

Results:

```text
VALID
ALREADY USED
INVALID
CANCELLED
EXPIRED
```

---

## 7.6 Ticket Usage

Valid ticket:

```text
NOT_USED
    ↓
USED
```

Second scan:

```text
ALREADY USED
```

The state change must be atomic.

---

## Completion Criteria

Customer can:

```text
Complete Booking
      ↓
Download Ticket PDF
      ↓
Show QR
```

Admin/staff can:

```text
Scan QR
    ↓
Verify Ticket
    ↓
Mark Ticket Used
```

---

# Phase 8 — Custom MovieMate Admin Dashboard

## Goal

Build the proper custom admin interface.

This is where the full MovieMate admin experience is created.

The dashboard should use:

```text
Dark + Blue
```

instead of the client:

```text
Dark + Red
```

---

## Dashboard

Display:

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

---

## Movie Management

Admin can:

* View movies.
* Add movie.
* Search OMDb.
* Import movie.
* Edit movie.
* Change categories.
* Activate/deactivate movie.

---

## Cinema Management

Admin can:

* Add cinema.
* Edit cinema.
* View cinemas.
* Manage city.
* Manage screens.
* Manage seats.

---

## Show Management

Admin can:

* Allocate movie.
* Select cinema.
* Set availability dates.
* Select screen.
* Create showtimes.
* Set prices.
* Edit shows.
* Cancel shows.

---

## Booking Management

Admin can:

* View bookings.
* Search bookings.
* Filter bookings.
* View booking details.
* View payment status.
* View ticket status.

---

## Ticket Verification

Admin can:

* Open scanner.
* Scan ticket QR.
* Verify ticket.
* Mark ticket used.

---

## Completion Criteria

The custom admin dashboard can manage the entire MovieMate platform without requiring Django's default admin for normal operations.

---

# Phase 9 — Analytics + Advanced Admin Features

## Goal

Add useful analytics and improve administrative control.

---

## Analytics

Implement:

```text
Bookings by Date
Revenue by Date
Tickets Sold by Movie
Most Booked Movies
Most Popular Cinemas
Cinema Performance
```

Use JavaScript charts where appropriate.

---

## Booking Analytics

Example:

```text
Today's Bookings
This Week
This Month
```

---

## Revenue Analytics

Display:

```text
Today's Revenue
Weekly Revenue
Monthly Revenue
Total Revenue
```

---

## Movie Analytics

Display:

```text
Most Booked Movies
Most Viewed/Selected Movies
Movie Ticket Sales
```

Only metrics supported by available database data should be displayed.

---

## Completion Criteria

The admin can understand the overall MovieMate platform from the dashboard without manually checking every booking.

---

# Phase 10 — UI Polish + Responsive Design

## Goal

Bring the entire application to the final MovieMate design standard.

---

## Client Theme

```text
Dark + Red
#E8283F
```

---

## Admin Theme

```text
Dark + Blue
```

---

## Tasks

Review:

* Navbar.
* Hero.
* Movie cards.
* Movie details.
* Search.
* Filters.
* Login.
* Signup.
* Profile.
* Cinema pages.
* Show pages.
* Seat selection.
* Checkout.
* Payment.
* Booking confirmation.
* Ticket.
* My bookings.
* Admin dashboard.
* Admin sidebar.
* Admin tables.
* Admin forms.
* Admin charts.

---

## Responsive Testing

Test:

```text
Desktop
Laptop
Tablet
Mobile
```

Ensure:

* Navigation works.
* Movie grids resize.
* Seat layouts remain usable.
* Forms remain usable.
* Tickets remain readable.
* Admin dashboard works on smaller screens.

---

## Completion Criteria

All major pages follow the approved MovieMate design system.

---

# Phase 11 — Testing + Security

## Goal

Perform full system testing before deployment.

---

## Authentication Tests

Test:

* Signup.
* Duplicate email.
* Invalid login.
* Logout.
* Password change.
* Unauthorized access.
* Admin access protection.

---

## Movie Tests

Test:

* OMDb search.
* Movie import.
* Invalid OMDb result.
* Movie categories.
* Movie activation/deactivation.

---

## Cinema Tests

Test:

* City creation.
* Cinema creation.
* Screen creation.
* Seat creation.
* Seat categories.

---

## Show Tests

Test:

* Valid show.
* Invalid allocation.
* Screen conflict.
* Expired show.
* Cancelled show.

---

## Booking Tests

Test:

```text
Single booking
Multiple seats
Same seat by two users
Expired seat lock
Cancelled booking
Failed payment
Successful payment
```

---

## Ticket Tests

Test:

```text
Valid QR
Invalid QR
Already-used QR
Cancelled ticket
Expired ticket
Completed show
```

---

## Security Tests

Check:

* CSRF.
* Authentication.
* Authorization.
* SQL injection protection.
* XSS protection.
* Secure passwords.
* Environment variables.
* File upload security.
* Payment validation.
* Ticket validation.

---

## Performance Tests

Check:

* Database queries.
* Movie listing.
* Search.
* Seat availability.
* Booking process.
* Dashboard queries.

Avoid unnecessary database queries.

---

## Completion Criteria

All critical user journeys work successfully without known high-severity bugs.

---

# Phase 12 — Deployment

## Goal

Deploy MovieMate to a production environment.

---

## Production Setup

Prepare:

```text
Django
PostgreSQL
Gunicorn
Nginx
```

Architecture:

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

External services:

```text
Django
 ├── OMDb
 └── Payment Provider
```

---

## Production Security

Before deployment:

* Set `DEBUG=False`.
* Configure allowed hosts.
* Configure production database.
* Configure environment variables.
* Configure static files.
* Configure media storage.
* Configure HTTPS.
* Secure secrets.
* Configure database backups.

---

# 4. Phase Dependency Map

The phases depend on each other.

```text
Phase 0
   │
   ▼
Phase 1
   │
   ▼
Phase 2
   │
   ▼
Phase 3
   │
   ▼
Phase 4
   │
   ▼
Phase 5
   │
   ▼
Phase 6
   │
   ▼
Phase 7
   │
   ▼
Phase 8
   │
   ▼
Phase 9
   │
   ▼
Phase 10
   │
   ▼
Phase 11
   │
   ▼
Phase 12
```

Some small tasks may overlap when technically necessary, but major phases should not be skipped.

---

# 5. AI Development Workflow

Whenever the AI starts a phase, it should follow:

```text
Read Documentation
       ↓
Inspect Existing Code
       ↓
Understand Current State
       ↓
Plan Phase
       ↓
Implement
       ↓
Test
       ↓
Fix Errors
       ↓
Verify Completion
       ↓
Update Memory.md
       ↓
Move to Next Phase
```

---

# 6. Phase Completion Rule

A phase is not considered complete simply because the code has been written.

A phase is complete only when:

```text
Feature Implemented
       +
Database Working
       +
UI Working
       +
Validation Working
       +
Error Handling Working
       +
Tests Passed
```

---

# 7. Do Not Skip Core Phases

The AI must not jump directly from:

```text
Login
```

to:

```text
Payment
```

without completing the required dependencies.

For example:

```text
Movie
 ↓
Cinema
 ↓
Show
 ↓
Seat
 ↓
Booking
 ↓
Payment
 ↓
Ticket
```

must exist in the correct order.

---

# 8. Admin Development Strategy

The complete custom admin interface is intentionally delayed.

Early development:

```text
Django Admin
     ↓
Create Test Data
     ↓
Build Client
```

Later:

```text
Custom MovieMate Admin
     ↓
Replace Normal Admin Workflow
```

This allows the core booking system to be tested earlier.

The Django built-in admin may continue to exist as a technical/back-office tool even after the custom admin dashboard is complete.

---

# 9. MVP Completion

The MovieMate MVP is complete when a customer can successfully perform:

```text
Signup
   ↓
Login
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
Checkout
   ↓
Payment
   ↓
Booking Confirmation
   ↓
Download Ticket PDF
   ↓
Show Ticket QR
   ↓
Ticket Verification
```

And the system administrator can:

```text
Manage Movies
      ↓
Manage Cinemas
      ↓
Manage Screens
      ↓
Manage Seats
      ↓
Allocate Movies
      ↓
Create Shows
      ↓
Set Prices
      ↓
View Bookings
      ↓
Verify Tickets
```

---

# 10. Final Development Order

The official MovieMate development order is:

```text
01. Project Setup
        ↓
02. Authentication + Database Foundation
        ↓
03. Movie + Cinema + Screen + Seat + Show Data
        ↓
04. Client Movie Discovery
        ↓
05. Cinema + Show + Seat Selection
        ↓
06. Booking + Seat Locking
        ↓
07. Payment
        ↓
08. Ticket PDF + QR Verification
        ↓
09. Custom Admin Dashboard
        ↓
10. Analytics
        ↓
11. UI Polish + Responsive Design
        ↓
12. Testing + Security
        ↓
13. Deployment
```

MovieMate should be developed incrementally, with each phase producing a working and testable part of the application.

The AI must never attempt to generate the entire application in one step.

The goal is to build MovieMate as a reliable system first and then progressively improve its administration, analytics, design, security, and deployment.
