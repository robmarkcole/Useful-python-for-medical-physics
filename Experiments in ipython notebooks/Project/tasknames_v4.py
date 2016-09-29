#import sys
import os
from difflib import SequenceMatcher

dire=os.getcwd();#current directory
files=os.listdir(dire);#list all archives
#lets take only the .txt
file_list=[];
organs=['BODY',
        'GTV',
        'Heart',
        'Foramen',
        'Foramen+3mm',
        'Oesophagus',
        'Trachea',
        'Bronchial tree',
        'Airway avoidance',
        'L Brachial plex',
        'R Brachial plex',
        'PTV CHEST',
        'Lt_Lung',
        'Rt_Lung',
        'Both Lungs-ITV',
        'Both Lungs',
        'Ribs', 
		'Ribs-PTV',
		'Airway avoidance',
        'PTV ring 2-3cm', 
		'Pseudo Ring',
		'Inner Ring',
        'Skin-PTV+2cm', 
        'Skin',
        'ITV',
        'Inner Ring',
		'PseudoPTV-ITV',
		'Pseudo ITV',
		'Pseudo Ribs',
		'Dose 100[%]',
		'Dose 50[%]',
		'Dose 27Gy',
		'Dose 30Gy',
		'cool',
		'Great vessels',
		'main vessels',
		'Artefact',
		'temp',
		'Liver',
		'25Gy isodose',
        'CONTRAST'];
for file in files:
	if file.endswith('.txt'):
		file_list.append(file);

#lest open all the .txt by order

change_log=open('change_log.csv','wt');#new file

for file in file_list:
	read_file=open(str(file),'r');#open file to read
	save_file=open('n'+str(file),'wt');#new file
	for line in read_file:#line by line
		if line.startswith('Structure:'):#where is the struc
			stru=line.split(':');
			orig_struct = stru[1];
			match=[];#array for matches
			for o in organs:
				ma = (SequenceMatcher(lambda x: x==" ",o, orig_struct).ratio())
				
				match.append(ma);
			pos=match.index(max(match));
			stru[1]=organs[pos];
			line=stru[0]+': '+stru[1];
			save_file.write(line+'\n')
			change_log.write(str(file) + ',' + orig_struct + ','+ organs[pos] +'\n')
			continue
		save_file.write(line)
	save_file.close()
	read_file.close()
			
			
