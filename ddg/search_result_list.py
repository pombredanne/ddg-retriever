import codecs
import csv
import logging
import os

from ddg.search_result import SearchResult
from util.exceptions import IllegalArgumentError

logger = logging.getLogger("ddg-retriever_logger")


class SearchResultList(object):
    """ List of search results. """

    def __init__(self):
        self.filename = ""
        self.values = []

    def get_rows(self):
        rows = []
        for result in self.values:
            rows.append(result.get_column_values())
        return rows

    def read_from_csv(self, input_file, delimiter):
        """
        Read search results from a CSV file (header required).
        :param input_file: Path to the CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        """

        # read CSV as UTF-8 encoded file (see also http://stackoverflow.com/a/844443)
        with codecs.open(input_file, encoding='utf8') as fp:
            logger.info("Reading search results from " + input_file + "...")

            reader = csv.reader(fp, delimiter=delimiter)

            # read header
            header = next(reader, None)
            if not header:
                raise IllegalArgumentError("Missing header in CSV file.")

            venue_index = header.index("venue")
            year_index = header.index("year")
            identifier_index = header.index("identifier")

            query_index = header.index("query")
            rank_index = header.index("rank")
            url_index = header.index("url")
            title_index = header.index("title")
            snippet_index = header.index("snippet")

            # read CSV file
            for row in reader:
                if row:
                    self.values.append(
                        SearchResult(row[query_index], row[rank_index],
                                     row[url_index], row[title_index], row[snippet_index])
                    )
                else:
                    raise IllegalArgumentError("Wrong CSV format.")

        self.filename = os.path.basename(input_file)
        logger.info(str(len(self.values)) + " search results have been imported.")

    def write_to_csv(self, output_dir, delimiter, filename=None):
        """
        Export search results to a CSV file.
        :param filename: Filename of file to export
        :param output_dir: Target directory for generated CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        """

        if filename is not None:
            self.filename = filename

        if len(self.values) == 0:
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
            try:
                for row in self.get_rows():
                    if len(row) == len(column_names):
                        writer.writerow(row)
                        count = count + 1
                    else:
                        raise IllegalArgumentError(
                            str(abs(len(column_names) - len(row))) + ' parameter(s) is/are missing for query "'
                            + str(row) + '"')

            except UnicodeEncodeError:
                logger.error('Encoding error while writing data for query: ' + str(query))

            logger.info(str(count) + ' search results have been exported.')
