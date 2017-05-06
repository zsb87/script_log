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
# import matlab.engine

testsubjfolder = str(sys.argv[1])
run = int(sys.argv[2])

save_flg = 1

if 1:
    if 1:

        #
        # train model
        #
        # columns = ['Prec(pos)','F1(pos)','TPR','FPR','Specificity','MCC','CKappa','w-acc']
        # crossValRes = pd.DataFrame(columns = columns, index = range(5))
        active_p_cnt = 0
        
        train_prtc = 'US'
        trainsubj = 'all'

        for threshold_str in ['0.5']:

            # for trainsubj in trainsubjs:

            df = pd.read_csv("./WS/"+train_prtc+"/"+trainsubj+"/engy_run_all_subjs_pred_features.csv")
            # df = pd.read_csv("./WS/subject/"+testsubjfolder+"feature/feature_"+str(i_part)+"/engy_run_pred_features.csv" )
            labelDf = pd.read_csv('./WS/'+train_prtc+"/"+trainsubj+'/seg_labels.csv',names = ['label'])

            # 
            # notice:   duration should not be included in features 
            #           as in detection period this distinguishable feature will be in different distribution
            # 
            X = df.iloc[:,:-1].as_matrix()
            Y = labelDf['label'].iloc[:].as_matrix()

            classifier = RandomForestClassifier(n_estimators=185)
            classifier.fit(X, Y)


            # save the classifier

            mdlFolder = './WS/'+train_prtc+'/'+trainsubj+'/model/' 
            if not os.path.exists(mdlFolder):
                os.makedirs(mdlFolder)

            with open(mdlFolder+'RF_185_trainset_motif_segs_thre'+threshold_str+'_run0.pkl', 'wb') as fid:
                cPickle.dump(classifier, fid)    


    test_Prtc = 'Field'
    testsubjfolder = testsubjfolder + '/'

    if testsubjfolder == 'P10/':
        numSplit = 10
    elif testsubjfolder == 'P12/':
        numSplit = 114
    elif testsubjfolder == 'P4/':
        numSplit = 119
    elif testsubjfolder == 'P18/':
        numSplit = 41
    elif testsubjfolder == 'P24/':
        numSplit = 184


    if train_prtc == 'US':
        resultfolder = './WS/'+test_Prtc+'/'+testsubjfolder+"run"+str(run)+'/result_USmotif/seg_clf/trainOnUS/' # testsubjfolder is 'P10/'
    elif train_prtc == 'IS':
        resultfolder = './WS/'+test_Prtc+'/'+testsubjfolder+"run"+str(run)+'/result_ISmotif/seg_clf/trainOnIS/' # testsubjfolder is 'P10/'
    if not os.path.exists(resultfolder):
        os.makedirs(resultfolder)

    if train_prtc == 'US':
        segfolder = './WS/'+test_Prtc+'/'+testsubjfolder+"run"+str(run)+"/segmentation_USmotif/"
    elif train_prtc == 'IS':
        segfolder = './WS/'+test_Prtc+'/'+testsubjfolder+"run"+str(run)+"/segmentation_ISmotif/"


    for i_part in range(1,numSplit+1,1):
        print('i_part: ')
        print(i_part)

        if 1:
            if train_prtc == 'US':
                featFolder = './WS/'+test_Prtc+'/'+testsubjfolder+"run"+str(run)+"/feature_USmotif/feature_"+str(i_part)+"/"
            elif train_prtc == 'IS':
                featFolder = './WS/'+test_Prtc+'/'+testsubjfolder+"run"+str(run)+"/feature_ISmotif/feature_"+str(i_part)+"/"

            datafile =  './WS/'+test_Prtc+'/'+testsubjfolder+"testdata/testdata_"+str(i_part)+".csv"

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
            # print(r_df.head)

            predActFilePath = segfolder+'engy_'+str(i_part)+'_run_pred/pred_headtail_reduced1.csv'
            gt_headtail = pd.read_csv(predActFilePath, names = ['Start','End','EnergyDur','dist'])

            allfeatDF = pd.DataFrame()

            for i in range(len(gt_headtail)):
                # looking back to this block, I think start*2+1 and end*2+4 should be correct
                # when start from the first point, 0*2-2 = -2, -> bug
                # when using motif and RF mdl built from *2-2, no problem for counting
                # 
                # in the future, when change to *2+1 and *2+4, the motif and modl should be rebuilt
                # 
                dataStart = int(gt_headtail['Start'].iloc[i])*2 - 2
                dataEnd = int(gt_headtail['End'].iloc[i])*2 + 1

                r_df_gesture = r_df.iloc[dataStart:dataEnd]
                

                # pass raw data into filter
                r_df_gesture = r_df_gesture[['Angular_Velocity_x', 'Angular_Velocity_y', 'Angular_Velocity_z', 'Linear_Accel_x','Linear_Accel_y','Linear_Accel_z']]

                # r_df_gesture = df_iter_flt(r_df_gesture)
                if i % 200 == 0:
                    print(i)
                r_df_gesture = add_pitch_roll(r_df_gesture)
                # generate the features
                feat = gen_feat(r_df_gesture)

                featDF = pd.DataFrame(feat[1:], columns=feat[0])
                allfeatDF = pd.concat([allfeatDF,featDF])


            outfile = featFolder + "engy_run_pred_features_"+str(i_part)+".csv"
            allfeatDF.to_csv(outfile, index =None)



            # 
            #   build model and dump to pkl
            #   3. from raw data of segments generate features
            # 
            
            # labelfile = './WS/'+train_prtc+'/'+trainsubj+'seg_labels.csv'
            # labelDf = pd.read_csv(labelfile)

            # featfile = './WS/'+train_prtc+'/'+trainsubj+'engy_run_all_subjs_pred_features.csv'
            # df = pd.read_csv(featfile)


            # X = df.iloc[:,:-1].as_matrix()
            # Y = labelDf['label'].iloc[:].as_matrix()

            # classifier = RandomForestClassifier(n_estimators=185)
            # classifier.fit(X, Y)


            # # save the classifier
            # mdlFolder = './WS/'+train_prtc+'/'+trainsubj+'/model/' 
            # if not os.path.exists(mdlFolder):
            #     os.makedirs(mdlFolder)

            # with open(mdlFolder+'RF_185_trainset_motif_segs_thre0.5_run'+str(run)+'.pkl', 'wb') as fid:
            #     cPickle.dump(classifier, fid)    

