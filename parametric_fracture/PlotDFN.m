% plot the fracture network
clear
clf
file_name='xxx\OutputSimulation201\dfn\DFN9.txt';

Lx=10;Ly=10;

values=load(file_name);
x_fract1=values(:,1);
y_fract1=values(:,2);
x_fract2=values(:,3);
y_fract2=values(:,4);

figure(1)
hold on 
for i=1:1:length(x_fract1)
    h=patch([x_fract1(i) x_fract2(i)]',[y_fract1(i) y_fract2(i)]','k','LineWidth',2);
end

axis equal;
axis([-Lx/2 Lx/2 -Ly/2 Ly/2]);
%axis off;
%axis fill;
box on
set(gca,'xtick',[]);set(gca,'ytick',[])
hold off 