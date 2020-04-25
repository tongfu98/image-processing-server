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

    # image process label
    process_label = ttk.Label(root, text="Processed Image")
    process_label.grid(column=3, row=0, columnspan=2)

    # invert label
    invert_label = ttk.Label(root, text="Invert the image you upload")
    invert_label.grid(column=3, row=1)

    # start invertion button
    invert_button = ttk.Button(root, text="Invert")
    invert_button.grid(column=3, row=2)

    # choose database dropdown
    ttk.Label(root, text="Select from database").grid(column=4, row=1)
    file_name = StringVar()
    processed_image_combo = ttk.Combobox(root, textvariable=file_name)
    processed_image_combo.grid(column=4, row=2, padx=5)
    processed_image_combo['values'] = ("x", "y", "z")
    processed_image_combo.state(['readonly'])

    # initialize processed background image
    background = Image.open("images/acl1.jpg")
    bg_image_2 = ImageTk.PhotoImage(background)
    bg_label_2 = ttk.Label(root, image=bg_image_2)
    bg_label_2.image = bg_image_1
    bg_label_2.grid(column=3, row=3, columnspan=2)

    # show processed metadata
    processed_timestamp_data = "Default"
    processed_timestamp_label = ttk.Label(root, text="timestamp: {}".format(processed_timestamp_data))
    processed_timestamp_label.grid(column=3, row=4, columnspan=2)
    processed_size_data = 0
    processed_size_data = ttk.Label(root, text="image size: {}".format(processed_size_data))
    processed_size_data.grid(column=3, row=5, columnspan=2)

    # download original button
    ori_download_button = ttk.Button(root, text="Download")
    ori_download_button.grid(column=3, row=6, columnspan=2)


    root.mainloop()
    return


if __name__ == '__main__':
    main_window()