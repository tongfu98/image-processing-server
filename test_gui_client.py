import pytest
import filecmp
import os
import numpy as np


@pytest.mark.parametrize("filename, expected", [

    ("test_image_1.jpg",
     "iVBORw0KGgoAAAANSUhEUgAABD0AAALmCAYAAABB3e+uAAAAAX"),
    ("test_image_2.jpg",
     "iVBORw0KGgoAAAANSUhEUgAAAJoAAABMCAYAAACVmK4lAAAAAX"),

])
def test_image_file_to_b64_string(filename, expected):
    from gui_client import image_file_to_b64_string
    b64str = image_file_to_b64_string(filename)
    assert b64str[0:50] == expected


@pytest.mark.parametrize("input_file, output_file, expected", [

    ("test_image_1.jpg", "test_image_output_1.jpg", True),
    ("test_image_2.jpg", "test_image_output_2.jpg", True),

])
def test_b64_string_to_image_file(input_file, output_file, expected):
    from gui_client import image_file_to_b64_string
    from gui_client import b64_string_to_image_file
    b64str = image_file_to_b64_string(input_file)
    b64_string_to_image_file(b64str, output_file)
    answer = filecmp.cmp(input_file, output_file)
    os.remove(output_file)
    assert answer == expected


@pytest.mark.parametrize("filename, expected", [

    ("test_image_1.jpg", np.array([[0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]])),
    ("test_image_2.jpg", np.array([[73, 74, 75, 255],
                                   [73, 74, 75, 255],
                                   [73, 74, 75, 255],
                                   [73, 74, 75, 255],
                                   [73, 74, 75, 255]])),

])
def test_b64_string_to_ndarray(filename, expected):
    from gui_client import b64_string_to_ndarray
    from gui_client import image_file_to_b64_string
    b64str = image_file_to_b64_string(filename)
    ndarray = b64_string_to_ndarray(b64str)
    answer = ndarray[0][0:5]
    assert (answer == expected).all


@pytest.mark.parametrize("filename, expected", [

    ("test_image_1.jpg",
     "iVBORw0KGgoAAAANSUhEUgAABD0AAALmCAYAAABB3e+uAADwp0"),
    ("test_image_2.jpg",
     "iVBORw0KGgoAAAANSUhEUgAAAJoAAABMCAYAAACVmK4lAAAJcE"),

])
def test_ndarray_to_b64_string(filename, expected):
    from gui_client import b64_string_to_ndarray
    from gui_client import image_file_to_b64_string
    from gui_client import ndarray_to_b64_string
    b64str = image_file_to_b64_string(filename)
    ndarray = b64_string_to_ndarray(b64str)
    answer = ndarray_to_b64_string(ndarray)[0:50]
    assert answer == expected


@pytest.mark.parametrize("filename, expected", [

    ("test_image_1.jpg",
     (1085, 742)),
    ("test_image_2.jpg",
     (154, 76)),

])
def test_get_image_size(filename, expected):
    from gui_client import get_image_size
    from gui_client import image_file_to_b64_string
    b64str = image_file_to_b64_string(filename)
    answer = get_image_size(b64str)
    assert answer == expected
