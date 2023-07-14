import tensorflow as tf
import string
import requests
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pronouncing
from tensorflow.keras.models import load_model
import transliteration

from better_profanity import profanity
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt

def get_phonetic_ending(word):
    try:
        phonemes = pronouncing.phones_for_word(word)[0]
        phonemes = phonemes.split()
        phonetic_ending = ""
        for phoneme in reversed(phonemes):
            if phoneme[-1].isdigit():
                phonetic_ending = phoneme + phonetic_ending
            else:
                break
        return phonetic_ending
    except IndexError:
        # Return empty string if pronunciation not found
        return ""

def transformation(structure, singer):
    print(structure)
    try:
        if singer == 'ADELE' or singer == 'EMINEM' or singer == 'LADYGAGA' or singer=='RIHANNA':
            array1=transliteration.translate_hindi(structure[:4])
            array1 = transliteration.translate_hindi_to_english(array1)
            
            array2 = transliteration.translate_hindi(structure[4:])
            array2 = transliteration.translate_hindi_to_english(array2)
            array = array1 + array2
            return array
        
    except TimeoutError:
        pass

    return structure

 

def generate_song(seed_text,singer):
    # response = requests.get('https://raw.githubusercontent.com/laxmimerit/poetry-data/master/adele.txt')
    # data = response.text.splitlines()
    filepath=''
    modelpath=''
    filepath=f'dataset/{singer}dataset.txt'
    modelpath=f'trained_model/song_generator_model_{singer}.h5'

    with open(filepath,encoding='utf') as file:
         
        text=file.read()
    data=text.splitlines()

    
    temperature=1.0
    n_lines=10
    # Tokenize the data
    token = Tokenizer()
    token.fit_on_texts(data)
    encoded_text = token.texts_to_sequences(data)

    # Generate sequences
    datalist = []
    for d in encoded_text:
        if len(d) > 1:
            for i in range(2, len(d)):
                datalist.append(d[:i])
    max_length = 20
    sequences = pad_sequences(datalist, maxlen=max_length, padding='pre')
    X = sequences[:, :-1]
    y = sequences[:, -1]
    y = to_categorical(y, num_classes=len(token.word_counts) + 1)
    seq_length = X.shape[1]

    # Define the model
    # model = Sequential()
    # model.add(Embedding(len(token.word_counts) + 1, 50, input_length=seq_length))
    # model.add(LSTM(100, return_sequences=True))
    # model.add(LSTM(100))
    # model.add(Dense(100, activation='relu'))
    # model.add(Dense(len(token.word_counts) + 1, activation='softmax'))
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # # Train the model
    # model.fit(X, y, batch_size=32, epochs=2)
    model = tf.keras.models.load_model(modelpath)

    lyrics = []
    
    rhyme_words = []
    for i in range(n_lines):
        text = []
        poetry_length=10
        
        for j in range(poetry_length):
          prediction_word=""
          if(i%2!=0 and j==9):
           
               
             while True:

                encoded = token.texts_to_sequences([seed_text])
                encoded = pad_sequences(encoded, maxlen=seq_length, padding='pre')
                y_pred = model.predict(encoded)[0]

                # Apply temperature to y_pred probabilities
                y_pred = np.log(y_pred) / temperature
                y_pred = np.exp(y_pred) / np.sum(np.exp(y_pred))

                # Select the next word randomly based on the probability distribution
                next_word_index = np.random.choice(len(y_pred), p=y_pred)
                predicted_word = ""
                for word, index in token.word_index.items():
                    if index == next_word_index:
                        predicted_word = word
                        break
                
                # Check if predicted word rhymes with rhyme_word
                if get_phonetic_ending(predicted_word) == get_phonetic_ending(rhyme_words[-1]):
                    # Check if predicted word makes sense in the given position
                    # response = requests.get(f"https://api.datamuse.com/words?rel_jjb={seed_text.split()[-position]}&rel_rhy={predicted_word}")
                    # if response.status_code == 200:
                    #     words = [word["word"] for word in response.json()]
                    #     if len(words) > 0:
                    prediction_word=predicted_word
                    break

          

          
          else:
              encoded = token.texts_to_sequences([seed_text])
              encoded = pad_sequences(encoded, maxlen=seq_length, padding='pre')

              y_pred = model.predict(encoded)[0]

                  # Apply temperature to y_pred probabilities
              y_pred = np.log(y_pred) / temperature
              y_pred = np.exp(y_pred) / np.sum(np.exp(y_pred))

                  # Select the next word randomly based on the probability distribution
              next_word_index = np.random.choice(len(y_pred), p=y_pred)
              predicted_word = ""

              for word, index in token.word_index.items():
                if index == next_word_index:
                          predicted_word = word

                          break
              prediction_word=predicted_word
              
            
          seed_text = seed_text + ' ' + prediction_word
          text.append(prediction_word)

        seed_text = text[-1]
        if(i%2==0):
            rhyme_words.append(text[-1])
        text = ' '.join(text)
        text=profanity.censor(text, '*')
        lyrics.append(text)
        
         

    for i in range(4):
        text = []
        poetry_length=10
        bridge_seed = 'i love you'
        for _ in range(poetry_length):
            encoded = token.texts_to_sequences([bridge_seed])
            encoded = pad_sequences(encoded, maxlen=seq_length, padding='pre')

            y_pred = model.predict(encoded)[0]

            # Apply temperature to y_pred probabilities
            y_pred = np.log(y_pred) / (temperature*1.5)
            y_pred = np.exp(y_pred) / np.sum(np.exp(y_pred))

            # Select the next word randomly based on the probability distribution
            next_word_index = np.random.choice(len(y_pred), p=y_pred)
            predicted_word = ""
            for word, index in token.word_index.items():
                if index == next_word_index:
                    predicted_word = word
                    break
            
            bridge_seed = bridge_seed + ' ' + predicted_word
            text.append(predicted_word)
        if(i%2!=0):
          last_word = rhyme_words[-1] if text else ""
          rhyming_words = pronouncing.rhymes(last_word)
          rhyming_words = [w for w in rhyming_words if w in token.word_index]
          if rhyming_words:
                predicted_word = rhyming_words[np.random.randint(len(rhyming_words))]
                text.append(predicted_word)
        bridge_seed = text[-1]
        if (i%2==0):
          rhyme_words.append(text[-1])
        text = ' '.join(text)
        text=profanity.censor(text, '*')
        lyrics.append(text)    
    # Print the generated lyrics in verse-chorus form
    verse1 = lyrics[:4]
    
    chorus1 = lyrics[4:6]
   
    verse2 = lyrics[6:10]
   
    chorus2 = chorus1
    chorus3 = chorus1
    bridge=lyrics[10:]
    
    structure=[verse1,chorus1,verse2,chorus2,bridge,chorus3]
    structure=transformation(structure,singer)
    
    
    return structure

