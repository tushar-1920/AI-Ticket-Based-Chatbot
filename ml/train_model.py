import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# Training data
data = {

    "text": [

        "cannot login",
        "login problem",
        "login error",

        "internet not working",
        "network issue",
        "wifi not working",

        "payment failed",
        "cannot pay",
        "transaction error",

        "hello",
        "hi",
        "good morning"

    ],

    "intent": [

        "login_issue",
        "login_issue",
        "login_issue",

        "network_issue",
        "network_issue",
        "network_issue",

        "payment_issue",
        "payment_issue",
        "payment_issue",

        "greeting",
        "greeting",
        "greeting"

    ]

}

df = pd.DataFrame(data)

# Create pipeline
model = Pipeline([

    ("vectorizer", TfidfVectorizer()),

    ("classifier", LogisticRegression())

])

# Train model
model.fit(df["text"], df["intent"])

# Save model
pickle.dump(
    model,
    open("ml/model.pkl", "wb")
)

print("Model trained and saved successfully.")