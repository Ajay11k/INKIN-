
from Database import db
from flask import Blueprint, render_template, session, redirect, url_for,jsonify,request
from Database import db
from Models import Review
from datetime import datetime, timedelta


review_bp = Blueprint('review', __name__, template_folder='template',url_prefix='/review')


@review_bp.route('/loadcontent')
def load_content():
    reviews = Review.query.order_by(Review.id.desc()).all()
    content = []

    for review in reviews:
        content.append({
            'user_name': review.user_name,
            'timestamp': review.timestamp,
            'paragraph': review.paragraph
        })

    return jsonify(content)


@review_bp.route('/feedback')
def feedback():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('account_setup.index'))

    return render_template('review.html')

@review_bp.route('/submit_review', methods=['POST'])
def submit_review():
    review_text = request.form.get('review')
    username = session.get('user_name')
    timestamp = datetime.now()

    review = Review(user_name=username, timestamp=timestamp, paragraph=review_text)
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review submitted successfully!'})