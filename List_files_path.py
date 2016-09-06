import os
import Tkinter
import tkFileDialog

root = Tkinter.Tk().withdraw()     # Close the root window
my_dir = tkFileDialog.askdirectory()  # get directory
print(my_dir)
# my_dir = "/Users/directory_path"

f = open("file_list.txt","a") #opens file with name of "file_list.txt", creates if doesnt exist

for file in os.listdir(my_dir):
   # print(os.path.join(my_path, file))
    f.write(os.path.join(my_dir, file))
    f.write("\n")
f.close()
