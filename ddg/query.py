import logging
import re
import urllib.parse
import requests
import time

from ddg.search_result import SearchResult
from random import randint
from lxml import html

from ddg.search_result_list import SearchResultList

logger = logging.getLogger("ddg-retriever_logger")


class Query(object):
    """ A venue on DBLP. """

    parentheses_regex = re.compile("\\s*[()]\\s*")

    def __init__(self, query_string, exact_matches, replace_parentheses):

        if replace_parentheses:
            sub_queries = filter(lambda q: len(q) > 0, Query.parentheses_regex.split(query_string))

            if exact_matches:
                self.query_string = '"' + '" "'.join(sub_queries) + '"'
            else:
                self.query_string = ' '.join(sub_queries)
        else:
            if exact_matches:
                self.query_string = '"' + str(query_string) + '"'
            else:
                self.query_string = str(query_string)

        self.uri = 'https://duckduckgo.com/html/?q=' + urllib.parse.quote(self.query_string)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept-Language": "en"
        }

        self.search_results = SearchResultList()

        # session for data retrieval
        self.session = requests.Session()

    def retrieve_search_results(self, max_results, min_wait, max_wait):
        try:
            # reduce request frequency as configured
            delay = randint(min_wait, max_wait)  # delay between requests in milliseconds
            time.sleep(delay / 1000)  # sleep for delay ms to prevent getting blocked

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
                    self.search_results.values.append(SearchResult(
                        self.query_string,
                        str(rank),
                        url,
                        title,
                        snippet
                    ))

                    # retrieve only up to max_results results
                    if rank == max_results:
                        break

                logger.info('Successfully parsed result list for query: ' + str(self))
            else:
                logger.error('An error occurred while retrieving result list for query: ' + str(self))

        except ConnectionError:
            logger.error('An error occurred while retrieving result list for query: ' + str(self))

    def __str__(self):
        return str(self.query_string)
