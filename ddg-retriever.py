import argparse
import configparser
import logging
import sys

from ddg.query_list import QueryList

logger = logging.getLogger('ddg-retriever_logger')


def get_argument_parser():
    arg_parser = argparse.ArgumentParser(
        description='Scrape search results from Duck Duck Go website.'
    )
    arg_parser.add_argument(
        '-c', '--config-file',
        required=True,
        help='Path to config file',
        dest='config_file'
    )
    return arg_parser


def main():
    # parse command line arguments
    parser = get_argument_parser()
    args = parser.parse_args()

    # parse config file
    config = configparser.ConfigParser()
    config.read(args.config_file)

    # read configuration
    if 'DEFAULT' not in config:
        logger.error("DEFAULT configuration missing.\nTerminating.")
        sys.exit()

    # i/o
    input_file = str(config['DEFAULT'].get('InputFile', None))
    output_dir = str(config['DEFAULT'].get('OutputDirectory', None))
    delimiter = str(config['DEFAULT'].get('Delimiter', None))

    if input_file is None or output_dir is None or delimiter is None:
        logger.error("Required configuration missing.\nTerminating.")
        sys.exit()

    # requests
    exact_matches = config['DEFAULT'].getboolean('ExactMatches', True)
    replace_parentheses = config['DEFAULT'].getboolean('ReplaceParentheses', True)
    max_results = config['DEFAULT'].getint('MaxResults', 25)
    min_wait = config['DEFAULT'].getint('MinWait', 500)
    max_wait = config['DEFAULT'].getint('MaxWait', 2000)

    # process venues
    query_list = QueryList()
    query_list.read_from_csv(input_file, exact_matches, replace_parentheses, delimiter)
    query_list.retrieve_search_results(max_results, min_wait, max_wait)
    query_list.write_to_csv(output_dir, delimiter)


if __name__ == '__main__':
    main()
