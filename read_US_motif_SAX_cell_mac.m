function SAX_cell = read_US_motif_SAX_cell_mac(folder)    

    for i = 1:17
        fname = strcat(['motif_SAX',num2str(i),'.csv']);
%         disp(strcat(folder, fname));
        SAX_cell{1,i} = csvread(strcat(folder, fname));
    end
end
