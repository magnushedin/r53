clear
close all
load("ignition")


l = size(ign_Master)(1);
for i=1:1:(l)
  #ign_Master_new(:,l-i+1) = ign_Master(:,i);
  ign_Master_new(l-i+1,:) = ign_Master(i,:);
end

surf(rpm_Link, MAP_Link, ign_Link)
figure
surf(rpm_Master, MAP_Master, ign_Master_new')

