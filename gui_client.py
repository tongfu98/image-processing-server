from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from skimage.io import imsave
from datetime import datetime


original_new_upload = {}
processed_new_upload = {}


def image_file_to_b64_string(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def b64_string_to_image_file(b64_string, new_file_name):
    image_bytes = base64.b64decode(b64_string)
    with open(new_file_name, "wb") as out_file:
        out_file.write(image_bytes)


def b64_string_to_ndarray(b64_string):
    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def ndarray_to_tkinter_image(img_ndarray):
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    out_img = io.BytesIO()
    out_img.write(f.getvalue())
    img_obj = Image.open(out_img)
    img_obj.thumbnail((500, 500), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(img_obj)
    return tk_image


def ndarray_to_b64_string(img_ndarray):
    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    y = base64.b64encode(f.getvalue())
    b64_string = str(y, encoding='utf-8')
    return b64_string


def get_new_upload_image(b64_str):
    img_ndarray = b64_string_to_ndarray(b64_str)
    tk_image = ndarray_to_tkinter_image(img_ndarray)
    return tk_image


def get_image_size(b64_str):
    imgdata = base64.b64decode(b64_str)
    im = Image.open(io.BytesIO(imgdata))
    width, height = im.size
    return width, height


def main_window():

    def open_button_cmd():
        root.newFilename = filedialog.askopenfilename(
            initialdir="/", title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        original_new_upload['name'] = root.newFilename
        b64str = image_file_to_b64_string(root.newFilename)
        original_new_upload['b64_string'] = b64str
        width = get_image_size(b64str)[0]
        height = get_image_size(b64str)[1]
        original_new_upload['upload_timestamp'] = str(datetime.now())
        # print("The selected image is {}".format(root.newFilename))
        new_tk_image = get_new_upload_image(b64str)
        ori_metadata_change(original_new_upload['upload_timestamp'],
                            width, height)
        original_new_upload['upload_size'] = [width, height]
        bg_label_1.image = new_tk_image
        bg_label_1.configure(image=new_tk_image)
        return

    def ori_metadata_change(timestamp, width, height):
        ori_timestamp_label["text"] = "timestamp: {}".format(timestamp)
        ori_size_label["text"] = "image size: {} * {}".format(width, height)
        return

    def invert_button_cmd():
        if len(original_new_upload) != 0:
            b64str = original_new_upload['b64_string']
            ndarray_inv = np.invert(b64_string_to_ndarray(b64str))
            original_new_upload['b64_string_inv'] = \
                ndarray_to_b64_string(ndarray_inv)
            b64str_inv = original_new_upload['b64_string_inv']
            width = get_image_size(b64str_inv)[0]
            height = get_image_size(b64str_inv)[1]
            original_new_upload['processed_timestamp'] = \
                str(datetime.now())
            new_tk_image_inv = ndarray_to_tkinter_image(ndarray_inv)
            pro_metadata_change(original_new_upload['processed_timestamp'],
                                width, height)
            original_new_upload['processed_size'] = [width, height]
            bg_label_2.image = new_tk_image_inv
            bg_label_2.configure(image=new_tk_image_inv)
            return

    def pro_metadata_change(timestamp, width, height):
        processed_timestamp_label["text"] = "timestamp: {}"\
            .format(timestamp)
        processed_size_label["text"] = "image size: {} * {}"\
            .format(width, height)
        return

    def download_ori_cmd():
        if len(original_new_upload) != 0:
            b64str = original_new_upload['b64_string']
            root.downloadname_ori = filedialog.asksaveasfilename(
                initialdir="/", title="Select file",
                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            b64_string_to_image_file(b64str, root.downloadname_ori)
            return

    def download_processed_cmd():
        if len(original_new_upload) != 0:
            b64str_inv = original_new_upload['b64_string_inv']
            root.downloadname_inv = filedialog.asksaveasfilename(
                initialdir="/", title="Select file",
                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            b64_string_to_image_file(b64str_inv, root.downloadname_inv)
            return

    root = Tk()
    root.title("Image Database")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry("{}x{}".format(int(screen_width*9/10), screen_height))

    # original image label
    select_label = ttk.Label(root, text="Original Image")
    select_label.grid(column=0, row=0, columnspan=2)

    # upload label
    select_label = ttk.Label(root, text="Upload a new image")
    select_label.grid(column=0, row=1)

    # open original button
    open_button = ttk.Button(root, text="Open", command=open_button_cmd)
    open_button.grid(column=0, row=2)

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
    bg_label_1.grid(column=0, row=3, columnspan=2, padx=5)

    # show original metadata
    ori_timestamp_label = ttk.Label(root, text="timestamp: ")
    ori_timestamp_label.grid(column=0, row=4, columnspan=2)
    ori_size_label = ttk.Label(root, text="image size: ")
    ori_size_label.grid(column=0, row=5, columnspan=2)

    # download original button
    ori_download_button = ttk.Button(root, text="Download",
                                     command=download_ori_cmd)
    ori_download_button.grid(column=0, row=6, columnspan=2)

    # image process label
    process_label = ttk.Label(root, text="Processed Image")
    process_label.grid(column=3, row=0, columnspan=2)

    # invert label
    invert_label = ttk.Label(root, text="Invert the image you upload")
    invert_label.grid(column=3, row=1)

    # start inverting button
    invert_button = ttk.Button(root, text="Invert",
                               command=invert_button_cmd)
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
    processed_timestamp_label = ttk.Label(root, text="timestamp: ")
    processed_timestamp_label.grid(column=3, row=4, columnspan=2)
    processed_size_label = ttk.Label(root, text="image size: ")
    processed_size_label.grid(column=3, row=5, columnspan=2)

    # download processed button
    processed_download_button = ttk.Button(root, text="Download",
                                           command=download_processed_cmd)
    processed_download_button.grid(column=3, row=6, columnspan=2)

    root.mainloop()
    return


if __name__ == '__main__':
    main_window()
