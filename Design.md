# MovieMate — Design System

## 1. Purpose

This document defines the visual design system for MovieMate.

The design must remain consistent across:

* Customer/client side.
* Authentication pages.
* Movie browsing.
* Movie details.
* Cinema and show selection.
* Seat selection.
* Checkout.
* Payment.
* Booking confirmation.
* Ticket/PDF.
* Admin dashboard.

MovieMate uses two visual themes:

```text
Client:
Dark + Red

Admin:
Dark + Blue
```

The client-side design is based on the approved MovieMate UI reference.

---

# 2. Overall Design Direction

MovieMate should feel like a modern digital cinema and ticket-booking platform.

The visual language should communicate:

* Cinema.
* Premium experience.
* Modern technology.
* Ticket booking.
* Clean navigation.
* Strong movie artwork.
* Simple booking flow.

The design should avoid looking like a generic e-commerce website.

The UI should use the ticket/cinema concept throughout the application.

---

# 3. Client Theme

The primary client theme is:

```text
Dark + Red
```

Primary accent:

```text
#E8283F
```

The reference design uses this color as the main accent for buttons, active navigation, badges, links, filters, logo highlights, and other important UI states.

---

# 4. Client Color System

## Background

```text
Base:
#111018

Surface:
#1A1823

Elevated:
#232030
```

## Borders

```text
Stroke:
#332F42
```

## Primary Accent

```text
Red:
#E8283F
```

## Dark Red

```text
Red Dim:
#8A1C2C
```

## Text

```text
Primary:
#F3F1EC

Muted:
#9C97AC

Faint:
#6B6779
```

These values are taken from the approved UI reference.

---

# 5. Accent Color Usage

The MovieMate red should be used for important actions and highlights.

Use `#E8283F` for:

* Primary buttons.
* Active navigation links.
* Active filters.
* Important links.
* Logo accent.
* Hero accents.
* Rating highlights.
* Booking CTAs.
* Important status indicators.
* Selected states.
* Ticket highlights.

Do not use the red on every element.

The accent should remain visually meaningful.

---

# 6. Admin Theme

The custom admin dashboard should use:

```text
Dark + Blue
```

The admin design should maintain the same overall MovieMate visual language but replace the client's red accent with blue.

The admin should still use:

* Dark surfaces.
* Rounded components.
* Clean typography.
* MovieMate branding.
* Ticket-inspired elements.
* Strong dashboard hierarchy.

The admin must feel like part of MovieMate rather than a completely separate application.

The exact admin blue palette should be defined consistently when the admin UI is implemented.

---

# 7. Typography

MovieMate uses three primary fonts:

```text
Bebas Neue
Plus Jakarta Sans
Space Mono
```

The reference imports these three fonts directly.

---

## 7.1 Bebas Neue

Use for:

* Main headings.
* Movie titles.
* Hero titles.
* Section headings.
* MovieMate branding.
* Large display text.

Example:

```text
MOVIEMATE
NOW SHOWING
CRIMSON HORIZON
BOOK YOUR SHOW
```

The reference uses `Bebas Neue` for display typography and the logo.

---

## 7.2 Plus Jakarta Sans

Use for:

* Body text.
* Navigation.
* Buttons.
* Forms.
* Labels.
* Descriptions.
* General UI.

This is the primary application font.

---

## 7.3 Space Mono

Use for:

* Ticket information.
* Booking IDs.
* Ticket numbers.
* Technical metadata.
* Small uppercase labels.
* Movie metadata.
* Show information.

The reference uses Space Mono for mono-style metadata and labels.

---

# 8. Typography Hierarchy

Use the following hierarchy:

```text
Hero Title
    ↓
Page Title
    ↓
Section Title
    ↓
Card Title
    ↓
Body Text
    ↓
Metadata
```

Hero titles should be large and bold.

Section titles should use `Bebas Neue`.

Body text should remain highly readable.

Metadata should use smaller text and may use `Space Mono`.

---

# 9. Global Layout

Maximum content width:

```text
1400px
```

Desktop horizontal padding:

```text
24px
```

The reference uses a maximum-width container with 24px horizontal padding.

The layout should remain centered.

---

# 10. Border Radius

Primary global radius:

```text
14px
```

Use rounded corners throughout the interface.

