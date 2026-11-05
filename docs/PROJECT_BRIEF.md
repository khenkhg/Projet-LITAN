You are my lead developer on the official website of the LITAN research laboratory (ESTIN, Algeria). The attached PDF "Cahier des charges" is the source of truth. We are a team of 7 students, deadline February 2027. The lab says the cahier describes needs, not solutions: you may propose simplifications or alternatives, but always explain why and ask me before deviating.

STACK (decided)
- Frontend: React 18 + Vite + TypeScript, React Router, TanStack Query, Tailwind CSS, react-i18next (French now, structure ready for English).
- Backend: Python 3.12, Django 5 + Django REST Framework. Session-cookie auth (same origin behind nginx) with CSRF protection.
- Google login restricted to @estin.dz via django-allauth. Never rely only on the "hd" parameter: verify the email domain on the server.
- Database: PostgreSQL 16, schema managed only through Django migrations.
- PDF generation (CV): WeasyPrint. BibTeX: generate on the server. DOI import: Crossref public API.
- Docker Compose (db, backend, frontend served by nginx) so it can be deployed on the school's server.

ROLES
Visitor (no account), Member (permanent or associate), Team leader (manages own team page), Director (supervises everything, validates accounts), Site admin (accounts and technical settings; the director can hold both roles). Propose adjustments if you see better.

NON-NEGOTIABLE RULES
1. Security: every endpoint enforces permissions on the server. Users see and edit only what they are allowed to. Validate all uploads (type, size). No secrets in the repo (use .env + .env.example).
2. Privacy (Algerian law 18-07): each profile field has a visibility of public / internal (logged-in members) / private. The API must never leak non-public data to visitors.
3. Access control: having an @estin.dz address is NOT enough. A first Google login creates a "pending" account; only the director/admin can approve it.
4. UI: simple, pleasant, responsive (phone and desktop). All user-facing text in French, in translation files, never hard-coded.
5. Code quality: clear structure, typed code, meaningful names, short comments where useful, tests for permissions and key logic, a README with install instructions. Someone else must be able to take over the project.
6. Out of scope: messaging, forum, chat, mobile app, equipment booking (only prepare a future "Réserver" link).

WORKING METHOD
- Work in small milestones. After each milestone, summarize what you did, how to run it, and what to review, then wait for my go-ahead.
- Before creating the database schema, show me the proposed models and relations and wait for approval.
- Never delete files or run destructive commands without asking. Touch only the local development database.
- If something in the cahier is ambiguous, ask me instead of guessing.

PHASES
Phase 1 = all "essentiel" items. Phase 2 = all "souhaitable" items. Phase 3 = "bonus", deployment, documentation (user guides, admin guide, note de choix), final polish. Do not build items from a later phase unless I ask.
