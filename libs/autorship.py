import imp
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score, roc_auc_score
import numpy as np

import sys
sys.path.insert(1, '../../libs')
from utils import SparseToArray

class AuthorClassifier:
    def __init__(self, 
                vectorizer=CountVectorizer(), 
                clf=MultinomialNB(),
                scaler=None,
                pca=None,
                kbest=None,
                param_grid=None):
        self.vectorizer = vectorizer
        self.clf = clf
        self.scaler = scaler
        self.pca = pca
        self.kbest = kbest
        self.param_grid = param_grid
        self.pipe = None
        self.predict_proba = None

    def fit(self, X_train, y_train, params=[]):
        steps = list() 
        steps.append(("vectorizer", self.vectorizer))

        if self.scaler or self.pca: 
            steps.append(("SparseToArray()", SparseToArray()))
        
        if self.scaler: 
            steps.append(("scaler", self.scaler))
        if self.pca: 
            steps.append(("pca", self.pca))
        if self.kbest:
            steps.append(("kbest", self.kbest))

        steps.append(("clf", self.clf))

        pipe = Pipeline(steps)

        if self.param_grid:
            pipe = GridSearchCV(pipe, self.param_grid, n_jobs=-1, cv=3)
    
        pipe.fit(X_train, y_train)
        self.pipe = pipe
        return self.pipe
    
    def predict(self, X_test):
        y_pred = self.pipe.predict(X_test)
        self.predict_proba = self.pipe.predict_proba(X_test)[:,1]
        return y_pred
    
    def get_best_params(self):
        if self.pipe: return self.pipe.best_params_
        return None

    def get_best_estimator(self):
        if self.pipe: return self.pipe.best_estimator_
        return None

    def evaluate(self, y_true, y_pred):
        metrics = dict()
        for i, author in enumerate(np.unique(y_true)):
            i += 1
            metrics[f"author{i}"] = author
        for i, author in enumerate(np.unique(y_true)):
            i += 1
            metrics[f"precision_author{i}"] = round(precision_score(y_true, y_pred, pos_label=author), 4)
            metrics[f"recall_author{i}"] = round(recall_score(y_true, y_pred, pos_label=author), 4)
            metrics[f"f1_score_author{i}"] = round(f1_score(y_true, y_pred, pos_label=author), 4)
        metrics["precision_weighted"] = round(precision_score(y_true, y_pred, average='weighted'), 4 )
        metrics["precision_micro"] = round(precision_score(y_true, y_pred, average='micro'), 4 )
        metrics["precision_macro"] = round(precision_score(y_true, y_pred, average='macro'), 4 )
        metrics["recall_weighted"] = round(recall_score(y_true, y_pred, average='weighted'), 4 )
        metrics["recall_micro"] = round(recall_score(y_true, y_pred, average='micro'), 4 )
        metrics["recall_macro"] = round(recall_score(y_true, y_pred, average='macro'), 4 )
        metrics["f1_weighted"] = round(f1_score(y_true, y_pred, average='weighted'), 4 )
        metrics["f1_micro"] = round(f1_score(y_true, y_pred, average='micro'), 4 )
        metrics["f1_macro"] = round(f1_score(y_true, y_pred, average='macro'), 4 )
        metrics["auc_score"] = round(roc_auc_score(y_true, self.predict_proba), 4)
        metrics["accuracy"] = round(accuracy_score(y_true, y_pred), 4 )

        return metrics
