"""
Methods for filtering mass spectra based on taxonomy
"""
# TODO: Should just use directory search to find models to speed filter time
import pickle
import difflib
import re
import sys
import gzip


def get_model(model_id):
    """
    Return sets of Inchikeys and names associated with the model id
    :param model_id: the name of the metabolic model
    :type model_id: str
    :return:
    :rtype: tuple(set, set)
    """
    def get_set(file):
        with gzip.GzipFile(file, 'rb') as infile:
            set_dict = pickle.load(infile)
        try:
            return set_dict[model_id]
        except KeyError:
            options = difflib.get_close_matches(model_id, set_dict.keys())
            raise ValueError('%s does not match any valid models. Did you '
                             'mean any of these: %s'
                             % (model_id, ", ".join(options)))

    return get_set('model_inchikeys.pkl.gz'), get_set('model_names.pkl.gz')


def filter_file(infile, model):
    """
    Filters a mass spectra library to only compounds that exist in a
    specific organism's metabolic model
    :param infile: The path to the file to be filtered
    :type infile: str
    :param model: The id of a model to use for filtering (e.g. 'eco')
    :type model: str
    :return: The number of input spectra in the file and number of spectra
    remaining after filtering
    :rtype: tuple(int, int)
    """
    def spec_gen(file):
        # This should probably be converted to a generator to be resilient
        # against really big spec libraries
        raw = open(file, 'r').read()
        sep_list = ["\n\n\n", "\n\n", "END IONS\n\nBEGIN IONS\n"]
        sep = max(sep_list, key=lambda x: raw.count(x, 0, 10000))
        for spec in raw.split(sep):
            yield spec+sep

    if '.msp' not in infile and '.mgf' not in infile:
        raise ValueError("%s is not a valid input file. Use MSP or MGF "
                         "formats" % infile)
    # Trigger file not found error quickly if applicable
    open(infile)

    m_inchikeys, m_names = get_model(model)
    outname = "%s_filtered_by_%s.%s" % (infile[:-4], model, infile[-3:])
    outfile = open(outname, "w")
    in_spec, out_spec = 0, 0
    for spec in spec_gen(infile):
        in_spec += 1
        inchikey = re.search("[A-Z]{14}-[A-Z]{10}-[A-Z]", spec)
        if inchikey:
            inchikey = inchikey.group(0)
        n_patt = "(Synon: METB N: |Name: |Synonym:)(\S+)"
        names = set([x[1] for x in re.findall(n_patt, spec) if x])
        ri = re.search('"retention index=(\w+)"', spec)
        if ri:
            spec = spec.replace("\nFormula:", "\nRI: %s\nFormula:" %
                                ri.group(1))
        if names & m_names or inchikey in m_inchikeys:
            out_spec += 1
            outfile.write(spec)
    outfile.close()
    return in_spec, out_spec

if __name__ == "__main__":
    inspec, outspec = filter_file(sys.argv[1], sys.argv[2])
    print("Filtered %s spectra down to %s based on the %s model"
          % (inspec, outspec, sys.argv[2]))
