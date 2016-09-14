#import sys
import os
from difflib import SequenceMatcher

dire=os.getcwd();#current directory
files=os.listdir(dire);#list all archives
#lets take only the .txt
dvh=[];
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
        'ribs', 
        'Ribs', 
        'PTV ring 2-3cm', 
        'Skin-PTV+2cm', 
        'Skin',
        'ITV',
        'Inner Ring',
        'Ribs-PTV', 
        'PseudoPTV-ITV',
        'Pseudo ITV',
        'Dose 100[%]',
        'Dose 50[%]',
        'CONTRAST'];
for i in files:
	if i.endswith('.txt'):
		dvh.append(i);

#lest open all the .txt by order

for a in dvh:
	arch=open(str(a),'r');#open file to read
	newarch=open('n'+str(a),'wt');#new file
	for l in arch:#line by line
		if l.startswith('Structure:'):#where is the struc
			stru=l.split(':');
			match=[];#array for matches
			for o in organs:
				ma = (SequenceMatcher(lambda x: x==" ",o, stru[1]).ratio())
				match.append(ma);
			pos=match.index(max(match));
			stru[1]=organs[pos];
			l=stru[0]+': '+stru[1];
			newarch.write(l+'\n')
			continue
		newarch.write(l)
	newarch.close()
	arch.close()
			
			
