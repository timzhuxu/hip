# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:35:15 2018

@author: zhuxu
"""

from anypytools import AnyPyProcess 
app = AnyPyProcess(num_processes = 1)
from anypytools import AnyMacro
from anypytools.macro_commands import (Load, SetValue, Dump,OperationRun)
from colorama import Back,Style,Fore
import numpy as np
from math import degrees
#%%
def Check_Scaling(Height):
    F_or_L = 'Lower'
    Body_Height = 1.8  
    Mechanical_Output = 5
    Cadence = 5
    Saddle_Height=Height
    Saddle_Pos= -0.25
    Pedal_Arm_Length= 0.2
    Pedal_Arm_Width= 0.107
    macro = [Load('../Application/Examples/BikeModel/BikeModel-'+F_or_L+'Body.main.any'),
              SetValue('Main.HumanModel.Scaling.Scaling.AnthroData.body_height', Body_Height),
              SetValue('Main.BikeParameters.MechOutput', Mechanical_Output),
              SetValue('Main.BikeParameters.Cadence', Cadence),
              SetValue('Main.BikeParameters.SaddleHeight', Saddle_Height),
              SetValue('Main.BikeParameters.SaddlePos', Saddle_Pos),
              SetValue('Main.BikeParameters.PedalArmLength', Pedal_Arm_Length),
              SetValue('Main.BikeParameters.PedalArmWidth', Pedal_Arm_Width)]
    macro.append(OperationRun('Main.Study.InitialConditions'))
    Check_study_macro = AnyMacro(macro)
    Check_results = app.start_macro(Check_study_macro)
    Error_Storage=[]
    for data in Check_results:#checks every result entry
        if 'ERROR' in data:#if there has been an error during the operations, its likely to be an error caused by the scaling fo the bike or the model
            Error_Storage.append(1)
    if len(Error_Storage) == 0:
        return 'OK'
    else:
        return 'Error'

#%%
def Create_Macro(Height): #creates the macro containing the AMS-operations
    F_or_L = 'Lower'
    Body_Height = 1.8
    BW = 96.84
    Fat_Percentage = 31.33
    Mechanical_Output = 5
    Cadence = 5
    Saddle_Height=Height
    Saddle_Pos= -0.26
    Pedal_Arm_Length= 0.2
    Pedal_Arm_Width= 0.107
    macro = [Load('../Application/Examples/BikeModel/BikeModel-'+F_or_L+'Body.main.any'),
              SetValue('Main.HumanModel.Scaling.Scaling.AnthroData.body_height', Body_Height),
              SetValue('Main.BikeParameters.MechOutput', Mechanical_Output),
              SetValue('Main.BikeParameters.Cadence', Cadence),
              SetValue('Main.BikeParameters.SaddleHeight', Saddle_Height),
              SetValue('Main.BikeParameters.SaddlePos', Saddle_Pos),
              SetValue('Main.BikeParameters.PedalArmLength', Pedal_Arm_Length),
              SetValue('Main.BikeParameters.PedalArmWidth', Pedal_Arm_Width)]
    macro.append(SetValue('Main.HumanModel.Scaling.Scaling.AnthroData.Body_Mass', BW))
    macro.append(SetValue('Main.HumanModel.Scaling.Scaling.FatPercent',Fat_Percentage))
    macro.append(OperationRun('Main.RunApplication'))
    macro.append(Dump('Main.Study.Output.Model.HumanModel.Right.Leg.InterfaceFolder.HipJoint_SeqZYX.HipFlexion.Pos'))
    return macro

#%%
def Check_Simulation(Height):
    Check_Result=Check_Scaling(Height)
    if Check_Result== 'OK':
        macro=Create_Macro(Height)
        parameter_study_macro = AnyMacro(macro)
        results = app.start_macro(parameter_study_macro)
        Error_List=[]
        for data in results:
            if 'ERROR' in data:
                print Height
                print(Back.GREEN+Style.BRIGHT+Fore.BLACK+'Simulation Error'+Style.RESET_ALL)
                Error_List.append(1)
                l=len(Error_List)
                return [l]
            else:
                return [0,results]
    else:
        print Height
        print(Back.GREEN+Style.BRIGHT+Fore.BLACK+'Scaling Error'+Style.RESET_ALL)
        return [1]
        
def Find_Height_Start(Height):
    aaa=Check_Simulation(Height)
    while aaa[0] > 0:
        Height= Height + 0.1
        aaa=Check_Simulation(Height)
    return (Height,aaa[1])
#%%
def GetData(results,Key): #creates a list which contains only the data stored under the key of all simulations
    DataList =[] 
    for data in results: 
        DataList.append(data[Key]) 
    return DataList

def Rad_to_Deg(results,Key):#range of motion is in radiant
    RadList = GetData(results,Key)#data in radiant
    DegList=[]
    for i in range(len(RadList)):#for every simulation
        DegElements=[]
        for data in RadList[i]:#for every data in the simulation
            DegElements.append(degrees(data[0]))#the data ist converted into degree (range of motion is stored in a one Element List inside another list therefore the index 0)
        DegList.append(np.asarray(DegElements))
    return DegList

#%%
def Max_Flexion(Height):
    Saddle_Data=Find_Height_Start(Height)
    Height=Saddle_Data[0]
    results=Saddle_Data[1]
    Deg_Flexion = Rad_to_Deg(results,'Main.Study.Output.Model.HumanModel.Right.ShoulderArm.InterfaceFolder.HipJoint_SeqZYX.HipFlexion.Pos')
    Max_Flexion=max(list(Deg_Flexion[0]))
    Abs_Max_Flexion=abs(Max_Flexion)
    return (Height,Abs_Max_Flexion)

def Saddle_Height(Height):
    Flexion=Max_Flexion(Height)
    Height=Flexion[0]
    Max=Flexion[1]
    while Max > 90:
        print Height
        print(Back.GREEN+Style.BRIGHT+Fore.BLACK+'Flexion too big'+Style.RESET_ALL)
        Height=Height + 0.1
        Flexion=Max_Flexion(Height)
        Height=Flexion[0]
        Max=Flexion[1]
       
    return (Height,Max)

sss=Saddle_Height(0)
print(Back.GREEN+Style.BRIGHT+Fore.BLACK+'Saddle_Height successfully found'+Style.RESET_ALL)
print sss
