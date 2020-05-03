
class SupermarktConnectorException(Exception):
    pass


class PaginationLimitReached(SupermarktConnectorException):
    pass
