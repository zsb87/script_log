import matplotlib
import matplotlib.pyplot as plt
import pylab
import datetime
import pandas as pd
import numpy as np

testsubjfolder = 'P18'
outfolder = './WS/Field/'+testsubjfolder+'/result_USmotif_run2017050501/seg_clf/trainOnUS/'# testsubjfolder is 'P18/'

n_part = 41
l_motif = 0
p = 0
all_indicesL = []
all_indicesArr = []
startList = []
endList = []
pntList = []

def rm_cand_overlaptail(df):
#     for i in range(len(y_predDf)):
#         if y_predDf['Head']>2000:
    df = df[df.Head <2001]
    return df


for i_part in range(1,n_part+1,1):
    y_predDf = pd.read_csv('./WS/Field/'+testsubjfolder+ '/segmentation_USmotif_len2100_overlap100_run2017050502/engy_'+str(i_part)+'_run_pred/pred_headtail_reduced1.csv',names=['Head','Tail','Duration','Dist'])

    if i_part < n_part:# remove the tail part of the overlap unless the last part file
        y_predDf = rm_cand_overlaptail(y_predDf)
        y_predDf.to_csv('./WS/Field/'+testsubjfolder+ '/segmentation_USmotif_len2100_overlap100_run2017050502/engy_'+str(i_part)+'_run_pred/pred_headtail_reduced1_rmoverlap.csv', index = None, header=False)
        
    if len(y_predDf) != 0:    
        print('Part', str(i_part), 'not empty')       
        l_motif += len(y_predDf)


y_predDf = pd.read_csv('./WS/Field/'+testsubjfolder+ '/segmentation_USmotif_len2100_overlap100_run2017050502/engy_'+str(i_part)+'_run_pred/pred_headtail_reduced1.csv',names=['Start','End','Duration','Dist'])

print('length of ', testsubjfolder,' is', l_motif)

