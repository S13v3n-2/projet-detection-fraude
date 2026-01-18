from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import warnings

# Class transformer pour traiter les données "trans_date_trans_time" et "dob"
class TransactionDateTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, trans_date_col='trans_date_trans_time', dob_col='dob'):
        self.trans_date_col = trans_date_col
        self.dob_col = dob_col

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # Vérifier que les colonnes existent
        missing_cols = [col for col in [self.trans_date_col, self.dob_col] if col not in X.columns]
        if missing_cols:
            raise ValueError(f"Colonnes manquantes dans le DataFrame : {missing_cols}")

        # Convertir en datetime, gérer erreurs (valeurs non convertibles deviennent NaT)
        X[self.trans_date_col] = pd.to_datetime(X[self.trans_date_col], errors='coerce')
        X[self.dob_col] = pd.to_datetime(X[self.dob_col], errors='coerce')

        # Vérifier les valeurs NaT (non converties) et prévenir
        nans_trans_date = X[self.trans_date_col].isna().sum()
        nans_dob = X[self.dob_col].isna().sum()
        if nans_trans_date > 0:
            warnings.warn(
                f"{nans_trans_date} valeurs invalides ou manquantes dans '{self.trans_date_col}' converties en NaT")
        if nans_dob > 0:
            warnings.warn(f"{nans_dob} valeurs invalides ou manquantes dans '{self.dob_col}' converties en NaT")

        # Calculer age_at_transaction en années
        diff = (X[self.trans_date_col] - X[self.dob_col]).dt.days / 365.25
        # Remplacer les valeurs négatives ou NaN par NaN (pas d'âge négatif)
        diff = diff.where(diff >= 0)
        X['age_at_transaction'] = diff.round(0).astype('Int64')  # supporte les NaN

        # Timestamp en secondes, gérer NaT -> NaN
        X['trans_date_trans_time_timestamp'] = X[self.trans_date_col].astype('int64') // 10 ** 9
        X['trans_date_trans_time_timestamp'] = X['trans_date_trans_time_timestamp'].astype('Int64')  # supporte NaN

        # Supprimer colonnes originales
        X = X.drop(columns=[self.trans_date_col, self.dob_col])

        return X
