import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV

def train_model(df, model_path="models/random_forest.pkl") :
    """
    Entrée : df
    Sortie : modèle entrainé sur le df, features pour un test avec les cibles
    """

    # séparation entre les features et la cible
    X = df.drop(columns=["target"])
    y = df["target"]

    # séparation train / test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # craétion du modèle
    # "balanced" sert à avoir 33% de bougies hautes/basses/neutres
    model = RandomForestClassifier(n_estimators=100, random_state=2, class_weight="balanced")
    # entrainement
    model.fit(X_train, y_train)

    # sauvegarde du modèle
    with open(model_path, 'wb') as f :
        pickle.dump(model, f)
    
    print("Modèle créé et enregistré")

    return model, X_test, y_test

def tune_model(df, model_path="models/random_forest.pkl"):
    """
    Entrée : dataframe avec features plus la colonne "target'
    Sortie : meilleur modèle après GridSearch
    """
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Toutes les combinaisons qui vont être testées
    param_grid = {
        "n_estimators": [100, 200, 300],       # nombre arbres
        "max_depth": [5, 10, 20, None],        # profondeur maximale de chaque arbre
        "min_samples_split": [2, 10, 20],      # nombre min d'exemples pour couper un noeud
        "min_samples_leaf": [1, 5, 10]         # nombre min d'exemples dans une feuille
    }

    grid = GridSearchCV(
        RandomForestClassifier(class_weight="balanced", random_state=42),
        param_grid,
        cv=5,               # découpe le train en 5 pour valider chaque combinaison
        scoring="f1_macro", # optimise sur les 3 classes équitablement
        n_jobs=-1,          # utilise tous tes CPU en //
        verbose=1
    )

    print("===============================================")
    print("Research of the bests parameters...")
    grid.fit(X_train, y_train)
    print(f"Bests parameters : {grid.best_params_}")

    with open(model_path, "wb") as f:
        pickle.dump(grid.best_estimator_, f)

    print("The model has been created")
    return grid.best_estimator_, X_test, y_test