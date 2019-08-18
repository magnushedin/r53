## Clear the workspace
clear
close all

## Load data
load oem_ignition_mapping

## Defines
TPS_filter_limit = 20
Ign_Adv_filter_limit = 10
xx = [50:5:200];

## Filters
filter_2000=abs(data.RPM - 2000) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_2500=abs(data.RPM - 2500) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_3000=abs(data.RPM - 3000) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_3500=abs(data.RPM - 3500) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_4000=abs(data.RPM - 4000) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_4500=abs(data.RPM - 4500) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_5000=abs(data.RPM - 5000) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_5500=abs(data.RPM - 5500) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;
filter_6000=abs(data.RPM - 6000) < 100 & data.TPS > TPS_filter_limit & data.Ign_Adv > Ign_Adv_filter_limit;

## Spline Function calculations
sf_2000 = splinefit(data.Intk_Mani_Press(filter_2000), data.Ign_Adv(filter_2000), 1)
sf_2500 = splinefit(data.Intk_Mani_Press(filter_2500), data.Ign_Adv(filter_2500), 1)
sf_3000 = splinefit(data.Intk_Mani_Press(filter_3000), data.Ign_Adv(filter_3000), 1)
sf_3500 = splinefit(data.Intk_Mani_Press(filter_3500), data.Ign_Adv(filter_3500), 1)
sf_4000 = splinefit(data.Intk_Mani_Press(filter_4000), data.Ign_Adv(filter_4000), 1)
sf_4500 = splinefit(data.Intk_Mani_Press(filter_4500), data.Ign_Adv(filter_4500), 1)
sf_5000 = splinefit(data.Intk_Mani_Press(filter_5000), data.Ign_Adv(filter_5000), 1)

## Curvefitted for data plot
sy_2000 = ppval(sf_2000, xx)
sy_2500 = ppval(sf_2500, xx)
sy_3000 = ppval(sf_3000, xx)
sy_3500 = ppval(sf_3500, xx)
sy_4000 = ppval(sf_4000, xx)
sy_4500 = ppval(sf_4500, xx)
sy_5000 = ppval(sf_5000, xx)

## Plot data and curvefitting
figure()
hold on
plot(data.Intk_Mani_Press(filter_2000), data.Ign_Adv(filter_2000), 'k*')
plot(data.Intk_Mani_Press(filter_2500), data.Ign_Adv(filter_2500), 'k*')
plot(data.Intk_Mani_Press(filter_3000), data.Ign_Adv(filter_3000), 'r*')
plot(data.Intk_Mani_Press(filter_3500), data.Ign_Adv(filter_3500), 'ro')
plot(data.Intk_Mani_Press(filter_4000), data.Ign_Adv(filter_4000), 'm*')
plot(data.Intk_Mani_Press(filter_4500), data.Ign_Adv(filter_4500), 'mo')
plot(data.Intk_Mani_Press(filter_5000), data.Ign_Adv(filter_5000), 'g*')
plot(xx, sy_2000, 'k-')
plot(xx, sy_2500, 'k-')
plot(xx, sy_3000, 'r-')
plot(xx, sy_3500, 'r-')
plot(xx, sy_4000, 'm-')
plot(xx, sy_4500, 'm-')
plot(xx, sy_5000, 'g-')
legend('2','2.5','3','3.4','4','4.5','5')


## Caluclate Ignition Map
## Setup axis and surface
axis_RPM = [2000:500:5000];
axis_MAP = [25 30 35 40 60 80 100 113 127 140 153 167 180 193 207 220];
surf_ign = zeros(length(axis_RPM),length(axis_MAP));

## Caluclate the data
surf_ign(1,:) = ppval(sf_2000, axis_MAP);
surf_ign(2,:) = ppval(sf_2500, axis_MAP);
surf_ign(3,:) = ppval(sf_3000, axis_MAP);
surf_ign(4,:) = ppval(sf_3500, axis_MAP);
surf_ign(5,:) = ppval(sf_4000, axis_MAP);
surf_ign(6,:) = ppval(sf_4500, axis_MAP);
surf_ign(7,:) = ppval(sf_5000, axis_MAP);


##Plot the Ignition Map
figure()
mesh(axis_MAP, axis_RPM, surf_ign)


%figure()
%plot(data.TPS(filter_2000), data.Ign_Adv(filter_2000), '*')
%hold on
%plot(data.TPS(filter_3000), data.Ign_Adv(filter_3000), 'r*')
%plot(data.TPS(filter_4000), data.Ign_Adv(filter_4000), 'm*')
%plot(data.TPS(filter_5000), data.Ign_Adv(filter_5000), 'g*')