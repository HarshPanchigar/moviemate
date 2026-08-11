# MovieMate — Product Requirements Document

## 1. Project Overview

**Project Name:** MovieMate

**Project Type:** Online Movie Ticket Booking System

**Frontend:** HTML, CSS, JavaScript

**Backend:** Django

**Database:** PostgreSQL

**External Movie API:** OMDb API

MovieMate is an online movie ticket booking platform where customers can search for movies, select their city, choose a cinema/theater, select a showtime, choose seats, make a payment, and receive a downloadable digital movie ticket.

The system will have two major sides:

1. **Client Side** — for customers/viewers.
2. **Admin Side** — for managing the complete MovieMate platform.

The main purpose of MovieMate is to provide a complete movie booking experience similar to platforms such as BookMyShow, while keeping the system focused on the core features required for this project.

---

# 2. Main Goal

The main goal of MovieMate is:

> **To provide customers with a complete online movie ticket booking experience while allowing administrators to manage movies, cinemas, shows, seats, bookings, payments, users, and ticket verification from one centralized system.**

The complete customer journey should be:

```text
Login / Signup
      ↓
Home
      ↓
Search Movie
      ↓
Select City
      ↓
Select Movie
      ↓
Select Theater
      ↓
Select Show Time
      ↓
Select Seats
      ↓
Payment
      ↓
Booking Confirmation
      ↓
Download Ticket PDF
      ↓
Show QR Ticket at Theat
er
      ↓
Ticket Verification
```

---

# 3. Target Users

MovieMate will have two main types of users.

## 3.1 Customer / Client

Customers are people who want to watch movies and book movie tickets online.

They can:

* Create an account.
* Log in.
* Manage their account.
* Search for movies.
* Select a city.
* View movies available in that city.
* Select a theater.
* View available showtimes.
* Select seats.
* Pay for tickets.
* Receive a booking confirmation.
* Download their ticket as a PDF.
* View their previous and upcoming bookings.
* Use their ticket QR code for verification at the theater.

---

## 3.2 Administrator

The administrator controls the MovieMate platform.

The administrator can:

* View platform analytics.
* Manage users.
* Add cinemas/theaters.
* Manage registered cinemas.
* Register movies.
* Fetch movie information from OMDb.
* Allocate movies to cinemas.
* Configure movie availability dates.
* Configure showtimes.
* Configure ticket prices.
* Manage seat categories.
* View bookings.
* View payment information.
* Verify tickets.
* Manage movie categories.
* Manage movies displayed on the homepage.
* Monitor the complete platform.

---

# 4. Client-Side Requirements

The client side is the main customer-facing portion of MovieMate.

---

# 5. User Registration

A new customer should be able to create a MovieMate account.

The signup form should collect appropriate user information such as:

* Full name.
* Email address.
* Phone number.
* Password.
* Confirm password.

The system should validate all required information before creating the account.

Passwords must be securely hashed using Django's authentication system.

There should be no profile picture functionality.

---

# 6. User Login

Registered customers should be able to log in using their credentials.

The login system should:

* Validate credentials.
* Prevent invalid login attempts.
* Create an authenticated session.
* Redirect the user to the appropriate client-side page after login.

Unauthenticated users should not be able to access protected customer features such as bookings and profile management.

---

# 7. User Profile

Customers should have a profile section.

The profile should allow users to view and edit their personal information.

Possible information:

* Name.
* Email.
* Phone number.

Users should be able to:

* View profile.
* Edit profile.
* Change password.
* Save updated information.

There should be **no profile image/profile picture feature**.

---

# 8. Home Page

The MovieMate homepage will be the primary discovery page.

The homepage should contain:

* Navigation bar.
* Movie search.
* City selection.
* Hero section.
* Featured movies.
* Trending movies.
* New movies.
* Highly rated movies.
* Movie cards.
* Footer.

The homepage should dynamically display movies managed by the administrator.

---

# 9. Hero Section

The hero section should dynamically display movies selected by the administrator.

Each movie can have a category such as:

* Hot
* Trending
* Rating
* New

The administrator can assign these categories while registering/managing movies.

The homepage should dynamically use these categories to determine which movies appear in the hero section.

The hero section can display movie images/posters dynamically.

The displayed hero movies may be randomized from the eligible movies so that the homepage does not always show the exact same movie/order.

The hero section should include a way for the user to proceed toward the movie details/booking flow.

---

# 10. Movie Search

