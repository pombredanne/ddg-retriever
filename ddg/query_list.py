import codecs
import csv
import logging
import os

from ddg.query import Query
from ddg.search_result_list import SearchResultList
from util.exceptions import IllegalArgumentError

logger = logging.getLogger("ddg-retriever_logger")
log_pace = 10


class QueryList(object):
    """ List of search queries. """

    def __init__(self):
        self.filename = ""
        self.values = list()
        self.unique_query_strings = set()
        self.search_results = SearchResultList()
        self.failed_queries = list()

    def initialize(self, filename, queries):
        self.filename = str(filename)
        for query_string in queries:
            query = Query(query_string, False, False)
            self.add_query(query)

    def add_query(self, query):
        self.unique_query_strings.add(query.query_string)
        self.values.append(query)

    def read_from_csv(self, input_file, exact_matches, remove_special_characters, delimiter):
        """
        Read search queries from a CSV file (header required).
        :param remove_special_characters: Split query string along special characters
            (see Query.special_character_regex).
        :param exact_matches: Only search for exact matches of query strings.
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

            query_string = header.index("query")

            # read CSV file
            for row in reader:
                if row:
                    query = Query(row[query_string], exact_matches, remove_special_characters)

                    if query.is_empty:
                        # print query string if it contains not only whitespaces (but, e.g., ignored characters)
                        if len(str(query).strip()) == 0:
                            logger.info("Empty query skipped.")
                        else:
                            logger.info("Empty query skipped: " + str(query))
                        continue

                    if query.query_string in self.unique_query_strings:
                        logger.info("Duplicate query skipped: " + str(query))
                        continue

                    self.add_query(query)
                else:
                    raise IllegalArgumentError("Wrong CSV format.")

        self.filename = os.path.basename(input_file)
        logger.info(str(len(self.values)) + " search queries have been imported.")

    def retrieve_search_results(self, max_results, min_wait, max_wait, wait_on_error, detect_languages):
        count = 0
        for query in self.values:
            self.handle_query(query, max_results, min_wait, max_wait, wait_on_error, detect_languages, count)
            count = count + 1
        # save failed queries
        self.failed_queries = [query for query in self.values if query.has_failed]

    def handle_query(self, query, max_results, min_wait, max_wait, wait_on_error, detect_languages, count):
        if count == 0 or count % log_pace == 0:
            logger.info('{0:.2f}'.format(count / len(self.values) * 100) + '% of the queries have been processed.')

        query.retrieve_search_results(max_results, min_wait, max_wait, wait_on_error)

        if query.is_empty:
            return

        if detect_languages:
            query.search_results.detect_languages()

        for search_result in query.search_results.values:
            self.search_results.values.append(search_result)

    def write_search_results_to_csv(self, output_dir, delimiter, include_language):
        """
        Export search results to a CSV file.
        :param include_language: Add column "language" if tool was configured to detect languages of snippets
        :param output_dir: Target directory for generated CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        """
        self.search_results.write_to_csv(output_dir, delimiter, include_language, self.filename)

    def get_rows(self):
        rows = []
        for query in self.values:
            rows.append(query.get_column_values())
        return rows

    def write_to_csv(self, output_dir, delimiter, filename=None):
        """
        Export queries to a CSV file.
        :param output_dir: Target directory for generated CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        :param filename: Filename of file to export.
        """

        if filename is not None:
            self.filename = filename

        if len(self.values) == 0:
            logger.info("Nothing to export.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, self.filename)

        # write queries to UTF8-encoded CSV file (see also http://stackoverflow.com/a/844443)
        with codecs.open(file_path, 'w', encoding='utf8') as fp:
            logger.info('Exporting queries to ' + file_path + '...')
            writer = csv.writer(fp, delimiter=delimiter)

            column_names = Query.get_column_names()

            # write header of CSV file
            writer.writerow(column_names)

            count = 0
            try:
                for row in self.get_rows():
                    if len(row) == len(column_names):
                        writer.writerow(row)
                        count = count + 1
                    else:
                        raise IllegalArgumentError(
                            str(abs(len(column_names) - len(row))) + ' parameter(s) is/are missing for "'
                            + str(row) + '"')

            except UnicodeEncodeError:
                logger.error('Encoding error while writing data for: ' + str(row))

            logger.info(str(count) + ' queries have been exported.')

    def write_failed_queries(self, output_dir, delimiter):
        if len(self.failed_queries) == 0:
            logger.info("No failed queries to write.")
            return

        logger.info("Writing failed queries...")
        failed_queries = QueryList()
        failed_queries.initialize("failed_queries.csv", self.failed_queries)
        failed_queries.write_to_csv(output_dir, delimiter)
