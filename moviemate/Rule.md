# MovieMate — Development Rules

## 1. Purpose of This Document

This document defines the rules, boundaries, coding standards, architectural restrictions, security requirements, and development behavior that must be followed while building MovieMate.

These rules apply to:

* AI coding assistants.
* Developers.
* Future contributors.
* Any future development session working on MovieMate.

The goal is to ensure that MovieMate remains:

* Consistent.
* Secure.
* Maintainable.
* Scalable.
* Easy to understand.
* Consistent with the approved PRD and Architecture.
* Consistent with the approved UI design.

---

# 2. Source of Truth

The following files are the primary project references:

```text
PRD.md
Architecture.md
Rules.md
Phases.md
Design.md
Memory.md
```

The priority should be:

```text
PRD.md
   ↓
Architecture.md
   ↓
Rules.md
   ↓
Design.md
   ↓
Phases.md
   ↓
Memory.md
```

If a new implementation conflicts with the PRD or Architecture, do not silently change the architecture.

First identify the conflict and explain it.

---

# 3. Do Not Invent Requirements

The AI must not invent major features that are not part of the approved project requirements.

Do not automatically add:

* Social login.
* User profile pictures.
* Reviews.
* Watchlists.
* Favorites.
* Food ordering.
* Loyalty programs.
* Coupons.
* Subscriptions.
* AI recommendations.
* Chat systems.
* Unrequested APIs.
* Unrequested frameworks.

These may only be added if explicitly approved.

Small technical improvements are allowed when they are required to make an existing feature work correctly.

---

# 4. Technology Restrictions

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

Do not replace the stack with:

```text
React
Next.js
Vue
Angular
Node.js
Express
MongoDB
Laravel
PHP
```

unless explicitly approved.

The project should remain a Django-based application.

---

# 5. Frontend Rules

The frontend must use:

```text
HTML
CSS
JavaScript
```

Do not introduce a frontend framework unnecessarily.

JavaScript should be used when the page requires:

* Dynamic filtering.
* Seat selection.
* AJAX/fetch requests.
* Form interactions.
* Hero slider.
* Search suggestions.
* QR scanner interactions.
* Dynamic UI updates.

Do not use JavaScript for functionality that Django can handle more reliably on the server.

---

# 6. Backend Rules

Django is the central backend.

Django must handle:

* Authentication.
* Authorization.
* Validation.
* Business logic.
* Database operations.
* Booking logic.
* Payment verification.
* Ticket verification.
* Price calculation.
* Seat availability.
* User permissions.

Critical business logic must never depend only on frontend JavaScript.

---

# 7. Database Rules

PostgreSQL is the primary database.

Do not use SQLite for the final MovieMate application.

SQLite may only be used temporarily for experimentation if explicitly approved.

The database should use proper:

* Foreign keys.
* Unique constraints.
* Indexes where appropriate.
* Transactions.
* Relationships.
* Validation.

Do not duplicate information unnecessarily.

---

# 8. Custom User Model Rule

A custom Django User model must be created from the beginning.

Do not start the project with Django's default User model and later replace it.

The user model should use email as the primary login identifier.

There must be no profile-image field.

---

# 9. User Role Rules

The initial roles are:

```text
CUSTOMER
ADMIN
```

Customers must not be able to access admin functionality.

Admins must have explicit authorization before accessing administrative operations.

Do not rely only on hiding admin buttons in HTML.

Permissions must also be enforced by Django.

---

# 10. Authentication Rules

Authentication must use Django's authentication system.

Passwords must never be stored as plain text.

Never:

```python
user.password = password
```

without Django's password hashing mechanism.

Use Django's password handling system.

Protected pages must verify authentication on the backend.

---

# 11. Authorization Rules

Hiding a button is not authorization.

For example:

```text
Admin button hidden
```

does not mean the customer cannot access the admin URL.

Django must explicitly check permissions.

Every sensitive admin endpoint must be protected.

---

# 12. CSRF Rules

CSRF protection must remain enabled.

Do not disable CSRF protection just to make a request work.

If a POST request fails because of CSRF, fix the implementation instead of removing the protection.