Customers should be able to search for movies.

The search should allow users to search by movie title.

Example:

```text
Search: Avengers
```

The system should display matching movies.

Search results should contain useful movie information such as:

* Movie poster.
* Movie title.
* Release year.
* Genre.
* Rating.
* Language where available.

Selecting a movie should take the user to the movie selection/details flow.

---

# 11. City Selection

MovieMate should support multiple cities.

Before selecting a theater, the customer should select their city.

Example:

```text
Ahmedabad
Mumbai
Delhi
Bangalore
Pune
Surat
Vadodara
```

The available theater list should depend on the selected city.

For example:

```text
City: Ahmedabad

Available Theaters:
├── Theater A
├── Theater B
├── Theater C
└── Theater D
```

A customer should only see theaters that are available in the selected city.

---

# 12. Movie Selection

After searching or browsing movies, the customer selects the movie they want to watch.

The system should show movie information before the booking process.

Possible information:

* Movie title.
* Poster.
* Description.
* Genre.
* Release date.
* Duration.
* Rating.
* Language.
* Other information obtained from OMDb.

The user should then be able to proceed to available theaters/showtimes.

---

# 13. Theater Selection

After selecting a movie and city, MovieMate should display theaters where the selected movie is currently available.

Example:

```text
Movie: Avengers

City: Ahmedabad

Theaters:

┌────────────────────────────┐
│ PVR Cinema                 │
│ Ahmedabad                  │
│                            │
│ 10:00 AM  1:30 PM  6:30 PM │
└────────────────────────────┘

┌────────────────────────────┐
│ INOX Cinema                │
│ Ahmedabad                  │
│                            │
│ 11:00 AM  3:00 PM  8:00 PM │
└────────────────────────────┘
```

The customer selects the theater they want.

---

# 14. Show Date and Showtime

After selecting the theater, the customer should see available movie shows.

A show should contain:

* Movie.
* Theater.
* Screen.
* Date.
* Start time.
* End time.
* Ticket price.
* Seat availability.

Example:

```text
Avengers
PVR Cinema

Today

10:00 AM
01:30 PM
06:30 PM
09:30 PM
```

The customer selects their preferred showtime.

Only active and available shows should be displayed.

---

# 15. Seat Selection

After selecting a show, the customer should be taken to the seat-selection page.

MovieMate should support three primary seat categories:

```text
PLATINUM
GOLD
SILVER
```

Example:

```text
                 SCREEN
        ─────────────────────

PLATINUM
[A1] [A2] [A3] [A4] [A5]

GOLD
[B1] [B2] [B3] [B4] [B5]
[C1] [C2] [C3] [C4] [C5]

SILVER
[D1] [D2] [D3] [D4] [D5]
[E1] [E2] [E3] [E4] [E5]
```

Seats should have different states:

```text
Available
Selected
Booked
```

The frontend should visually differentiate these states.

A customer should not be able to select an already-booked seat.

---

# 16. Ticket Price

Each seat category can have a different price.

Example:

```text
Silver   → ₹150
Gold     → ₹200
Platinum → ₹300
```

The exact prices should be configurable by the administrator.

The total price should be calculated automatically.

Example:

```text
2 × Gold      = ₹400
1 × Platinum  = ₹300
---------------------
Total         = ₹700
```

The server must calculate and validate the final amount.

The frontend price must never be trusted as the final payment amount.

---

# 17. Seat Booking Protection

MovieMate must prevent two customers from successfully booking the same seat for the same show.

For example:

```text
Customer A → Show 1 → Seat A1
Customer B → Show 1 → Seat A1
```

Only one customer should be able to successfully obtain that seat.

The booking system should use appropriate database transactions and validation to protect against double booking.

---

# 18. Payment

After selecting seats, the customer proceeds to payment.

The payment page should display:

* Movie.
* Theater.
* Show date.
* Show time.
* Selected seats.
* Ticket prices.
* Total amount.

The project will use a QR-based payment concept.

The customer will be shown a payment QR code.

Example:

```text
┌─────────────────────────┐
│                         │
│       PAYMENT QR        │
│                         │
│       [ QR CODE ]       │
│                         │
│     Amount: ₹700        │
│                         │
└─────────────────────────┘
```

The customer can scan the QR code using a supported payment application.

### Important Payment Requirement

The system must distinguish between:

**QR code being displayed/scanned**

and

**payment actually being confirmed.**

