import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib


def load_training_data(features_csv: str, winners_csv: str):
    """Merge feature data with winners to build a labelled dataset."""
    features = pd.read_csv(features_csv)
    winners = pd.read_csv(winners_csv)

    data = features.merge(winners, on="Year", how="left")
    data["Label"] = (data["Name"] == data["Winner"]).astype(int)
    data.fillna(0, inplace=True)

    X = data[["Views", "Tweet Count"]]
    y = data["Label"]
    return X, y


def train_model(X, y):
    """Train a RandomForest model with simple grid search."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    param_grid = {"n_estimators": [100, 200, 300], "max_depth": [None, 5, 10]}
    clf = RandomForestClassifier(random_state=42)
    search = GridSearchCV(clf, param_grid, cv=5, scoring="accuracy")
    search.fit(X_train, y_train)

    best = search.best_estimator_
    y_pred = best.predict(X_test)
    print("Best parameters:", search.best_params_)
    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

    joblib.dump(best, "person_of_the_year_model.pkl")
    return best


def predict_next_year(model_path: str, features_csv: str):
    model = joblib.load(model_path)
    df = pd.read_csv(features_csv)
    X_future = df[["Views", "Tweet Count"]]
    df["Score"] = model.predict_proba(X_future)[:, 1]
    return df.sort_values("Score", ascending=False)


if __name__ == "__main__":
    # paths can be changed as needed
    X, y = load_training_data("training_features.csv", "winners.csv")
    trained_model = train_model(X, y)

    predictions = predict_next_year(
        "person_of_the_year_model.pkl", "features_2024.csv"
    )
    print(predictions[["Name", "Score"]].head())
