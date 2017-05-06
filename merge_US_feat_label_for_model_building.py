import pandas as pd
import numpy as np
import sys, os

# i_subj = int(sys.argv[1])


outdatafolder = "../inlabUnstr/subject/all/feature/36_features/"
outdatafile = "../inlabUnstr/subject/all/feature/36_features/"+"engy_run2017050602_all_subjs_36features.csv"
subjs = ['P1','P3','P6','P7','P8']
run = 2017050602
# subj = subjs[i_subj]



if not os.path.exists(outdatafolder):
    os.makedirs(outdatafolder)

featDfList = []
labelDfList = []

for subjf in subjs:
    if subjf == 'P1':
        n_part = 5
    elif subjf == 'P3':
        n_part = 23
    elif subjf == 'P6':
        n_part = 39
    elif subjf == 'P7':
        n_part = 30
    elif subjf == 'P8':
        n_part = 35

    for i_part in range(1, n_part+1):
        featfile = "../inlabUnstr/subject/" + subjf + '/feature/36_features/part_'+str(i_part)+'/engy_run' + str(run) + '_pred_features.csv'
        featDf = pd.read_csv(featfile)
        featDfList.append(featDf)

        labelfile = "../inlabUnstr/subject/" + subjf + '/segmentation/engy_run'+str(run)+'_pred_label_thre0.5_rmoverlap/seg_labels_'+str(i_part)+'.csv'
        labelDf = pd.read_csv(labelfile, names = ['label'])
        labelDfList.append(labelDf)


outlabelfile = "../inlabUnstr/subject/all/feature/36_features/"+"engy_run2017050602_all_subjs_36feat_labels.csv"

featDf = pd.concat(featDfList)
featDf.to_csv(outdatafile, index = None)

labelDf = pd.concat(labelDfList)
labelDf.to_csv(outlabelfile, index = None)


featlabel = pd.concat([featDf, labelDf], axis=1)

pos_df = featlabel.loc[featlabel['label'] == 1]
print('# of positive instances: ',len(pos_df))

featlabel.to_csv("../inlabUnstr/subject/all/feature/36_features/"+"engy_run2017050602_all_subj_36feature_labels.csv",index = None)