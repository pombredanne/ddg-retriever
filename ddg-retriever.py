import argparse
import codecs
import configparser
import csv
import logging
import sys

from ddg.query_list import QueryList
from ddg.search_result_list import SearchResultList
from util.exceptions import IllegalArgumentError

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
    remove_special_characters = config['DEFAULT'].getboolean('RemoveSpecialCharacters', True)
    max_results = config['DEFAULT'].getint('MaxResults', 25)
    min_wait = config['DEFAULT'].getint('MinWait', 500)
    max_wait = config['DEFAULT'].getint('MaxWait', 2000)
    wait_on_error = config['DEFAULT'].getint('WaitOnError', 30000)

    # detecting languages of snippets
    detect_languages = config['DEFAULT'].getboolean('DetectLanguages', True)

    queries_only = False

    # read CSV as UTF-8 encoded file (see also http://stackoverflow.com/a/844443)
    with codecs.open(input_file, encoding='utf8') as fp:
        logger.info("Checking input format in " + input_file + "...")
        reader = csv.reader(fp, delimiter=delimiter)
        # read header
        header = next(reader, None)
        if not header:
            raise IllegalArgumentError("Missing header in CSV file.")
        queries_only = len(header) == 1

    if queries_only:
        logger.info("Input file contains only queries, retrieving search results...")
        query_list = QueryList()
        query_list.read_from_csv(input_file, exact_matches, remove_special_characters, delimiter)
        query_list.retrieve_search_results(max_results, min_wait, max_wait, wait_on_error, detect_languages)
        query_list.write_search_results_to_csv(output_dir, delimiter, detect_languages)
        query_list.write_failed_queries(output_dir, delimiter)
    elif detect_languages:
        logger.info("Input file contains search results, detecting language of snippets...")
        search_result_list = SearchResultList()
        search_result_list.read_from_csv(input_file, delimiter)
        search_result_list.detect_languages()
        search_result_list.write_to_csv(output_dir, delimiter, detect_languages)
    else:
        logger.info("No action configured, terminating...")

    logger.info("Finished.")


if __name__ == '__main__':
    main()