Simply showing a QR code or clicking a "Payment Done" button must not automatically make a booking confirmed.

For the actual production implementation, payment confirmation should be verified through a suitable payment mechanism/API.

For the academic/demo version, a controlled payment simulation may be implemented if a real payment gateway is not available.

---

# 19. Booking Confirmation

After successful payment verification:

```text
Payment Successful
       ↓
Booking Confirmed
       ↓
Generate Ticket
       ↓
Generate Ticket QR
       ↓
Show Confirmation
```

The booking should receive a unique booking ID.

Example:

```text
Booking ID: MM20260811001
```

---

# 20. Digital Ticket

After successful booking, the customer should receive a digital ticket.

The ticket should contain:

* Movie name.
* Movie poster or relevant movie information.
* Theater name.
* Theater address.
* Screen number/name.
* Date.
* Showtime.
* Selected seats.
* Seat categories.
* Total amount.
* Booking ID.
* Booking status.
* Ticket QR code.

---

# 21. Ticket PDF

The customer should have a **Download Ticket** button.

The system should generate a PDF ticket.

Example:

```text
MOVIEMATE
─────────────────────────────

Movie: Avengers
Theater: MovieMate Cinema
Screen: Screen 2

Date: 15 August 2026
Time: 06:30 PM

Seats:
A1 - Platinum
A2 - Platinum

Total: ₹600

Booking ID:
MM20260815001

        [ QR CODE ]

─────────────────────────────
Present this ticket at the theater.
```

The PDF should contain the QR code used for ticket verification.

---

# 22. Ticket Verification

The QR code on the ticket should contain a secure ticket identifier or verification token.

The administrator/theater staff should be able to scan the QR code.

The system should verify:

* Whether the ticket exists.
* Whether the ticket belongs to MovieMate.
* Whether the ticket is authentic.
* Whether the booking is confirmed.
* Whether the ticket has already been used.
* Whether the ticket belongs to the correct show.
* Whether the show has already ended.

Possible results:

### Valid Ticket

```text
✓ VALID TICKET

Booking ID: MM20260815001
Movie: Avengers
Show: 06:30 PM
Seats: A1, A2
Status: Valid
```

### Already Used

```text
✕ TICKET ALREADY USED
```

### Invalid Ticket

```text
✕ INVALID TICKET
```

### Cancelled Ticket

```text
✕ BOOKING CANCELLED
```

---

# 23. Ticket Usage

A ticket should not be reusable.

Once a valid ticket has been scanned and accepted:

```text
VALID
  ↓
USED
```

If someone attempts to scan the same ticket again:

```text
USED
  ↓
INVALID / ALREADY USED
```

This prevents the same ticket from being used multiple times.

---

# 24. What Happens After the Movie Ends?

Once the show/movie timing has passed, the show should automatically become inactive.

For example:

```text
Show:
15 August
06:30 PM – 09:00 PM

Before 06:30 PM
→ Booking Available

After show starts
→ Booking Closed

After 09:00 PM
→ Show Completed
```

After a show ends:

* New bookings must not be allowed.
* The show should no longer appear in active show listings.
* Existing bookings remain available in booking history.
* Tickets remain available for viewing/download.
* Ticket verification should recognize the show as completed.
* Seat availability for that show no longer matters for new bookings.

Historical booking data should **never be deleted simply because the movie/show has ended**.

---

# 25. My Bookings

Customers should have a **My Bookings** section.

It should contain:

### Upcoming Bookings

Tickets for future shows.

### Completed Bookings

Tickets for shows that have already ended.

### Cancelled Bookings

Bookings that were cancelled.

Each booking should display:

* Movie.
* Theater.
* Date.
* Time.
* Seats.
* Amount.
* Booking ID.
* Status.

The user should be able to open a booking and view/download the ticket.

---

# 26. Admin Dashboard

The administrator dashboard should provide an overview of the MovieMate platform.

The dashboard should contain analytics such as:

* Total users.
* Total cinemas.
* Total movies.
* Total shows.
* Total bookings.
* Total tickets sold.
* Total revenue.
* Today's bookings.
* Upcoming shows.
* Completed shows.
* Most booked movies.
* Most popular cinemas.
* Recent bookings.

Charts and graphs can be used where appropriate.

Example:

