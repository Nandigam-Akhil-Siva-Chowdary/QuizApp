📘 Quiz Application – Complete Technical Documentation
1. Overview

This project is a secure online quiz platform built as a separate app that integrates with the existing NexusOfThings ecosystem.

It uses:

Django + MongoDB (same DB as NexusOfThings)

HTML + Tailwind CSS

Vanilla JavaScript

Cloudinary (certificates)

Render Free Tier–friendly architecture

No Redis / No Celery / No WebSockets

The system is designed to be:

Anti-cheat aware

Session-based (no passwords)

Admin-controlled

Scalable within free-tier limits

2. High-Level Architecture
Browser (User/Admin)
        |
        v
Django Views (HTML + API)
        |
        v
Services Layer (business logic)
        |
        v
MongoDB (Quiz + NexusOfThings DB)
        |
        v
Cloudinary (Certificates)

Key Design Decisions

❌ No Redis (Render free tier limitation)

❌ No long-running workers

✅ Stateless HTTP APIs

✅ Session-based identity

✅ Server-side enforcement (time, attempts, disqualification)

3. User Roles
3.1 Admin

Creates quizzes

Configures quiz behavior

Uploads questions via CSV

Monitors attempts & violations

Generates & sends certificates

3.2 User (Participant)

Logs in using registered email

Confirms registration details

Attempts assigned quiz

Receives certificate via team leader email

4. Authentication & Session Flow
4.1 Email-Only Login

User enters team leader email

Email is verified against NexusOfThings Participant collection

No password, no Django auth user

Session is created

Session key:

request.session["quiz_user"]


Contains:

team_code

team_name

team_lead_email

college_name

event

4.2 Registration Confirmation

User confirms:

Roll number (mandatory)

Extra member (optional)

Same / different college

✔ Stored only in session
❌ Not written back to NexusOfThings DB

5. Quiz Lifecycle (User)
Step 1: Quiz Home

Shows only active quizzes

Enforces quiz time window

Step 2: Instructions Page

Displays:

Rules

Time limit

Attempts allowed

Fullscreen requirement

Anti-cheat rules

User must explicitly start quiz.

Step 3: Attempt Creation

Attempt is created only once

Refresh resumes same attempt

Attempt stores:

question order

option order

start time

Step 4: Quiz Attempt Page
Features

Countdown timer

Question navigation

Mark for review

Autosave answers

Auto submit on timeout

Anti-Cheat Enforcement
Action	Result
Exit fullscreen	Violation
Tab switch	Violation
Copy attempt	Violation
DevTools open	Violation
Exceed warnings	Auto submit / Disqualify

Violations are recorded via API and enforced server-side.

Step 5: Submission

Manual submit OR auto submit

Attempt status updated:

submitted

auto_submitted

disqualified

Step 6: Result Page

Controlled by admin flag:

allow_immediate_results

If disabled → user sees “Results will be published later”

If enabled → explanations shown (optional)

6. Quiz Configuration (Admin)

Each quiz can configure:

Setting	Description
Time limit	Minutes
Max attempts	Per team
Warnings allowed	Anti-cheat
Shuffle questions	Yes/No
Shuffle options	Yes/No
Immediate results	Yes/No
Start / End time	Availability
7. Question Management
7.1 CSV Upload

Admin uploads CSV containing:

Question text

Question type (single / multiple)

Options

Correct answers

Optional explanations

✔ CSV is validated
✔ Errors shown row-wise
✔ Preview before saving
✔ No DB write until confirmed

7.2 Question Types

Single correct answer

Multiple correct answers

UI clearly labels question type.

8. Anti-Cheat System (Core Feature)
Frontend Detection

Fullscreen exit

Visibility change

Copy event

Keyboard shortcuts

DevTools detection (viewport delta)

Backend Enforcement

All violations sent via API

Server increments counters

Server decides:

warning

auto submit

disqualification

✔ Client cannot bypass enforcement.

9. Attempt & Answer Storage
QuizAttempt

Stores:

team_code

quiz_id

status

start / end time

warnings_used

violation counters

question order

option order

QuizAnswer

Stores:

attempt_id

question_id

selected options

marked for review

10. Certificates System
Admin Flow

Upload Canva design (PNG/PDF) to Cloudinary

Paste Cloudinary URL

Select teams

Generate certificates

Send emails

Certificate Generation

Node-style logic using:

PDFKit or Puppeteer (conceptual)

Name, college, roll no overlaid

Stored on Cloudinary

Email Delivery

Sent only to team leader email

Bulk selection supported

Duplicate sends prevented

11. Static Files Structure
quiz/static/
├── css/
│   ├── tailwind.css
│   └── quiz.css
└── js/
    ├── quiz_timer.js
    ├── fullscreen.js
    ├── anti_cheat.js
    ├── devtools_detect.js
    ├── navigation.js
    └── submit.js


✔ All files are Render-safe
✔ No CDN dependency
✔ No build step on server

12. Templates Structure
quiz/templates/
├── base.html
├── navbar.html
├── footer.html
│
├── auth/
│   ├── email_login.html
│   └── verify_registration.html
│
├── user/
│   ├── quiz_home.html
│   ├── quiz_instructions.html
│   ├── quiz_attempt.html
│   ├── quiz_submit.html
│   └── quiz_result.html
│
└── admin/
    ├── quiz_create.html
    ├── quiz_edit.html
    ├── quiz_csv_upload.html
    ├── quiz_results.html
    ├── certificate_review.html
    └── quiz_delete_confirm.html

13. Utilities & Services
Utilities

time.py – time calculations

csv_parser.py – CSV validation

randomizer.py – shuffle logic

constants.py – enums & keys

validation.py – data validation

anti_cheat_helpers.py – violation mapping

Services

QuizService

AttemptService

AntiCheatService

CertificateService

EmailService

All business logic is outside views.

14. Deployment (Render Free Tier)
Why This Works on Render

No Redis

No background workers

Stateless APIs

Minimal memory usage

Required Environment Variables
DJANGO_SECRET_KEY
MONGODB_URI
CLOUD_NAME=
API_KEY=
API_SECRET=
CLOUDINARY_URL
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD

15. Security Notes

✔ Server-side enforcement
✔ No answers exposed in APIs
✔ Session-based identity
✔ No password storage
✔ Admin-controlled result visibility

⚠️ Note:
Client-side anti-cheat is a deterrent, not a guarantee.
Final authority is always server-side.

16. Known Limitations (Accepted)

DevTools detection is heuristic

No real-time proctoring

Email-based login assumes secure inbox

Free tier cold starts may delay submission (handled via fallback)

17. Conclusion

This quiz platform is:

Production-grade

Free-tier friendly

Highly controlled

Extensible

It cleanly integrates with NexusOfThings, avoids architectural traps, and provides a strong balance between security, usability, and cost.