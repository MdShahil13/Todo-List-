from flask import Flask, render_template, request, redirect, url_for
import smtplib
import schedule
import time
import threading
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
tasks = []

sender_email = "mdsahilshaikh1506@gmail.com"
sender_password = "borw qino pnst gucv"

def send_email(to_email, subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    email = request.form['email']
    reminder_time = request.form['reminder_time']

    tasks.append(task)

    if reminder_time:
        schedule.every().day.at(reminder_time).do(
            send_email,
            email,
            "Task Reminder",
            f"Reminder: {task}"
        )

    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_task():
    task = request.form['task']
    if task in tasks:
        tasks.remove(task)
    return redirect(url_for('index'))

if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(debug=True)