---

# 13. Environment Variable Rules

Sensitive values must never be hardcoded.

Examples:

```text
SECRET_KEY
DATABASE_PASSWORD
OMDB_API_KEY
PAYMENT_KEY
PAYMENT_SECRET
EMAIL_PASSWORD
```

These must be stored in `.env`.

Example:

```text
OMDB_API_KEY=your_api_key
```

The `.env` file must never be committed to Git.

The `.env.example` file should contain variable names without real credentials.

---

# 14. OMDb Rules

OMDb should only be accessed through the dedicated movie service.

The API key must come from the environment.

Do not call OMDb directly from templates.

Do not expose the OMDb API key to JavaScript.

Do not expose the API key to the client browser.

The architecture should remain:

```text
Django
   ↓
OMDb Service
   ↓
OMDb API
```

---

# 15. Movie Registration Rules

Movies are not automatically added to MovieMate just because they exist on OMDb.

The administrator must:

```text
Search OMDb
     ↓
Select Movie
     ↓
Review Movie
     ↓
Save Movie
```

Only selected movies should enter the MovieMate database.

---

# 16. Movie Category Rules

The initial categories are:

```text
HOT
TRENDING
RATING
NEW
```

A movie may belong to multiple categories.

Do not create additional categories unless explicitly approved.

These categories control homepage/movie discovery behavior.

---

# 17. Cinema Structure Rules

The cinema hierarchy must remain:

```text
City
 ↓
Cinema
 ↓
Screen
 ↓
Seat
```

A seat belongs to a screen.

A screen belongs to a cinema.

A cinema belongs to a city.

Do not break this relationship without architectural justification.

---

# 18. Seat Rules

Seat categories are:

```text
SILVER
GOLD
PLATINUM
```

A physical seat should not have a global:

```text
is_booked
```

field.

The booking state belongs to the relationship between:

```text
Seat + Show
```

Example:

```text
Seat A1

Show 1 → BOOKED
Show 2 → AVAILABLE
Show 3 → BOOKED
```

---

# 19. Seat Selection Rules

The seat layout shown to the customer must come from the selected screen.

The frontend may display seat states, but Django must verify the actual state before booking.

The customer must never be able to book a seat that:

* Does not exist.
* Does not belong to the selected screen.
* Does not belong to the selected show.
* Is already booked.
* Is currently locked by another customer.

---

# 20. Double Booking Rule

Double booking is one of the highest-priority problems in MovieMate.

The backend must prevent:

```text
User A → Seat A1 → Show 1
User B → Seat A1 → Show 1
```

from both becoming successful bookings.

Use appropriate:

* Database constraints.
* Transactions.
* Row locking.
* Seat-lock logic.

Do not rely only on:

```javascript
if (seat.available) {
    bookSeat();
}
```

because another request may book the seat simultaneously.

---

# 21. Seat Lock Rules

Selected seats should be temporarily locked while the customer completes payment.

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

Expired locks must not permanently block seats.

---

# 22. Price Rules

Prices must always be calculated and validated on the backend.

The frontend may display:

```text
Silver   ₹150
Gold     ₹200
Platinum ₹300
```

but Django must calculate the final amount.

Never trust a client-provided value such as:

```text
total_amount = 50
```

when the actual server-side total is ₹500.

---

# 23. Historical Price Rule

Once a booking is confirmed, the price paid for each seat must be preserved.

If an administrator later changes:

```text
Gold:
₹200 → ₹250
```

an old booking that paid ₹200 must continue showing ₹200.

Historical booking data must not change because future pricing changed.

---

# 24. Show Rules

Every show must belong to:

```text
Movie
Cinema
Screen
Date
Start Time
End Time
```

A show must not be created if:

* The movie is not allocated to the cinema.
* The screen does not belong to the cinema.
* The date is outside the movie's allocation period.
* The show overlaps another show on the same screen.

---

# 25. Show Scheduling Rules

The admin can configure repeated showtimes.

Example:

```text
Movie:
Avengers

Period:
15 Aug → 30 Aug

Times:
10:00 AM
02:00 PM
06:00 PM
09:00 PM
```

