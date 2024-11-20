'''
A script to compare PD vs. HC subcortical volumes in the QPN cohort.
@author: Andrew Vo
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from enigmatoolbox.plotting import plot_subcortical
from statsmodels.stats.multitest import multipletests

path = '/Users/Andrew/Documents/Research/Projects/qpn_data/'
demo = pd.read_csv(path+'matched_data/matched_data_ses-01_range-6mo.csv')
demo['group'] = demo['group'].replace('PD', 'pd')

# clean up derivative measures
vols = pd.read_csv(path+'tabular/aseg.csv')
rois = [
    'participant_id', 'Left-Lateral-Ventricle', 'Left-Thalamus', 'Left-Caudate',
    'Left-Putamen', 'Left-Pallidum', 'Left-Hippocampus', 'Left-Amygdala',
    'Left-Accumbens-area', 'Right-Lateral-Ventricle', 'Right-Thalamus',
    'Right-Caudate', 'Right-Putamen', 'Right-Pallidum', 'Right-Hippocampus',
    'Right-Amygdala', 'Right-Accumbens-area', 'EstimatedTotalIntraCranialVol'
]
vols = vols[rois]
vols.iloc[:, 1:17] = vols.iloc[:, 1:17].div(vols['EstimatedTotalIntraCranialVol'], axis=0) * 100 #normalize to tiv
vols['participant_id'] = vols['participant_id'].str.replace('sub-', '', regex=False) #remove 'sub-' prefix

# match demographic and imaging data
vols = vols[vols['participant_id'].isin(demo['participant_id'])].reset_index(drop=True)

# run linear model
covs = demo[['group', 'mri_age', 'sex']].copy()
betas = pd.DataFrame(index=['const', 'group', 'age', 'sex'], columns=vols.iloc[:, 1:17].columns)
dvals = pd.DataFrame(index=['const', 'group', 'age', 'sex'], columns=vols.iloc[:, 1:17].columns)
pvals = pd.DataFrame(index=['const', 'group', 'age', 'sex'], columns=vols.iloc[:, 1:17].columns)

for roi in vols.iloc[:, 1:17].columns:
    X = pd.concat([pd.get_dummies(covs['group'], drop_first=True), covs['mri_age'],
                       pd.get_dummies(covs['sex'], drop_first=True)], axis=1)
    X = sm.add_constant(X)
    model = sm.OLS(vols.iloc[:, 1:17][roi], X.astype(float)).fit()
    betas[roi] = model.params.values
    dvals[roi] = model.params[1]/np.std(model.resid, ddof=1)
    pvals[roi] = model.pvalues.values
enigma_order = [7, 6, 2, 5, 4, 3, 1, 0, 15, 14, 10, 13, 12, 11, 9, 8]
b = betas.loc['group'][enigma_order]
d = dvals.loc['group'][enigma_order]
p = multipletests(pvals.loc['group'], method='fdr_bh')[1][enigma_order]

# visualize results
fig = plot_subcortical(array_name=d.where(p < 0.05, other=pd.NA), size=(800, 200), scale=(5,5), cmap='coolwarm',
                       color_bar=True, color_range=(-max(abs(d)), max(abs(d))), nan_color=(0.75,0.75,0.75,1),
                       screenshot=True, filename = path+'figures/aseg_effectsize_thresholded.pdf')
