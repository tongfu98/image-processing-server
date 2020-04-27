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
import requests
import json


server_name = "http://127.0.0.1:5000/"

original_new_upload = {}


def image_file_to_b64_string(filename):

    """Convert image file to base64 string.

        This function converts image file to base64 string.

        Args:
            filename (string): the path and name of the
            image file on computer

        Returns:
            b64_string (string): image bytes encoded
            as a base64 string

        """

    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def b64_string_to_image_file(b64_string, new_file_name):

    """Convert base64 string to image file.

        This function converts base64 string to image file.

        Args:
            b64_string (string): the image bytes
            encoded as a base64 string

            new_file_name (string): name of the file

        Returns:
            image_file (image file): an image file on the local computer
            with the path and name contained in the new_filename variable
        """

    image_bytes = base64.b64decode(b64_string)
    with open(new_file_name, "wb") as out_file:
        out_file.write(image_bytes)


def b64_string_to_ndarray(b64_string):

    """Convert base64 string to ndarray.

        This function converts base64 string to ndarray
         containing image data.

        Args:
            b64_string (string): the image bytes
            encoded as a base64 string

        Returns:
            img_ndarray (ndarray): variable containing an
            ndarray with image data
        """

    image_bytes = base64.b64decode(b64_string)
    image_buf = io.BytesIO(image_bytes)
    img_ndarray = mpimg.imread(image_buf, format='JPG')
    return img_ndarray


