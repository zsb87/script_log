import pandas as pd

featfile = "../inlabUnstr/subject/all/mset1/engy_run2017050501_all_subjs_pred_features.csv"
labelfile =  "../inlabUnstr/subject/all/mset1/seg_labels.csv"

featdf = pd.read_csv(featfile)
labeldf = pd.read_csv(labelfile)

featlabel = pd.concat([featdf, labeldf], axis=1)

pos_df = featlabel.loc[featlabel['label'] == 1]
print(len(pos_df))
featlabel.to_csv("../inlabUnstr/subject/all/mset1/all_subj_36feature_labels.csv",index = None)