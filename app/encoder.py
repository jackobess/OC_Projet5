import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder

class FeatureEncoder(BaseEstimator, TransformerMixin):
    
    def __init__(self, encoding_map):
        self.encoding_map = encoding_map
    
    def fit(self, X, y=None):
        self.ohe_categories_ = {}
        for col, params in self.encoding_map.items():
            if params.split(',')[0] == 'ohe':
                self.ohe_categories_[col] = sorted(X[col].unique().tolist())
        X_transformed = self.transform(X)
        self.feature_names_out_ = X_transformed.columns.tolist()
        return self
    
    def transform(self, X):
        X = X.copy()
        cols_ohe = []
        
        for col, params in self.encoding_map.items():
            parts = params.split(',')
            enc_type = parts[0]
            
            if enc_type == 'asis': pass
            
            elif enc_type == 'bin':
                mapping = {}
                for p in parts[1:]:
                    k, v = p.split('=')
                    mapping[k] = int(v)
                X[f'~bin_{col}'] = X[col].map(mapping)
                X = X.drop(columns=[col])
            
            elif enc_type == 'ohe':
                cols_ohe.append(col)
            
            elif enc_type == 'ord':
                categories = parts[1:]
                enc = OrdinalEncoder(categories=[categories])
                X[f'~ord_{col}'] = enc.fit_transform(X[[col]])
                X = X.drop(columns=[col])
        
        if cols_ohe:
            for col in cols_ohe:
                prefix = f'~ohe_{col}'
                for cat in self.ohe_categories_[col]:
                    X[f'{prefix}_{cat}'] = (X[col] == cat).astype(int)
                X = X.drop(columns=[col])
        
        # Réordonner les colonnes comme au fit
        if hasattr(self, 'feature_names_out_'):
            X = X[self.feature_names_out_]

        return X