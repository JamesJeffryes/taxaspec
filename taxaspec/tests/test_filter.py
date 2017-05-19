from taxaspec import filter
from nose.tools import raises
import os


def test_get_model():
    inchikeys, names = filter.get_model('eco')
    assert len(inchikeys) == 1084
    assert "NWQWQKUXRJYXFH-UHFFFAOYSA-N" in inchikeys
    assert len(names) == 3420
    assert "Glucose" in names


@raises(ValueError)
def test_missing_model():
    filter.get_model("bacillus")


def test_filter_msp_file():
    try:
        spec_in, spec_out = filter.filter_file('tests/test.msp', 'eco')
        assert spec_in == 76
        assert spec_out == 1
        assert os.path.exists("tests/test_filtered_by_eco.msp")
    finally:
        os.remove("tests/test_filtered_by_eco.msp")


def test_msl_file():
    try:
        spec_in, spec_out = filter.filter_file('tests/test.msl', 'eco')
        assert spec_in == 3
        assert spec_out == 1
        assert os.path.exists("tests/test_filtered_by_eco.msl")
    finally:
        os.remove("tests/test_filtered_by_eco.msl")


@raises(ValueError)
def test_filter_bad_input_file():
    filter.filter_file('tests/test_filter.py', 'eco')


@raises(FileNotFoundError)
def test_filter_missing_input_file():
    filter.filter_file('fake.msp', 'eco')
