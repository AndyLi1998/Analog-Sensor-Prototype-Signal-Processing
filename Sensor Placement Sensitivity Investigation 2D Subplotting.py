import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors
from sys import argv

CH1abs=np.array([])
CH1cplx=np.array([])
CH1sth=np.array([])
CH1SNR=np.array([])
CH2abs=np.array([])
CH2cplx=np.array([])
CH2sth=np.array([])
CH2SNR=np.array([])

#read txt file into array 
filename=r'C:\\Users\\andyl\\OneDrive\\Desktop\\Gastops\\Mutibore data analysis\\BalV and SNR.txt'
DatInArr=np.loadtxt(filename,dtype=complex,converters={0:lambda s:complex(s.decode().replace('+-','-'))})

CH1abs=np.append(CH1abs,DatInArr[:,1])
CH1cplx=np.append(CH1cplx,DatInArr[:,2])
CH1sth=np.append(CH1sth,DatInArr[:,3])
CH1SNR=np.append(CH1SNR,DatInArr[:,4])
CH2abs=np.append(CH2abs,DatInArr[:,5])
CH2cplx=np.append(CH2cplx,DatInArr[:,6])
CH2sth=np.append(CH2sth,DatInArr[:,7])
CH2SNR=np.append(CH2SNR,DatInArr[:,8])

SeparationDist=np.linspace(0,6,10)
AxialPlcment=[0,0.125,0.25]
AxialRotat=[0,2.5,5]


#def ROC(yArr,xArr):
 #   n=np.size(yArr)
 #   ROCArr=np.array([])
 #   for i in range(1,n):
 #       ROCArr=np.append(ROCArr,float((yArr[i]-yArr[i-1])/(xArr[i]-xArr[i-1])))
 #   return ROCArr;

#BalV vs. Axial Placement Plot
xAxisAxialPlcment=[0,0.125,0.25]
    #CH1 lines
yAxisBalV11=np.gradient(CH1abs[0:61:30],0.125)
yAxisBalV111=np.gradient(CH1abs[3:64:30],0.125)
yAxisBalV112=np.gradient(CH1abs[6:67:30],0.125)
yAxisBalV113=np.gradient(CH1abs[9:70:30],0.125)

yAxisBalV12=np.gradient(CH1abs[90:151:30],0.125)
yAxisBalV121=np.gradient(CH1abs[93:154:30],0.125)
yAxisBalV122=np.gradient(CH1abs[96:157:30],0.125)
yAxisBalV123=np.gradient(CH1abs[99:160:30],0.125)

yAxisBalV13=np.gradient(CH1abs[180:241:30],0.125)
yAxisBalV131=np.gradient(CH1abs[183:244:30],0.125)
yAxisBalV132=np.gradient(CH1abs[186:247:30],0.125)
yAxisBalV133=np.gradient(CH1abs[189:250:30],0.125)

yAxisBalV21=np.gradient(CH1abs[270:331:30],0.125)
yAxisBalV211=np.gradient(CH1abs[273:334:30],0.125)
yAxisBalV212=np.gradient(CH1abs[276:337:30],0.125)
yAxisBalV213=np.gradient(CH1abs[279:340:30],0.125)

yAxisBalV22=np.gradient(CH1abs[360:421:30],0.125)
yAxisBalV221=np.gradient(CH1abs[363:424:30],0.125)
yAxisBalV222=np.gradient(CH1abs[366:427:30],0.125)
yAxisBalV223=np.gradient(CH1abs[369:430:30],0.125)

yAxisBalV23=np.gradient(CH1abs[450:511:30],0.125)
yAxisBalV231=np.gradient(CH1abs[453:514:30],0.125)
yAxisBalV232=np.gradient(CH1abs[456:517:30],0.125)
yAxisBalV233=np.gradient(CH1abs[459:520:30],0.125)

    #CH2 lines
CH2yAxisBalV11=np.gradient(CH2abs[0:61:30],0.125)
CH2yAxisBalV111=np.gradient(CH2abs[3:64:30],0.125)
CH2yAxisBalV112=np.gradient(CH2abs[6:67:30],0.125)
CH2yAxisBalV113=np.gradient(CH2abs[9:70:30],0.125)

CH2yAxisBalV12=np.gradient(CH2abs[90:151:30],0.125)
CH2yAxisBalV121=np.gradient(CH2abs[93:154:30],0.125)
CH2yAxisBalV122=np.gradient(CH2abs[96:157:30],0.125)
CH2yAxisBalV123=np.gradient(CH2abs[99:160:30],0.125)

CH2yAxisBalV13=np.gradient(CH2abs[180:241:30],0.125)
CH2yAxisBalV131=np.gradient(CH2abs[183:244:30],0.125)
CH2yAxisBalV132=np.gradient(CH2abs[186:247:30],0.125)
CH2yAxisBalV133=np.gradient(CH2abs[189:250:30],0.125)

