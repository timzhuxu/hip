# -*- coding: utf-8 -*-
from anypytools import AnyPyProcess
from Modules.MainFunctions import Start_Simulation
#%%
#####################Inital-Definitionen#############################

app = AnyPyProcess(num_processes = 2, anybodycon_path ='C:\Program Files\AnyBody Technology\AnyBody.7.0\AnyBody.exe',logfile_prefix='LogFiles/' )

##############Ende Inital-Definitionen################
#%%
Config = {
"Full_or_Lower_BodyModel":'Lower',
#Model Data
"Body_Height": 1.8, #Height in m 
"Body_Weight": 96.84,#Weight in kg
"Fat_Percentage":31.33,#Fat in percent

#Mechanical Output List Definition
"Mechanical_Output_Start_Value":60, #Lowest MechOutput avlue to be set - Integer or Float
"Mechanical_Output_Step_Value":20, #Steps between the different values - Integer or Float
"Mechanical_Output_Num_of_Elements":1, #Number of values to be set - Integer or Float

#Cadence List Definitions
"Cadence_Start_Value":40, #Lowest Cadence value to be set - Integer or Float
"Cadence_Step_Value":20, #Steps between the different Values - Integer or Float
"Cadence_Num_of_Elements":3, #Numbers of values to be set - Integer or Float

#Saddle Height List Definition
"Saddle_Height_Start_Value":0.7, #Lowest SaddleHeight value to be set -Integer or Float
"Saddle_Height_Step_Value":0.01, #Steps between the different values - Integer or Float
"Saddle_Height_Num_of_Elements":1, #Number of values to be set - Integer or Float

#Saddle Pos List Definition
"Saddle_Pos_Start_Value":-0.25, #Lowest SaddlePos value to be set - Integer or FLoat
"Saddle_Pos_Step_Value":0.01, #Steps between the different values - Integer or Float
"Saddle_Pos_Num_of_Elements":1, #Numbers of values to be set - Integer or Float

#Crank Length List Definition
"Pedal_Arm_Length_Start_Value":0.2, #Lowest PedalArmLength value to be set - Integer or Float
"Pedal_Arm_Length_Step_Value":0.01, #Steps between the different values - Integer or Float
"Pedal_Arm_Length_Num_of_Elements":1, #Number of values to be set - Integer or Float

#Crank Width List Definitions
"Pedal_Arm_Width_Start_Value":0.11, #Lowest PedalArmWidth value to be set - Integer or Float
"Pedal_Arm_Width_Step_Value":0.01, #Steps between the different values - Integer or Float
"Pedal_Arm_Width_Num_of_Elements":1, #Numbers of values to be set - Integer or Float

#####Output Definition#######
#Which data should be dumped?
"Dump_Left_or_Right":'Right', #Left leg or Right leg - Left or Right
"Delete_old_Output_CSV_H5PY?":'no',

"Dump_HipForce":'no', # yes or no
"Dump_HipMoment":'no', # yes or no
"Dump_Range_of_Motion":'no', # yes or no

"Dump_Adduktor_Muscle_Activity":'no',# yes or no
"Dump_Adductor_Length":'no',# yes or no
"Dump_Gluteus_Muscle_Activity":'no',# yes or no
"Dump_Gluteus_Length":'no',
"Dump_Iliopsoas_Muscle_Activity":'no',# yes or no
"Dump_Iliopsoas_Length":'no',# yes or no
"Dump_Ischiokrural_Muscle_Activity":'no',# yes or no
"Dump_Ischiokrural_Length":'no',# yes or no
"Dump_SartoriusRectus_Muscle_Activity":'no',# yes or no
"Dump_SartoriusRectus_Length":'no',# yes or no
"Dump_ExternalRot_Muscle_Activity":'no',# yes or no
"Dump_ExternalRot_Length":'no'# yes or no
}

zhuxu
#%%
results = Start_Simulation(Config,app)
