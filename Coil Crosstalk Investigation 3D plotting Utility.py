from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sys import argv


fig = plt.figure()
ax = plt.axes(projection="3d")

CH1abs=np.array([])
CH1cplx=np.array([])
CH1sth=np.array([])
CH1SNR=np.array([])
CH2abs=np.array([])
CH2cplx=np.array([])
CH2sth=np.array([])
CH2SNR=np.array([])

#read txt file into array 
filename=r'BalV and SNR.txt'
DatInArr=np.loadtxt(filename,dtype=complex,converters={0:lambda s:complex(s.decode().replace('+-','-'))})

CH1abs=np.append(CH1abs,DatInArr[:,1])
CH1cplx=np.append(CH1cplx,DatInArr[:,2])
CH1sth=np.append(CH1sth,DatInArr[:,3])
CH1SNR=np.append(CH1SNR,DatInArr[:,4])
CH2abs=np.append(CH2abs,DatInArr[:,5])
CH2cplx=np.append(CH2cplx,DatInArr[:,6])
CH2sth=np.append(CH2sth,DatInArr[:,7])
CH2SNR=np.append(CH2SNR,DatInArr[:,8])

print('----------------------------------Gastops Ltd.---------------------------------\n\nWelcome to Multi-bore Bobbin Crosstalk Investigation 3D Plotting Utility V2000\n\n--------------------------------Author: Andy Li--------------------------------\n\n\n\n')
#define x,y,z axis
for I in range(0,1000):
    Xaxis=int(input("Choose one of the followings as X axis:\n1:    Particle Pull Radial Distance\n2:    Separation Distance\n3:    Axial Placement\n9:    Exit\nEnter your choice:\n\n"))
    print("\n")

    if (Xaxis==9):
        break

    if (Xaxis==1):#x=Particle Pull Radial Distance
    
        Yaxis=int(input("Choose one of the followings as Y axis:\n1:    Separation Distance\n2:    Axial Placement\n3:    Axial Rotation Angle\n9:    Exit\nEnter your choice:\n\n"))
        print("\n")

        if (Yaxis==9):
            break
    
        x=[0,0.5,1]
        xAdd=[0,0.5,1]
        if (Yaxis==1):#y=Separation Distance

            for i in range(0,9):
                x=np.hstack((x,xAdd))
        
            yAdd=0
            for j in range(0,10):
                for k in range(0,3):
                    if (j==0)&(k==0):
                        y=[0]
                    else:
                        y=np.hstack((y,yAdd))
                yAdd=yAdd+0.6

        if (Yaxis==2):#y=Axial Placement

            for i in range(0,2):
                x=np.hstack((x,xAdd))

            yAdd=0
        
            for j in range(0,3):
                for k in range(0,3):
                    if (j==0)&(k==0):
                        y=[0]
                    else:
                        y=np.hstack((y,yAdd))
                yAdd=yAdd+0.125
        
        if (Yaxis==3):#y=Axial Ratation Angle

            for i in range(0,2):
                x=np.hstack((x,xAdd))

            yAdd=0
            for j in range(0,3):
                for k in range(0,3):
                    if (j==0)&(k==0):
                        y=[0]
                    else:
                        y=np.hstack((y,yAdd))
                yAdd=yAdd+2.5


    if (Xaxis==2):#x=Separation Distance

        Yaxis=int(input("Choose one of the followings as Y axis:\n1:    Axial Placement\n2:    Axial Rotation Angle\n9:    Exit\nEnter your choice:\n\n"))
        print("\n")

        if (Yaxis==9):
            break

        x=np.linspace(0,5.4,10)
        xAdd=np.linspace(0,5.4,10)

        for i in range(0,2):
            x=np.hstack((x,xAdd))

            yAdd=0
            for j in range(0,3):
                for k in range(0,10):
                    if (j==0)&(k==0):
                        y=[0]
                    else:
                        y=np.hstack((y,yAdd))
                if (Yaxis==1):#y=Axial Placement
                    yAdd=yAdd+0.125
                if (Yaxis==2):#y=Axial Ratation Angle
                    yAdd=yAdd+2.5


    if (Xaxis==3):#x=Axial Placement
        print("----ATTENTION----\nY-axis:   Axial Roation Angle\nParticle Pull Position:    Center\n")
        SepditChoice=int(input("Select separation distance between two bobbin:\n1:  0in.\n2:  0.6in.\n3:  1.2in.\n4:  1.8in.\n5:  2.4in.\n6:  3in.\n7:  3.6in.\n8:  4.2in.\n9:  4.8in.\n10: 5.4in.\n11:    Exit\nEnter your choice:\n\n"))

        if (SepditChoice==11):
            break
        x=[0,0.125,0.25,0,0.125,0.25,0,0.125,0.25]
        y=[0,0,0,2.5,2.5,2.5,5,5,5]



    #Choose z axis

    SelectedZAxis=np.array([])
    Zaxis=int(input("Choose one of the followings as Z axis:\n1:    Absolute Balance Voltage\n3:    Particle Sensitivity\n4:    SNR\n5:    Rate of Change of Absolute Balance Voltage\n7:    Rate of Change of Particle Sensitivity\n8:    Rate of Change of SNR\n9:    Exit\nEnter your choice:\n\n"))
    print("\n")
    if (Zaxis==9):
        break
    if(Zaxis==1)or(Zaxis==3)or(Zaxis==4):
        SelectedZAxis1=np.append(SelectedZAxis,DatInArr[:,int(Zaxis)])
        SelectedZAxis2=np.append(SelectedZAxis,DatInArr[:,int(Zaxis+4)])
    if(Zaxis==5)or(Zaxis==7)or(Zaxis==8):
        SelectedZAxis1=np.append(SelectedZAxis,DatInArr[:,int(Zaxis-4)])
        SelectedZAxis2=np.append(SelectedZAxis,DatInArr[:,int(Zaxis)])
    
    z1=np.array([])
    z2=np.array([])

    if(Xaxis==1):
        if(Yaxis==1):
            z1=np.absolute(SelectedZAxis1[0:30])
            z2=np.absolute(SelectedZAxis2[0:30])
            if(Zaxis==5)or(Zaxis==7)or(Zaxis==8):
                z1=np.array([])
                z2=np.array([])
                tempArr1a=np.gradient(np.absolute(SelectedZAxis1[0:28:3]),0.6)
                tempArr1b=np.gradient(np.absolute(SelectedZAxis1[1:29:3]),0.6)
                tempArr1c=np.gradient(np.absolute(SelectedZAxis1[2:30:3]),0.6)
                tempArr2a=np.gradient(np.absolute(SelectedZAxis2[0:28:3]),0.6)
                tempArr2b=np.gradient(np.absolute(SelectedZAxis2[1:29:3]),0.6)
                tempArr2c=np.gradient(np.absolute(SelectedZAxis2[2:30:3]),0.6)
                for i in range(0,10):
                    z1=np.append(z1,tempArr1a[i])
                    z1=np.append(z1,tempArr1b[i])
                    z1=np.append(z1,tempArr1c[i])
                    z2=np.append(z2,tempArr2a[i])
                    z2=np.append(z2,tempArr2b[i])
                    z2=np.append(z2,tempArr2c[i])
                    


        if(Yaxis==2):
            for i in range(0,3):
                for j in range(1,4):
                    z1=np.append(z1,np.absolute(SelectedZAxis1[i*30+j]))
                    z2=np.append(z2,np.absolute(SelectedZAxis2[i*30+j]))
            if(Zaxis==5)or(Zaxis==7)or(Zaxis==8):
                z1=np.array([])
                z2=np.array([])
                tempArr1a=np.gradient(np.absolute(SelectedZAxis1[0:61:30]),0.125)
                tempArr1b=np.gradient(np.absolute(SelectedZAxis1[1:62:30]),0.125)
                tempArr1c=np.gradient(np.absolute(SelectedZAxis1[2:63:30]),0.125)
                tempArr2a=np.gradient(np.absolute(SelectedZAxis2[0:61:30]),0.125)
                tempArr2b=np.gradient(np.absolute(SelectedZAxis2[1:62:30]),0.125)
                tempArr2c=np.gradient(np.absolute(SelectedZAxis2[2:63:30]),0.125)
                for i in range(0,3):
                    z1=np.append(z1,tempArr1a[i])
                    z1=np.append(z1,tempArr1b[i])
                    z1=np.append(z1,tempArr1c[i])
                    z2=np.append(z2,tempArr2a[i])
                    z2=np.append(z2,tempArr2b[i])
                    z2=np.append(z2,tempArr2c[i])


        if(Yaxis==3):
            for i in range(0,3):
                for j in range(1,4):
                    z1=np.append(z1,np.absolute(SelectedZAxis1[i*90+j]))
                    z2=np.append(z2,np.absolute(SelectedZAxis2[i*90+j]))
            if(Zaxis==5)or(Zaxis==7)or(Zaxis==8):   
                z1=np.array([])
                z2=np.array([])
                tempArr1a=np.gradient(np.absolute(SelectedZAxis1[0:181:90]),2.5)
                tempArr1b=np.gradient(np.absolute(SelectedZAxis1[1:182:90]),2.5)
                tempArr1c=np.gradient(np.absolute(SelectedZAxis1[2:183:90]),2.5)
                tempArr2a=np.gradient(np.absolute(SelectedZAxis2[0:181:90]),2.5)
                tempArr2b=np.gradient(np.absolute(SelectedZAxis2[1:182:90]),2.5)
                tempArr2c=np.gradient(np.absolute(SelectedZAxis2[2:183:90]),2.5)
                for i in range(0,3):
                    z1=np.append(z1,tempArr1a[i])
                    z1=np.append(z1,tempArr1b[i])
                    z1=np.append(z1,tempArr1c[i])
                    z2=np.append(z2,tempArr2a[i])
                    z2=np.append(z2,tempArr2b[i])
                    z2=np.append(z2,tempArr2c[i])


    if(Xaxis==2):
        if(Yaxis==1):
            for i in range(1,91,3):
                z1=np.append(z1,np.absolute(SelectedZAxis1[i]))
                z2=np.append(z2,np.absolute(SelectedZAxis2[i]))
            if(Zaxis==5)or(Zaxis==7)or(Zaxis==8):
                z1=np.array([])
                z2=np.array([])
                tempArr1a=np.gradient(np.absolute(SelectedZAxis1[0:28:3]),0.6)
                tempArr1b=np.gradient(np.absolute(SelectedZAxis1[30:58:3]),0.6)
                tempArr1c=np.gradient(np.absolute(SelectedZAxis1[60:88:3]),0.6)
                tempArr2a=np.gradient(np.absolute(SelectedZAxis2[0:28:3]),0.6)
                tempArr2b=np.gradient(np.absolute(SelectedZAxis2[30:58:3]),0.6)
                tempArr2c=np.gradient(np.absolute(SelectedZAxis2[60:88:3]),0.6)
                z1=np.hstack((tempArr1a,tempArr1b,tempArr1c))
                z2=np.hstack((tempArr2a,tempArr2b,tempArr2c))

        if(Yaxis==2):
            for i in range(0,3):
                for j in range(0,10):
                    z1=np.append(z1,np.absolute(SelectedZAxis1[i*90+j]))
                    z2=np.append(z2,np.absolute(SelectedZAxis2[i*90+j]))
            if(Zaxis==5)or(Zaxis==7)or(Zaxis==8):   
                z1=np.array([])
                z2=np.array([])
                tempArr1a=np.gradient(np.absolute(SelectedZAxis1[0:28:3]),2.5)
                tempArr1b=np.gradient(np.absolute(SelectedZAxis1[90:118:3]),2.5)
                tempArr1c=np.gradient(np.absolute(SelectedZAxis1[180:208:3]),2.5)
                tempArr2a=np.gradient(np.absolute(SelectedZAxis2[0:28:3]),2.5)
                tempArr2b=np.gradient(np.absolute(SelectedZAxis2[90:118:3]),2.5)
                tempArr2c=np.gradient(np.absolute(SelectedZAxis2[180:208:3]),2.5)
                z1=np.hstack((tempArr1a,tempArr1b,tempArr1c))
                z2=np.hstack((tempArr2a,tempArr2b,tempArr2c))

    if(Xaxis==3):
        for i in range(0,9):
            z1=np.append(z1,np.absolute(SelectedZAxis1[(SepditChoice-1)*3+i*30]))
            z2=np.append(z2,np.absolute(SelectedZAxis2[(SepditChoice-1)*3+i*30]))
        if(Zaxis==5)or(Zaxis==7)or(Zaxis==8):
            Xeql3ROCchoice=int(input("ROC respect to __:\n1:    Axial Placement\n2:    Anxial Angular Rotation\n9:    Exit\n"))   
            if (Xeql3ROCchoice==9):
                break
            z1=np.array([])
            z2=np.array([])
            if(Xeql3ROCchoice==1):
                tempArr1a=np.gradient(np.absolute(SelectedZAxis1[0:61:30]),0.125)
                tempArr1b=np.gradient(np.absolute(SelectedZAxis1[90:151:30]),0.125)
                tempArr1c=np.gradient(np.absolute(SelectedZAxis1[180:241:30]),0.125)
                tempArr2a=np.gradient(np.absolute(SelectedZAxis2[0:61:30]),0.125)
                tempArr2b=np.gradient(np.absolute(SelectedZAxis2[90:151:30]),0.125)
                tempArr2c=np.gradient(np.absolute(SelectedZAxis2[180:241:30]),0.125)
                z1=np.hstack((tempArr1a,tempArr1b,tempArr1c))
                z2=np.hstack((tempArr2a,tempArr2b,tempArr2c))
            if(Xeql3ROCchoice==2):
                tempArr1a=np.gradient(np.absolute(SelectedZAxis1[0:181:90]),2.5)
                tempArr1b=np.gradient(np.absolute(SelectedZAxis1[31:211:90]),2.5)
                tempArr1c=np.gradient(np.absolute(SelectedZAxis1[61:241:90]),2.5)
                tempArr2a=np.gradient(np.absolute(SelectedZAxis2[0:181:90]),2.5)
                tempArr2b=np.gradient(np.absolute(SelectedZAxis2[31:211:90]),2.5)
                tempArr2c=np.gradient(np.absolute(SelectedZAxis2[61:241:90]),2.5)
                for i in range(0,3):
                    z1=np.append(z1,tempArr1a[i])
                    z1=np.append(z1,tempArr1b[i])
                    z1=np.append(z1,tempArr1c[i])
                    z2=np.append(z2,tempArr2a[i])
                    z2=np.append(z2,tempArr2b[i])
                    z2=np.append(z2,tempArr2c[i])
        
        
        

    ax = plt.axes(projection='3d')
    ax.scatter(x,y,z1,color="red")
    surf1=ax.plot_trisurf(x, y, z1, cmap='Reds', linewidth=0.1)

    ax.scatter(x,y,z2,color="blue")
    surf2=ax.plot_trisurf(x, y, z2, cmap='Blues', linewidth=0.1)
    #fig.colorbar(surf, shrink=0.5, aspect=5)

    #label x,y,z axis
    if(Xaxis==1):
        ax.set_xlabel('Partical Pull Radial Distance',fontweight ='bold')
        if(Yaxis==1):
            ax.set_ylabel('Separation Distance [in.]',fontweight ='bold')
            if(Zaxis==5):
                ax.set_zlabel('Rate of Change of Absolute Balance Voltage respect to Separation Distance [uV/in.]',fontweight ='bold')
            if(Zaxis==7):
                ax.set_zlabel('Rate of Change of Signal Stength respect to Separation Distance [uV/in.]',fontweight ='bold')
            if(Zaxis==8):
                ax.set_zlabel('Rate of Change of SNR respect to Separation Distance [per in.]',fontweight ='bold')
        if(Yaxis==2):
            ax.set_ylabel('Axial Placement [in.]',fontweight ='bold')
            if(Zaxis==5):
                ax.set_zlabel('Rate of Change of Absolute Balance Voltage respect to Axial Placement [uV/in.]',fontweight ='bold')
            if(Zaxis==7):
                ax.set_zlabel('Rate of Change of Signal Stength respect to Axial Placement [uV/in.]',fontweight ='bold')
            if(Zaxis==8):
                ax.set_zlabel('Rate of Change of SNR respect to Axial Placement [per in.]',fontweight ='bold')
        if(Yaxis==3):
            ax.set_ylabel('Axial Angular Rotation [degree]',fontweight ='bold')
            if(Zaxis==5):
                ax.set_zlabel('Rate of Change of Absolute Balance Voltage respect to Axial Angular Rotation [uV/degree]',fontweight ='bold')
            if(Zaxis==7):
                ax.set_zlabel('Rate of Change of Signal Stength respect to Axial Angular Rotation [uV/degree]',fontweight ='bold')
            if(Zaxis==8):
                ax.set_zlabel('Rate of Change of SNR respect to Axial Angular Rotation [per degree]',fontweight ='bold')

    if(Xaxis==2):
        ax.set_xlabel('Separation Distance [in.]',fontweight ='bold')
        if(Yaxis==1):
            ax.set_ylabel('Axial Placement [in.]',fontweight ='bold')
        if(Yaxis==2):
            ax.set_ylabel('Axial Angular Rotation [degree]',fontweight ='bold')
        if(Zaxis==5):
            ax.set_zlabel('Rate of Change of Absolute Balance Voltage respect to Separation Distance [uV/in.]',fontweight ='bold')
        if(Zaxis==7):
            ax.set_zlabel('Rate of Change of Signal Stength respect to Separation Distance [uV/in.]',fontweight ='bold')
        if(Zaxis==8):
            ax.set_zlabel('Rate of Change of SNR respect to Separation Distance [per in.]',fontweight ='bold')

    if(Xaxis==3):
        ax.set_xlabel('Axial Placement [in.]',fontweight ='bold')
        ax.set_ylabel('Axial Angular Rotation [degree]',fontweight ='bold')
        if(Zaxis==5):
            if(Xeql3ROCchoice==1):
                ax.set_zlabel('Rate of Change of Absolute Balance Voltage respect to Axial Placement [uV/in.]',fontweight ='bold')
            if(Xeql3ROCchoice==2):
                ax.set_zlabel('Rate of Change of Absolute Balance Voltage respect to Axial Angular Rotation [uV/degree]',fontweight ='bold')
        if(Zaxis==7):
            if(Xeql3ROCchoice==1):
                ax.set_zlabel('Rate of Change of Signal Stength respect to Axial Placement [uV/in.]',fontweight ='bold')
            if(Xeql3ROCchoice==2):
                ax.set_zlabel('Rate of Change of Signal Stength respect to Axial Angular Rotation [uV/degree]',fontweight ='bold')
        if(Zaxis==8):
            if(Xeql3ROCchoice==1):
                ax.set_zlabel('Rate of Change of SNR respect to Axial Placement [per in.]',fontweight ='bold')
            if(Xeql3ROCchoice==2):
                ax.set_zlabel('Rate of Change of SNR respect to Axial Angular Rotation [per degree]',fontweight ='bold')
        

        
    if(Zaxis==1):
        ax.set_zlabel('Absolute Balance Voltage [uV]',fontweight ='bold')
    if(Zaxis==3):
        ax.set_zlabel('Signal Stength [uV]',fontweight ='bold')
    if(Zaxis==4):
        ax.set_zlabel('SNR',fontweight ='bold')
    
        
    plt.show()
    print('___________________________End of Plot '+str(I+1)+'_____________________________\n')