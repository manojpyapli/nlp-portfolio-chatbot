import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.neural_network import MLPClassifier
import pickle

lemmatizer = WordNetLemmatizer()

# Load intents
with open("intents.json") as file:
    data = json.load(file)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# -----------------------------
# Prepare training data
# -----------------------------
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))

        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatize and clean words
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

training = []
output_empty = [0] * len(classes)

# Create Bag of Words
for document in documents:
    bag = []
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in document[0]]

    for word in words:
        bag.append(1 if word in word_patterns else 0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1

    training.append([bag, output_row])

training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

# -----------------------------
# Train Model
# -----------------------------
model = MLPClassifier(hidden_layer_sizes=(8, 8), max_iter=1000)
model.fit(train_x, train_y)

# Save files
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

print("Training completed.")
