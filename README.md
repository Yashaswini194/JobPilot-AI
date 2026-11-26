# JobPilot AI – Smart Job Application Tracker

A web app that helps job seekers track applications, interview dates and follow-ups in one place, with an AI job description analyzer that compares a job post against your resume.

Inspired by Tsenta (Y Combinator) as part of the CloudCosmos "Clone & Elevate" hiring drive.

## Planned Features
- [x] Save job applications (company, role, link, dates, notes)
- [x] Track stages: Applied, Assessment, Interview, Offer, Rejected
- [x] Follow-up reminders (overdue ones are highlighted)
- [ ] AI job description analyzer (key skills + resume gap analysis)
- [ ] Dashboard with stage statistics

## Tech Stack
Python, Django, SQLite, HTML, CSS, AI API (Gemini)

## Run Locally
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
