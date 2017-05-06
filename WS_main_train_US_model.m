function WS_main_train_US_model(subj)

motif_file = '../inlabUnstr/subject/all/mset2/motifs/';
config_file ='WS_config_file_us_build_model';
protocol = 'inlabUnstr';

run = 2017050602;

try
    eval(config_file);
catch
    disp('config file!_main')
end


if strcmp(subj, 'P1')
    n_file = 5;
end
if strcmp(subj, 'P3')
    n_file = 23;
end
if strcmp(subj, 'P6')
    n_file = 39;
end
if strcmp(subj, 'P7')
    n_file = 30;
end
if strcmp(subj, 'P8')
    n_file = 35;
end

[sig_cell, gt_htcell] = FG_save_load_subj_engy_set(subj, n_file, config_file);

[motif_SAX_cell] = read_US_motif_SAX_cell_mac(motif_file);

std_thres = 0.01;
dist_thres = 0.7;
[pred_htcell, num_pred] = FG_seg_engy_detect_save(subj, motif_SAX_cell, sig_cell, std_thres, dist_thres, run, config_file);  

meas_thres = 0.5;                
[seg_label_cell, recall] = FG_seg_measure(pred_htcell, gt_htcell, meas_thres, config_file);

for n= 1:size(seg_label_cell,2)  
    folder = ['../',protocol,'/subject/',subj,'/segmentation/engy_run',num2str(run),'_pred_label_thre',num2str(meas_thres)];
    if ~exist(folder,'dir') mkdir(folder), end   
    csvwrite([folder,'/seg_labels_',num2str(n),'.csv'],seg_label_cell{1,n});
end
disp(recall);