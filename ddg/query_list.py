import codecs
import csv
import logging
import os

from ddg.search_result import SearchResult
from ddg.query import Query
from util.exceptions import IllegalArgumentError

logger = logging.getLogger("ddg-retriever_logger")


class QueryList(object):
    """ List of search queries. """

    def __init__(self):
        self.filename = ""
        self.queries = []

    def read_from_csv(self, input_file, exact_matches, delimiter):
        """
        Read search queries from a CSV file (header required).
        :param input_file: Path to the CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        """

        # read CSV as UTF-8 encoded file (see also http://stackoverflow.com/a/844443)
        with codecs.open(input_file, encoding='utf8') as fp:
            logger.info("Reading search queries from " + input_file + "...")

            reader = csv.reader(fp, delimiter=delimiter)

            # read header
            header = next(reader, None)
            if not header:
                raise IllegalArgumentError("Missing header in CSV file.")

            query = header.index("query")

            # read CSV file
            for row in reader:
                if row:
                    self.queries.append(
                        Query(row[query], exact_matches)
                    )
                else:
                    raise IllegalArgumentError("Wrong CSV format.")

        self.filename = os.path.basename(input_file)
        logger.info(str(len(self.queries)) + " search queries have been imported.")

    def retrieve_search_results(self):
        for query in self.queries:
            query.retrieve_search_results()

    def write_to_csv(self, output_dir, delimiter):
        """
        Export retrieved search results to a CSV file.
        :param output_dir: Target directory for generated CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        """

        if len(self.queries) == 0:
            logger.info("Nothing to export.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, self.filename)

        # write search results to UTF8-encoded CSV file (see also http://stackoverflow.com/a/844443)
        with codecs.open(file_path, 'w', encoding='utf8') as fp:
            logger.info('Exporting search results to ' + file_path + '...')
            writer = csv.writer(fp, delimiter=delimiter)

            column_names = SearchResult.get_column_names()

            # write header of CSV file
            writer.writerow(column_names)

            count = 0
            for query in self.queries:
                try:
                    for row in query.get_rows():
                        if len(row) == len(column_names):
                            writer.writerow(row)
                            count = count + 1
                        else:
                            raise IllegalArgumentError(
                                str(abs(len(column_names) - len(row))) + ' parameter(s) is/are missing for query "'
                                + str(query) + '"')

                except UnicodeEncodeError:
                    logger.error('Encoding error while writing data for query: ' + str(query))

            logger.info(str(count) + ' search results have been exported.')
