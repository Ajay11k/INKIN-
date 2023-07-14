import random
from datetime import datetime, timedelta
from flask_mail import Message
from Account_setup.email_sender import send_verification_email,send_account_email
# from myproject.app import app, mail
from Models import Review,Verifyuser
from Database import db

# Utility functions code goes here
def send_otp(username, email,password):
    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Calculate the OTP expiry time (10 minutes from now)
    otp_expiry = datetime.now() + timedelta(minutes=10)
    password=generate_password_hash(password)
    # Create a new User object
    new_user = Verifyuser(username=username, email=email, otp=otp, expiry=otp_expiry,password=password)

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Send the verification OTP via email
    send_verification_email(email, otp, username)

def verify_otp(email, otp):
    # Get the user from the database
    user = Verifyuser.query.filter_by(email=email).order_by(Verifyuser.id.desc()).first()

    # Check if the OTP is valid and has not expired
    if user and user.otp == otp and datetime.now() <= user.expiry:
        return True
