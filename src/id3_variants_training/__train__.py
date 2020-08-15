from .local_API import LOCAL_API
from .ga4gh_API import GA4GH_API
from .ID3_Class import ID3
import argparse
import pickle


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('config-file', help='path to the config file that contains variant ranges in JSON format')
    parser.add_argument('--use-candig-apis', action='store_true', default=False,
                        help='use remote API to access variant information rather than local VCF files')
    args = parser.parse_args()

    use_local_vcf_files = not args.use_candig_apis
    config_file_path = getattr(args, 'config-file')

    # get either a LOCAL_API or GA4GH_API object depending on the command line arguments passed in
    api = get_api(config_file_path, use_local_vcf_files, True)

    # create ID3 tree and serialize it to file called 'id3_tree'
    id3_tree = ID3(api)
    output_file = open('id3_tree', 'wb')
    pickle.dump(id3_tree, output_file)
    output_file.close()


def get_api(file_path, local, conf_matrix):
    """
    Constructs and returns an API object (LOCAL_API or GA4GH_API) depending on the values of <file_path>, <local> and
    <conf_matrix>.

    :param file_path: path to JSON file that contains the variant ranges
    :type file_path: str
    :param local: True if you want to construct an API that reads locally. False if you want to construct an API that
    reads from a server.
    :type local: bool
    :param conf_matrix: True if you want to construct an API for use in a confusion matrix. False otherwise. Note that
    if the value of this parameter is True, an API that reads locally is constructed regardless of the value of
    the <local> parameter.
    :type conf_matrix: bool
    :return: API object created based on the values of the function parameters
    :rtype: LOCAL_API | GA4GH_API
    """
    if local or conf_matrix:
        api = LOCAL_API(file_path, conf_matrix)
    else:
        api = GA4GH_API(file_path)

    return api


if __name__ == '__main__':
    train()
