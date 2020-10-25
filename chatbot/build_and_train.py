from nltk.stem.lancaster import LancasterStemmer
from tensorflow import reset_default_graph
import json
import os
import nltk
import numpy as np
import pickle
import tflearn as tfl

stemmer = LancasterStemmer()

with open('../intents.json') as file:
    intents = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

# ===================== Data Preprocessing =====================
for intent in intents:
    for pattern in intent['patterns']:
        tokenized_words = nltk.word_tokenize(pattern)
        # Add the tokenized_words into words list
        words.extend(tokenized_words)
        docs_x.append(tokenized_words)
        docs_y.append(intent['tag'])

    # Put the tags inside the labels list
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

# Strip the words into their root words:
words = [stemmer.stem(word.lower()) for word in words if word != '?']
# Remove the duplicates and sort the words:
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

output_empty = [0] * len(labels)

for x, doc in enumerate(docs_x):
    bag = []

    stemmed_words = [stemmer.stem(word.lower()) for word in doc]

    for word in words:
        # If the word exist, append 1
        if word in stemmed_words:
            bag.append(1)
        else:
            bag.append(0)

    output_row = output_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

# Convert into numpy array:
training = np.array(training)
output = np.array(output)

# Check if objects folder exists:
if not os.path.exists('objects'):
    os.mkdir('objects')

# Save into a pickle file:
with open('objects/data.pickle', 'wb') as f:
    pickle.dump((words, labels, training, output), f)


# ===================== Building the model =====================
reset_default_graph()
net = tfl.input_data(shape=[None, len(training[0])])
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, 8)
net = tfl.fully_connected(net, len(output[0]), activation='softmax')
net = tfl.regression(net)

model = tfl.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save('objects/chatbot_model.h5')
