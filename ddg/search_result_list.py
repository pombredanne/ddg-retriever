import codecs
import csv
import logging
import os

from langdetect.lang_detect_exception import LangDetectException

from ddg.search_result import SearchResult
from util.exceptions import IllegalArgumentError
from langdetect import detect, DetectorFactory

logger = logging.getLogger("ddg-retriever_logger")


class SearchResultList(object):
    """ List of search results. """

    def __init__(self):
        self.filename = ""
        self.values = list()

    def get_rows(self, include_languages):
        rows = []
        for result in self.values:
            rows.append(result.get_column_values(include_languages))
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

    def detect_languages(self):
        logger.info("Detecting snippet languages...")
        DetectorFactory.seed = 0

        for search_result in self.values:
            try:
                search_result.language = detect(search_result.snippet)
            except LangDetectException:
                search_result.language = "error"

    def write_to_csv(self, output_dir, delimiter, include_language, filename=None):
        """
        Export search results to a CSV file.
        :param include_language: Add column "language" if tool was configured to detect languages of snippets
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

            column_names = SearchResult.get_column_names(include_language)

            # write header of CSV file
            writer.writerow(column_names)

            count = 0
            try:
                for row in self.get_rows(include_language):
                    if len(row) == len(column_names):
                        writer.writerow(row)
                        count = count + 1
                    else:
                        raise IllegalArgumentError(
                            str(abs(len(column_names) - len(row))) + ' parameter(s) is/are missing for "'
                            + str(row) + '"')

            except UnicodeEncodeError:
                logger.error('Encoding error while writing data for: ' + str(row))

            logger.info(str(count) + ' search results have been exported.')
