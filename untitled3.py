# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:35:15 2018

@author: zhuxu
"""
from anypytools import AnyPyProcess 
app = AnyPyProcess(num_processes = 1)
from anypytools import AnyMacro
from anypytools.macro_commands import (Load, SetValue, OperationRun)
from colorama import Back,Style,Fore

#%%
def Macro_Result(Height):
    results=Check_Scaling_Macro(Height)
    Error_List=[]
    for data in results:
        if 'ERROR' in data:
            Error_List.append(1)
            l=len(Error_List)
            return l
        
def Find_Start(Height):
    aaa = Macro_Result(Height)
    while aaa > 0:
        Height = Height + 0.2
        aaa = Macro_Result(Height)
    print(Back.GREEN+Style.BRIGHT+Fore.BLACK+'Saddle_Height_Start_Value'+Style.RESET_ALL)
    print Height        
sss=Find_Start(0)     
#%%
def Check_Scaling_Macro(Height):
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
    macro.append(OperationRun('Main.Study.InitialConditions'))
    Check_study_macro = AnyMacro(macro)
    Check_results = app.start_macro(Check_study_macro)
    Error_Storage=[]
    for data in Check_results:#checks every result entry
        if 'ERROR' in data:#if there has been an error during the operations, its likely to be an error caused by the scaling fo the bike or the model
            Error_Storage.append(1)
    if len(Error_Storage) == 0:
        macro.append(SetValue('Main.HumanModel.Scaling.Scaling.AnthroData.Body_Mass', BW))
        macro.append(SetValue('Main.HumanModel.Scaling.Scaling.FatPercent',Fat_Percentage))
        macro.remove(OperationRun('Main.Study.InitialConditions'))
        macro.append(OperationRun('Main.RunApplication'))
        parameter_study_macro = AnyMacro(macro)
        results = app.start_macro(parameter_study_macro)
        return results
    else:#if there are not no errors = there are erros
        print(Back.BLACK+Fore.WHITE+Style.BRIGHT+'Scaling Error!'+Style.RESET_ALL)
        print(str(len(Error_Storage))+' Errors occured')#prints the number of scaling errors
        #it is possible, that the error was caused by an licence error. Running the script twice or thrice may solve it    
    return results  

