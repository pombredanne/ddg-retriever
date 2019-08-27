import logging
import urllib.parse

import requests

from lxml import html

from ddg.search_result import SearchResult

logger = logging.getLogger("ddg-retriever_logger")


class Query(object):
    """ A venue on DBLP. """

    def __init__(self, query_string, exact_matches):
        self.query_string = '"' + str(query_string) + '"' if exact_matches else str(query_string)
        self.uri = 'https://duckduckgo.com/html/?q=' + urllib.parse.quote(self.query_string)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept-Language": "en"
        }

        self.search_results = []

        # session for data retrieval
        self.session = requests.Session()

    def retrieve_search_results(self):
        try:
            # retrieve data
            response = self.session.get(self.uri, headers=self.headers)

            if response.ok:
                logger.info('Successfully retrieved search results for query: ' + str(self))

                tree = html.fromstring(response.content)
                items = tree.xpath('//div[@class="results"]'
                                   '/div[contains(@class, "result")]'
                                   '/div[contains(@class, "result__body")]')

                rank = 0
                for item in items:
                    title = "".join(item.xpath('h2[@class="result__title"]/a[@class="result__a"]/descendant::text()'))
                    url = "".join(item.xpath('h2[@class="result__title"]/a[@class="result__a"]/@href'))
                    snippet = "".join(item.xpath('a[@class="result__snippet"]/descendant::text()'))

                    rank += 1
                    self.search_results.append(SearchResult(
                        self.query_string,
                        str(rank),
                        url,
                        title,
                        snippet
                    ))

                logger.info('Successfully parsed result list for query: ' + str(self))
            else:
                logger.error('An error occurred while retrieving result list for query: ' + str(self))

        except ConnectionError:
            logger.error('An error occurred while retrieving result list for query: ' + str(self))

    def get_rows(self):
        rows = []
        for query in self.search_results:
            rows.append(query.get_column_values())
        return rows

    def __str__(self):
        return str(self.query_string)
