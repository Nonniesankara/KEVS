
---# 🇰🇪 KEVS – Kenyan Electronic Voting System

**KEVS** is a full-stack, secure, and accessible digital voting platform designed to simulate real-world Kenyan elections. It supports a complete election cycle, from hierarchical location selection to multi-position candidate voting, tailored especially for military personnel, persons with disabilities, and remote voters.

---

##  Project Summary

KEVS supports secure voter login, dynamic ballot generation, and real-time vote counting across all key Kenyan electoral positions:

- President
- Governor
- Senator
- Member of Parliament (MP)
- Member of County Assembly (MCA)

Built with accessibility, realism, and security in mind, it mimics Kenya’s actual electoral geography.

---

##  Technology Stack

| Layer      | Technology                                                                 |
|------------|----------------------------------------------------------------------------|
| Backend    | Python (Flask), Flask-SQLAlchemy, Flask-Migrate, Flask-CORS                |
| Frontend   | React.js (Vite, Axios, React Router)                                       |
| Database   | SQLite (for development), structured with Alembic migrations               |
| Seeding    | JSON files for location, voter, and candidate data                         |

---

##  Backend Architecture

### Models

- **County, Constituency, Ward, PollingStation**: Realistic hierarchy of Kenyan electoral zones
- **Voter**: Has credentials and a polling station association
- **Candidate**: Linked to a region depending on their position (Ward/Constituency/County/National)
- **Vote**: Stores voter-candidate selection with timestamp and spoil flag

### Key Endpoints

#### GET
- `/counties`, `/constituencies`, `/wards`, `/pollingstations`, `/candidates`, `/votes`
- `/votes/count` – vote results by candidate
- Filtered:
  - `/constituencies?county_id=X`
  - `/wards?constituency_id=X`
  - `/pollingstations?ward_id=X`

#### POST
- `/login` – voter authentication
- `/vote` – submit vote

#### PATCH
- `/votes/<id>/spoil` – spoil a vote

---

## 🌐 Frontend Overview

### Key Pages

- `/login` – Secure voter authentication
- `/vote` – Step-by-step selection: County → Station → Candidate
- `/confirm` – Summary of selections
- `/results` – Live vote counts

### Features

- Dynamic, filtered dropdowns by location
- Candidate filtering by position and location
- Dark mode (persisted via localStorage)
- Responsive layout using Kenyan flag color themes
- Axios for API interaction and state management

---

##  Database Seeding

A robust `seed.py` script loads data from a structured JSON file:

- 9 Counties → Constituencies → Wards → Polling Stations
- Candidates mapped to correct levels (President: national, MCA: ward)
- Voter accounts linked to stations

✅ Fixed voter seeding logic to ensure all voters are properly created.

---

## 🧠 Key Features

-  **Authentication** – Secure login via username/password
-  **Hierarchical Voting** – Region-based selection before voting
-  **Multi-Position Support** – Vote for all 5 elective positions
-  **Vote Spoiling** – Option to spoil individual votes
-  **Real-Time Results** – Results page reflects live tallies

---

##  Challenges Solved

| Challenge | Solution |
|----------|----------|
| Empty voter table | Updated seed script to include voters |
| Wards mixed across counties | Added filtered API routes + frontend logic |
| Preventing double voting | `has_voted` flag with backend check |
| Spoiling votes | Added PATCH endpoint to mark vote as spoilt |
| Frontend confusion in selections | Reset dropdowns dynamically using React state |

---

##  Results Visualization

- Displays party, candidate name, position, and total votes
- Styled for readability and responsive design
- Sorted and grouped per position

---

## Folder Structure (Simplified)



## Future Enhancements

-  Encrypt passwords (currently plaintext)
-  Admin dashboard for managing voters/candidates
-  Visual dashboards for real-time analytics
-  Email/SMS confirmation after voting
-  Mobile-friendly version or native app
-  Deploy on Render, Railway, or similar platforms
-  Add unit and integration tests

---

##  Demo Flow

1. Log in using test voter credentials
2. Select: County → Constituency → Ward → Polling Station
3. Vote for each position
4. Confirm votes on summary page
5. View live results

---

##  Why KEVS Matters

> "KEVS makes voting **simpler**, **secure**, and **transparent**. It mirrors the actual Kenyan voting structure and ensures every voter can confidently and fairly participate in democracy."

---

##  Authors & Contributors

- Team KEVS – Moringa School Phase 4 Project

---


