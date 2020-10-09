from nltk.stem.lancaster import LancasterStemmer
from random import choice
from tensorflow import reset_default_graph
import json
import nltk
import numpy as np
import pickle
import tflearn as tfl

stemmer = LancasterStemmer()

with open('intents.json') as file:
    data = json.load(file)

try:
    with open('chatbot/objects/data.pickle', 'rb') as f:
        words, labels, training, output = pickle.load(f)
except:
    print('Cannot find data.pickle file. Please try to run build_and_train.py first.')


reset_default_graph()
net = tfl.input_data(shape=[None, len(training[0])])
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, len(output[0]), activation='softmax')
net = tfl.regression(net)

model = tfl.DNN(net)

try:
    model.load('chatbot/objects/chatbot_model.h5')
except Exception as e:
    print('ERROR:', e)


def bag_of_words(s, words):
    bag = [0] * len(words)

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def response(sentence):
    results = model.predict([bag_of_words(sentence, words)])[0]
    results_index = np.argmax(results)
    tag = labels[results_index]

    # If the accuracy is greater than 70%, return a response from the model
    if results[results_index] > 0.7:
        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']

        return choice(responses)

    else:
        return 'I didn\'t get that, please try again.'
