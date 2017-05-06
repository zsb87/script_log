import pandas as pd
import numpy as np

outdatafile = "../inlabUnstr/subject/all/mset1/engy_run2017050501_all_subjs_pred_features.csv"
subjfolders = ['trainP1','testP1','trainP3','testP3','trainP6','testP6','trainP7','testP7','trainP8','testP8']

featDfList = []
    
for subjf in subjfolders:
    run = 2017050501
        
    featfile = "../inlabUnstr/subject/" + subjf + '/mset1/feature/all_features/engy_run' + str(run) + '_pred_features.csv'
    featDf = pd.read_csv(featfile)
    
    featDfList.append(featDf)

pd.concat(featDfList).to_csv(outdatafile, index = None)



outdatafile =  "../inlabUnstr/subject/all/mset1/seg_labels.csv"

labelDfList = []
    
for subjf in subjfolders:
    
    labelfile = "../inlabUnstr/subject/" + subjf + '/mset1/segmentation/engy_run'+str(run)+'_pred_label_thre0.5/seg_labels.csv'
    labelDf = pd.read_csv(labelfile, names = ['label'])
    
    labelDfList.append(labelDf)
    
pd.concat(labelDfList).to_csv(outdatafile, index = None)