import json
import pickle
import random
import numpy as np
import nltk
from fastapi.middleware.cors import CORSMiddleware
import info
from fastapi.staticfiles import StaticFiles


from fastapi.staticfiles import StaticFiles



from fastapi import FastAPI
from nltk.stem import WordNetLemmatizer

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



lemmatizer = WordNetLemmatizer()

# Load trained files
model = pickle.load(open("model.pkl", "rb"))
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

with open("intents.json") as file:
    intents = json.load(file)


# -----------------------------
# Helper Functions
# -----------------------------

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [
        lemmatizer.lemmatize(word.lower())
        for word in sentence_words
    ]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)

    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)


def predict_class(sentence):

    bow = bag_of_words(sentence)

    probabilities = model.predict_proba([bow])[0]

    max_prob = max(probabilities)
    predicted_index = np.argmax(probabilities)

    # Confidence threshold
    if max_prob < 0.6:
        return "unknown"

    return classes[predicted_index]



def get_response(tag):

    if tag == "unknown":
        return {
        "type": "text",
        "response": "I am not capable of understanding this message yet. Please try asking in a different way."
    }


    elif tag == "about":
        return {"type": "about", "response": info.get_about()}

    elif tag == "skills":
        return {"type": "skills", "response": info.get_skills()}

    elif tag == "projects":
        return {"type": "projects", "response": info.get_projects()}

    elif tag == "experience":
        return {"type": "experience", "response": info.get_experience()}

    elif tag == "contact":
        return {"type": "contact", "response": info.get_contact()}
    
    elif tag == "resume":
        return {"type": "resume", "response": info.get_resume()}


    else:
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                return {"type": "text", "response": random.choice(intent["responses"])}



# -----------------------------
# API Endpoint
# -----------------------------


@app.get("/chat")
def chat(msg: str):
    tag = predict_class(msg)
    return get_response(tag)
