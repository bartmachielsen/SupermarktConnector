import requests

HEADERS = {
    'User-Agent': 'android/6.29.3 Model/phone Android/7.0-API24',
    'Host': 'ms.ah.nl',
}


class AHConnector:
    @staticmethod
    def get_anonymous_access_token():
        response = requests.post(
            'https://ms.ah.nl/create-anonymous-member-token',
            headers=HEADERS,
            params={"client": "appie-anonymous"}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def __init__(self):
        self._access_token = self.get_anonymous_access_token()

    def search_products(self, query=None, page=0, size=750, sort='RELEVANCE'):
        response = requests.get(
            'https://ms.ah.nl/mobile-services/product/search/v2?sortOn=RELEVANCE',
            params={"sortOn": sort, "page": page, "size": size, "query": query},
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
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
        response = self.search_products(page=0, **kwargs)
        yield from response['products']

        for page in range(1, response['page']['totalPages']):
            response = self.search_products(page=page, **kwargs)
            yield from response['products']

    def get_product_by_barcode(self, barcode):
        response = requests.get(
            'https://ms.ah.nl/mobile-services/product/search/v1/gtin/{}'.format(barcode),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_product_details(self, product):
        """
        Get advanced details of a product
        :param product: Product ID (also called webshopId) or original object containing webshopId
        :return: dict containing product information
        """
        product_id = product if not isinstance(product, dict) else product['webshopId']
        response = requests.get(
            'https://ms.ah.nl/mobile-services/product/detail/v3/fir/{}'.format(product_id),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_categories(self):
        response = requests.get(
            'https://ms.ah.nl/mobile-services/v1/product-shelves/categories',
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_sub_categories(self, category):
        category_id = category if not isinstance(category, dict) else category['id']
        response = requests.get(
            'https://ms.ah.nl/mobile-services/v1/product-shelves/categories/{}/sub-categories'.format(category_id),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    connector = AHConnector()
    # print(connector.search_products())
    # print(len(list(connector.search_all_products(query='smint'))))
    # print(connector.get_product_details(connector.get_product_by_barcode('8410031965902')))
    # print(connector.get_categories())
    print(connector.get_sub_categories(connector.get_categories()[0]))