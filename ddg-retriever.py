import argparse
import logging

from ddg.query_list import QueryList

logger = logging.getLogger('ddg-retriever_logger')


def get_argument_parser():
    arg_parser = argparse.ArgumentParser(
        description='Scrape search results from Duck Duck Go website.'
    )
    arg_parser.add_argument(
        '-i', '--input-file',
        required=True,
        help='CSV file with search queries.',
        dest='input_file'
    )
    arg_parser.add_argument(
        '-o', '--output-dir',
        required=True,
        help='Path to output directory',
        dest='output_dir'
    )
    arg_parser.add_argument(
        '-e', '--exact-matches',
        required=False,
        default=False,
        help='search for exact matches of query strings (using double quotes)',
        dest='exact_matches'
    )
    arg_parser.add_argument(
        '-d', '--delimiter',
        required=False,
        default=',',
        help='delimiter for CSV files (default: \',\')',
        dest='delimiter'
    )
    return arg_parser


def main():
    # parse command line arguments
    parser = get_argument_parser()
    args = parser.parse_args()

    # process venues
    query_list = QueryList()
    query_list.read_from_csv(args.input_file, args.exact_matches, args.delimiter)
    query_list.retrieve_search_results()
    query_list.write_to_csv(args.output_dir, args.delimiter)


if __name__ == '__main__':
    main()
