import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import speech_to_text
import speech_recognition as sr

with open('intents_copy.json') as file:
    data = json.load(file)

words = []
labels = []
docs_x = [] # tokenized words
docs_y = [] # associated tags for each words

# reading json
for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

# stemming and sorting
words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

# bag of words / one-hot encode string data
training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)

# model
net = tflearn.input_data(shape=[None, len(training[0])]) # create input layer
net = tflearn.fully_connected(net, 8) # create 8 hidden layer
net = tflearn.fully_connected(net, 8) # create 8 hidden layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") # create output layer using softmax activation function
net = tflearn.regression(net)

model = tflearn.DNN(net)

# training model
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

# encode input with one hot encoding
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return numpy.array(bag)

# transform speech to text
def speech_recog():
    speech_to_text.recorder()

    try:
        r = sr.Recognizer()
        audio = sr.AudioFile("output.wav")
        with audio as source:
            audio = r.record(source)
        
        inp = r.recognize_google(audio)
    except:
        print("File .wav not found")

    return inp  

# main function
def chat():
    # get input from text or speech
    while True:
        print("Press '1' to interact using terminal. Press '2' to interact using speech. Type 'quit' to quit chatbot")
        user_input = input("> ")

        if user_input == "1":
            print("Start talking with the bot! (Type quit to stop)")
            inp = input("You: ")
                
        elif user_input == "2":
            print("Start talking with the bot.")
            inp = speech_recog()

        elif user_input.lower() == "quit":
            break

        else:
            print("Enter correct input!!")
            continue

        # use input to generate output 
        results = model.predict([bag_of_words(inp, words)])
        result_index = numpy.argmax(results)
        tag = labels[result_index]

        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]

        print(random.choice(responses))
        print("\n")

chat()