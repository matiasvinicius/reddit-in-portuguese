from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
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
                pca=None):
        self.vectorizer = vectorizer
        self.clf = clf
        self.scaler = scaler
        self.pca = pca
        self.pipe = None
        self.decision_function = None

    def fit(self, X_train, y_train):
        steps = list() 
        steps.append((self.vectorizer.__str__(), self.vectorizer))

        if self.scaler or self.pca: 
            steps.append(("SparseToArray()", SparseToArray()))
        
        if self.scaler: 
            steps.append((self.scaler.__str__(), self.scaler))
        if self.pca: 
            steps.append((self.pca.__str__(), self.pca))
        
        steps.append((self.clf.__str__(), self.clf))

        pipe = Pipeline(steps)
        pipe.fit(X_train, y_train)
        self.pipe = pipe
        return pipe
    
    def predict(self, X_test):
        y_pred = self.pipe.predict(X_test)
        self.decision_function = self.pipe.predict_proba(X_test)[:,1]
        return y_pred
    
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
        metrics["auc_score"] = round(roc_auc_score(y_true, self.decision_function), 4)
        metrics["accuracy"] = round(accuracy_score(y_true, y_pred), 4 )

        return metrics
