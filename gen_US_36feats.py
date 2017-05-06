import os
import re
import csv
import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import time
import random
import glob
from sklearn import preprocessing
from sklearn import svm, neighbors, metrics, cross_validation, preprocessing
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import auc, silhouette_score
from sklearn.cluster import KMeans, DBSCAN
from scipy import *
from scipy.stats import *            
from scipy.signal import *
from collections import Counter
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score
import _pickle as cPickle
from stru_utils import *
import shutil   
import matlab.engine

protocol = str(sys.argv[1])
i_subj = int(sys.argv[2])
run = int(sys.argv[3])
dist = float(sys.argv[4])
n_motif = float(sys.argv[5])
config_file = str(sys.argv[6])

print(protocol)

if protocol == 'inlabStr':
    subjs = ['P3','P4','P5', 'P10']
if protocol == 'inlabUnstr':
    subjs = ['P1','P3','P6','P7','P8']
subj = subjs[i_subj]


# 
# # segmentation based on motif
# 


save_flg = 1

if 1:
    if 1:
        # generate feature files both for test and train set of this subj
        split_subjs = ['train'+subj,'test'+subj]

        for split_subj in split_subjs:

            subjfolder = split_subj + '/'
            folder = '../'+protocol+'/subject/'
            featFolder = folder+subjfolder+"mset1/feature/all_features/"

            datafile =  folder+subjfolder+"testdata_labeled.csv"
            segfolder = folder+subjfolder+"mset1/segmentation/"
               
            # 
            #   generate prediction segment features
            #   1. generate raw data files from Head tail 
            # 
            if not os.path.exists(featFolder):
                os.makedirs(featFolder)

            # read in the raw data file
            # dataFrame:     Time  Angular_Velocity_x  Angular_Velocity_y  Angular_Velocity_z  
            #                 Linear_Accel_x  Linear_Accel_y  Linear_Accel_z  unixtime synctime  
            r_df = pd.read_csv(datafile)

            predActFilePath = segfolder+'engy_run'+str(run)+'_pred/pred_headtail_reduced_1.csv'
            gt_headtail = pd.read_csv(predActFilePath, names = ['Start','End','EnergyDur','dist'])

            # if os.path.exists(segfolder+'accx_pred_data/'):
            #     shutil.rmtree(segfolder+'accx_pred_data/')


            if not os.path.exists(segfolder+'engy_run'+str(run)+'_pred_data/'):
                os.makedirs(segfolder+'engy_run'+str(run)+'_pred_data/')

            for f in glob.glob(segfolder+'engy_run'+str(run)+'_pred_data/*'):
                os.remove(f)

            for i in range(len(gt_headtail)):
                saveFilePath = segfolder+'engy_run'+str(run)+'_pred_data/' + 'engy_pred_gesture_' + str(i) + '.csv'

                dataStart = int(gt_headtail['Start'].iloc[i])*2 - 2
                dataEnd = int(gt_headtail['End'].iloc[i])*2 + 1

                r_df_gesture = r_df.iloc[dataStart:dataEnd]
                
                r_df_gesture.to_csv(saveFilePath)



            # 
            #   generate prediction segment features
            #   2. from raw data of segments generate features
            # 

            predFolder = segfolder+'engy_run'+str(run)+'_pred_data/'

            allfeatDF = pd.DataFrame()
            for _, dirnames, filenames in os.walk(predFolder):
                n_gest = len(filenames)

                if n_gest == 0:
                    print("no prediction file for current subject")
                    continue
                else:
                    for i in range(n_gest):

                        # read in the raw data file
                        # dataFrame:     Time  Angular_Velocity_x  Angular_Velocity_y  Angular_Velocity_z  
                        #                 Linear_Accel_x  Linear_Accel_y  Linear_Accel_z  unixtime synctime  

                        r_df = pd.read_csv(predFolder + 'engy_pred_gesture_' + str(i) + '.csv')

                        # pass raw data into filter
                        r_df = r_df[['Angular_Velocity_x', 'Angular_Velocity_y', 'Angular_Velocity_z', 'Linear_Accel_x','Linear_Accel_y','Linear_Accel_z']]

                        # r_df = df_iter_flt(r_df)
                        if i % 200 == 0:
                            print(i)
                        # r_df = add_pitch_roll(r_df)
                        # generate the features
                        # 1,5,14,18,24,25,26,29,31,37,40,41,47,48,49,55,57,59,60,65,67,70,76,81,87,106,108
                        feat = gen_feat_36(r_df)

                        featDF = pd.DataFrame(feat[1:] , columns=feat[0])
                        allfeatDF = pd.concat([allfeatDF,featDF])


            outfile = featFolder + "engy_run"+ str(run) +"_pred_features.csv"
            allfeatDF.to_csv(outfile, index =None)