def generate_poem(seed_text, n_lines, language,temperature=1.0):
    filepath=f'dataset/{language}.txt'
    modelpath=f'trained_model/song_generator_model_{language}.h5'

    with open(filepath,encoding='utf') as file:
         
        text=file.read()
    data=text.splitlines()
    temperature=1.0
    
    # Tokenize the data
    token = Tokenizer()
    token.fit_on_texts(data)
    
    # help(token)
    token.word_index

    encoded_text = token.texts_to_sequences(data)

# Prepare the training data
    max_length = 20
    datalist = []
    for d in encoded_text:
        if len(d) > 1:
            for i in range(2, len(d)):
                datalist.append(d[:i])
                print(d[:i])

    sequences = pad_sequences(datalist, maxlen=max_length, padding='pre')
    X = sequences[:, :-1]
    y = sequences[:, -1]
    y = to_categorical(y, num_classes=len(token.word_index) + 1)

# Define the model architecture
    seq_length = X.shape[1]
    model = tf.keras.models.load_model(f'trained_model/song_generator_model_{language}.h5')
    lyrics=[]
    poetry_length=10
    for _ in range(n_lines):
        text=[]
        
        
        for _ in range(poetry_length):
            encoded = token.texts_to_sequences([seed_text])
            encoded = pad_sequences(encoded, maxlen=seq_length, padding='pre')

            y_pred = model.predict(encoded)[0]

            # Apply temperature to y_pred probabilities
            y_pred = np.log(y_pred) / temperature
            y_pred = np.exp(y_pred) / np.sum(np.exp(y_pred))

            # Select the next word randomly based on the probability distribution
            next_word_index = np.random.choice(len(y_pred), p=y_pred)
            predicted_word = ""
            for word, index in token.word_index.items():
                if index == next_word_index:
                    predicted_word = word
                    break

            seed_text = seed_text + ' ' + predicted_word
            text.append(predicted_word)
            # with open('output.txt', 'a') as file:
            #      file.write(seed_text)
            
        text = ' '.join(text)
        lyrics.append(text)
        
    # data = open('output.txt', encoding="utf8").read()
    # wordcloud = WordCloud(max_font_size=20,
    #     					max_words=100,
    #     					background_color="black").generate(data)

    #     # Plotting the WordCloud
    # plt.figure(figsize=(8, 4))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.savefig("WordCloud.png")
    # plt.show()
        
    structure=[lyrics]    
    return structure



# with open(file_path, 'a') as file:
#     file.write(seed_text)
# data = open('output.txt', encoding="utf8").read()
# wordcloud = WordCloud(max_font_size=20,
# 					max_words=100,
# 					background_color="black").generate(data)

# # Plotting the WordCloud
# plt.figure(figsize=(8, 4))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.savefig("WordCloud.png")
# plt.show()

