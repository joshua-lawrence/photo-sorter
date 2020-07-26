from tkinter import *
from PIL import ImageTk,Image
import os

import os
if not os.path.exists('saved'):
    os.makedirs('saved')

import os
if not os.path.exists('discarded'):
    os.makedirs('discarded')

root = Tk()

root.title('Image Sorter')

image_list = []
file_list = []


def load_images():
    for file in os.listdir("."):
        if file.endswith(".raw"):
            thisfile = ImageTk.PhotoImage(Image.open(file))
            image_list.append(thisfile)
            file_list.append(file)

load_images()



global current_image
current_image = 0

if len(image_list) == 0:
    my_label = Label(text = "There aren't any files here")
    my_label.grid(row=0, column=0, columnspan=3)
    exit


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
    button_forward = Button(root, text=">", command=lambda: forward(image_number+1))
    button_back = Button(root, text="<", command=lambda: back(image_number-1))
    my_label.grid(row=0, column=0, columnspan=3)

    current_image = image_number - 1

    if image_number == len(image_list):
        button_forward = Button(root, text=">", state=DISABLED)

    if len(image_list) == 1:
        button_back = Button(root, text="<", state=DISABLED)
        button_forward = Button(root, text=">", state=DISABLED)

    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)

def back(image_number):
    global my_label
    global button_forward
    global buton_back
    global current_image
    global image_list
    global file_list

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number-1])
    button_forward = Button(root, text=">", command=lambda: forward(image_number+1))
    button_back = Button(root, text="<", command=lambda: back(image_number-1))
    my_label.grid(row=0, column=0, columnspan=3)

    current_image = image_number - 1

    if image_number == 1:
        button_back = Button(root, text="<", state=DISABLED)

    if len(image_list) == 1:
        button_back = Button(root, text="<", state=DISABLED)
        button_forward = Button(root, text=">", state=DISABLED)

    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)

def save(event=None):
    global current_image
    global image_list
    global file_list
    os.rename(file_list[current_image], './saved/' + file_list[current_image])

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
    os.rename(file_list[current_image], './discarded/' + file_list[current_image])

    file_list.pop(current_image)
    image_list.pop(current_image)

    if len(image_list) == 0:
        my_label = Label(text = "There are no more files.")
    else:
        forward(current_image + 1)


root.bind("<s>", save)
root.bind("<d>", discard)

button_back = Button(root, text="<", state=DISABLED)
button_forward = Button(root, text=">", command=lambda: forward(2))

button_back.grid(row=1, column=0)
button_forward.grid(row=1, column=2)

root.mainloop()
                            
