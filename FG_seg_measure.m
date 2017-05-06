%
%   UNSTRUCTURED
%
% Input:
% Output:
% save file:

function [seg_label_cell, recall] = FG_seg_measure(test_pred_htcell, test_gt_htcell, meas_thres, config_file)
    %% Evaluate global configuration file
    try
        eval(config_file);
    catch
        disp('config file seg_measure');
    end
    
    gt_det_cell = []; 
    
    gt_all_detected_flg = [];
    
    %% --------------------------------------------------------------------
    %  read all pred results in cell
    %  --------------------------------------------------------------------
    % read ground truth for all activities in one file
    for i = 1:size(test_gt_htcell,2)
        % when there is no ground truth feeding gesture, no need to compare
        % the truth for the segments are all 0
        if test_gt_htcell{i} == 0
            seg_label_cell{i} = zeros(size(test_pred_htcell{i},1),1);
        else
        gt_act = test_gt_htcell{i};  gt_act = gt_act(:,1:2);
        pred_act = test_pred_htcell{i}(:,1:2);  
        
        %% --------------------------------------------------------------------
        %  core function
        %  --------------------------------------------------------------------
        pred_act = sortrows(pred_act);
        [gt_det_cell{i}, seg_label_cell{i}] = eventBasedEvaluate(pred_act, gt_act,meas_thres);
        gt_all_detected_flg = [gt_all_detected_flg ;gt_det_cell{i}];
        end
    end
    
    recall = sum(gt_all_detected_flg)/length(gt_all_detected_flg);
end 