Typical components:

```text
Cards:
14px

Hero Poster:
16px

Inputs:
10px

Buttons:
999px

Filter Chips:
999px

Small Badges:
999px
```

The reference uses a 14px global radius and pill-shaped controls.

---

# 11. Buttons

Buttons should be:

* Rounded.
* Bold.
* Compact.
* Easy to identify.
* Consistent across the application.

Primary button:

```text
Background: #E8283F
Text: #FFFFFF
```

The reference primary button uses a flat red background with a subtle dark shadow and a slightly lighter hover state.

---

## Primary Button

Example:

```text
Book Now
Book Tickets
Create Account
Log In
Continue
Proceed to Payment
Download Ticket
```

---

## Secondary/Ghost Button

Use:

```text
Background: transparent
Border: #332F42
Text: #F3F1EC
```

Hover:

```text
Border → darker red accent
```

The reference uses this style for ghost buttons.

---

# 12. Button Interaction

Buttons should have subtle interaction.

Use:

```text
Hover:
Slight background/border change

Active:
Small scale-down effect
```

Avoid excessive animations.

The reference uses a subtle active scale effect and short transitions.

---

# 13. Navigation Bar

The client navbar should be:

```text
Sticky
Dark
Semi-transparent
Blurred
Bottom border
```

The reference uses a sticky navigation bar with a dark translucent background, blur, and border.

---

## Navbar Structure

Desktop:

```text
MOVIEMATE
   ↓
City
   ↓
Search
                    Movies
                    My Bookings
                    Offers
                    Login
                    Sign Up
```

---

## Logo

The logo should read:

```text
MOVIE MATE
```

or:

```text
MOVIEMATE
```

The word `MATE` uses the red accent.

The reference uses `Bebas Neue` for the logo and red for the `MATE` portion.

---

# 14. City Selector

The selected city appears as a pill-shaped navigation element.

Example:

```text
📍 Ahmedabad
```

The location icon uses the primary red accent.

The city selector should eventually become dynamic.

---

# 15. Search Bar

The search bar should use:

```text
Background:
#1A1823

Border:
#332F42

Rounded:
999px
```

Placeholder:

```text
Search movies, cinemas...
```

The reference uses this exact visual structure.

---

# 16. Hero Section

The hero section is one of the most important visual elements of MovieMate.

It should include:

```text
Movie information
Movie title
Description
Movie metadata
Tags
Book Now
Watch Trailer
Movie poster
Category badge
Slider controls
Slider indicators
```

The reference uses a large two-column hero with movie information on the left and poster artwork on the right.

---

# 17. Hero Background

The hero should use a dark layered background.

It may contain subtle:

* Red atmospheric glow.
* Dark gradients.
* Movie artwork influence.
* Soft lighting.

Avoid strong colorful gradients that overpower the movie artwork.

The reference uses subtle layered radial/linear backgrounds.

---

# 18. Hero Title

Hero movie titles use:

```text
Bebas Neue
```

They should be:

* Large.
* Strong.
* High contrast.
* Short line length.
* Visually dominant.

Important words may use the MovieMate red accent.

---

# 19. Hero Metadata

Movie metadata can include:

```text
Certification
Genre
Duration
Language
Rating
```

Example:

```text
UA13+
Action, Sci-Fi
2h 21m
```

Metadata should be compact and visually secondary.

---

# 20. Hero Tags

Hero tags use pill-shaped containers.

Example:

```text
UA13+
Action, Sci-Fi
2h 21m
```

Use:

```text
Background:
#232030

Border:
#332F42

Text:
#9C97AC
```

---

# 21. Hero Poster

Hero posters should:

* Use a 3:4 ratio.
* Have rounded corners.
* Have subtle border/shadow.
* Have a dark bottom overlay.
* Display movie information near the bottom.
* Support category/rating badges.

The reference uses a 3:4 poster ratio, 16px radius, and a strong dark shadow.

---

# 22. Hero Slider

The hero must support multiple movies.

Controls:

```text
Previous
Next
Dots
Automatic Rotation
```

The reference automatically changes slides approximately every 6 seconds and provides manual arrows/dots.
The actual MovieMate implementation should use movies dynamically loaded from the database.

---

# 23. Movie Categories

MovieMate should visually support:

