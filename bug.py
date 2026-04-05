from flask import Flask, request
from celery import Celery
import time

app = Flask(__name__)

# Setup Celery with Redis as the broker
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

# THE TASK
@celery_app.task
def send_welcome_email(user_data):
    time.sleep(10)  # Pretend it takes 10 seconds to send an email
    print(f"Email sent to {user_data['email']}")
    return "Done!"

@app.route('/signup')
def signup():
    user = {"email": "bob@example.com", "name": "Bob"}

    # --- BUG #1: Calling it like a normal function ---
    # This ignores Celery and Redis entirely! 
    # The user has to wait 10 seconds for the page to load.
    send_welcome_email(user) 

    # --- BUG #2: Blocking the main thread for the result ---
    # Even if we use Celery correctly (.delay), calling .get() 
    # makes the website wait until the task is finished.
    # result = send_welcome_email.delay(user).get() 

    return "Signup successful!"
