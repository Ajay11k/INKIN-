import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('brown')
nltk.download('conll2000')
nltk.download('movie_reviews')
nltk.download('treebank')
nltk.download('maxent_ne_chunker')
nltk.download('words')


from nrclex import NRCLex

def get_max_emotion(lyrics):
    emotions = {
        'fear': [0.0, 0],
        'anger': [0.0, 1],
        'anticip': [0.0, 2],
        'trust': [0.0, 3],
        'surprise': [0.0, 4],
        'positive': [0.0, 5],
        'negative': [0.0, 6],
        'sadness': [0.0, 7],
        'disgust': [0.0, 8],
        'joy': [0.0, 9],
        'anticipation': [0.0, 2]
    }

    total_lines = 0

    for verse in lyrics:
        for line in verse:
            text_object = NRCLex(line)
            emotion_scores = text_object.affect_frequencies
            for emotion, score in emotion_scores.items():
                emotions[emotion][0] += score
            total_lines += 1

    for emotion, score in emotions.items():
        emotions[emotion][0] = score[0] / total_lines

    max_emotion = max(emotions, key=lambda x: emotions[x][0])
    print(max_emotion)
    return emotions[max_emotion][1]


