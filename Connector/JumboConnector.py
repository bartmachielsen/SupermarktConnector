import requests
from Connector.WebConnector import Connector, succes

class JumboConnector(Connector):



    @property
    def host(self):
        return "http://mobileapi.jumbo.com"

    @property
    def products_category(self):
        return "/v2/products"

    @property
    def categorys(self):
        return "/v2/categories"

    def __init__(self):
        Connector.__init__(self)

    def request(self, method, host, url, parameters=None, body=None):
        response = requests.request(method, host+url, params=parameters, data=body)
        if succes(response.status_code):
            return response.json()

    def get_products(self, category, page=0, amount=25):
        return self.request(Connector.GET,
                            self.host, self.products_category,
                            {"categoryId":category, "count":amount})

    def get_categorys(self, head_category=None):
        params = {}
        if head_category is not None:
            params = {id:head_category}
        return self.request(Connector.GET,
                            self.host, self.categorys,
                            params)


if __name__ == "__main__":
    conn = JumboConnector()
    print(conn.get_products("SG13HG4_2"))