#             # read in test file features

            testfeatFile = featFolder+ 'engy_run_pred_features.csv'
            df_all = pd.read_csv(testfeatFile)
            print(len(df_all))

# #             labelFile = folder+testsubj + '/segmentation/engy_run'+str(run)+'_pred_label_thre'+threshold_str+'/seg_labels.csv'
# #             labelDf = pd.read_csv(labelFile, names = ['label'])
# #             print(len(labelDf))

            
            mdlFolder = './WS/'+train_prtc+'/'+trainsubj+'/model/' 
            threshold_str = '0.5'

            with open(mdlFolder+'RF_185_trainset_motif_segs_thre'+threshold_str+'_run0.pkl', 'rb') as fid:
                classifier = cPickle.load(fid)
            X = df_all.iloc[:,:-1].as_matrix()
            y_pred = classifier.predict(X)

            y_predDf = pd.DataFrame(data = y_pred, columns = ['label'])
            y_predDf.to_csv(resultfolder + 'pred'+str(i_part)+'.csv', index = None)


            # prec_pos, f1_pos, TPR, FPR, Specificity, MCC, CKappa, w_acc, cm, y_pred = clf_cm_pickle(classifier, X, Y)




#             # 
#             # notice:   duration should not be included in features 
#             #           as in detection period this distinguishable feature will be in different distribution
#             # 
#             X = df_all.iloc[:,:-1].as_matrix()
#             Y = labelDf['label'].as_matrix()
            

#             prec_pos, f1_pos, TPR, FPR, Specificity, MCC, CKappa, w_acc, cm, y_pred = clf_cm_pickle(classifier, X, Y)
#             ts = time.time()
#             current_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')

#             print(current_time)
#             np.savetxt(resultfolder+'RF_185_motif_dist'+str(dist)+'_multi-thre_'+protocol+'_'+subj+'_run'+str(run)+'(109)_cm'+str(current_time)+'.csv', cm, delimiter=",")

#             crossValRes['Prec(pos)'][active_p_cnt] = prec_pos
#             crossValRes['F1(pos)'][active_p_cnt] = f1_pos
#             crossValRes['TPR'][active_p_cnt] = TPR
#             crossValRes['FPR'][active_p_cnt] = FPR
#             crossValRes['Specificity'][active_p_cnt] = Specificity
#             crossValRes['MCC'][active_p_cnt] = MCC
#             crossValRes['CKappa'][active_p_cnt] = CKappa
#             crossValRes['w-acc'][active_p_cnt] = w_acc
#             active_p_cnt = active_p_cnt+1

#         ts = time.time()
#         current_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
#         print(current_time)

#         crossValRes.to_csv( resultfolder+'RF_185_motif_dist'+str(dist)+'_multi-thre_'+protocol+'_'+subj+'_run'+str(run)+'(109)_'+str(current_time)+'.csv', index = None)

        
#         # remove useless data files
#         split_subjs = ['train'+subj,'test'+subj]

#         for split_subj in split_subjs:

#             testsubjfolder = split_subj + '/'
#             folder = '../'+protocol+'/subject/'
#             segfolder = folder+testsubjfolder+"segmentation/"

#             for f in glob.glob(segfolder+'engy_run'+str(run)+'_pred_data/*'):
#                 os.remove(f)