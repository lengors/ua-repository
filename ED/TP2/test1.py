# imports
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.ensemble import RandomForestClassifier
from concurrent.futures import ProcessPoolExecutor
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC, SVC
from sklearn.decomposition import PCA, KernelPCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, math


def test(args):
    f_count, X, y = args

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

    amount = 2000
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

    return f_count, rf_accuracy / amount, mlp_accuracy / amount, sgd_accuracy / amount, linear_svc_accuracy / amount, ppn_accuracy / amount, svc_accuracy / amount

if __name__ == '__main__':
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
    # overall = overall[[ feature for feature in overall.columns if 'correct' not in feature ]]
    overall = overall[overall[[ feature for feature in overall.columns if feature not in gender_info.columns ]].sum(axis = 1) > 0]
    columns = [ column for column in overall.columns if column not in gicolumns ]

    # apply standard scaling
    x = overall[columns].values
    standard_scaler = StandardScaler()
    x = standard_scaler.fit_transform(x)
    topca = pd.DataFrame(x, columns = columns)

    # apply PCA
    # pca = PCA()

    iterable = list()
    for i in range(1, 34):
        pca = KernelPCA(n_components = i, kernel = 'rbf', gamma = 15, fit_inverse_transform = True)
        x_pca = pca.fit_transform(topca)

    # print(x_pca.shape)
    # x_pca = pd.DataFrame(pca.components_, columns = x.columns, index = [ 'PC{}'.format(i + 1) for i in range(len(pca.explained_variance_ratio_)) ])

    # normalization
        x = x_pca
        min_max_scaler = MinMaxScaler()
        x = min_max_scaler.fit_transform(x)

        iterable.append((i, x, overall['Gender'].values))
    # overall[columns] = pd.DataFrame(x, columns = columns, index = overall.index)

    with open('results7.txt', 'w') as fout:
        pass

    print('Processing...')

    # iterable = [ (f_count, overall, list(set([ x_pca.columns[np.abs(x_pca.loc['PC{}'.format(i + 1), :].values).argmax() ] for i in range(f_count) ]))) for f_count in range(1, len(pca.explained_variance_ratio_) + 1) ]
    # iterable.append((len(columns), overall, columns))

    # iterable = x_pca, overall['Gender'].values

    with ProcessPoolExecutor(max_workers = 12) as executor:
        for f_count, rf_accuracy, mlp_accuracy, sgd_accuracy, linear_svc_accuracy, ppn_accuracy, svc_accuracy in executor.map(test, iterable):
            print('\ntop-{}'.format(f_count))
            print('Random Forest Accuracy: {}'.format(rf_accuracy))
            print('MLP Accuracy: {}'.format(mlp_accuracy))
            print('SGD Accuracy: {}'.format(sgd_accuracy))
            print('Linear SVC Accuracy: {}'.format(linear_svc_accuracy))
            print('PPN Accuracy: {}'.format(ppn_accuracy))
            print('SVC Accuracy: {}'.format(svc_accuracy))

            with open('results7.txt', 'a+') as fout:
                fout.write('\ntop-{}:\n'.format(f_count))
                fout.write('Random Forest Accuracy: {}\n'.format(rf_accuracy))
                fout.write('MLP Accuracy: {}\n'.format(mlp_accuracy))
                fout.write('SGD Accuracy: {}\n'.format(sgd_accuracy))
                fout.write('Linear SVC Accuracy: {}\n'.format(linear_svc_accuracy))
                fout.write('PPN Accuracy: {}\n'.format(ppn_accuracy))
                fout.write('SVC Accuracy: {}\n'.format(svc_accuracy))
