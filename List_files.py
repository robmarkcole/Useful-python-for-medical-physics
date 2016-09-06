import os
f = open("file_list.txt","a") #opens file with name of "file_list.txt", creates if doesnt exist
for file in os.listdir("/Users/robincole/Dropbox/09 Med phys/NPL files/Pinnacle/RD_DW"):
    #print(file)
    f.write(file)
    f.write("\n")
f.close()