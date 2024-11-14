import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load and prepare the data
data = pd.read_csv("ECG-Dataset.csv")
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
    "svm": SVC(),
    "knn": KNeighborsClassifier(),
}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    joblib.dump(model, f"{name}_model.pkl")

    # Generate predictions for the test set
    y_pred = model.predict(X_test_scaled)

    # Print the classification report
    print(f"Classification Report for {name.capitalize()}:\n")
    print(classification_report(y_test, y_pred))
    print("-" * 60)
