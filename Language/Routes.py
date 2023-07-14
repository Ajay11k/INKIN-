

from flask import Blueprint, render_template, request, session
import transliteration

language_manipulation_bp = Blueprint('language_manipulation', __name__, template_folder='template', url_prefix='/language_manipulation')

@language_manipulation_bp.route('/transliterate', methods=['POST'])
def transliterate():
    array = request.form['lyrics']
    array = json.loads(array)
    array = transliteration.do_transliteration(array)
    return jsonify(array)

@language_manipulation_bp.route('/translate', methods=['POST'])
def translate():
    lyrics = request.form['lyrics']
    lyrics = json.loads(lyrics)
    language = request.form['language']
    array = []

    if language == 'hi':
        array = transliteration.translate_hindi_to_english(lyrics)
    elif language == 'ko':
        array = transliteration.translate_korean_to_english(lyrics)
    elif language == 'es':
        array = transliteration.translate_spanishtoenglish(lyrics)

    return jsonify(array)
