
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
from googletrans import Translator

def get_last_sound(hindi_word):
    phonetic_text = transliterate(hindi_word, sanscript.DEVANAGARI, sanscript.ITRANS)
    last_sound = phonetic_text[-1]
    return last_sound


def do_transliteration(hindi_text):
    roman_array = []

    for section in hindi_text:
        roman_section = []
        for lyrics in section:
            roman_text = ""
            lyrics = lyrics.split()
            for word in lyrics:
                text = sanscript.transliterate(word, sanscript.DEVANAGARI, sanscript.ITRANS)
                if get_last_sound(word) == 'a':
                    text = text[:-1]
                elif get_last_sound(word) == 'M':
                    text = text[:-1]
                roman_text = roman_text + " " + text
            roman_text = roman_text.lower()
            roman_section.append(roman_text)
        roman_array.append(roman_section)
    
    return roman_array



def translate_hindi_to_english(array):
    translator = Translator(service_urls=['translate.google.com'])
    translated_array = []

    for row in array:
        translated_row = []
        for text in row:
            translation = translator.translate(text, src='hi', dest='en')
            translated_text = translation.text
            translated_row.append(translated_text)
        translated_array.append(translated_row)
    
    return translated_array



def translate_korean_to_english(korean_text):
    translator = Translator(service_urls=['translate.google.com'])
    translated_array = []

    for row in korean_text:
        translated_row = []
        for text in row:
            translation = translator.translate(text, src='ko', dest='en')
            translated_text = translation.text
            translated_row.append(translated_text)
        translated_array.append(translated_row)
    
    return translated_array



def translate_hindi(array):
    translator = Translator(service_urls=['translate.google.com'])
    translated_array = []

    for row in array:
        translated_row = []
        for text in row:
            translation = translator.translate(text, src='en', dest='hi')
            translated_text = translation.text
            translated_row.append(translated_text)
        translated_array.append(translated_row)
    
    return translated_array

def translate_spanishtoenglish(array):
    translator = Translator(service_urls=['translate.google.com'])
    translated_array = []

    for row in array:
        translated_row = []
        for text in row:
            translation = translator.translate(text, src='es', dest='en')
            translated_text = translation.text
            translated_row.append(translated_text)
        translated_array.append(translated_row)
    
    return translated_array




# Example usage



# Example usage
# korean_text = "Oh 난 떨리는 걸음을 조심히 다가가 봐 Oh 난 더 가까이 갈수록 어쩐지 두려워져"
# english_text = translate_korean_to_english(korean_text)
# print(english_text)