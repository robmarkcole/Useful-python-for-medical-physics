import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class eclipse_DVH(object): 
    def __init__(self, file):  # file = 'Case1_AAA.txt'  string
        with open(file, "r") as file_:
            my_file = [line for line in file_.readlines()]  # my_file is a list representation of the text file
        file_.close()        
        self.file_len = len(my_file)                                # number of lines in the file
        self.patID = my_file[1].split(':')[-1].strip('\n').strip()
        self.prescription = my_file[13].split(':')[-1].strip('\n').strip()
        print(file + ' loaded \t patID = ' + self.patID + '\t Prescription [Gy] = ' + self.prescription)
        
        ## Get the structures
        self.structures_indexs_list = []
        self.structures_names_list  = []
        for i, line in enumerate(my_file):
            if line.startswith('Structure:'):
                self.structures_indexs_list.append(i)  
                self.structures_names_list.append(line.split(':')[-1].strip('\n').strip())
        
        # iterate through all structures and place Eclipse metrics into dataframe
        for i, index in enumerate(self.structures_indexs_list):
            # Metrics first
            metric_list = []
            value_list = []   
        
            for line in my_file[index:index+13]:     # get 'header' of each structure
                metric_list.append(line.split(':')[0])
                value_list.append(line.split(':')[-1:][0].strip('\n').strip())    
            
            # Now DVH
            start = self.structures_indexs_list[i]+18  # first line of DVH data
            if i < len(self.structures_indexs_list)-1:
                end = self.structures_indexs_list[i+1]-2  # find the last line of the DVH from the next index, BEWARE THE +1
            else:
                end = len(my_file)-2
            DVH_data = my_file[start:end]  # get list with data
            
            DVH_list = [line.split() for line in DVH_data]  # create list of lists split
            Rel_dose_pct, Dose_Gy, Ratio_pct = zip(*DVH_list) # unzip to 3 lists
            
            # Populate temp dataframes
            temp_metric_df = pd.DataFrame({'Metric' : metric_list, self.structures_names_list[i]: value_list})
            temp_DVH_df    = pd.DataFrame({'Dose_Gy' : Dose_Gy, self.structures_names_list[i]: Ratio_pct}).astype(float)
            if i == 0: 
                self.metrics_df = temp_metric_df 
                self.DVH_df = temp_DVH_df
            else:                          
                self.metrics_df = pd.merge(left = self.metrics_df, right=temp_metric_df, how='inner', on=['Metric'])
                self.DVH_df = pd.merge(self.DVH_df, temp_DVH_df, on=['Dose_Gy'])
        
        # Tidy up
        self.DVH_df.set_index(keys='Dose_Gy', drop=True, inplace=True)            
        self.metrics_df.set_index(keys='Metric', inplace=True)  # write to self