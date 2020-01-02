# imports
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import KernelPCA
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
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

# load data with gnender info
overall = pd.read_excel(os.path.join('RAVEN', 'overall_energy_ratios.xlsx'))
overall_immersion = pd.read_excel(os.path.join('RAVEN', 'overall_immersion.xlsx'))
overall_immersion.columns = [ 'immersion_{}'.format('_'.join(column.split(' '))) for column in overall_immersion.columns ]
overall = pd.concat([ overall, overall_immersion ], axis = 1)
overall_P100 = pd.read_excel(os.path.join('RAVEN', 'Overall_P100.xlsx'))
overall = pd.merge(overall, overall_P100, on = 'Indiv')
# overall_P100_correct_incorrect = pd.read_excel(os.path.join('RAVEN', 'Overall_P100_correct_incorrect.xlsx'))
# overall = pd.merge(overall, overall_P100_correct_incorrect, on = 'Indiv')
overall_P300 = pd.read_excel(os.path.join('RAVEN', 'Overall_P300.xlsx'))
overall = pd.merge(overall, overall_P300, on = 'Indiv')
# overall_P300_correct_incorrect = pd.read_excel(os.path.join('RAVEN', 'Overall_P300_correct_incorrect.xlsx'))
# overall = pd.merge(overall, overall_P300_correct_incorrect, on = 'Indiv')
overall = pd.merge(overall, gender_info, on = 'Indiv')

for target in classes:
    keep = overall['Gender'] == target
    target_df = overall[keep]
    overall[keep] = target_df.fillna(target_df.mean())

# select columns and rows
overall = overall[overall[[ feature for feature in overall.columns if feature not in gender_info.columns ]].sum(axis = 1) > 0]
columns = [ column for column in overall.columns if column not in gicolumns ]

x = overall[columns].values
standard_scaler = StandardScaler()
x = standard_scaler.fit_transform(x)
x = pd.DataFrame(x, columns = columns)

# apply PCA
pca = KernelPCA(n_components = 28, kernel = 'rbf', gamma = 15, fit_inverse_transform = True)
x = pca.fit_transform(x)

# normalization
min_max_scaler = MinMaxScaler()
x = min_max_scaler.fit_transform(x)

y = overall['Gender'].values

yset = set(y)
yset = dict([ (value, i) for i, value in enumerate(yset) ])
y = [ yset[value] for value in y ]
length = x.shape[0]

amount = 1000
linear_svc_accuracy = 0
for i in range(amount):
    linear_svc_classifier = LinearSVC(C = 1.0, max_iter = 100000, tol = 1e-05, verbose = 0)

    training_size = math.floor(length * 0.8)
    testing_size = length - training_size

    training_choice = list(np.random.choice(x.shape[0], training_size, replace = False))
    testing_choice = [ i for i in range(x.shape[0]) if i not in training_choice ]

    X_training = x[training_choice, :]
    Y_training = [ y[value] for value in training_choice ]

    X_testing = x[testing_choice, :]
    Y_testing = [ y[value] for value in testing_choice ]

    linear_svc_classifier.fit(X_training, Y_training)
    linear_svc_Y_pred = linear_svc_classifier.predict(X_testing)

    linear_svc_accuracy += accuracy_score(Y_testing, linear_svc_Y_pred)

print('Linear SVC Accuracy: {}'.format(linear_svc_accuracy / amount))