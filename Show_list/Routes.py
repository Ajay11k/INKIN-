
from flask import Blueprint, render_template, session, request, redirect, url_for
from Database import db  
from sqlalchemy.sql import text
import json

showlist_bp = Blueprint('show_list', __name__, template_folder='template', url_prefix='/show_list')

@showlist_bp.route('/show')
def show():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return 'You must be logged in to view data'

    user_id = session['user_id']

    # Retrieve the data from the user's table
    table_name = f"album1_{user_id.replace('@', '').replace('.', '_')}"
    select_query = text(f"SELECT * FROM {table_name}")
    result = db.session.execute(select_query).fetchall()
    titles = []
    for row in result:
        data = row[1]
        data = json.loads(data)
        for entry in data:
            title = entry.get('title')  # Access the 'title' key from each dictionary
            titles.append(title)

    return render_template('showlist.html', songs=result, titles=titles)


@showlist_bp.route('/fetch/<int:song_id>', methods=['GET'])
def fetch(song_id):
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return 'You must be logged in to fetch data'

    user_id = session['user_id']
    songid = song_id

    # Fetch the row from the user's data table
    table_name = f"album1_{user_id.replace('@', '').replace('.', '_')}"
    select_query = text(f"SELECT * FROM {table_name} WHERE id=:id")
    result = db.session.execute(select_query, {'id': songid}).fetchone()
    data = json.loads(result[1])
    data_json = json.dumps(data)
    flag = True
    if result[3] == 'song':
        return render_template('song_page.html', songs=data, song_json=data_json, num_songs=result[2], flag=flag)
    else:
        return render_template('poem_page.html', poetry=data, poetry_json=data_json, flag=flag)


@showlist_bp.route('/delete', methods=['POST'])
def delete():
    if 'logged_in' not in session or not session['logged_in']:
        return 'You must be logged in to fetch data'

    user_id = session['user_id']
    song_id = request.form['song_id']

    # Fetch the first row from the user's data table
    table_name = f"album1_{user_id.replace('@', '').replace('.', '_')}"
    delete_query = text(f"DELETE FROM {table_name} WHERE id=:id")
    db.session.execute(delete_query, {'id': song_id})
    db.session.commit()
    update_query = text(f"UPDATE {table_name} SET id = id - 1 WHERE id > :deleted_id")
    db.session.execute(update_query, {'deleted_id': song_id})
    db.session.commit()

    return redirect(url_for('show_list.show'))
