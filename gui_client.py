from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import base64
import io
import matplotlib.image as mpimg
from skimage.io import imsave


original_new = []
processed_new = []


def main_window():

    # def open_button_cmd():
    #     image_name = organ_choice.get()
    #     print("The selected image is {}".format(image_name))
    #     new_tk_image = get_new_image(image_name)
    #     image_label.image = new_tk_image
    #     image_label.configure(image=new_tk_image)
    #     return


    root = Tk()

    # original image label
    select_label = ttk.Label(root, text="Original Image")
    select_label.grid(column=0, row=0, columnspan=2)

    # upload label
    select_label = ttk.Label(root, text="Upload a new image")
    select_label.grid(column=0, row=1)

    # Select original button
    select_button = ttk.Button(root, text="Open")
    select_button.grid(column=0, row=2)

    # choose database dropdown
    ttk.Label(root, text="Select from database").grid(column=1, row=1)
    file_name = StringVar()
    original_image_combo = ttk.Combobox(root, textvariable=file_name)
    original_image_combo.grid(column=1, row=2, padx=5)
    original_image_combo['values'] = ("x", "y", "z")
    original_image_combo.state(['readonly'])

    # initialize upload background image
    background = Image.open("images/acl1.jpg")
    bg_image_1 = ImageTk.PhotoImage(background)
    bg_label_1 = ttk.Label(root, image=bg_image_1)
    bg_label_1.image = bg_image_1
    bg_label_1.grid(column=0, row=3, columnspan=2)

    # show original metadata
    ori_timestamp_data = "Default"
    ori_timestamp_label = ttk.Label(root, text="timestamp: {}".format(ori_timestamp_data))
    ori_timestamp_label.grid(column=0, row=4, columnspan=2)
    ori_size_data = 0
    ori_size_data = ttk.Label(root, text="image size: {}".format(ori_size_data))
    ori_size_data.grid(column=0, row=5, columnspan=2)

    # download original button
    ori_download_button = ttk.Button(root, text="Download")
    ori_download_button.grid(column=0, row=6, columnspan=2)

    # # image processing label
    # process_label = ttk.Label(root, text="Image Processing")
    # process_label.grid(column=1, row=0)
    #
    # # begin button
    # begin_button = ttk.Button(root, text="Begin")
    # begin_button.grid(column=1, row=1)
    #
    # # initialize image processing background image
    # bg_image_2 = ImageTk.PhotoImage(background)
    # bg_label_2 = ttk.Label(root, image=bg_image_2)
    # bg_label_2.image = bg_image_2
    # bg_label_2.grid(column=1, row=2, columnspan=1)




    # root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
    #                                            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

    # path = tkFileDialog.askopenfilename(filetypes=[("Image File", '.jpg')])
    # im = Image.open(path)
    # tkimage = ImageTk.PhotoImage(im)
    # myvar = Label(root, image=tkimage)
    # myvar.image = tkimage
    # myvar.pack()


    #
    # organ_choice = StringVar()
    # organ_choice_box = ttk.Combobox(root, textvariable=organ_choice)
    # organ_choice_box.grid(column=1, row=0)
    # organ_choice_box['value'] = ('brain.png', 'heart.png', 'kidney.png')
    #
    #

    #
    #
    # open_button = ttk.Button(root, text="Open", command=open_button_cmd)
    # open_button.grid(column=0, row=2, columnspan=2)


    root.mainloop()
    return


if __name__ == '__main__':
    # init_db()
    main_window()