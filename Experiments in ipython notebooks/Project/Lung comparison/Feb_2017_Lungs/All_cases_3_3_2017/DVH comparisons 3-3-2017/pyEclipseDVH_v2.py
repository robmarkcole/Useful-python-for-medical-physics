import numpy as np
import pandas as pd
from scipy import interpolate
import os

def List_txt():
    files = os.listdir()   # return a list of files
    return [file for file in files if file.endswith('.txt')]

def Load_patient(file):  # file = 'Case1_AAA.txt'  string
    with open(file, "r") as file_:
        my_file = [line for line in file_.readlines()]  # my_file is a list representation of the text file
    file_.close()        
    file_len = len(my_file)                                # number of lines in the file
    patID = my_file[1].split(':')[-1].strip('\n').strip()
    planID = my_file[10].split(':')[-1].strip('\n').strip()
    
        
    ## Get the structures
    structures_indexs_list = []
    structures_names_list  = []
    for i, line in enumerate(my_file):
        if line.startswith('Structure:'):
            structures_indexs_list.append(i)  
            structures_names_list.append(line.split(':')[-1].strip('\n').strip())
    
    
    ##structures_names_list = ['PTV CHEST', 'Foramen'] # hard code to limit number of structures and prevent memory issues
    
    print(file + ' loaded \t patID:' + patID + ' PlanID:' + planID + ' and number of structures is ' + str(len(structures_names_list)))
    dose_index = np.linspace(0,100, 2001)  # New dose index in range 0 - 100 Gy in 0.05 Gy steps
    
    data = np.zeros((dose_index.shape[0], len(structures_names_list)))
    
    # iterate through all structures and place interpolated DVH data in matrix
    for i, index in enumerate(structures_indexs_list):
        start = structures_indexs_list[i]+18  # first line of DVH data
        if i < len(structures_indexs_list)-1:
            end = structures_indexs_list[i+1]-2  # find the last line of the DVH from the next index, BEWARE THE +1
        else:
            end = len(my_file)-2
        DVH_data = my_file[start:end]  # get list with data
            
        DVH_list = [line.split() for line in DVH_data]  # create list of lists split
        Rel_dose_pct, Dose_Gy, Ratio_pct = zip(*DVH_list) # unzip to 3 lists, they are strings so conver to float
        
        Ratio_pct = np.asarray(Ratio_pct, dtype=np.float32)
        Dose_Gy = np.asarray(Dose_Gy, dtype=np.float32)
        ## Now working with dose data
      
        f = interpolate.interp1d(x=Dose_Gy,y=Ratio_pct, bounds_error=False, fill_value=0)   # returns a linear interpolate function, fill values outside range wiwth 0 

        data[:,i] = f(dose_index)
    
    my_iterables = [[patID], [planID], structures_names_list]
    my_index = pd.MultiIndex.from_product(my_iterables, names = ['patID', 'planID', 'Structure'])

    df = pd.DataFrame(data.T, index = my_index)
    df = df.T
    df.index  = dose_index
    df.index.name = 'Dose (Gy)'
    return df
	
def Load_files_to_df(files_list):    # pass a list of files to load into a df
    for i, file in enumerate(files_list):
        if i == 0:
            multi_df = Load_patient(file)        
        else:
            multi_df = pd.concat([multi_df, Load_patient(file)], axis=1)
    return multi_df
	
def get_dmin(df):
    return df[(df < 100.0) & (df > 0.0)].idxmax() 
	
def get_dmax(df):
    return df[(df < 100.0) & (df > 0.0)].idxmin() 
	
def get_d_metric(df, D_metric_pct):                 # dunction to get e.g the D50% metric passing '50' and a DVH entry ()
    x = df.values
    y = df.index.values
    f = interpolate.interp1d(x,y, bounds_error=False, fill_value=0)
    return f(D_metric_pct)*1    # adding the *1 turns it from an array to a double..