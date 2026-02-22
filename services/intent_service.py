import pickle

# Load model
model = pickle.load(open("ml/model.pkl", "rb"))


def predict_intent(message):

    intent = model.predict([message])[0]

    confidence = max(
        model.predict_proba([message])[0]
    )

    return intent, confidence