The system should create individual show records.

Each show must be independently bookable and trackable.

---

# 26. Show Status Rules

Show statuses are:

```text
UPCOMING
ACTIVE
COMPLETED
CANCELLED
```

A completed show must not accept new bookings.

Historical bookings associated with completed shows must remain available.

---

# 27. Movie Allocation Rules

A movie must be allocated to a cinema before it becomes bookable there.

Allocation contains:

```text
Movie
Cinema
Start Date
End Date
Status
```

A movie may be allocated to multiple cinemas.

There should be an option to allocate a movie to all active cinemas.

---

# 28. Booking Rules

The booking process must be:

```text
Select Movie
   ↓
Select City
   ↓
Select Cinema
   ↓
Select Show
   ↓
Select Seats
   ↓
Temporary Lock
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
```

A booking must not become `CONFIRMED` before payment verification.

---

# 29. Booking Status Rules

Allowed booking statuses:

```text
PENDING
CONFIRMED
CANCELLED
EXPIRED
```

Do not create arbitrary statuses without updating the project documentation.

---

# 30. Payment Rules

The payment system must distinguish between:

```text
Payment QR
```

and:

```text
Ticket QR
```

They are completely different systems.

### Payment QR

Used to make payment.

### Ticket QR

Used to verify the movie ticket.

Never use the ticket QR as proof of payment.

---

# 31. Payment Verification Rule

The backend must never trust the browser to say:

```text
payment_success = true
```

Payment success must come from the actual payment verification mechanism.

For the academic/demo version, a controlled payment simulation may be used if a real gateway is not available.

The payment architecture must remain replaceable so a real payment provider can be integrated later.

---

# 32. Ticket Rules

Every confirmed booking must generate a unique ticket/booking identifier.

The ticket should contain:

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

# 33. Ticket QR Rules

The ticket QR must not contain sensitive information directly.

It should contain a secure ticket identifier/token.

Example:

```text
MM-TICKET-8f92a1c4...
```

The backend must verify the token.

The frontend must never decide whether a ticket is valid.

---

# 34. Ticket Verification Rules

Ticket verification must check:

1. Ticket exists.
2. Ticket belongs to MovieMate.
3. Booking exists.
4. Booking is confirmed.
5. Ticket is not cancelled.
6. Ticket has not already been used.
7. Show information is valid.
8. Ticket has not expired where applicable.

Possible results:

```text
VALID
ALREADY USED
INVALID
CANCELLED
EXPIRED
```

---

# 35. Ticket Usage Rule

A valid ticket can only be used once.

Initial state:

```text
NOT_USED
```

After successful verification:

```text
USED
```

A second scan must return:

```text
ALREADY USED
```

The update must be atomic.

---

# 36. QR Security Rule

Do not put sensitive information such as:

* Passwords.
* Payment secrets.
* Database IDs unnecessarily.
* Personal information.

directly inside the QR code.

The QR should contain only the information required to securely identify the ticket.

---

# 37. PDF Ticket Rules

A PDF ticket should only be generated after successful booking confirmation.

The ticket PDF must contain the ticket QR.

The PDF should visually follow MovieMate's ticket-inspired design.

PDF generation should be handled by a dedicated service instead of being duplicated inside views.

---

# 38. Client UI Rules

The client-side UI must follow the approved MovieMate design.

Primary theme:

```text
DARK + RED
```

Primary red:

```text
#E8283F
```

The UI should maintain:

* Dark cinema atmosphere.
* Rounded cards.
* Rounded buttons.
* Pill-shaped filters.
* Strong typography.
* Movie poster cards.
* Ticket-inspired elements.
* Subtle borders.
* Clean spacing.
* Minimal unnecessary effects.

Do not randomly change the visual language during development.

---

# 39. Admin UI Rules

The admin interface must use the same MovieMate visual identity.

Primary theme:

```text
DARK + BLUE
```

Where the client uses the red accent, the admin should use the blue accent.

The exact admin blue must come from `Design.md`.

Do not use a completely different dashboard template or visual identity without approval.

