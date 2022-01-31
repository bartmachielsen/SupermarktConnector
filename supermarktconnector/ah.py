import requests
from pprint import pprint
from datetime import datetime

HEADERS = {
    'Host': 'api.ah.nl',
    'x-dynatrace': 'MT_3_4_772337796_1_fae7f753-3422-4a18-83c1-b8e8d21caace_0_1589_109',
    'x-application': 'AHWEBSHOP',
    'user-agent': 'Appie/8.8.2 Model/phone Android/7.0-API24',
    'content-type': 'application/json; charset=UTF-8',
}


class AHConnector:
    @staticmethod
    def get_anonymous_access_token():
        response = requests.post(
            'https://api.ah.nl/mobile-auth/v1/auth/token/anonymous',
            headers=HEADERS,
            json={"clientId": "appie"}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def __init__(self):
        self._access_token = self.get_anonymous_access_token()

    def search_products(self, query=None, page=0, size=750, sort='RELEVANCE'):
        response = requests.get(
            'https://api.ah.nl/mobile-services/product/search/v2?sortOn=RELEVANCE',
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
            'https://api.ah.nl/mobile-services/product/search/v1/gtin/{}'.format(barcode),
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
            'https://api.ah.nl/mobile-services/product/detail/v4/fir/{}'.format(product_id),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_categories(self):
        response = requests.get(
            'https://api.ah.nl/mobile-services/v1/product-shelves/categories',
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_sub_categories(self, category):
        category_id = category if not isinstance(category, dict) else category['id']
        response = requests.get(
            'https://api.ah.nl/mobile-services/v1/product-shelves/categories/{}/sub-categories'.format(category_id),
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_bonus_periods(self):
        """
        Information about the current bonus periods active.
        Returns a list with all periods, each period has a start and end date and sections, to view the products
        you need the sections within 'urlMetadataList' using 'get_bonus_periods_products'
        """
        response = requests.get(
            'https://api.ah.nl/mobile-services/bonuspage/v1/metadata',
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()['periods']

    def get_bonus_periods_groups_or_products(self, url):
        response = requests.get(
            f'https://api.ah.nl/mobile-services/{url}',
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_bonus_group_products(self, group_id, date):
        response = requests.get(
            f'https://api.ah.nl/mobile-services/bonuspage/v1/segment',
            headers={**HEADERS, "Authorization": "Bearer {}".format(self._access_token.get('access_token'))},
            params={"date": date.strftime('%Y-%m-%d'), "segmentId": group_id, "includeActivatableDiscount": "false"}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get_all_bonus_products(self, date=None):
        """
        Get all available bonus products in a certain period, pass a datetime or date object to filter on a specific date
        default is None which means current date
        """
        date = date or datetime.today()

        for period in self.get_bonus_periods():
            if date < datetime.strptime(period['bonusStartDate'], '%Y-%m-%d') or date > datetime.strptime(period['bonusEndDate'], "%Y-%m-%d"):
                continue

            for meta_data in period['urlMetadataList']:
                for bon_group_or_prod in \
                        self.get_bonus_periods_groups_or_products(meta_data['url'])['bonusGroupOrProducts']:

                    if bon_group_or_prod.get('product'):
                        yield bon_group_or_prod['product']

                    if bon_group_or_prod.get('bonusGroup'):
                        for product in \
                                self.get_bonus_group_products(bon_group_or_prod['bonusGroup']['id'], date).get('products', []):
                            yield product


if __name__ == '__main__':
    connector = AHConnector()
    # pprint(connector.search_products())
    # pprint(len(list(connector.search_all_products(query='smint'))))
    # pprint(connector.get_product_details(connector.get_product_by_barcode('8410031965902')))
    # pprint(connector.get_categories())
    # pprint(connector.get_sub_categories(connector.get_categories()[0]))

    # pprint(connector.search_products('Smint')['products'])

    # pprint(connector.get_product_details(177119))

    # pprint(connector.get_bonus_periods())
    # pprint(connector.get_bonus_periods_products(connector.get_bonus_periods()[0]['urlMetadataList'][0]['url']))

    for bonus_prod in connector.get_all_bonus_products():
        print(bonus_prod)
