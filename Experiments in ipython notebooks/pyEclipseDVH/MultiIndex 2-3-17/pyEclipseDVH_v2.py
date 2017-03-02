import numpy as np
import pandas as pd
from scipy import interpolate

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
    
    my_iterables = [[patID], ['AAA'], structures_names_list]
    my_index = pd.MultiIndex.from_product(my_iterables, names = ['Patient ID', 'Plan ID', 'Structure'])

    df = pd.DataFrame(data.T, index = my_index)
    df = df.T
    df.index  = dose_index
    df.index.name = 'Dose (Gy)'
    return df