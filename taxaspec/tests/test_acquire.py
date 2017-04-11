from taxaspec import acquire
import filecmp
import os
from subprocess import call


def test_from_mona():
    query = 'compound.metaData=q=\'name=="molecular formula" and ' \
            'value=="C47H74O12S"\''
    expected_name = "mona_compound.metaData=q='name=="\
                    + '"molecular formula" and value=="C47H74O12S"' + "'.msp"
    try:
        file_name = acquire.from_mona(query)
        filecmp.cmp(file_name, "tests/mona_results.msp")
    finally:
        os.remove(expected_name)


def test_mona_commandline():
    try:
        rc = call(['python', 'acquire.py', 'mona', 'tags.text=="GC-MS"', 'eco'])
        assert not rc
        assert os.path.exists('mona_tags.text=="GC-MS".msp')
        assert os.path.exists('mona_tags.text=="GC-MS"_filtered_by_ec.msp')

    finally:
        os.remove('mona_tags.text=="GC-MS".msp')
        os.remove('text=="GC-MS"_filtered_by_eco.msp')
