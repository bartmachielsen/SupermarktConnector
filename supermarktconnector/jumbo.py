import requests
from math import ceil
from supermarktconnector.errors import PaginationLimitReached
import logging
logger = logging.getLogger('supermarkt_connector')
logger.setLevel(logging.INFO)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0'
}


class JumboConnector:
    def search_products(self, query=None, page=0, size=30):
        if (page + 1 * size) > 30:
            raise PaginationLimitReached('Pagination limit on Jumbo connector of 30')

        response = requests.get(
            'https://mobileapi.jumbo.com/v9/search',
            headers=HEADERS,
            params={"offset": page * size, "limit": size, "q": query},
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def search_all_products(self, **kwargs):
        """
        Iterate all the products available, filtering by query or other filters. Will return generator.
        :param kwargs: See params of 'search_products' method, note that size should not be altered to optimize/limit pages
        :return: generator yielding products
        """
        size = kwargs.pop('size', None) or 30
        response = self.search_products(page=0, size=size, **kwargs)
        yield from response['products']['data']

        for page in range(1, ceil(response['products']['total'] / size)):
            try:
                response = self.search_products(page=page, **kwargs)
            except PaginationLimitReached as e:
                logger.warning('Pagination limit reached, capping response: {}'.format(e))
                return
            yield from response['products']['data']

    def get_product_by_barcode(self, barcode):
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/search',
            headers=HEADERS,
            params={"q": barcode},
        )
        if not response.ok:
            response.raise_for_status()
        products = response.json()['products']['data']
        return products[0] if products else None

    def get_product_details(self, product):
        """
        Get advanced details of a product
        :param product: Product ID or raw product object containing ID field
        :return: dict containing product information
        """
        product_id = product if not isinstance(product, dict) else product['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/products/{}'.format(product_id),
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_categories(self):
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/categories',
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['categories']['data']

    def get_sub_categories(self, category):
        category_id = category if not isinstance(category, dict) else category['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/categories',
            headers=HEADERS,
            params={"id": category_id}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['categories']['data']

    def get_all_stores(self):
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/stores',
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['stores']['data']

    def get_store(self, store):
        store_id = store if not isinstance(store, dict) else store['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/stores/{}'.format(store_id),
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['store']['data']

    def get_all_promotions(self):
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/promotion-overview',
            headers=HEADERS
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['tabs']

    def get_promotions_store(self, store):
        store_id = store if not isinstance(store, dict) else store['id']
        response = requests.get(
            'https://mobileapi.jumbo.com/v9/promotion-overview',
            headers=HEADERS,
            params={"store_id": store_id}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['tabs']

if __name__ == '__main__':
    from pprint import pprint
    connector = JumboConnector()
    # pprint(connector.search_products(query='Smint'))
    pprint(len(list(connector.search_all_products(query='Smint'))))
    # pprint(connector.get_product_details(connector.get_product_by_barcode('8410031965902')))
    # pprint(connector.get_categories())
    # pprint(connector.get_sub_categories(connector.get_categories()[0]))
