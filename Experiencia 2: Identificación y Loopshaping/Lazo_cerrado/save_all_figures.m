function save_all_figures(dir_name, prefix)
    if nargin < 2
        prefix = 'figure';
    end
    figlist=findobj('type','figure');
    for i=1:numel(figlist)
        saveas(figlist(i),fullfile(dir_name,[prefix, num2str(figlist(i).Number) '.png']));
    end
    disp('Save successfull');
end
