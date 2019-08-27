import logging

logger = logging.getLogger("ddg-retriever_logger")


class SearchResult(object):
    """ Search result retrieved from Duck Duck Go. """

    # TODO: Continue here tomorrow

    def __init__(self, query, rank, url, title, snippet):
        self.query = query
        self.rank = rank
        self.url = url
        self.title = title
        self.snippet = snippet

    def __str__(self):
        return str(self.title)

    def get_column_values(self):
        return [self.query, self.rank, self.url, self.title, self.snippet]

    @classmethod
    def get_column_names(cls):
        return ["query", "rank", "title", "url", "snippet"]
