import pytest
import filecmp
import os
import numpy as np


@pytest.mark.parametrize("filename, expected", [

    ("sseniaxasduhxjsal", False),

])
def is_upload_in_database(b64str, expected):
    from cloud_server import is_upload_in_database
    answer = is_upload_in_database(b64str)
    assert answer == expected


@pytest.mark.parametrize("filename, expected", [

    ("sseniaxasduhxjsal", False),

])
def is_inverted_in_database(b64str, expected):
    from cloud_server import is_inverted_in_database
    answer = is_inverted_in_database(b64str)
    assert answer == expected


@pytest.mark.parametrize("name, b64str, time, size, expected", [

    ("hello.jpg", "huioaisuhjl", "20130203", [30, 30], True),

])
def add_original_to_database(name, b64str, time, size, expected):
    from cloud_server import add_original_to_database
    answer = add_original_to_database(name, b64str, time, size)
    assert answer == expected


@pytest.mark.parametrize("name, b64str, time, size, expected", [

    ("hello.jpg", "huioaisuhjl", "20130203", [30, 30], True),

])
def add_inverted_to_database(name, b64str, time, size, expected):
    from cloud_server import add_inverted_to_database
    answer = add_inverted_to_database(name, b64str, time, size)
    assert answer == expected