```text
HOT
TRENDING
RATING
NEW
```

These categories can influence:

* Hero movies.
* Movie sections.
* Filters.
* Movie discovery.

---

# 24. Section Headers

Sections should use:

```text
Eyebrow
Section Title
Optional View All
```

Example:

```text
IN THEATRES

NOW SHOWING                         View all →
```

The reference uses a small mono eyebrow followed by a large display title.

---

# 25. Eyebrow Labels

Eyebrow labels use:

```text
Space Mono
Uppercase
Small size
Letter spacing
Red accent
```

They may include a short decorative line before the text.

Example:

```text
— IN THEATRES
```

The reference uses this exact visual concept.

---

# 26. Movie Cards

Movie cards are designed like cinematic ticket stubs.

Structure:

```text
Poster
 ↓
Perforation
 ↓
Genre / Language
 ↓
Book Tickets
```

The reference uses ticket-stub cards with a poster area and perforated divider.

---

# 27. Movie Card Dimensions

Desktop movie cards should be approximately:

```text
220px width
2:3 poster ratio
```

Cards should be horizontally scrollable in rails where appropriate.

The reference uses 220px cards and horizontal scrolling.

---

# 28. Movie Card Hover

On hover:

```text
Card:
Slight upward movement

Border:
Accent becomes more visible
```

Do not use extreme scaling.

The reference uses a subtle upward movement.

---

# 29. Movie Rating Badge

Rating should appear in a small pill.

Example:

```text
★ 8.2
```

Use the red accent for the rating.

The badge should have a dark translucent background and subtle border.

---

# 30. Certification Badge

Certification examples:

```text
U
UA
UA13+
UA16+
A
```

The badge should appear near the top-left of the poster.

---

# 31. Ticket Perforation Motif

Ticket perforation is a core MovieMate visual identity.

Use perforated edges in:

* Movie cards.
* Tickets.
* Booking confirmation.
* PDF tickets.
* Authentication visual ticket.
* Other ticket-related UI where appropriate.

The reference uses repeated circular cut-outs to create the perforation effect.

Do not use the motif on every component.

---

# 32. Weekly Release Strip

The homepage can include a horizontally scrollable weekly-release section.

Each item should use:

```text
Circular movie indicator
Movie name
Genre
```

The reference uses pill-shaped weekly release items.

---

# 33. Authentication Design

Login and signup pages should use a split-screen layout on desktop.

```text
LEFT:
MovieMate visual/ticket section

RIGHT:
Authentication form
```

The reference uses a two-column authentication layout.

---

# 34. Authentication Visual Panel

The left side should include:

* Large display heading.
* Supporting text.
* Floating ticket.
* Ticket metadata.
* Movie information.
* Subtle red glow.

Example concept:

```text
Welcome back
to the front row.

[ Ticket ]
```

---

# 35. Authentication Ticket

The floating ticket should use:

* Dark surface.
* Red border.
* Red glow.
* Ticket perforation.
* Mono metadata.
* Subtle animation.

The reference includes a floating ticket card with a red glow and subtle animation.

Animations must remain subtle.

---

# 36. Authentication Form

Forms should use:

```text
Dark surface
Thin border
Rounded corners
Clear labels
Readable input text
Red focus state
```

The reference uses dark input containers with rounded 10px borders and accent-colored focus states.

---

# 37. Form Fields

Structure:

```text
Label
Input
Optional helper/error
```

Labels should use muted text.

Inputs should use:

```text
Background:
#1A1823

Border:
#332F42

Text:
#F3F1EC
```

---

# 38. Form Focus

When an input receives focus:

```text
Border → MovieMate red/dim red
```

Do not use bright browser-default focus styling.

The reference uses an accent border on focus.

---

# 39. Authentication Mobile Design

On smaller screens:

```text
Desktop:
Visual + Form

Mobile:
Form only
```

The decorative visual panel may be hidden on mobile to preserve usability.

The reference hides the visual panel below approximately 860px.

---

# 40. Filter Chips

Filters should be pill-shaped.

Example:

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

Inactive:

```text
Dark Surface
Dark Border
Muted Text
```

Active:

```text
Red Background
White Text
```

The reference uses this exact interaction pattern.

---

# 41. Booking Flow UI

