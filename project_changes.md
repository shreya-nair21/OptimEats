# OptimEats Feature Update Summary

This document outlines the changes made to the OptimEats project to implement the "Workflow Dual Registration", "Marketplace of Need", "Donation Logic", and "Transparency Portal" features.

## 1. Dual Registration Workflow

### New File: `frontend/signup.html`
- **Feature**: Created a unified entry point for registration.
- **Details**: 
  - Implemented a "Toggle" system (Bootstrap Tabs) to switch between **"I want to Donate"** and **"I am an Organization"**.
  - **Donor Form**: Captures Name, Email, Password, Phone. API: `/api/users`.
  - **Organization Form**: Captures Type (Old Age/Orphanage), Name, Contact, Email, Password, Count of People, **Current Needs** (new field), and Address. API: `/businesses/register`.

### Modified: `routes/business.py` & `models.py`
- **Change**: Added a `needs` field to the `Business` model and registration route.
- **Why**: To allow organizations to specify what they urgently require (e.g., "Rice, Winter Clothes") which is displayed in the marketplace.

## 2. Marketplace of Need (Donor Dashboard)

### New File: `frontend/donor_dashboard.html`
- **Feature**: A dedicated dashboard for Donors to browse organizations.
- **Details**:
  - **Feed**: Fetches all registered businesses from `/api/businesses` and displays them as cards.
  - **Organization Card**: Shows the Name, Type, People Count, and **Needs**.
  - **Donate Action**: A "Donate to this Home" button opens a simplified modal.

### Modified: `frontend/home.html`
- **Change**: Updated the "Get Started" buttons to point to the new Verified Workflows:
  - "Join OptimEats" -> `signup.html`
  - "Donor Dashboard" -> `donor_dashboard.html`

## 3. Donation Logic & Backend Updates

### Modified: `routes/donation.py`
- **Feature**: Enhanced donation handling.
- **Details**: 
  - Support for **Clothes** donation type in `handle_donation`.
  - Logic to handle donations without a specific `meal_id` (generic money or goods).
  - Updated `transparency_report` to tally "Meals Donated" and "Clothes Donated" separately.

### Modified: `models.py`
- **Change**: Added `CLOTHES` to `DonationType` Enum.
- **Change**: Added `needs` column to `Business` table.

## 4. Transparency Portal

### Modified: `frontend/transparency.html`
- **Feature**: A public-facing impact report.
- **Upgrade**: Replaced static placeholders with dynamic visualizations.
  - **Charts.js**: Added a Bar Chart for Donation Volumes (Meals vs Clothes) and a Doughnut Chart for Financial Impact.
  - **Leaflet Map**: Added a "Live Map" visualization to show active organization locations (currently using mock coordinates for demonstration).
  - **Stats**: Connected to `/api/transparency` to show real-time "Total Funds", "Meals Donated", etc.

## 5. App Configuration

### Modified: `app.py`
- **Change**: Registered new routes to serve the HTML pages:
  - `/signup.html`
  - `/donor_dashboard.html`

## Database Migration
**Note**: Since we added a column (`needs`) to an existing `Business` table, a migration script `migrate_db.py` was created and run to update your local `optimEat.db` without losing data. 

---

### How to Run
1. Ensure your virtual environment is active.
2. Run `python app.py`.
3. Visit `http://localhost:5000` and navigate through the new "Join OptimEats" flow.
