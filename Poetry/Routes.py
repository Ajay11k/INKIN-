from flask import make_response, render_template, request,session,jsonify,Blueprint
import json
import song_generator
from gtts import gTTS
from Poetry.imagegen import add_text_to_image
import os

poetry_bp = Blueprint('poetry', __name__, template_folder='template', url_prefix='/poetry')

@poetry_bp.route('/select')
def select():
    if 'logged_in' not in session or not session['logged_in']:
        return  redirect(url_for('account_setup.index'))
    
    
    return render_template('select.html')



@poetry_bp.route('/process_poetry',methods=['GET'])
def process_poetry():
    language = request.args.get('language')
    num_lines = int(request.args.get('numLines'))
    print(num_lines)
    title = request.args.get('title')

    # Perform any necessary processing with the form data
    # ...
    result=song_generator.generate_poem(title, num_lines, language)
    poetry=[]
    # Create a dictionary with the selected valuesh
    data = {
        'language': language,
        'num_lines': num_lines,
        'title': title,
        'poetrylines':result
    }
    poetry.append(data)
    
    poetry_json=json.dumps(poetry)
    return render_template('poem_page.html', poetry=poetry,poetry_json=poetry_json)

@poetry_bp.route('/download_poetry', methods=['POST'])
def download_poetry():

    # Assume your 2D array of strings is called 'my_strings'
    # my_strings = [['hello', 'world'], ['foo', 'bar'], ['baz', 'qux']]
    
    my_strings_json = request.form['data']
    
    my_strings = json.loads(my_strings_json)
    my_title=my_strings[0]['title']
    poems=my_strings[0]['poetrylines']
    # Create a new file dialog to allow the user to select the file path
    
    
    # Create a new file with the selected file path in write mode
    with open('my_strings.txt', 'w',encoding='utf-8') as f:
        # Loop through each row of the 2D array
        f.write(f'*********   {my_title}   *********\n\n')
        i = 1
    # Loop through each row of the 2D array
        for row in poems:
        #     # Join the strings in the row with newline characters
        #     # and write them to the file
            
                
        
            # Join the centered strings with whitespace and write them to the file
            f.write('\n'.join(row) + '\n')
            

    # Create a Flask response with the file as the body
    response = make_response(open('my_strings.txt',encoding='utf-8').read())
    # Set the content type to 'text/plain'
    response.headers.set('Content-Type', 'text/plain')
    # Set the content disposition to 'attachment', which specifies
    # that the file should be downloaded rather than displayed in the browser
    response.headers.set('Content-Disposition', 'attachment', filename='my_strings.txt')
    return response

@poetry_bp.route('/regenerate_poetry',methods=['POST'])
def regenerate_poetry():
    my_string=request.form['data']
    poems=json.loads(my_string)
    print(poems)
    title=poems[0]['title']
    language=poems[0]['language']
    num_lines=poems[0]['num_lines']
    result=song_generator.generate_poem(title, num_lines, language)
    poetry=[]
    # Create a dictionary with the selected values
    data = {
        'language': language,
        'num_lines': num_lines,
        'title': title,
        'poetrylines':result
    }
    poetry.append(data)
    
    poetry_json=json.dumps(poetry)
    return render_template('poem_page.html', poetry=poetry,poetry_json=poetry_json)

@poetry_bp.route('/show_image',methods=['GET'])
def show_image():
    my_string=request.args.get('data')
    
   
   
    return render_template('index3.html',text=my_string)

@poetry_bp.route('/save', methods=['POST'])
def save():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return 'You must be logged in to save data'

    user_id = session['user_id']
    my_strings_json = request.form['data']
    
    no_song=int(request.form['num_songs'])
    genre=request.form['genre']
    
    # Insert the data into the user's data table
    table_name = f"album1_{user_id.replace('@', '').replace('.', '_')}"
    create_table_query = text(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, data TEXT, no_song INT, genre VARCHAR(50))")
    db.session.execute(create_table_query)

    insert_query = text(f"INSERT INTO {table_name} ( data,no_song,genre) VALUES (:data,:no_song,:genre)")
    db.session.execute(insert_query, {"data": my_strings_json,"no_song":no_song,"genre":genre})
    db.session.commit()

    return 'added'

@poetry_bp.route('/play_audio', methods=['POST'])
def play_audio():
    data = request.get_json()
    lines = data.get('lines')
    language = data.get('language')
    full_text = ""
    for row in lines:
        for word in row:
            full_text += word + " "
        full_text += "\n"

    tts = gTTS(text=full_text, lang=language)
    filename="static/output_audio.mp3"
    tts.save(filename)
    return jsonify({'audio_path': filename})

@poetry_bp.route('/poetry_image', methods=['GET'])
def poetry_image():
    slide_name = request.args.get('slideName')
    poetry=request.args.get('lyricsValue')
    poetry=json.loads(poetry)
    
    text=poetry[0]['poetrylines']
    language=poetry[0]['language']
    
    
    # Logic to generate image URL based on slide name
    # Replace this with your actual logic to generate the image URL
    image_url = generate_image_url(slide_name,text,language)

    response = {'image_url': image_url}
    print(image_url)
    return jsonify(response)

def generate_image_url(slide_name,song_lyrics,language):
    # Logic to generate image URL based on slide name
    # Replace this with your actual logic to generate the image URL
    # You can query the database or use any other method to retrieve the image URL
    name=slide_name
    text_array=song_lyrics
    result = '\n'.join('\n'.join(inner_list) for inner_list in text_array)
    image_url = f'static/Images/bg{name}.jpg'
    
    
    image_url=add_text_to_image(result, slide_name, image_url,language)
    
    # Add more conditions for other slide names
   
    return image_url

