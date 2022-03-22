import os
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, fbeta_score

if __name__ == '__main__':
    dir = os.getcwd()
    dataset = pd.read_csv(os.path.join(os.path.dirname(dir), "data.csv"))
    xdata = dataset[['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']]
    ydata = dataset['Label']
    X_train, X_test, y_train, y_test = train_test_split(xdata, ydata, test_size = 0.3)

    param_grid = {
        'alpha': np.arange(0.9, 1.1, 0.1),
        'fit_prior': [True, False]
    }
    estimator = MultinomialNB()
    model = GridSearchCV(estimator, param_grid, n_jobs = -1, cv = 5, verbose = 1)
    model.fit(X_train, y_train)
    print(model.best_params_)
    best_model = model.best_estimator_

    train_predictions = best_model.predict(X_train)
    # train_probs = best_model.predict_proba(X_train)[:, 1]
    test_predictions = best_model.predict(X_test)
    # test_probs = best_model.predict_proba(X_test)[:, 1]

    tn, fp, fn, tp = confusion_matrix(y_train, train_predictions).ravel()
    Precision = tp / (tp + fp)
    Recall = tp / (fn + tp)
    FPRate = fp / (fp + tn)
    FNRate = fn / (fn + tp)
    print('\nBayesian on training set:')
    print('TP: {:<10d}\tTN: {:<10d}\tFP: {:<10d}\tFN: {:<10d}'.format(tp, tn, fp, fn))
    print('Accuracy: {:.2%}\tFbeta_Score: {:.2%}'.format(best_model.score(X_train, y_train), fbeta_score(y_train, train_predictions, beta=0.5)))
    print('Precision: {:.2%}\tRecall: {:.2%}\tFP Rate: {:.2%}\tFN Rate: {:.2%}'.format(Precision, Recall, FPRate, FNRate))

    tn, fp, fn, tp = confusion_matrix(y_test, test_predictions).ravel()
    Precision = tp / (tp + fp)
    Recall = tp / (fn + tp)
    FPRate = fp / (fp + tn)
    FNRate = fn / (fn + tp)
    print('\nBayesian on test set:')
    print('TP: {:<10d}\tTN: {:<10d}\tFP: {:<10d}\tFN: {:<10d}'.format(tp, tn, fp, fn))
    print('Accuracy: {:.2%}\tFbeta_Score: {:.2%}'.format(best_model.score(X_test, y_test), fbeta_score(y_test, test_predictions, beta=0.5)))
    print('Precision: {:.2%}\tRecall: {:.2%}\tFP Rate: {:.2%}\tFN Rate: {:.2%}'.format(Precision, Recall, FPRate, FNRate))