def ndarray_to_tkinter_image(img_ndarray):

    """Convert ndarray  into a Tkinter label.

        This function loads an ndarray containing an
        image into a Tkinter label.

        Args:
            img_ndarray (ndarray): an ndarray with image data

        Returns:
            tk_image (Tk image): can be assigned to the 'image'
            property of a tkinter Label or Button
        """

    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    out_img = io.BytesIO()
    out_img.write(f.getvalue())
    img_obj = Image.open(out_img)
    img_obj.thumbnail((500, 500), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(img_obj)
    return tk_image


def ndarray_to_b64_string(img_ndarray):

    """Convert image in ndarray format into a base64 string.

        This function converts ndarray to a base64 string.

        Args:
            img_ndarray (ndarray): an ndarray with image data

        Returns:
            b64_string (string): image bytes
            encoded as a base64 string
        """

    f = io.BytesIO()
    imsave(f, img_ndarray, plugin='pil')
    y = base64.b64encode(f.getvalue())
    b64_string = str(y, encoding='utf-8')
    return b64_string


def get_new_upload_image(b64_str):

    """Convert base64 string into a Tk image.

        This function converts base64 string into a image
        that can be furthur used as Tkinter label.

        Args:
            b64_str (string): image bytes
            encoded as a base64 string

        Returns:
            tk_image (Tk image): can be assigned to the 'image'
            property of a tkinter Label or Button
        """

    img_ndarray = b64_string_to_ndarray(b64_str)
    tk_image = ndarray_to_tkinter_image(img_ndarray)
    return tk_image


def get_image_size(b64_str):

    """Gets image dimensions.

        This function get image dimensions from a base64 string.

        Args:
            b64_str (string): image bytes
            encoded as a base64 string

        Returns:
            width, height (list): a list containing width and height
            in pixels
        """

    imgdata = base64.b64decode(b64_str)
    im = Image.open(io.BytesIO(imgdata))
    width, height = im.size
    return width, height


def add_new_upload_to_db():

    """Send info to database.

        This function post the dictionary original_new_upload to database
        in API route /addOriginal.

        Args:
            None

        Returns:
            r (request): a request that will dump the information
            in json file to the database through API route
        """

    new_upload = original_new_upload
    r = requests.post(server_name + "/addOriginal", json=new_upload)
    return r


def add_new_processed_to_db():

    """Send info to database.

        This function post the dictionary original_new_upload to database
        in API route /addInverted.

        Args:
            None

        Returns:
            r (request): a request that will dump the information
            in json file to the database through API route
        """

    new_upload = original_new_upload
    r = requests.post(server_name + "/addInverted", json=new_upload)
    return r


def main_window():

    def open_button_cmd():

        """
            This function will create a tk image from the base64 string
            when the open button is pressed. It will also add the new
            image information to the database.
            """

        root.newFilename = filedialog.askopenfilename(
            initialdir="/", title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        original_new_upload['name'] = root.newFilename.split("/")[-1]
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
        add_new_upload_to_db()
        return

    def ori_metadata_change(timestamp, width, height):

        """Send info to database.

            This function will change the metadata under
            the original image to show the time the image is opened
            and the dimensions of the image.

            Args:
                timestamp (string): time stamp of current time
                width (int): width of the image in pixel
                height (int): height of the image in pixel

            Returns:
                None
            """

        ori_timestamp_label["text"] = "timestamp: {}".format(timestamp)
        ori_size_label["text"] = "image size: {} * {}".format(width, height)
        return

    def invert_button_cmd():

        """
            This function will invert a tk image from the base64 string
            when the invert button is pressed. It will also add the inverted
            image information to the database.
            """

        if len(original_new_upload) != 0:
            if original_image_combo.get() == "":
                original_new_upload['inverted_name'] = \
                    root.newFilename.split("/")[-1].split(".")[0] +\
                    "_inv." + root.newFilename.split("/")[-1].split(".")[-1]
            else:
                original_new_upload['inverted_name'] = \
                    original_image_combo.get()
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
            add_new_processed_to_db()
            return

    def pro_metadata_change(timestamp, width, height):

        """Send info to database.

            This function will change the metadata under
            the inverted image to show the time the image is inverted
            and the dimensions of the image.

            Args:
                timestamp (string): time stamp of current time
                width (int): width of the image in pixel
                height (int): height of the image in pixel

            Returns:
                None
            """

        processed_timestamp_label["text"] = "timestamp: {}"\
            .format(timestamp)
        processed_size_label["text"] = "image size: {} * {}"\
            .format(width, height)
        return

    def download_ori_cmd():

        """
            This function will download the image (original)
            to local computer (a download window will show up),
            and will allow the user to select the path.
            """

        if len(original_new_upload) != 0:
            b64str = original_new_upload['b64_string']
            root.downloadname_ori = filedialog.asksaveasfilename(
                initialdir="/", title="Select file",
                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            b64_string_to_image_file(b64str, root.downloadname_ori)
            return

    def download_processed_cmd():

        """
            This function will download the image (inverted)
            to local computer (a download window will show up),
            and will allow the user to select the path.
            """

        if len(original_new_upload) != 0:
            b64str_inv = original_new_upload['b64_string_inv']
            root.downloadname_inv = filedialog.asksaveasfilename(
                initialdir="/", title="Select file",
                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            b64_string_to_image_file(b64str_inv, root.downloadname_inv)
            return

    def change_names_ori():

        """Change the values in combobox.

            This function will change the values in combobox
            dynamically to reflect the change in database.
            It will gives all the names of the images that are
            currently stored in the database.

            Args:
                None

            Returns:
                new_list (list): a list that is generated by
                making a get request from route /getOriginalNames
            """

        r = requests.get(server_name + "/getOriginalNames")
        str = r.content.decode("utf-8")[1:-2]
        new_str = str.split(":")[1][1:-1]
        list = new_str.split(",")
        new_list = []
        for item in list:
            new_list.append(item[1:-1])
        return new_list

    def get_original_b64():

        """Get base64 string information in database.

            This function will make a get request from
            route /getOriginalB64 and will get base64
            of all images that are stored in database.

            Args:
                None

            Returns:
                new_list (list): a list containing all base64
                info of the images that is stored in database
            """

        r = requests.get(server_name + "/getOriginalB64")
        str = r.content.decode("utf-8")[1:-2]
        new_str = str.split(":")[1][1:-1]
        list = new_str.split(",")
        new_list = []
        for item in list:
            new_list.append(item[1:-1])
        return new_list

    def open_data_ori_button_cmd():

        """
            This function will open the image if an image
            is selected in the combobox menu.
            """

        name = original_image_combo.get()
        for ind, item in enumerate(change_names_ori()):
            if name == item:
                b64str = get_original_b64()[ind]
        original_new_upload['name'] = change_names_ori()[ind]
        new_tk_image = get_new_upload_image(b64str)
        original_new_upload['b64_string'] = b64str
        width = get_image_size(b64str)[0]
        height = get_image_size(b64str)[1]
        original_new_upload['upload_timestamp'] = str(datetime.now())
        ori_metadata_change(original_new_upload['upload_timestamp'],
                            width, height)
        original_new_upload['upload_size'] = [width, height]
        bg_label_1.image = new_tk_image
        bg_label_1.configure(image=new_tk_image)
        # add_new_upload_to_db()
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
    open_button_1 = ttk.Button(root, text="Open", command=open_button_cmd)
    open_button_1.grid(column=0, row=2)

    # choose database dropdown
    ttk.Label(root, text="Select from database").grid(column=1, row=1)
    file_name = StringVar()
    original_image_combo = ttk.Combobox(root, textvariable=file_name,
                                        values=change_names_ori())
    original_image_combo.grid(column=1, row=2, padx=5)
    original_image_combo.state(['readonly'])

    # open database original button
    open_button = ttk.Button(root, text="Open",
                             command=open_data_ori_button_cmd)
    open_button.grid(column=1, row=3)

    # initialize upload background image
    background = Image.open("background.jpg")
    background.thumbnail((500, 500), Image.ANTIALIAS)
    bg_image_1 = ImageTk.PhotoImage(background)
    bg_label_1 = ttk.Label(root, image=bg_image_1)
    bg_label_1.image = bg_image_1
    bg_label_1.grid(column=0, row=4, columnspan=3, padx=20)

    # show original metadata
    ori_timestamp_label = ttk.Label(root, text="timestamp: ")
    ori_timestamp_label.grid(column=0, row=5, columnspan=2)
    ori_size_label = ttk.Label(root, text="image size: ")
    ori_size_label.grid(column=0, row=6, columnspan=2)

    # download original button
    ori_download_button = ttk.Button(root, text="Download",
                                     command=download_ori_cmd)
    ori_download_button.grid(column=0, row=7, columnspan=2)

    # image process label
    process_label = ttk.Label(root, text="Processed Image")
    process_label.grid(column=3, row=0, columnspan=2)

    # invert label
    invert_label = ttk.Label(root, text="Invert the image you select")
    invert_label.grid(column=3, row=2, columnspan=2)

    # start inverting button
    invert_button = ttk.Button(root, text="Invert",
                               command=invert_button_cmd)
    invert_button.grid(column=3, row=3, columnspan=2)

    # initialize processed background image
    background = Image.open("background.jpg")
    background.thumbnail((500, 500), Image.ANTIALIAS)
    bg_image_2 = ImageTk.PhotoImage(background)
    bg_label_2 = ttk.Label(root, image=bg_image_2)
    bg_label_2.image = bg_image_1
    bg_label_2.grid(column=3, row=4, columnspan=2, padx=50)

    # show processed metadata
    processed_timestamp_label = ttk.Label(root, text="timestamp: ")
    processed_timestamp_label.grid(column=3, row=5, columnspan=2)
    processed_size_label = ttk.Label(root, text="image size: ")
    processed_size_label.grid(column=3, row=6, columnspan=2)

    # download processed button
    processed_download_button = ttk.Button(root, text="Download",
                                           command=download_processed_cmd)
    processed_download_button.grid(column=3, row=7, columnspan=2)

    root.mainloop()
    return


if __name__ == '__main__':
    main_window()
