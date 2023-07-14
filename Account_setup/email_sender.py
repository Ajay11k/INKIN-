import ssl
import smtplib
from email.message import EmailMessage

def send_verification_email(receiver_email,otp,user):
    subject = "inkin' Email Verification OTP"
    body = f"""
    
Dear {user},

Thank you for signing up with inkin'', the premier platform for unleashing your creative potential. We're thrilled to have you as a member of our vibrant community.

To ensure the security of your account and provide you with seamless access to inkin'', we have sent you a One-Time Password (OTP) for email verification purposes. Please find the OTP details below:

OTP: { otp }

Please note that this OTP is valid for a limited time and should be used to verify your email address promptly. Enter the OTP on the inkin' website to complete the verification process and unlock the full range of features.

If you did not sign up for an inkin' account, please disregard this email. Your account will not be activated.

At inkin', we prioritize the privacy and security of your personal information. Rest assured that your email address will only be used for essential communications related to your account and platform updates. We do not share your information with any third parties without your consent.

If you encounter any difficulties during the verification process or have any questions, our dedicated support team is ready to assist you. Please reach out to us.

Thank you for choosing inkin' to embark on a creative journey! We look forward to seeing your incredible creations and contributions within our community.

Best regards,

The inkin' Team
    """
    subject2="Complete Your Email Verification - Welcome to inkin'"
    body2= f""" 
Dear {user},

Congratulations on joining inkin', the ultimate platform for unleashing your creative potential! We're excited to have you as a valued member of our thriving community.

To ensure the security of your account and provide you with seamless access to all the features and benefits inkin' has to offer, we kindly request you to verify your email address. By doing so, you'll be able to fully explore the endless possibilities and connect with like-minded individuals.

Please follow the steps below to complete your email verification:

Step 1: Retrieve Your One-Time Password (OTP)
In a moment of anticipation, we have generated a unique One-Time Password (OTP) for you. Your OTP is as follows: [Insert OTP]. Please keep this code confidential and do not share it with anyone.

Step 2: Verify Your Email Address
Now, head over to the inkin' website and navigate to the email verification page. Once there, enter the provided OTP in the designated field and click the verification button. This will instantly activate your inkin' account and grant you full access to all our incredible features.

At inkin', we prioritize the privacy and security of your personal information. Rest assured that your email address will only be used for essential communications related to your account and platform updates. We do not share your information with any third parties without your consent.

If you did not sign up for an inkin' account, please disregard this email. Rest assured that your account will not be activated.

Should you encounter any difficulties during the verification process or have any questions, our dedicated support team is ready to assist you. Simply reach out to us, and we'll be more than happy to help.

Thank you for choosing inkin' to embark on your creative journey! We can't wait to witness the incredible artwork, stories, and ideas you'll bring to life within our community.

Best regards,

The inkin' Team

    """
    
    # sender_email = 'sainiajay4217@gmail.com'
    # password = 'jxyvnuwvvlmkbwpl'
    sender_email='noreply.inkin@gmail.com'
    password='uxppratibryevswq'
    en = EmailMessage()
    em = EmailMessage()
    en['From'] = sender_email
    en['To'] = receiver_email
    en['Subject'] = subject
    en.set_content(body)
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject2
    em.set_content(body2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, en.as_string())
        smtp.sendmail(sender_email, receiver_email, em.as_string())

# Example usage:


def send_account_email(receiver_email,user):
    subject = "Welcome to inkin' - Unleash Your Creative Potential"

    body = f'''
    Dear {user},
    
    Thank you for joining inkin', the creative platform for song and poem generation. We are thrilled to have you as a member of our community.

    inkin' provides a vibrant space where you can unleash your creativity and express yourself through the power of words. Whether you're passionate about writing poems or composing songs, inkin' offers the tools and inspiration to bring your ideas to life.

    Explore a diverse collection of genres, experiment with different themes, and collaborate with fellow artists. Share your creations, receive feedback, and connect with like-minded individuals who share your passion for artistic expression.

    If you ever need any assistance or have any questions, our support team is here to help. Feel free to reach out to us at support@inkin'.com.

    Once again, welcome to inkin'! We're excited to see the amazing songs and poems you'll create and share with our community.

    Best regards,
    The inkin' Team
    '''

    
    # sender_email = 'sainiajay4217@gmail.com'
    # password = 'jxyvnuwvvlmkbwpl'
    sender_email='noreply.inkin@gmail.com'
    password='uxppratibryevswq'
    en = EmailMessage()
    em = EmailMessage()
    en['From'] = sender_email
    en['To'] = receiver_email
    en['Subject'] = subject
    en.set_content(body)
    

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, en.as_string())