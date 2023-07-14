from Database import db

class User(db.Model):
    user_name = db.Column(db.String(50),  nullable=False)
    user_password = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(20), primary_key=True, nullable=False)
    

class Verifyuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    otp = db.Column(db.String(6))
    expiry = db.Column(db.DateTime)    
    password = db.Column(db.String(20), nullable=False)
    

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))  
    timestamp = db.Column(db.DateTime) 
    paragraph = db.Column(db.Text) 
