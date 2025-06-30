from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import uuid
import requests


API_HOST = "jsearch.p.rapidapi.com"
API_KEY = "YOUR_RAPIDAPI_KEY"

def fetch_job_availability(title, company):
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": f"{title} at {company}",
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if data.get("data"):
            return data["data"][0]["job_city"], data["data"][0]["job_country"]
    except Exception as e:
        print("API error:", e)
    return None, None


app = Flask(__name__)
EXCEL_FILE = 'job_applications.xlsx'

def read_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=["Application ID", "Company Name", "Job Title", "Status", "Location"])

def write_data(df):
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    df = read_data()
    status_counts = df['Status'].value_counts().to_dict()
    return render_template('home.html', status_counts=status_counts)

@app.route('/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        df = read_data()

        company = request.form['company']
        title = request.form['title']
        status = request.form['status']

        city, country = fetch_job_availability(title, company)

        new_entry = {
            "Application ID": str(uuid.uuid4())[:8],
            "Company Name": company,
            "Job Title": title,
            "Status": status,
            "Location": f"{city}, {country}" if city and country else "Unknown"
        }

        if "Location" not in df.columns:
            df["Location"] = ""

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        write_data(df)
        return redirect(url_for('list_applications'))
    return render_template('add.html')

@app.route('/update/<app_id>', methods=['GET', 'POST'])
def update_status(app_id):
    df = read_data()
    app_row = df[df['Application ID'] == app_id]

    if app_row.empty:
        return "APPLICATION NOT FOUND", 404

    app = app_row.iloc[0]

    if request.method == 'POST':
        if 'delete' in request.form:
            df = df[df['Application ID'] != app_id]
            write_data(df)
            return redirect(url_for('list_applications'))
        else:
            df.loc[df['Application ID'] == app_id, 'Status'] = request.form['status']
            write_data(df)
            return redirect(url_for('list_applications'))

    return render_template('update.html', app=app)

    
@app.route('/list')
def list_applications():
    df = read_data()
    sort_by = request.args.get('sort', 'Company Name')
    filter_status = request.args.get('filter')
    if filter_status:
        df = df[df['Status'].str.lower() == filter_status.lower()]
    df = df.sort_values(by=sort_by)
    return render_template('list.html', apps=df.to_dict(orient='records'), sort_by=sort_by)


@app.route('/available_jobs')
def available_jobs():
    df = read_data()
    results = []

    for _, row in df.iterrows():
        company = row['Company Name']
        title = row['Job Title']
        city, country = fetch_job_availability(title, company)
        if city and country:
            results.append({
                'Company': company,
                'Title': title,
                'Location': f"{city}, {country}"
            })

    return render_template('available_jobs.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
