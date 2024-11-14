from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import joblib
import numpy as np

# import matplotlib.pyplot as plt

app = Flask(__name__)

# Load and train the models
data = pd.read_csv("ECG-Dataset.csv")

# Assuming the target column is named 'target'
X = data.drop(columns=["target"])
y = data["target"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train models
models = {
          "random_forest": RandomForestClassifier(), 
          "svm": SVC()
          }

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    joblib.dump(model, f"{name}_model.pkl")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Extract the features dynamically from the incoming JSON data
    feature_keys = [
        "age",
        "sex",
        "smoke",
        "years",
        "ldl",
        "chp",
        "height",
        "weight",
        "fh",
        "active",
        "lifestyle",
        "ihd",
        "hr",
        "dm",
        "bpsys",
        "bpdias",
        "htn",
        "ivsd",
        "ecgpatt",
        "qwave",
    ]

    # Create the feature list dynamically based on provided keys
    features_list = [data.get(key, 0) for key in feature_keys]

    # Convert to numpy array and reshape for model input
    features = np.array(features_list).reshape(1, -1)
    scaled_features = scaler.transform(features)

    predictions = {}
    accuracies = {}

    for name, model in models.items():
        # Make the prediction for the given input features
        prediction = model.predict(scaled_features)[0]
        predictions[name] = int(prediction)  # Convert numpy.int64 to Python int

        # Calculate the accuracy on the test set and convert to percentage
        accuracy_percentage = model.score(X_test_scaled, y_test) * 100
        accuracies[name] = round(accuracy_percentage, 2)  # Round to two decimal places

    return jsonify({"predictions": predictions, "accuracies": accuracies})


if __name__ == "__main__":
    app.run(debug=True)
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)