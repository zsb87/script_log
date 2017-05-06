import pandas as pd
import numpy as np
import os

testsubjfolders = ['P10', 'P12', 'P18', 'P24']


for testsubjfolder in testsubjfolders:
	engyfile = './WS/Field/'+testsubjfolder+'/engy_ori_win4_str2.csv' # testsubjfolder is 'P10/'
	datafile = './WS/Field/'+testsubjfolder+'/testdata.csv'

	engyDf = pd.read_csv(engyfile)
	dataDf = pd.read_csv(datafile)

	fcount = -(-(len(engyDf)-100) // 2000)

	if not os.path.exists('./WS/Field/'+testsubjfolder+'/engy_ori_win4_str2_len2100_overlap100/'):
	    os.makedirs('./WS/Field/'+testsubjfolder+'/engy_ori_win4_str2_len2100_overlap100/')

	for i in range(fcount-1):
	    engyDfPart = engyDf.iloc[i*2000:i*2000+2100]
	    engyDfPart.to_csv('./WS/Field/'+testsubjfolder+'/engy_ori_win4_str2_len2100_overlap100/engy_ori_win4_str2_'+str(i+1)+'.csv',index = None)

	engyDfPart = engyDf.iloc[(fcount-1)*2000:]
	engyDfPart.to_csv('./WS/Field/'+testsubjfolder+'/engy_ori_win4_str2_len2100_overlap100/engy_ori_win4_str2_'+str(fcount)+'.csv',index = None)

	if not os.path.exists('./WS/Field/'+testsubjfolder+'/testdata_len4200_overlap200/'):
	    os.makedirs('./WS/Field/'+testsubjfolder+'/testdata_len4200_overlap200/')

	for i in range(fcount-1):
	    dataDfPart = dataDf.iloc[i*4000:i*4000+4200]
	    dataDfPart.to_csv('./WS/Field/'+testsubjfolder+'/testdata_len4200_overlap200/testdata_'+str(i+1)+'.csv',index = None)

	dataDfPart = dataDf.iloc[(fcount-1)*4000:]
	dataDfPart.to_csv('./WS/Field/'+testsubjfolder+'/testdata_len4200_overlap200/testdata_'+str(fcount)+'.csv',index = None)