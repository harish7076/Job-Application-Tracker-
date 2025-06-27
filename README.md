# Job-Application-Tracker-
# 📝 Job Application Tracker (Flask + Excel + RapidAPI)

This is a **Flask-based web application** that helps you manage and track your job applications. It stores application data in an Excel file (`.xlsx`) and uses the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) from RapidAPI to fetch job availability information (city and country) based on the job title and company.

---

## 🚀 Features

- ✅ Add new job applications
- ✏️ Update or delete applications
- 🔍 Filter and sort applications by company or status
- 📊 View application status summary on the home page
- 🌍 Fetch location data (city and country) from **JSearch API**
- 💾 All data stored in an Excel file (`job_applications.xlsx`)

---

## 📁 Project Structure

job-tracker/
│
├── templates/
│ ├── base.html
│ ├── home.html
│ ├── add.html
│ ├── update.html
│ ├── list.html
│ └── available_jobs.html
│
├── job_applications.xlsx # Automatically created after first entry
├── app.py # Main Flask application
└── README.md # This file

▶️ How to Run
python app.py

📄 Template Pages
Template File	Purpose
base.html	             Base layout for all pages (navbar, etc.)
home.html	             Dashboard showing status summary
add.html	             Form to add a new job application
update.html	           Update status or delete application
list.html	             View all applications, sort/filter them
available_jobs.html	   Show fetched job locations via API


💡 Notes
Application IDs are auto-generated using UUID.

Job location will default to "Unknown" if the API call fails or returns no data.

Excel file is updated every time an application is added or updated.

<img width="1440" alt="Screenshot 2025-06-27 at 3 58 21 PM" src="https://github.com/user-attachments/assets/1e0bf533-6926-4bf0-8f12-d897d4e333f4" />

