import errno
import logging
import re
import sys
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

    special_character_regex = re.compile("\\s*[()/\\\\?;:,]+\\s*")

    def __init__(self, query_string, exact_matches, remove_special_characters):
        self.query_string = str(query_string)
        self.is_empty = False

        if remove_special_characters:
            sub_queries = list(filter(lambda q: len(q) > 0, Query.special_character_regex.split(query_string)))

            if len(sub_queries) == 0:
                self.is_empty = True
            else:
                if exact_matches:
                    self.query_string = '"' + '" "'.join(sub_queries) + '"'
                else:
                    self.query_string = ' '.join(sub_queries)
        else:
            self.query_string = str(query_string).strip()

            if len(self.query_string) == 0:
                self.is_empty = True
            elif exact_matches:
                self.query_string = '"' + self.query_string + '"'

        self.uri = 'https://duckduckgo.com/html/?q=' + urllib.parse.quote(self.query_string)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept-Language": "en"
        }

        self.search_results = SearchResultList()

        # session for data retrieval
        self.session = requests.Session()

    def retrieve_search_results(self, max_results, min_wait, max_wait, depth=0):
        if self.is_empty:
            return

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

                    if len(url) == 0 or len(title) == 0:
                        logger.info("Rank " + str(rank) + " empty for query: " + str(self))
                    else:
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

                    if len(self.search_results.values) == 0:
                        logger.info("No search results retrieved for query: " + str(self))
                        self.is_empty = True

                if not self.is_empty:
                    logger.info('Successfully parsed result list for query: ' + str(self))
            else:
                logger.error('An error occurred while retrieving result list for query: ' + str(self))

        except (ConnectionError, OSError, requests.exceptions.RequestException) as e:
            logger.error('An error occurred while retrieving result list for query: ' + str(self))
            if depth <= 5 and (isinstance(e, requests.exceptions.RequestException)
                               or (type(e) == OSError and e.errno == errno.ENETDOWN)):
                logger.info('Retrying after one minute... ')
                time.sleep(60)
                self.retrieve_search_results(max_results, min_wait, max_wait, depth + 1)
            elif type(e) == ConnectionError or isinstance(e, requests.exceptions.RequestException):
                logger.info('Continuing with next query...')
                return
            else:
                logger.error('Terminating.')
                sys.exit(1)

    def __str__(self):
        return str(self.query_string)
