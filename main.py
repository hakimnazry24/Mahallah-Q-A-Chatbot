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
import speech_recognition as sr
import speech_to_text
# test

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

# bag of words
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

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

# model
net = tflearn.input_data(shape=[None, len(training[0])]) # create input layer
net = tflearn.fully_connected(net, 8) # create 8 hidden layer
net = tflearn.fully_connected(net, 8) # create 8 hidden layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") # create output layer using softmax activation function
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return numpy.array(bag)

def speech_recog():
    speech_to_text.speech_to_text()

    try:
        r = sr.Recognizer()
        audio = sr.AudioFile("output.wav")
        with audio as source:
            audio = r.record(source)
        
        inp = r.recognize_google(audio)
    except:
        print("File .wav not found")

    return inp  
    # steps
    # 1. kite cakap kat mic
    # 2. google api translate jadi speech.txt
    # 3. pass speech.txt as input
    # 4. model cari best response
    # 5. model pass output

def chat():
    #print("Training model ....")
    #model()
    #print("Finish training model ...")

    # interaction using terminal / text
    # print("Start talking with the bot! (Type quit to stop)")
    # while True:
    #     inp = input("You: ")
    #     if inp.lower() == 'quit':
    #         break

    #     results = model.predict([bag_of_words(inp, words)])
    #     result_index = numpy.argmax(results)
    #     tag = labels[result_index]
    #     #print(tag)

    #     for tg in data["intents"]:
    #         if tg["tag"] == tag:
    #             responses = tg["responses"]
        
    #     print(random.choice(responses))
    #     print("\n")

    # INTERACTION USING SPEECH
    
    while True:
        inp = speech_recog()

        while True:
            results = model.predict([bag_of_words(inp, words)])
            result_index = numpy.argmax(results)
            tag = labels[result_index]

            for tg in data["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]

            print(random.choice(responses))
            print("\n")
            
            user_inp = input("Press 1 to speak.")
            if user_inp == "1":
                break
    
chat()