CH2yAxisBalV21=np.gradient(CH2abs[270:331:30],0.125)
CH2yAxisBalV211=np.gradient(CH2abs[273:334:30],0.125)
CH2yAxisBalV212=np.gradient(CH2abs[276:337:30],0.125)
CH2yAxisBalV213=np.gradient(CH2abs[279:340:30],0.125)

CH2yAxisBalV22=np.gradient(CH2abs[360:421:30],0.125)
CH2yAxisBalV221=np.gradient(CH2abs[363:424:30],0.125)
CH2yAxisBalV222=np.gradient(CH2abs[366:427:30],0.125)
CH2yAxisBalV223=np.gradient(CH2abs[369:430:30],0.125)

CH2yAxisBalV23=np.gradient(CH2abs[450:511:30],0.125)
CH2yAxisBalV231=np.gradient(CH2abs[453:514:30],0.125)
CH2yAxisBalV232=np.gradient(CH2abs[456:517:30],0.125)
CH2yAxisBalV233=np.gradient(CH2abs[459:520:30],0.125)


#xAxisAxialPlcment=['0-0.125','0.125-0.25']
#yAxisBalV11=ROC(CH1abs[0:61:30],AxialPlcment)
#yAxisBalV12=ROC(CH1abs[90:151:30],AxialPlcment)
#yAxisBalV13=ROC(CH1abs[180:241:30],AxialPlcment)
#yAxisBalV21=ROC(CH1abs[270:331:30],AxialPlcment)
#yAxisBalV22=ROC(CH1abs[360:421:30],AxialPlcment)
#yAxisBalV23=ROC(CH1abs[450:511:30],AxialPlcment)

fig, axs=plt.subplots(2,3, sharex=True, sharey=True)

#Subplot[0,0]
#CH1
axs[0, 0].plot(xAxisAxialPlcment, yAxisBalV11/1000,'-x',color='xkcd:midnight blue',label='CH1 @ 0 in. Separation Distance')
#axs[0, 0].plot(xAxisAxialPlcment, yAxisBalV111/1000,'-x',color='xkcd:primary blue',label='CH1 @ 0.6 in. Separation Distance')
#axs[0, 0].plot(xAxisAxialPlcment, yAxisBalV112/1000,'-x',color='xkcd:sky blue',label='CH1 @ 1.2 in. Separation Distance')
axs[0, 0].plot(xAxisAxialPlcment, yAxisBalV113/1000,'-x',color='xkcd:cloudy blue',label='CH1 @ 1.8 in. Separation Distance')
#CH2
axs[0, 0].plot(xAxisAxialPlcment, CH2yAxisBalV11/1000,'-x',color='xkcd:dark red',label='CH2 @ 0 in. Separation Distance')
#axs[0, 0].plot(xAxisAxialPlcment, CH2yAxisBalV111/1000,'-x',color='xkcd:red',label='CH2 @ 0.6 in. Separation Distance')
#axs[0, 0].plot(xAxisAxialPlcment, CH2yAxisBalV112/1000,'-x',color='xkcd:reddish',label='CH2 @ 1.2 in. Separation Distance')
axs[0, 0].plot(xAxisAxialPlcment, CH2yAxisBalV113/1000,'-x',color='xkcd:peachy pink',label='CH2 @ 1.8 in. Separation Distance')
axs[0, 0].set_title('0 degree axial angular rotation')

#Subplot[0,1]
#CH1
axs[0, 1].plot(xAxisAxialPlcment, yAxisBalV12/1000,'-x',color='xkcd:midnight blue')
#axs[0, 1].plot(xAxisAxialPlcment, yAxisBalV121/1000,'-x',color='xkcd:primary blue')
#axs[0, 1].plot(xAxisAxialPlcment, yAxisBalV122/1000,'-x',color='xkcd:sky blue')
axs[0, 1].plot(xAxisAxialPlcment, yAxisBalV123/1000,'-x',color='xkcd:cloudy blue')
#CH2
axs[0, 1].plot(xAxisAxialPlcment, CH2yAxisBalV12/1000,'-x',color='xkcd:dark red')
#axs[0, 1].plot(xAxisAxialPlcment, CH2yAxisBalV121/1000,'-x',color='xkcd:red')
#axs[0, 1].plot(xAxisAxialPlcment, CH2yAxisBalV122/1000,'-x',color='xkcd:reddish')
axs[0, 1].plot(xAxisAxialPlcment, CH2yAxisBalV123/1000,'-x',color='xkcd:peachy pink')
axs[0, 1].set_title('2.5 degree axial angular rotation')

