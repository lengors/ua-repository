# imports
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, math

# set columns and classes
gicolumns = [ 'Indiv', 'Gender' ]
classes = [ 'Feminino', 'Masculino' ]

# load and filter gender info
gender_info = pd.read_csv(os.path.join('RAVEN', 'data.csv'), header = None, engine = 'python')
gender_info = gender_info[gender_info[1].isin(classes)]

# calculate ratios of correct answers
gender_info['training'] = gender_info[2] / (gender_info[2] + gender_info[3])
gender_info['testing'] = gender_info[4] / (gender_info[4] + gender_info[5])

# rename and select gender and indiv columns
gender_info.rename(columns = dict(enumerate(gicolumns)), inplace = True)
gender_info = gender_info[gicolumns + [ 'training', 'testing' ]]

# load overall energy ratios and merge with gnender info
overall = pd.read_excel(os.path.join('RAVEN', 'overall_energy_ratios.xlsx'))
overall_immersion = pd.read_excel(os.path.join('RAVEN', 'overall_immersion.xlsx'))
overall_immersion.columns = [ 'immersion_{}'.format('_'.join(column.split(' '))) for column in overall_immersion.columns ]

overall = pd.concat([ overall, overall_immersion ], axis = 1)

overall_P100 = pd.read_excel(os.path.join('RAVEN', 'Overall_P100.xlsx'))
overall = pd.merge(overall, overall_P100, on = 'Indiv')

overall_P300 = pd.read_excel(os.path.join('RAVEN', 'Overall_P300.xlsx'))
overall = pd.merge(overall, overall_P300, on = 'Indiv')

overall = pd.merge(overall, gender_info, on = 'Indiv')

# select columns and rows
overall = overall[[ feature for feature in overall.columns if 'correct' not in feature ]]
overall.dropna(inplace = True)
overall = overall[overall[[ feature for feature in overall.columns if feature not in gender_info.columns ]].sum(axis = 1) > 0]

columns = [ column for column in overall.columns if column not in gicolumns ]

# apply standard scaling
x = overall[columns].values
y = overall[[ 'Gender' ]].values
standard_scaler = StandardScaler()
x = standard_scaler.fit_transform(x)
x = pd.DataFrame(x, columns = columns)

# apply PCA
pca = PCA()
x_pca = pca.fit_transform(x)
x_pca = pd.DataFrame(pca.components_, columns = x.columns, index = [ 'PC{}'.format(i + 1) for i in range(len(pca.explained_variance_ratio_)) ])
x_pca['Gender'] = y

# print(pca.explained_variance_ratio_)

features = dict()
for column in columns:
    feature = [ abs(value) for value in x_pca.loc[:, column] ]
    features[column] = sum([ x * y for x, y in zip(pca.explained_variance_ratio_, feature) ])
    # values, columns = zip(*sorted(zip([ abs(value) for value in x_pca.iloc[[ row ]].values[0] ], x_pca.columns), key = lambda x : x[0], reverse = True))
    # result = pd.DataFrame(np.array([ values ]), columns = columns, index = [ row ])

values = features.items()
vector = [ value for _, value in values ]

m = min(vector)
b = max(vector) - m
vector = [ (x - m) / b for x in vector ]
values = zip([ value for value, _ in values ], vector)

columns = [ column for column, value in values if value > 0.5 ]

# normalization
x = overall[columns].values
min_max_scaler = MinMaxScaler()
x = min_max_scaler.fit_transform(x)
overall[columns] = pd.DataFrame(x, columns = columns, index = overall.index)

from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.cluster import KMeans

y = overall['Gender'].values
X = overall[columns].values

yset = set(y)
yset = dict([ (value, i) for i, value in enumerate(yset) ])
y = [ yset[value] for value in y ]
length = X.shape[0]

rf_accuracy = 0
mlp_accuracy = 0
sgd_accuracy = 0
linear_svc_accuracy = 0
ppn_accuracy = 0
svc_accuracy = 0

amount = 1000
for i in range(amount):
    rf_classifier = RandomForestClassifier(max_depth = 3, min_samples_split = 5,n_estimators = 10, max_features = 'log2', oob_score = False)
    mlp_classifier = MLPClassifier(activation = 'tanh', hidden_layer_sizes = (10, 5), alpha = 0.01, max_iter = 5000)
    sgd_classifier = SGDClassifier(loss = 'log', max_iter = 100000)
    linear_svc_classifier = LinearSVC(C = 1.0, max_iter = 100000, tol = 1e-05, verbose = 0)
    ppn_classifier = Perceptron(penalty = None, alpha = 0.0001, fit_intercept = True, max_iter = 10000, tol = None, 
                   eta0 = 0.1, n_jobs = 1, random_state = 0, class_weight = None, warm_start = False)
    svc_classifier = SVC(C = 1.0, kernel = 'rbf', max_iter = 100000, tol = 1e-05, verbose = 0)

    training_size = math.floor(length * 0.8)
    testing_size = length - training_size

    training_choice = list(np.random.choice(X.shape[0], training_size, replace = False))
    testing_choice = [ i for i in range(X.shape[0]) if i not in training_choice ]

    X_training = X[training_choice, :]
    Y_training = [ y[value] for value in training_choice ]

    X_testing = X[testing_choice, :]
    Y_testing = [ y[value] for value in testing_choice ]

    rf_classifier.fit(X_training, Y_training)
    rf_Y_pred = rf_classifier.predict(X_testing)

    mlp_classifier.fit(X_training, Y_training)
    mlp_Y_pred = mlp_classifier.predict(X_testing)

    sgd_classifier.fit(X_training, Y_training)
    sgd_Y_pred = sgd_classifier.predict(X_testing)

    linear_svc_classifier.fit(X_training, Y_training)
    linear_svc_Y_pred = linear_svc_classifier.predict(X_testing)

    ppn_classifier.fit(X_training, Y_training)
    ppn_Y_pred = ppn_classifier.predict(X_testing)

    svc_classifier.fit(X_training, Y_training)
    svc_Y_pred = svc_classifier.predict(X_testing)

    rf_accuracy += accuracy_score(Y_testing, rf_Y_pred)
    mlp_accuracy += accuracy_score(Y_testing, mlp_Y_pred)
    sgd_accuracy += accuracy_score(Y_testing, sgd_Y_pred)
    linear_svc_accuracy += accuracy_score(Y_testing, linear_svc_Y_pred)
    ppn_accuracy += accuracy_score(Y_testing, ppn_Y_pred)
    svc_accuracy += accuracy_score(Y_testing, svc_Y_pred)
    print(i)

print('Random Forest Accuracy: {}'.format(rf_accuracy / amount))
print('MLP Accuracy: {}'.format(mlp_accuracy / amount))
print('SGD Accuracy: {}'.format(sgd_accuracy / amount))
print('Linear SVC Accuracy: {}'.format(linear_svc_accuracy / amount))
print('PPN Accuracy: {}'.format(ppn_accuracy / amount))
print('SVC Accuracy: {}'.format(svc_accuracy / amount))

# print(sorted(, key = lambda x : x[1], reverse = True))

# print(overall)