The booking UI should visually communicate progress.

Recommended flow:

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

Completed steps should be visually distinguishable.

---

# 42. Cinema Selection

Cinema cards should display:

```text
Cinema Name
Address
Distance if available
Available Showtimes
Amenities if supported
```

Do not add amenities unless the data model supports them.

The selected cinema should use the red accent.

---

# 43. Show Selection

Showtimes should be displayed as compact buttons/chips.

Example:

```text
10:00 AM
01:30 PM
04:30 PM
07:30 PM
10:00 PM
```

Available show:

```text
Dark Surface
Red/Neutral Border
```

Selected show:

```text
Red Background
White Text
```

---

# 44. Seat Selection Design

The seat-selection interface must visually separate:

```text
Silver
Gold
Platinum
```

Seat states:

```text
Available
Selected
Locked
Booked
```

Do not communicate state only through color.

Use:

* Color.
* Border.
* Opacity.
* Text/icon where appropriate.

---

# 45. Seat Legend

Display a clear legend:

```text
○ Available
● Selected
○ Booked
○ Locked
```

The actual visual shapes/colors should remain consistent with the MovieMate theme.

---

# 46. Seat Selection Layout

The screen should be visually represented.

Example:

```text
             SCREEN
────────────────────────

   A1 A2 A3 A4 A5 A6

   B1 B2 B3 B4 B5 B6

   C1 C2 C3 C4 C5 C6
```

The actual layout must come from the cinema screen configuration.

Do not hardcode seat layouts.

---

# 47. Booking Summary

The booking summary should display:

```text
Movie
Cinema
Screen
Date
Time
Selected Seats
Seat Categories
Subtotal
Taxes/Fees if applicable
Total
```

The total should be visually emphasized.

---

# 48. Payment UI

Payment should be simple and focused.

Display:

```text
Booking Summary
Total Amount

Payment QR

Payment Status
```

The payment QR should not be confused visually with the ticket QR.

---

# 49. Confirmation UI

Successful booking should feel clearly successful.

Display:

```text
✓ Booking Confirmed

Movie
Cinema
Date
Time
Seats

Booking ID

[ Download Ticket ]
```

The ticket QR should be clearly visible or accessible.

---

# 50. Ticket Design

The MovieMate ticket should use the ticket-stub concept.

Use:

```text
Dark background
Red accent
Perforated divider
Space Mono metadata
Bebas Neue movie title
QR code
```

The ticket should visually resemble a premium cinema ticket rather than a normal invoice.

---

# 51. PDF Ticket

The generated PDF should follow the same design system.

The PDF must contain:

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

The PDF should remain readable when printed.

---

# 52. Admin Dashboard Design

The custom admin dashboard should use:

```text
Dark + Blue
```

The overall structure should include:

```text
Sidebar
       ↓
Top Navigation
       ↓
Dashboard Content
```

---

# 53. Admin Sidebar

The sidebar should contain sections such as:

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

The exact navigation can be refined during the admin phase.

---

# 54. Admin Dashboard Cards

Dashboard cards should display important statistics.

Examples:

```text
Total Users
Total Movies
Total Cinemas
Total Shows
Total Bookings
Revenue
```

Cards should use dark elevated surfaces.

Important values can use the admin blue accent.

---

# 55. Admin Tables

Tables should use:

```text
Dark Surface
Subtle Borders
Readable Header
Compact Rows
Clear Status Badges
```

Example statuses:

```text
ACTIVE
INACTIVE
CONFIRMED
PENDING
CANCELLED
COMPLETED
```

Use blue accent for important active/admin states where appropriate.

---

# 56. Admin Forms

Admin forms should follow the same general form system as the client but use blue as the primary accent.

Example:

```text
Cinema Name
City
Address
Phone
Status

[ Save Cinema ]
```

---

# 57. Admin Movie Import

The OMDb movie-import interface should follow:

```text
Search
   ↓
Results
   ↓
Select Movie
   ↓
Preview
   ↓
Import
```

The imported movie should be visually clear before confirmation.

---

# 58. Admin Analytics

Charts should use the admin visual language.

Possible charts:

```text
Revenue
Bookings
Movies
Cinemas
Ticket Sales
```

Charts should remain clean and readable.

Do not overload the dashboard with unnecessary charts.

