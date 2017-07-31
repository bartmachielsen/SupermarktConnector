import requests
from Connector.WebConnector import Connector, succes


class JumboConnector(Connector):

    HOST = "http://mobileapi.jumbo.com"
    STORES = "/v2/stores"
    @property
    def host(self):
        return JumboConnector.HOST

    @property
    def products_category(self):
        return "/v2/products"

    @property
    def stores(self):
        return JumboConnector.STORES

    @property
    def categorys(self):
        return "/v2/categories"

    def __init__(self):
        Connector.__init__(self)
        self.homestore = None
        self.token = self.get_token()


    @staticmethod
    def get_token():
        result = requests.get(JumboConnector.HOST + "/v2/configuration")
        if succes(result.status_code):
            return result.headers["x-jumbo-token"]

    @staticmethod
    def get_stores():
        result = requests.get(JumboConnector.HOST + JumboConnector.STORES)
        if succes(result.status_code):
            return result.json()["stores"]["data"]

    def set_homestore(self, store_id, complex_id):
        self.homestore = store_id
        body ={
            "id":store_id,
            "complexNumber":complex_id
        }
        self.request(Connector.PUT, self.host, "/v2/users/me/homestore",body=body)

        respond = self.request(Connector.GET, self.host, "/v2/basket", body={})
        return respond["basket"]["data"]["usedPriceLine"]["pricing"]


    def request(self, method, host, url, parameters=None, body=None):
        headers = {"x-jumbo-token":self.token}

        response = requests.request(method, host+url, params=parameters, data=body, headers=headers)
        if succes(response.status_code):
            self.token = response.headers["x-jumbo-token"]
            return response.json()

    def get_products(self, category, page=0, amount=25):
        result = self.request(Connector.GET,
                            self.host, self.products_category,
                            {"categoryId":category, "count":amount, "offset":page})

        if result is None:
            return []

        return result


    def get_categorys(self, head_category=None):
        params = {}
        if head_category is not None:
            params = {"id":head_category}
        found_categories = self.request(Connector.GET,
                            self.host, self.categorys,
                            params)

        if found_categories is None:
            return []

        categories = []
        for category in found_categories['categories']['data']:
            cat_id = category["id"]
            sub_count = category["subCategoriesCount"]
            # if sub_count > 0:
            #     # categories.extend(self.get_categorys(cat_id))
            #     pass
            # else:
            categories.append({"id":cat_id,"title":category["title"]})
        return categories

