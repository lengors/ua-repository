# imports
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA, KernelPCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# set columns and classes
columns = [ 'Indiv', 'Gender' ]
classes = [ 'Feminino', 'Masculino' ]

# load and filter gender info
gender_info = pd.read_csv(os.path.join('RAVEN', 'data.csv'), header = None, engine = 'python')
gender_info = gender_info[gender_info[1].isin(classes)]

# rename and select gender and indiv columns
gender_info.rename(columns = dict(enumerate(columns)), inplace = True)
gender_info = gender_info[columns]

# load overall energy ratios and merge with gnender info
overall_energy_ratios = pd.read_excel(os.path.join('RAVEN', 'overall_energy_ratios.xlsx'))
overall_energy_ratios = pd.merge(overall_energy_ratios, gender_info, on = 'Indiv')
overall_energy_ratios.dropna(inplace = True)

# select features to apply PCA
features = overall_energy_ratios.columns
features = [ feature for feature in features if feature not in columns ]

# apply standard scaling
x = overall_energy_ratios[features].values
y = overall_energy_ratios[[ 'Gender' ]].values
x = StandardScaler().fit_transform(x)
x = pd.DataFrame(x, columns = features)

# apply PCA
pca = PCA()
x_pca = pca.fit_transform(x)
# x_pca = pd.DataFrame(x_pca)
x_pca = pd.DataFrame(pca.components_, columns = x.columns, index = [ 'PC{}'.format(i + 1) for i in range(len(pca.explained_variance_ratio_)) ])
# x_pca['Gender'] = y

# get most relevant features
x_pca = x_pca[[ i < 14 for i in range(len(pca.explained_variance_ratio_)) ]]
for row in range(x_pca.shape[0]):
    values, columns = zip(*sorted(zip([ abs(value) for value in x_pca.iloc[[ row ]].values[0] ], x_pca.columns), key = lambda x : x[0], reverse = True))
    print(pd.DataFrame(np.array([ values ]), columns = columns, index = [ row ]))
# print(pca.explained_variance_ratio_)
'''
fig = plt.figure()
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1') 
ax.set_ylabel('Principal Component 2') 
ax.set_title('2 component PCA')
colors = [ 'r', 'b' ]
for target, color in zip(classes, colors):
    indicesToKeep = x_pca['Gender'] == target
    ax.scatter(x_pca.loc[indicesToKeep, 'PC1'], x_pca.loc[indicesToKeep, 'PC3'], c = color, s = 50)
ax.legend(classes)
ax.grid()

plt.show(fig)'''

print(sum(pca.explained_variance_ratio_[:14]))

plt.bar(range(len(pca.explained_variance_ratio_)), pca.explained_variance_ratio_, alpha=0.5, align='center')
plt.step(range(len(pca.explained_variance_ratio_)), np.cumsum(pca.explained_variance_ratio_), where='mid')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.show()