---

# 59. Responsive Design

MovieMate must be responsive.

Supported screen sizes:

```text
Desktop
Laptop
Tablet
Mobile
```

## The reference already includes responsive breakpoints for the navigation, hero, authentication pages, and footer.

# 60. Mobile Navigation

On smaller screens:

* Hide desktop search when necessary.
* Collapse navigation.
* Keep primary actions accessible.
* Maintain MovieMate branding.

The navigation should not overflow horizontally.

---

# 61. Mobile Hero

On mobile:

```text
Movie Information
       ↓
Poster
       ↓
CTA
```

The hero should become a single-column layout.

The reference switches the hero from two columns to one column on smaller screens.

---

# 62. Motion and Animation

Animations should be:

* Short.
* Smooth.
* Subtle.
* Purposeful.

Allowed examples:

```text
Card hover
Button press
Hero slider
Ticket floating
Ticket shine
Small transitions
```

Avoid:

* Excessive bouncing.
* Large zoom animations.
* Constant movement.
* Distracting effects.

---

# 63. Shadows

Use dark, soft shadows.

Avoid strong colored neon shadows throughout the application.

The reference uses mostly neutral dark shadows with restrained red glow around specific ticket elements.

---

# 64. Gradients

Gradients may be used for:

* Hero backgrounds.
* Movie artwork.
* Authentication visual backgrounds.
* Subtle decorative elements.

Do not use gradients on primary buttons.

The approved primary button uses a flat red background.

---

# 65. Icons

Icons should be:

* Simple.
* Minimal.
* Consistent.
* Easy to understand.

Icons should not dominate the UI.

Use icons for:

* Search.
* Location.
* Navigation.
* Seats.
* Calendar.
* Clock.
* Payment.
* Ticket.
* Verification.

---

# 66. Images and Movie Posters

Movie posters should maintain their natural aspect ratio.

Primary poster ratio:

```text
2:3
```

Hero poster:

```text
3:4
```

Do not stretch images.

Use appropriate object fitting when required.

---

# 67. Empty States

When no data exists, show a clear empty state.

Examples:

```text
No movies found.

No shows available.

No cinemas available in this city.

No bookings yet.

No tickets found.
```

Empty states should maintain the MovieMate design.

---

# 68. Error States

Errors should use clear visual hierarchy.

Example:

```text
Something went wrong.

We couldn't load the available shows.

[ Try Again ]
```

Avoid technical error messages in the client UI.

---

# 69. Success States

Successful actions should be clearly communicated.

Examples:

```text
Booking confirmed.
Movie added successfully.
Cinema created successfully.
Profile updated successfully.
Ticket verified successfully.
```

Use the appropriate accent/status treatment.

---

# 70. Design Consistency Rules

Every new page must follow:

```text
Same colors
Same typography
Same spacing system
Same border style
Same button style
Same radius
Same interaction style
Same responsive principles
```

Do not create a completely different visual style for a new page.

---

# 71. What Must Not Change

Without explicit approval, do not change:

```text
Client:
Dark + Red

Primary Red:
#E8283F

Client Fonts:
Bebas Neue
Plus Jakarta Sans
Space Mono
```

Do not replace the approved MovieMate visual identity with a generic Bootstrap/Tailwind-looking interface.

---

# 72. Design Source of Truth

The uploaded MovieMate UI reference is the primary visual reference for the client-side implementation.

The reference establishes:

* Color variables.
* Typography.
* Buttons.
* Navbar.
* Hero.
* Movie cards.
* Filter chips.
* Ticket motifs.
* Authentication pages.
* Responsive behavior.
  Future client-side pages should visually extend this system rather than replace it.

---

# 73. Final Design Principle

MovieMate should always feel like:

> **A premium digital cinema ticket experience.**

The interface should combine:

```text
Cinema
+
Modern UI
+
Ticket Design
+
Dark Theme
+
Strong Red Accent
+
Clean Typography
```

Client:

```text
DARK
+
#E8283F RED
+
CINEMA/TICKET AESTHETIC
```

Admin:

```text
DARK
+
BLUE ACCENT
+
PROFESSIONAL DASHBOARD
```

The design should remain clean, premium, readable, responsive, and consistent throughout the entire MovieMate application.
