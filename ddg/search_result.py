import logging

logger = logging.getLogger("ddg-retriever_logger")


class SearchResult(object):
    """ Search result retrieved from Duck Duck Go. """

    def __init__(self, query, rank, url, title, snippet):
        self.query = query
        self.rank = rank
        self.url = url
        self.title = title
        self.snippet = snippet
        self.language = None

    def __str__(self):
        return str(self.title)

    def get_column_values(self, include_language=False):
        if include_language:
            return [self.query, self.rank, self.language, self.url, self.title, self.snippet]
        else:
            return [self.query, self.rank, self.url, self.title, self.snippet]

    @classmethod
    def get_column_names(cls, include_language=False):
        if include_language:
            return ["query", "rank", "language", "url", "title", "snippet"]
        else:
            return ["query", "rank", "url", "title", "snippet"]
