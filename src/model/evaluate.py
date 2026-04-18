from sklearn.metrics import classification_report, confusion_matrix

import pandas as pd
import matplotlib.pyplot as plt

def evaluate(model, X_test, y_test):
    """
    Entrée : le modèle, les features et les cibles
    Sortie : performances et matrice de confusion
    """

    y_pred = model.predict(X_test)

    print("===============================================")
    print("Performances : ")
    print(classification_report(y_test, y_pred, target_names=["Down", "Neutral", "Up"], zero_division=0))
    
    print("===============================================")
    print("Confusion matrix : ")
    print(confusion_matrix(y_test, y_pred))

def show_feature_importance(model, feature_names):
    importance = pd.Series(
        model.feature_importances_,
        index=feature_names
    ).sort_values(ascending=False)

    print("===============================================")
    print("Importance des features")
    print(importance)

    importance.plot(kind="bar", figsize=(12, 5), title="Feature Importance")
    plt.tight_layout()
    plt.savefig("models/feature_importance.png")
    plt.show()