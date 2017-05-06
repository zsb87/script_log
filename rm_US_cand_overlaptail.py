import matplotlib
import matplotlib.pyplot as plt
import pylab
import datetime
import pandas as pd
import numpy as np
import sys,os

subj = str(sys.argv[1])

if subj == 'P1':
    n_part = 5;
elif subj == 'P3':
    n_part = 23
elif subj == 'P6':
    n_part = 39
elif subj == 'P7':
    n_part = 30
elif subj == 'P8':
    n_part = 35


l_motif = 0
p = 0
all_indicesL = []
all_indicesArr = []
startList = []
endList = []
pntList = []

def rm_cand_overlaptail(df):
    df = df[df.Head <2001]
    return df


outfolder = '../inlabUnstr/subject/'+subj+'/segmentation/engy_run2017050602_pred_rmoverlap/'
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

outfolder = '../inlabUnstr/subject/'+subj+'/segmentation/engy_run2017050602_pred_label_thre0.5_rmoverlap/'
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
    

# remove the tail part of the overlap unless the last part file
for i_part in range(1,n_part,1):
    y_predDf = pd.read_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred/pred_headtail_reduced_'+str(i_part)+'.csv',names=['Head','Tail','Duration','Dist'])
    y_gt_labelDf = pd.read_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred_label_thre0.5/seg_labels_'+str(i_part)+'.csv',names=['Label'])

    y_predDf = rm_cand_overlaptail(y_predDf)
    y_predDf.to_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred_rmoverlap/pred_headtail_reduced_'+str(i_part)+'.csv', index = None, header=False)
    y_gt_labelDf = y_gt_labelDf.iloc[:len(y_predDf)]
    y_gt_labelDf.to_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred_label_thre0.5_rmoverlap/seg_labels_'+str(i_part)+'.csv', index = None, header=False)
# totally copy the last part file
i_part = n_part
y_predDf = pd.read_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred/pred_headtail_reduced_'+str(i_part)+'.csv',names=['Head','Tail','Duration','Dist'])
y_predDf.to_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred_rmoverlap/pred_headtail_reduced_'+str(i_part)+'.csv', index = None, header=False)
y_gt_labelDf = pd.read_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred_label_thre0.5/seg_labels_'+str(i_part)+'.csv',names=['Label'])
y_gt_labelDf.to_csv('../inlabUnstr/subject/'+subj+ '/segmentation/engy_run2017050602_pred_label_thre0.5_rmoverlap/seg_labels_'+str(i_part)+'.csv', index = None, header=False)



print('finish ',subj)

    # if len(y_predDf) != 0:    
    #     print('Part', str(i_part), 'not empty')       
    #     l_motif += len(y_predDf)

