
from flask import Blueprint, render_template, request, session
from Database import db  
from sqlalchemy.sql import text
import json
import song_generator
import Song.video

song_bp = Blueprint('song', __name__, template_folder='template', url_prefix='/song')

@song_bp.route('/song')
def song():
    if 'logged_in' not in session or not session['logged_in']:
        return  redirect(url_for('account_setup.index'))
    
    return render_template('singer.html')

@song_bp.route('/process_song', methods=['GET'])
def process_song():
    language = request.args.get('language')
    singer = request.args.get('singer')
    num_songs = int(request.args.get('numSongs'))
    titles = request.args.get('titles')

    songs = []
    titles_list = [t.strip() for t in titles.split(',')]

    if len(titles_list) != num_songs:
        return render_template('singer.html', error="Number of songs and number of titles do not match.")

    id = 1
    for title in titles_list:
        result = song_generator.generate_song(title, singer)

        data = {
            'id': id,
            'language': language,
            'singer': singer,
            'title': title,
            'song': result
        }
        songs.append(data)
        id += 1

    song_json = json.dumps(songs)

    return render_template('song_page.html', songs=songs, song_json=song_json, num_songs=num_songs)

@song_bp.route('/regenerate_song', methods=['POST'])
def regenerate_song():
    my_string = request.form['data']
    songs = json.loads(my_string)
    num_songs = int(request.form['num_songs'])

    songscollection = []
    id = 1
    for song in songs:
        title = song['title']
        language = song['language']
        singer = song['singer']
        result = song_generator.generate_song(title, singer)

        data = {
            'id': id,
            'language': language,
            'singer': singer,
            'title': title,
            'song': result
        }
        id += 1
        songscollection.append(data)

    song_json = json.dumps(songscollection)

    return render_template('song_page.html', songs=songscollection, song_json=song_json, num_songs=num_songs)

@song_bp.route('/generate_psong', methods=['POST'])
def generate_psong():
    title = request.form.get('title')
    singer = request.form.get('singer')
    result = song_generator.generate_song(title, singer)

    return result

@song_bp.route('/generate_video', methods=['POST'])
def generate_video():
    result = request.form['data']
    songid = int(request.form['songid'])
    language = request.form['language']

    lyrics = []
    songs = json.loads(result)

    for song in songs:
        if song['id'] == songid:
            lyrics = song['song']
            break

    video.generatevideo(lyrics, language)

    return render_template('show_lyrics.html')

@song_bp.route('/save', methods=['POST'])
def save():
    if 'logged_in' not in session or not session['logged_in']:
        return 'You must be logged in to save data'

    user_id = session['user_id']
    my_strings_json = request.form['data']
    no_song = int(request.form['num_songs'])
    genre = request.form['genre']

    table_name = f"album1_{user_id.replace('@', '').replace('.', '_')}"
    create_table_query = text(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, data TEXT, no_song INT, genre VARCHAR(50))")
    db.session.execute(create_table_query)

    insert_query = text(f"INSERT INTO {table_name} (data, no_song, genre) VALUES (:data, :no_song, :genre)")
    db.session.execute(insert_query, {"data": my_strings_json, "no_song": no_song, "genre": genre})
    db.session.commit()

    return 'added'

@song_bp.route('/download_song', methods=['POST'])
def download_song():

    
    
    my_strings_json = request.form['data']
    
    my_strings = json.loads(my_strings_json)
    
    with open('my_strings.txt','w', encoding='utf-8') as f:
    
        for song in my_strings:
            my_title=song['title']
            lyrics=song['song']
            

        # Loop through each row of the 2D array
            f.write(f'\n\n*********   {my_title}   *********\n\n')
            i = 1
        # Loop through each row of the 2D array
            for row in lyrics:
            #     # Join the strings in the row with newline characters
            #     # and write them to the file
                if i==1 or i==3:
                    f.write('\n VERSE \n\n')
                elif i==2 or i==4 or i==6:
                    f.write('\n CHORUS \n\n')
                elif i==5:
                    f.write('\n BRIDGE \n\n')
                    
            
                # Join the centered strings with whitespace and write them to the file
                f.write('\n'.join(row) + '\n')
                i += 1

    # Create a Flask response with the file as the body
    response = make_response(open('my_song.txt',encoding='utf-8').read())
    # Set the content type to 'text/plain'
    response.headers.set('Content-Type', 'text/plain')
    # Set the content disposition to 'attachment', which specifies
    # that the file should be downloaded rather than displayed in the browser
    response.headers.set('Content-Disposition', 'attachment', filename='my_song.txt')
    return response