```text
ADMIN DASHBOARD

┌────────────┐ ┌────────────┐ ┌────────────┐
│ Users      │ │ Bookings   │ │ Revenue    │
│  2,450     │ │ 8,420      │ │ ₹12.4 L    │
└────────────┘ └────────────┘ └────────────┘

        Booking Analytics
       [ Chart / Graph ]

        Popular Movies
       [ Movie Data ]

        Recent Bookings
       [ Booking Table ]
```

---

# 27. Admin Sidebar

The admin panel should have a sidebar for navigation.

The initial structure should be:

```text
Dashboard

Movies
├── All Movies
├── Add Movie
└── Movie Categories

Cinemas
├── All Cinemas
├── Add Cinema
├── Screens
└── Seats

Shows
├── All Shows
├── Add Show
└── Manage Shows

Bookings
├── All Bookings
└── Ticket Verification

Users
└── All Users

Analytics

Settings
```

The exact arrangement can be refined during the UI/design stage.

---

# 28. Cinema Management

The administrator should be able to add cinemas/theaters.

The Add Cinema form may include:

* Cinema name.
* Address.
* City.
* State.
* Pincode.
* Contact information.
* Number of screens.
* Other required cinema details.

Example:

```text
Cinema Name: MovieMate Cinema
Address: SG Highway
City: Ahmedabad
State: Gujarat
Pincode: 380054
```

After creating a cinema, the administrator should be able to configure its screens and seats.

---

# 29. Screen Management

Each cinema can contain multiple screens.

Example:

```text
PVR Ahmedabad

Screen 1
Screen 2
Screen 3
Screen 4
```

The administrator should be able to configure:

* Screen name/number.
* Seat count.
* Seat layout.
* Seat category.

---

# 30. Seat Category Management

Seats should support:

* Silver.
* Gold.
* Platinum.

Each seat should have a category.

Example:

```text
Screen 1

A1 → Platinum
A2 → Platinum
A3 → Platinum

B1 → Gold
B2 → Gold
B3 → Gold

C1 → Silver
C2 → Silver
C3 → Silver
```

The seat category determines the ticket price for that seat/show.

---

# 31. Movie Registration

Movies should be registered in the MovieMate system before they can be allocated to cinemas.

The project will use the **OMDb API** to fetch movie information.

The administrator should have an **Add Movie** section.

The flow:

```text
Admin
 ↓
Add Movie
 ↓
Search OMDb
 ↓
Search Movie Title
 ↓
Display Results
 ↓
Select Movie
 ↓
Fetch Movie Details
 ↓
Save Movie to MovieMate
```

The system should retrieve appropriate information from OMDb, such as:

* Title.
* Poster.
* Release date/year.
* Genre.
* Director.
* Actors.
* Plot/description.
* Runtime.
* IMDb rating.
* IMDb ID.

Only movies selected by the administrator should become part of the MovieMate movie database.

---

# 32. Movie Categories

When an administrator registers or manages a movie, the administrator should be able to assign homepage/display categories.

The initial categories are:

```text
HOT
TRENDING
RATING
NEW
```

A movie may belong to one or more categories depending on the implementation.

Example:

```text
Avengers

Categories:
✓ HOT
✓ TRENDING
✓ RATING
```

These categories will control how movies are displayed dynamically throughout the client-side homepage.

---

# 33. Movie Allocation to Cinemas

After a movie is registered, the administrator should allocate it to cinemas.

The preferred approach is:

```text
Select Movie
      ↓
Select Cinemas
      ↓
Set Availability Period
      ↓
Set Shows / Timings
      ↓
Set Ticket Prices
      ↓
Publish
```

The administrator should be able to allocate a movie to:

* One cinema.
* Multiple selected cinemas.
* All available cinemas.

Example:

```text
Movie:
Avengers

Allocate To:
☑ Cinema A
☑ Cinema B
☐ Cinema C
☑ Cinema D
```

There should also be an option similar to:

```text
☑ Allocate to all cinemas
```

---

# 34. Movie Availability Period

When allocating a movie, the administrator should define its availability period.

Example:

```text
Movie: Avengers

Available From:
15 August 2026

Available Until:
30 August 2026
```

The movie should only be available for booking during the configured period.

After the end date:

```text
Movie Allocation
       ↓
Expired
       ↓
No New Bookings
```

Existing historical bookings should remain in the system.

---

# 35. Show Scheduling

The administrator should configure when and where the movie will play.

A show should be connected to:

```text
Movie
+
Cinema
+
Screen
+
Date
+
Start Time
+
End Time
+
Ticket Prices
```

Example:

```text
Movie: Avengers

Cinema: Cinema A
Screen: Screen 2

Date:
15 August 2026

Shows:
10:00 AM
01:30 PM
06:30 PM
09:30 PM
```

The administrator should be able to create multiple shows for the same movie.

---

# 36. Show Scheduling Approach

MovieMate should support scheduling repeated showtimes during the movie's availability period.

For example:

```text
Movie:
15 Aug → 30 Aug

Cinema:
Cinema A

Screen:
Screen 1

Showtimes:
10:00 AM
02:00 PM
06:00 PM
09:00 PM
```

The system can generate/create the required individual show records for the applicable dates.

The final scheduling UI and implementation will be defined in `Architecture.md`.

---

# 37. Booking Management

Administrators should be able to see all bookings.

Booking information should include:

* Booking ID.
* Customer.
* Movie.
* Cinema.
* Screen.
* Show date.
* Showtime.
* Selected seats.
* Amount.
* Payment status.
* Booking status.
* Created date.

Administrators should be able to filter bookings by:

* Date.
* Movie.
* Cinema.
* Customer.
* Booking status.
* Payment status.

---

# 38. Payment Records

The admin should be able to view payment information associated with bookings.

Information may include:

* Booking ID.
* Transaction/reference ID.
* Amount.
* Payment status.
* Payment method.
* Payment date/time.

Sensitive payment information must never be exposed unnecessarily.

---

# 39. Ticket Verification System

The admin side should include a ticket verification feature.

The administrator/staff should be able to:

1. Open the ticket verification page.
2. Scan the customer's QR code.
3. Send the ticket identifier to the backend.
4. Verify the ticket.
5. Display the result.

Verification should happen on the server.

The QR code should **not simply contain trusted booking information** that can be manually modified.

Instead, it should contain a secure identifier/token that the backend can verify.

---

# 40. Ticket Verification States

Tickets should have clear states.

```text
CONFIRMED
   ↓
VALID
   ↓
USED
```

Other possible states:

```text
PENDING
CANCELLED
EXPIRED
```

Verification should reject:

* Cancelled tickets.
* Invalid tickets.
* Fake tickets.
* Already-used tickets.
* Tickets for incorrect/expired shows where appropriate.

---

# 41. Data Relationships

The core system relationship should look approximately like this:

```text
USER
 │
 └────────────── BOOKING
                    │
                    ├── SHOW
                    │     │
                    │     ├── MOVIE
                    │     ├── CINEMA
                    │     └── SCREEN
                    │
                    └── BOOKING SEATS
                              │
                              └── SEAT


CINEMA
  │
  └── SCREEN
        │
        └── SEAT


MOVIE
  │
  └── MOVIE ALLOCATION
        │
        ├── CINEMA
        ├── DATE RANGE
        └── SHOWS
```

---

# 42. Important Business Rules

The following rules must always be enforced:

### Rule 1 — Authentication

Users must be authenticated before booking tickets.

### Rule 2 — Movie Availability

A movie can only be booked while it is allocated and available.

### Rule 3 — Show Availability

Users cannot book shows that have already ended.

### Rule 4 — Seat Availability

A booked seat cannot be booked again for the same show.

### Rule 5 — Payment

A booking should only become confirmed after successful payment verification.

### Rule 6 — Ticket

Every confirmed booking must have a unique booking/ticket identifier.

### Rule 7 — Ticket Verification

A ticket can only be successfully used once.

### Rule 8 — Historical Data

Completed shows and previous bookings should not be deleted automatically.

### Rule 9 — Admin Control

Only authorized administrators can add cinemas, register movies, allocate movies, configure shows, and verify tickets.

### Rule 10 — Server-Side Validation

Important booking, seat, price, payment, and ticket operations must be validated on the backend.

---

# 43. Out of Scope for Initial Version

The following features are not required for the first version unless added later:

* User profile pictures.
* Social login.
* Movie reviews.
* Movie ratings submitted by users.
* Watchlist.
* Favorites.
* Food/snack ordering.
* Loyalty programs.
* Coupons.
* Subscription plans.
* Mobile application.
* AI movie recommendations.
* Multiple user types for individual theater employees.
* Advanced cinema owner dashboard.
* Automatic refund system.
* Complex promotional campaigns.

These may be considered future features.

---

# 44. Future Improvements

After the core MovieMate system is complete, possible improvements include:

