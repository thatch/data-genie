import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../genie_pkg")

import pytest
import random

from fw_genie import generate, anonymise_columns

type_choices = ['int', 'float', 'str']
min_width = 5 #this is to make sure floats are valid

def test_fw():
    # Run all the tests in a loop to have better confidance of randomisation.
    for i in range(2, 5):
        ncols = random.randint(1, 10)
        nrows = random.randint(1, 3)
        default_specs = [(random.randint(min_width, 10), random.choice(type_choices),) for i in range(ncols)]
        colspecs =  default_specs + [(10, 'date', '%d/%m/%Y'), 
                                    (10, 'float', 3), 
                                    (15, 'email', 'mail.com'),
                                    (10, 'myval', 'returnasis')]
        data = generate(colspecs, nrows=1)
        expected_length = sum([c[0] for c in colspecs])
        for d in data:
            decoded = d.decode()
            assert len(decoded) == expected_length


def test_generate_bad_decode():
    #has to have atleast 1 special char for this test to work
    ncols = random.randint(1, 10)
    colspecs = [(random.randint(min_width, 10), random.choice(type_choices),) for i in range(ncols)]
    #run the test more than once
    for i in range(2, 5):
        for d in generate(colspecs + [(8, 'str')], nrows=1, encoding='windows-1252'):
            try:
                print(d.decode('utf-8'))
                assert False
            except UnicodeDecodeError as e:
                assert True


def test_generate_good_decode():
    ncols = random.randint(1, 10)
    colspecs = [(random.randint(min_width, 10), random.choice(type_choices),) for i in range(ncols)]
    for d in generate(colspecs + [(8, 'str')], nrows=1):
        try:
            print(d.decode())
            assert True
        except e:
            assert False


def test_anonymise():
    input_encoding = 'windows-1252'
    row = 'FReNG£Ni£iFthtR¥ubOswUPhmQWJoypvF¢MFcR'.encode(input_encoding)

    anonymous_col_specs = [(0, 5, 'int'), (28, 38, 'float')]
    anonymised = anonymise_columns(row, anonymous_col_specs, input_encoding)
    decoded = anonymised.decode(input_encoding)
    assert len(decoded) == len(row.decode(input_encoding))
    v = decoded[:5]
    assert v != 'FReNG'
    assert isinstance(int(v), int) == True


def test_bad_email_config_throws_exception():
    with pytest.raises(Exception) as e_info:
        row = 'FReNG£Ni£iFthtR¥ubOswUPhmQWJoypvF¢MFcR'.encode()

        anonymous_col_specs = [(28, 38, 'email', 'hotmail.com')]
        anonymise_columns(row, anonymous_col_specs)

def test_bad_myval_throws_exception():
    with pytest.raises(Exception) as e_info:
        colspecs =  [(10, 'myval', '14/3/2019')]
        for d in generate(colspecs, nrows=1):
            assert d is not None

def test_bad_date_length_throws_exception():
    with pytest.raises(Exception) as e_info:
        colspecs =  [(8, 'date')]
        for d in generate(colspecs, nrows=1):
            assert d is not None
