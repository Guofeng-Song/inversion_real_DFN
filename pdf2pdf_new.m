clear all
clc
%path='E:\standford_paper\general_distribution\general\OutputSimulation1'
%path_pdfnew='E:\standford_paper\general_distribution\general\OutputSimulation1\pdf_new'
%define the cell to save all results for 20 seeds
 
for m=1:1:20
    stri_test=['I:\stanford_research\standford_paper\general_distribution\paper\corre_new\fracture_inversion_with_particle_tracers&FCNN\generate_source\example\OutputSimulation',num2str(m)]
    
    path_pdfnew=fullfile(stri_test,'\pdfnew\')
    path=fullfile(stri_test,'\pdf\')
    FileList = dir(strcat(path,'*txt'));
    N = size(FileList,1);
    for k = 1:N
        %get the file name:
        filename = FileList(k).name;
        disp(filename);
        A=isstrprop(filename,'digit');
        B=filename(A);
        z=zeros(99,2);
        x=load([path filename]);
        for i=1:1:99
            z(i,1)=x(i,1);
            z(i,2)=(x(i+1,1)-x(i,1))*x(i,2);
        end
     save(['I:\stanford_research\standford_paper\general_distribution\paper\corre_new\fracture_inversion_with_particle_tracers&FCNN\generate_source\example\OutputSimulation',num2str(m),'\pdfnew\pdf',B,'.txt'],'z','-ascii');  
    end
    
end

