"""
Methods for acquiring mass spectra from public libraries
"""
import requests


def from_mona(query):
    """
    Pull mass spectra stored in the MoNA(http://mona.fiehnlab.ucdavis.edu)
    database in MSP format
    :param query: A valid RSQL query string. It can be helpful to test the
    query on the mona website to ensure proper formatting
    :type query: str
    :return: The path to the generated MSP file
    :rtype: str
    """
    endpoint = "http://mona.fiehnlab.ucdavis.edu/rest/spectra/search?query="
    r = requests.get(endpoint+query, headers={"Accept": "text/msp"})
    if not r.status_code == 200:
        raise RuntimeError("Mona query failed with status code %s"
                           % r.status_code)
    filename = "mona_%s.msp" % query
    with open(filename, "w") as outfile:
        outfile.write(r.text)
    return filename
