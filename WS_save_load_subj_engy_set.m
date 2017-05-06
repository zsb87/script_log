function [sig_cell, gt_htcell] = WS_save_load_subj_engy_set(subj,n_file, config_file)

for i_part = 1:n_file
    %% Evaluate global configuration file
    try
        eval(config_file);
    catch
        disp('config file!');
    end
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %
    % save all activities' ground truth in 'gt_feeding_headtail.csv'
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    sigfolder = [folder, subj,'/feature/energy/engy_ori_win4_str2_len2100_overlap100/'];
    sigfile = ['engy_ori_win', num2str(win), '_str2_', num2str(i_part),'.csv'];
    n = csvread(strcat(sigfolder,sigfile),1,1);
%     [n,s,r] = xlsread(strcat(sigfolder,sigfile));
    
    fClass = n(:,engy_fCol);
    
    sig_cell{1,i_part} = n(:,engy_engyfCol);
    
    gtHtFolder = [folder, subj,'/segmentation/engy_gt/engy_ori_win4_str2_len2100_overlap100/'];
    if ~exist(gtHtFolder, 'dir')    mkdir(gtHtFolder),   end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % save all activities' ground truth in one file
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    gt_headtail = pointwise2headtail(fClass);
    save_headtail(gt_headtail, strcat(gtHtFolder,'gt_feeding_headtail_',num2str(i_part),'.csv'));
    gt_htcell{1,i_part} = csvread(strcat(gtHtFolder,'gt_feeding_headtail_',num2str(i_part),'.csv'));% it has (n,3) shape now
 
    end
    
end
