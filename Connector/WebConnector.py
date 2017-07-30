def parameterize_url(url, parameters):
    """Function for adding parameters from a dictionairy to a string object
    The parameters can be None or empty. The original URL will be returned"""

    if parameters is None or len(parameters.keys()) == 0:
        return url
    for index, key in enumerate(parameters.keys()):
        if index != 0:
            url += "&"
        else:
            url += "?"
        url += str(key) + "=" + str(parameters[key])
    return url

def succes(status_code):
    """Check the response code from the http-result"""
    return status_code in [200,201]

class Connector:
    """Connector is a base class for different supermarket connections"""

    # METHODS that are used to connect to a website.
    GET = "GET"
    POST = "POST"
    PUT = "PUT"

    @property
    def host(self):
        return None

    @property
    def products_category(self):
        return None

    @property
    def categorys(self):
        return None

    def __init__(self):
        """Base constructor that does not have a purpose yet.."""
        pass

    def request(self, method, host, url, parameters=None, body=None):
        """Function for requesting a page from the connector.
        Parameters and body are optional
        Method should be a string like GET, POST, PUT... or object like Connector.GET
        The host is the base adress like www.x.nl
        The url is the directory on the host"""
        pass

    def get_products(self, category, page=0, amount=25):
        return self.request(Connector.GET,
                            self.host, self.products_category.format(CATEGORY_ID=category),
                            {"page": page, "size": amount})

    def get_categorys(self, head_category=None):
        return self.request(Connector.GET, self.host, self.categorys)