---

# 40. Typography Rules

The approved UI typography is:

```text
Bebas Neue
Plus Jakarta Sans
Space Mono
```

Use:

### Bebas Neue

For:

* Large headings.
* Movie titles.
* Section headings.
* Branding.

### Plus Jakarta Sans

For:

* Body text.
* Navigation.
* Buttons.
* Forms.
* General UI.

### Space Mono

For:

* Ticket information.
* Technical labels.
* Metadata.
* Booking/ticket identifiers.

Do not randomly introduce additional fonts.

---

# 41. Component Reuse

Repeated UI components should be reusable.

Examples:

```text
Navbar
Footer
Movie Card
Movie Rail
Filter Chip
Button
Modal
Alert
Seat
Ticket
Form Field
Admin Sidebar
Dashboard Card
```

Do not copy the same large HTML structure into multiple pages unnecessarily.

---

# 42. Template Rules

Use Django templates for server-rendered pages.

Use:

```text
base.html
```

for common layout.

Use reusable template components/includes for repeated UI.

Avoid putting large amounts of business logic inside templates.

Templates should primarily handle presentation.

---

# 43. JavaScript Rules

JavaScript should handle:

* UI interactions.
* Dynamic frontend behavior.
* AJAX/fetch requests.
* Seat selection interface.
* Search interactions.
* Hero slider.
* Filters.
* QR scanner interface where required.

JavaScript must not be the source of truth for:

* Price.
* Seat availability.
* Payment status.
* Booking status.
* Ticket validity.
* Permissions.

---

# 44. View Rules

Django views should remain reasonably small.

If a view contains complex business logic, move that logic into a service.

Bad:

```text
View
 ├── Validate everything
 ├── Calculate price
 ├── Lock seats
 ├── Create payment
 ├── Generate QR
 ├── Generate PDF
 └── Confirm booking
```

Prefer:

```text
View
   ↓
Service
   ↓
Business Logic
```

---

# 45. Service Layer Rules

Use services for complex operations such as:

```text
OMDb movie import
Show scheduling
Seat locking
Booking creation
Payment verification
Ticket verification
PDF generation
QR generation
```

Services should contain business logic that may be reused by multiple views.

---

# 46. Error Handling Rules

Errors must be handled gracefully.

Examples:

```text
Movie not found
Cinema unavailable
Show unavailable
Seat unavailable
Payment failed
Booking expired
Invalid ticket
Ticket already used
Unauthorized access
```

The user should receive a clear message.

Do not expose:

* Tracebacks.
* SQL queries.
* Secret keys.
* Internal file paths.
* Sensitive backend information.

---

# 47. Error Handling Principle

Never hide an error just to make the application appear to work.

Bad approach:

```text
try:
    ...
except:
    pass
```

Do not silently ignore exceptions.

Errors should be:

* Handled when expected.
* Logged when appropriate.
* Shown to users in a safe form.

---

# 48. Database Migration Rules

Whenever a model changes:

```text
python manage.py makemigrations
python manage.py migrate
```

must be considered.

Do not manually edit migration files unless there is a clear reason.

Do not delete migrations simply to solve a database problem.

If migrations become inconsistent, diagnose the actual problem.

---

# 49. Django ORM Rules

Use Django ORM for database operations.

Avoid raw SQL unless there is a strong technical reason.

Use:

```python
select_related()
prefetch_related()
```

where appropriate to prevent unnecessary database queries.

Avoid N+1 query patterns.

---

# 50. Database Transaction Rules

Use transactions for operations where multiple database changes must succeed together.

Especially:

```text
Booking
Seat Locking
Payment Confirmation
Ticket Verification
```

A partially completed booking must not leave the database in an inconsistent state.

---

# 51. URL Rules

URLs should be:

* Simple.
* Predictable.
* REST-like where appropriate.
* Named using Django URL names.

Do not hardcode URLs inside templates.

Prefer:

```django
{% url 'movie_detail' movie.id %}
```

instead of manually writing paths.

---

# 52. Form Rules

User input must be validated on the backend.

This includes:

* Signup.
* Login.
* Profile updates.
* Cinema creation.
* Movie management.
* Show creation.
* Seat selection.
* Booking.
* Payment-related data.

HTML validation is useful but is not sufficient.

---

# 53. Admin Rules

The custom MovieMate admin dashboard must be protected.

Customers must never be able to access admin functionality by manually entering an admin URL.

Every admin operation must perform backend authorization.

---

# 54. File Upload Rules

MovieMate does not require user profile image uploads.

Do not add profile image upload functionality.

Any future file upload must:

* Validate file type.
* Validate file size.
* Use safe filenames/storage.
* Avoid exposing sensitive files.

---

# 55. API Rules

If Django endpoints are used through JavaScript:

* Validate requests on the server.
* Return appropriate HTTP status codes.
* Return predictable JSON structures.
* Do not expose sensitive information.
* Authenticate protected requests.
* Validate all parameters.

Do not create APIs simply because an operation can be done with an API.

Use APIs where they provide a clear benefit.

---

# 56. OMDb Failure Rules

If OMDb is unavailable:

```text
OMDb API
   ↓
Error
   ↓
User-friendly message
```

Do not crash the entire admin dashboard.

Do not expose the OMDb API error directly to the user.

---

# 57. Payment Failure Rules

If payment fails:

```text
Payment FAILED
      ↓
Booking remains unconfirmed
      ↓
Seat lock expires/releases
      ↓
Seat becomes available
```

Do not mark a failed payment as a successful booking.

---

# 58. Booking Failure Rules

If booking creation fails:

* Do not charge the user without a valid booking flow.
* Do not leave seats permanently locked.
* Do not create duplicate bookings.
* Roll back incomplete database operations where necessary.

---

# 59. Completed Show Rules

Once a show has ended:

```text
Show → COMPLETED
```

The system must:

* Stop new bookings.
* Keep historical bookings.
* Keep tickets.
* Keep payment records.
* Keep analytics data.

Do not delete completed shows automatically.

---

# 60. Git Rules

Do not commit:

```text
.env
__pycache__/
*.pyc
venv/
.venv/
media/private/
```

Use `.gitignore`.

Commit messages should clearly describe the change.

Examples:

```text
feat: add movie search
feat: implement seat selection
fix: prevent duplicate seat booking
feat: add ticket verification
style: update client movie cards
```

---

# 61. Code Quality Rules

Code should be:

* Readable.
* Consistent.
* Modular.
* Properly named.
* Properly formatted.
* Free of unnecessary duplication.

Avoid:

```text
Huge views
Huge models
Huge JavaScript files
Duplicate HTML
Duplicate business logic
Magic numbers
Hardcoded secrets
```

---

# 62. Naming Rules

Use descriptive names.

Good:

```text
MovieAllocation
BookingSeat
ShowSeatPrice
verify_ticket()
lock_seats()
create_booking()
```

Avoid:

```text
x
temp
data1
abc
test2
thing
```

unless the variable is genuinely temporary and obvious.

---

# 63. Comments

Comments should explain **why**, not simply repeat **what** the code does.

Bad:

```python
# Create booking
booking = Booking.objects.create(...)
```

Good:

```python
# Use a transaction here because seat reservation and booking creation
# must succeed together to prevent duplicate bookings.
```

Do not add unnecessary comments everywhere.

---

# 64. No Unnecessary Dependencies

Do not install libraries just because they might be useful.

Before adding a dependency:

1. Check whether Django/Python already provides the functionality.
2. Check whether an existing project dependency can handle it.
3. Add a new library only when it provides clear value.

Any new major dependency should be documented.

---

# 65. No Architecture Drift

Do not randomly change:

```text
Django → FastAPI
PostgreSQL → MongoDB
HTML/CSS/JS → React
```

Do not introduce microservices.

Do not split MovieMate into multiple backend services unless explicitly approved.

The initial architecture is a modular Django monolith.

---

# 66. AI Coding Rules

When an AI is working on MovieMate, it must:

1. Read the relevant project documentation before making major changes.
2. Follow `PRD.md`.
3. Follow `Architecture.md`.
4. Follow `Rules.md`.
5. Check `Memory.md` for current project progress.
6. Inspect existing code before modifying it.
7. Avoid overwriting working functionality unnecessarily.
8. Explain architectural changes before implementing major changes.
9. Keep changes focused on the current task.
10. Update `Memory.md` when meaningful development progress occurs.

---

# 67. AI Must Not Assume

The AI must not assume that:

* A library is installed.
* A model already exists.
* A URL exists.
* A variable exists.
* A feature is already implemented.
* A payment provider is configured.
* A database migration exists.
* A file contains specific code.

If the existing project can be inspected, inspect it first.

---

# 68. AI Code Modification Rule

Before modifying existing code:

```text
Inspect
  ↓
Understand
  ↓
Identify required change
  ↓
Modify
  ↓
Test
```

Do not blindly replace entire files when only a small change is required.

Preserve working functionality.

---

# 69. AI Error-Fixing Rule

When an error occurs:

```text
Read Error
   ↓
Find Root Cause
   ↓
Inspect Relevant Code
   ↓
Apply Minimal Correct Fix
   ↓
Test
```

Do not randomly change multiple files until the error disappears.

Do not hide errors with:

```python
try:
    ...
except:
    pass
```

---

# 70. AI Testing Rule

After implementing a significant feature, test:

1. Normal successful flow.
2. Invalid input.
3. Unauthorized access.
4. Edge cases.
5. Failure scenario.

For booking functionality, additionally test:

```text
Two users selecting the same seat
Payment failure
Expired seat lock
Cancelled booking
Already-used ticket
Completed show
```

---

# 71. AI Documentation Rule

If a major architectural decision changes, update the relevant documentation.

Examples:

```text
Architecture change
→ Architecture.md

New development rule
→ Rules.md

New feature requirement
→ PRD.md

Development phase change
→ Phases.md

Visual system change
→ Design.md

Development progress
→ Memory.md
```

Do not leave documentation inconsistent with the actual project.

---

# 72. UI Consistency Rule

New pages must use existing MovieMate components where possible.

Do not create:

```text
Page A → one button style
Page B → completely different button style
Page C → another card style
```

Instead, maintain a consistent design system.

Client:

```text
Dark + Red
```

Admin:

```text
Dark + Blue
```

---

# 73. Responsive Design Rule

MovieMate must work on:

* Desktop.
* Laptop.
* Tablet.
* Mobile.

The existing UI uses responsive behavior for navigation, hero sections, movie grids, authentication pages, and ticket layouts.

Do not design desktop-only pages.

---

# 74. Accessibility Rules

Where practical:

* Use semantic HTML.
* Provide labels for form inputs.
* Use accessible buttons.
* Provide meaningful alt text for images.
* Ensure keyboard navigation works.
* Maintain sufficient text contrast.
* Do not rely only on color to communicate important states.

For example, seat availability should not depend only on color.

---

# 75. Performance Rules

Avoid unnecessary:

* Database queries.
* API calls.
* Large JavaScript files.
* Large images.
* Duplicate requests.

Use caching only where it provides a clear benefit.

Do not prematurely optimize simple functionality.

---

# 76. Security Priority

When a conflict exists between:

```text
Convenience
```

and:

```text
Security
```

security should win.

Especially for:

* Authentication.
* Payments.
* Bookings.
* Seats.
* Tickets.
* Admin access.
* API keys.

---

# 77. Final Rule

The most important rule is:

> **Do not make MovieMate work by breaking the architecture.**

Every implementation should preserve:

```text
PRD
 ↓
Architecture
 ↓
Security
 ↓
Database Integrity
 ↓
UI Design
 ↓
Code Quality
```

MovieMate should remain a clean, modular Django monolith with:

```text
HTML + CSS + JavaScript
          ↓
        Django
          ↓
      PostgreSQL
```

The client side must maintain:

```text
DARK + RED
```

The admin side must maintain:

```text
DARK + BLUE
```

The system must prioritize secure booking, accurate seat availability, verified payments, valid tickets, and maintainable code over shortcuts.