axs[0, 2].plot(xAxisAxialPlcment, yAxisBalV13/1000,'-x',color='xkcd:midnight blue')
#axs[0, 2].plot(xAxisAxialPlcment, yAxisBalV131/1000,'-x',color='xkcd:primary blue')
#axs[0, 2].plot(xAxisAxialPlcment, yAxisBalV132/1000,'-x',color='xkcd:sky blue')
axs[0, 2].plot(xAxisAxialPlcment, yAxisBalV133/1000,'-x',color='xkcd:cloudy blue')
axs[0, 2].plot(xAxisAxialPlcment, CH2yAxisBalV13/1000,'-x',color='xkcd:dark red')
#axs[0, 2].plot(xAxisAxialPlcment, CH2yAxisBalV131/1000,'-x',color='xkcd:red')
#axs[0, 2].plot(xAxisAxialPlcment, CH2yAxisBalV132/1000,'-x',color='xkcd:reddish')
axs[0, 2].plot(xAxisAxialPlcment, CH2yAxisBalV133/1000,'-x',color='xkcd:peachy pink')
axs[0, 2].set_title('5 degree axial angular rotation')

axs[1, 0].plot(xAxisAxialPlcment, yAxisBalV21/1000,'-x',color='xkcd:midnight blue')
#axs[1, 0].plot(xAxisAxialPlcment, yAxisBalV211/1000,'-x',color='xkcd:primary blue')
#axs[1, 0].plot(xAxisAxialPlcment, yAxisBalV212/1000,'-x',color='xkcd:sky blue')
axs[1, 0].plot(xAxisAxialPlcment, yAxisBalV213/1000,'-x',color='xkcd:cloudy blue')
axs[1, 0].plot(xAxisAxialPlcment, CH2yAxisBalV21/1000,'-x',color='xkcd:dark red')
#axs[1, 0].plot(xAxisAxialPlcment, CH2yAxisBalV211/1000,'-x',color='xkcd:red')
#axs[1, 0].plot(xAxisAxialPlcment, CH2yAxisBalV212/1000,'-x',color='xkcd:reddish')
axs[1, 0].plot(xAxisAxialPlcment, CH2yAxisBalV213/1000,'-x',color='xkcd:peachy pink')
axs[1, 0].set_title('reverse direction 0 degree axial angular rotation')

axs[1, 1].plot(xAxisAxialPlcment, yAxisBalV22/1000,'-x',color='xkcd:midnight blue')
#axs[1, 1].plot(xAxisAxialPlcment, yAxisBalV221/1000,'-x',color='xkcd:primary blue')
#axs[1, 1].plot(xAxisAxialPlcment, yAxisBalV222/1000,'-x',color='xkcd:sky blue')
axs[1, 1].plot(xAxisAxialPlcment, yAxisBalV223/1000,'-x',color='xkcd:cloudy blue')
axs[1, 1].plot(xAxisAxialPlcment, CH2yAxisBalV22/1000,'-x',color='xkcd:dark red')
#axs[1, 1].plot(xAxisAxialPlcment, CH2yAxisBalV221/1000,'-x',color='xkcd:red')
#axs[1, 1].plot(xAxisAxialPlcment, CH2yAxisBalV222/1000,'-x',color='xkcd:reddish')
axs[1, 1].plot(xAxisAxialPlcment, CH2yAxisBalV223/1000,'-x',color='xkcd:peachy pink')
axs[1, 1].set_title('reverse direciton 2.5 degree axial angular rotation')

axs[1, 2].plot(xAxisAxialPlcment, yAxisBalV23/1000,'-x',color='xkcd:midnight blue')
#axs[1, 2].plot(xAxisAxialPlcment, yAxisBalV231/1000,'-x',color='xkcd:primary blue')
#axs[1, 2].plot(xAxisAxialPlcment, yAxisBalV232/1000,'-x',color='xkcd:sky blue')
axs[1, 2].plot(xAxisAxialPlcment, yAxisBalV233/1000,'-x',color='xkcd:cloudy blue')
axs[1, 2].plot(xAxisAxialPlcment, CH2yAxisBalV23/1000,'-x',color='xkcd:dark red')
#axs[1, 2].plot(xAxisAxialPlcment, CH2yAxisBalV231/1000,'-x',color='xkcd:red')
#axs[1, 2].plot(xAxisAxialPlcment, CH2yAxisBalV232/1000,'-x',color='xkcd:reddish')
axs[1, 2].plot(xAxisAxialPlcment, CH2yAxisBalV233/1000,'-x',color='xkcd:peachy pink')
axs[1, 2].set_title('reverse direction 5 degree axial angular rotation')

lines = []
labels = []

for ax in axs.flat:
    ax.set(xlabel='Axial Displacement [in.]', ylabel='Rate of Change of Balance Voltage [mV/in.]')
    ax.label_outer()
    axLine, axLabel = ax.get_legend_handles_labels()
    lines.extend(axLine)
    labels.extend(axLabel)
    ax.grid(True)
    
fig.legend(lines, labels,loc = 'right')
plt.suptitle('Rate of Change of Balance Voltage at different Axial Angular Rotation',size=24)

plt.show()