"""
Methods for acquiring mass spectra from public libraries
"""
import requests


def from_mona(query):
    endpoint = "http://mona.fiehnlab.ucdavis.edu/rest/spectra/search?query="
    r = requests.get(endpoint+query, headers={"Accept": "text/msp"})
    if not r.status_code == 200:
        raise RuntimeError("Mona query failed with status code %s"
                           % r.status_code)
    filename = "mona_%s.msp" % query
    with open(filename, "w") as outfile:
        outfile.write(r.text)
    return filename
