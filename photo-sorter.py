from PIL import Image as Img
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
import rawpy
import os, sys


root = Tk()

root.title('Image Sorter')

application_path = filedialog.askdirectory()

image_list = []
file_list = []
count = 0
max_height = root.winfo_screenheight() - 100

root.state('zoomed')

main_frame = Frame(root, bg="grey")

if not os.path.exists(application_path + '/saved'):
    os.makedirs(application_path + '/saved')
if not os.path.exists(application_path + '/discarded'):
    os.makedirs(application_path + '/discarded')

main_frame.grid(row=0, column=1, sticky="NESW")
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

myFont = font.Font(family='Helvetica', size=20, weight='bold')

def how_many_images():
    global count
    for file in os.listdir(application_path):
        if file.endswith(".NEF"):
             count = count + 1
            
how_many_images()

def load_images():
    current = 0
    for file in os.listdir(application_path):
        if file.endswith(".NEF"):

            #Read in the raw file, process it, and convert it into an image PIL can use.
            raw = rawpy.imread(application_path + '/' + file)
            rgb = raw.postprocess()
            img = Img.fromarray(rgb)

            h, w = img.size

            img_height_pct = (max_height/float(h))
            calc_w = int(max_height * (h/w))
                        
            resized_img = img.resize((calc_w, max_height))
                        
            thisfile = ImageTk.PhotoImage(resized_img)
            image_list.append(thisfile)
            file_list.append(file)
            current = current + 1
            print('Loaded ', current, '/', count, ': ', file)

load_images()



global current_image
current_image = 0


my_label = Label(image=image_list[current_image])
my_label.grid(row=0, column=0, columnspan=3)


def forward(image_number):
    global my_label
    global button_forward
    global buton_back
    global current_image
    global image_list
    global file_list

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number-1])
    button_forward = Button(main_frame, text=">", command=lambda: forward(image_number+1))
    button_back = Button(main_frame, text="<", command=lambda: back(image_number-1))
    button_forward['font'] = myFont
    button_back['font'] = myFont
    my_label.grid(row=0, column=0, columnspan=3)

    current_image = image_number - 1

    if image_number == len(image_list):
        button_forward = Button(main_frame, text=">", state=DISABLED)

    if len(image_list) == 1:
        button_back = Button(main_frame, text="<", state=DISABLED)
        button_forward = Button(main_frame, text=">", state=DISABLED)
        button_forward['font'] = myFont
        button_back['font'] = myFont

    button_back.grid(row=0, column=0)
    button_forward.grid(row=0, column=2)

def back(image_number):
    global my_label
    global button_forward
    global buton_back
    global current_image
    global image_list
    global file_list

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number-1])
    button_forward = Button(main_frame, text=">", command=lambda: forward(image_number+1))
    button_back = Button(main_frame, text="<", command=lambda: back(image_number-1))
    my_label.grid(row=0, column=0, columnspan=3)

    current_image = image_number - 1

    if image_number == 1:
        button_back = Button(main_frame, text="<", state=DISABLED)
        button_back['font'] = myFont

    if len(image_list) == 1:
        button_back = Button(main_frame, text="<", state=DISABLED)
        button_forward = Button(main_frame, text=">", state=DISABLED)
        button_forward['font'] = myFont
        button_back['font'] = myFont

    button_back.grid(row=0, column=0)
    button_forward.grid(row=0, column=2)

def save(event=None):
    global current_image
    global image_list
    global file_list
    os.rename(application_path + '/' + file_list[current_image], application_path + '/saved/' + file_list[current_image])

    file_list.pop(current_image)
    image_list.pop(current_image)

    if len(image_list) == 0:
        my_label = Label(text = "There are no more files.")
    else:
        forward(current_image + 1)

def discard(event=None):
    global current_image
    global image_list
    global file_list
    os.rename(application_path + '/' + file_list[current_image], application_path + '/discarded/' + file_list[current_image])

    file_list.pop(current_image)
    image_list.pop(current_image)

    if len(image_list) == 0:
        my_label = Label(text = "There are no more files.")
    else:
        forward(current_image + 1)


root.bind("<s>", save)
root.bind("<d>", discard)

button_back = Button(main_frame, text="<", state=DISABLED)
if(count == 1):
    button_forward = Button(main_frame, text=">", state=DISABLED)
else:
    button_forward = Button(main_frame, text=">", command=lambda: forward(2))


button_forward['font'] = myFont
button_back['font'] = myFont

button_back.grid(row=0, column=0)
button_forward.grid(row=0, column=2)

def fix():
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))
root.update()
root.after(0, fix)

root.mainloop()
                            
