from taxaspec import acquire
import filecmp
import os
import glob
from subprocess import call

query = 'compound.metaData=q=\'name=="molecular formula" and ' \
            'value=="C47H74O12S"\''
expected_name = "mona_compound.metaData=q='name=="\
                    + '"molecular formula" and value=="C47H74O12S"' + "'.msp"
def test_from_mona():
    query = 'compound.metaData=q=\'name=="molecular formula" and ' \
            'value=="C47H74O12S"\''
    expected_name = "mona_compound.metaData=q='name=="\
                    + '"molecular formula" and value=="C47H74O12S"' + "'.msp"
    try:
        file_name = acquire.from_mona(query)
        filecmp.cmp(file_name, "tests/mona_results.msp")
    finally:
        for file in glob.glob('*.msp'):
            os.remove(file)


def test_mona_commandline():
    try:
        rc = call(['python', 'acquire.py', 'mona', query, 'eco'])
        assert not rc
        assert len(glob.glob('*.msp')) == 2
        assert len(glob.glob('*_filtered_by_eco.msp')) == 1

    finally:
        for file in glob.glob('*.msp'):
            os.remove(file)


def test_from_mine():
    one = acquire.from_mine("EcoCycexp2", "", "eco", False,
                            [[True, 20], [False, 40]])
    assert len(one)
    two = acquire.from_mine('EcoCycexp2', "{'Formula': {'$regex': '^C6H'}}",
                            "", True, [])
    assert len(two)