* Movie recommendations.
* User reviews.
* Watchlist.
* Favorites.
* Food and beverage booking.
* Coupons and discounts.
* Email/SMS notifications.
* WhatsApp notifications.
* Multiple payment gateways.
* Theater staff accounts.
* Advanced analytics.
* Revenue reports.
* QR scanner using mobile camera.
* PWA/mobile application.
* AI-based movie recommendations.

---

# 45. Complete MovieMate Flow

## Customer Flow

```text
                    CUSTOMER
                       │
                       ▼
                  Signup / Login
                       │
                       ▼
                    Home Page
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
        Search Movie        Browse Movies
             │                   │
             └─────────┬─────────┘
                       ▼
                  Select City
                       │
                       ▼
                 Select Movie
                       │
                       ▼
               Select Theater
                       │
                       ▼
                 Select Date
                       │
                       ▼
                 Select Showtime
                       │
                       ▼
                 Select Seats
                       │
              ┌────────┴────────┐
              ▼                 ▼
           Silver             Gold
                                +
                             Platinum
              │                 │
              └────────┬────────┘
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
                Booking Confirmed
                       │
                       ▼
                 Generate Ticket
                       │
                       ▼
                  Generate QR
                       │
                       ▼
                  Download PDF
                       │
                       ▼
                 Visit Theater
                       │
                       ▼
                 Scan Ticket QR
                       │
                       ▼
                Ticket Verified
                       │
                       ▼
                   Watch Movie
```

---

# 46. Complete Admin Flow

```text
                      ADMIN
                        │
                        ▼
                  Admin Dashboard
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
    Cinemas          Movies           Analytics
       │                │
       ▼                ▼
 Add Cinema        Search OMDb
       │                │
       ▼                ▼
 Add Screens       Select Movie
       │                │
       ▼                ▼
 Configure Seats   Save Movie
       │                │
       └────────┬───────┘
                ▼
          Allocate Movie
                │
                ▼
        Select Cinema(s)
                │
                ▼
       Set Date Availability
                │
                ▼
          Create Shows
                │
                ▼
        Set Seat Pricing
                │
                ▼
          Publish Shows
                │
                ▼
          Users Can Book
                │
                ▼
         Admin Monitors
                │
       ┌────────┼─────────┐
       ▼        ▼         ▼
   Bookings  Payments  Analytics
                │
                ▼
         Ticket Verification
```

---

# 47. MVP Definition

The first working version of MovieMate should contain the following:

### Customer

* Signup.
* Login.
* Logout.
* Profile.
* Edit profile.
* Change password.
* Movie search.
* City selection.
* Movie selection.
* Theater selection.
* Show selection.
* Seat selection.
* Silver/Gold/Platinum seats.
* Dynamic pricing.
* QR-based payment flow.
* Booking confirmation.
* Digital ticket.
* Ticket PDF download.
* Ticket QR code.
* My bookings.

### Admin

* Admin login.
* Dashboard.
* Analytics.
* Add cinema.
* Manage cinema.
* Manage screens.
* Manage seats.
* Search OMDb.
* Register movies.
* Movie categories.
* Allocate movies to cinemas.
* Set availability dates.
* Create shows.
* Configure showtimes.
* Configure ticket prices.
* View bookings.
* View payments.
* Ticket verification.

---

# 48. Success Criteria

MovieMate will be considered functionally complete when a customer can successfully complete this journey:

```text
Signup
  ↓
Login
  ↓
Search Movie
  ↓
Select City
  ↓
Select Movie
  ↓
Select Theater
  ↓
Select Show
  ↓
Select Seats
  ↓
Pay
  ↓
Booking Confirmed
  ↓
Download PDF Ticket
  ↓
QR Ticket Generated
  ↓
Admin Scans QR
  ↓
Ticket Successfully Verified
```

At the same time, an administrator must be able to control the movie-booking ecosystem:

```text
Add Cinema
     ↓
Configure Screens & Seats
     ↓
Register Movie from OMDb
     ↓
Allocate Movie to Cinema
     ↓
Set Availability
     ↓
Create Shows
     ↓
Set Prices
     ↓
Customers Book
     ↓
Monitor Bookings & Revenue
     ↓
Verify Tickets
```

---

# 49. Product Vision

MovieMate should provide a clean, simple, and reliable movie-ticketing experience.

The core philosophy is:

> **Discover → Choose → Book → Pay → Get Ticket → Verify → Watch**

The initial version should focus on making this flow reliable before adding advanced entertainment or recommendation features.
