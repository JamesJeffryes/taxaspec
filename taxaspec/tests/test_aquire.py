from taxaspec import aquire
import filecmp
import os


def test_from_mona():
    query = 'compound.metaData=q=\'name=="molecular formula" and ' \
            'value=="C47H74O12S"\''
    expected_name = "mona_compound.metaData=q='name=="\
                    + '"molecular formula" and value=="C47H74O12S"' + "'.msp"
    try:
        file_name = aquire.from_mona(query)
        filecmp.cmp(file_name, "tests/mona_results.msp")
    finally:
        os.remove(expected_name)


"""
def test_get_gc():
    query = 'tags.text=="GC-MS"'
    file_name = aquire.from_mona(query)"""
