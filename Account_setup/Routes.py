from flask import render_template, redirect, url_for, request, flash, session
from Database import db
from Models import User, Verifyuser
from werkzeug.security import generate_password_hash, check_password_hash
from Account_setup.utils import send_verification_email, send_otp, verify_otp,send_account_email
from flask import Blueprint




account_setup_bp = Blueprint('account_setup', __name__,template_folder='template')
# Home page
@account_setup_bp.route('/')
def index():
   
    if 'logged_in' not in session:
        session['logged_in'] = False
        
    if session['logged_in']:
        return redirect(url_for('account_setup.logout'))
        
    return render_template('login.html')
    

# User registration
@account_setup_bp.route("/success")
def success():
    return render_template('success.html') 

@account_setup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form['username']
        user_password = request.form['password']
        user_email = request.form['email']

        # Check if the email already exists in the database
        if User.query.filter_by(user_email=user_email).first():
            flash('Email already exists')
            return render_template('signup.html')

        # Generate and send the OTP
        send_otp(user_name, user_email,user_password)

        return render_template('verify.html',user_email=user_email)
    return render_template('signup.html')


# Verify the user's email and OTP
@account_setup_bp.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        email = request.form.get("email")
        otp = request.form.get("otp")
        
       
        
        # Verify the OTP
        if verify_otp(email, otp):
            # Get the user details from the database
            user = Verifyuser.query.filter_by(email=email).order_by(Verifyuser.id.desc()).first()
            
            # Add the user details to the Users table
            new_user = User(user_name=user.username, user_password=user.password, user_email=user.email)
            db.session.add(new_user)
            db.session.commit()
            send_account_email(user.email, user.username)
            db.session.query(Verifyuser).filter_by(email=email).delete()
            db.session.commit()
            
            
            return redirect('/success')
        else:
            flash('Invalid OTP')
            return redirect("/verify")

# User login
@account_setup_bp.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        user_email = request.form['email']
        user_password = request.form['password']

        #Check if the user exists in the database and the password is correct
        user = User.query.filter_by(user_email=user_email).first()
       
        if user and  check_password_hash(user.user_password, user_password):
            # Set the 'logged_in' session variable to True
            session['logged_in'] = True
            session['user_id'] = user.user_email
            session['user_name']=user.user_name
            
            # Store the user ID in the session
             
            return  redirect(url_for('account_setup.dashboard'))
        else:
            flash("Invalid login credentials")
            return render_template('login.html')


# User dashboard
@account_setup_bp.route('/dashboard')
def dashboard():
    # Route code goes here
    if 'logged_in' not in session or not session['logged_in']:
        return  redirect(url_for('account_setup.index'))
    return render_template('homepage.html')

@account_setup_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You have been logged out. Please log in again.')
    return redirect(url_for('index'))

