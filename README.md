# SupermarketConnector

![Publish](https://github.com/bartmachielsen/SupermarktConnector/workflows/Publish/badge.svg)

Collecting product information from Dutch supermarkets: Albert Heijn and Jumbo

## Getting Started
Install the Pip package
```bash
pip install supermarktconnector
```

## Sample
Import the jumbo connector and search for a product
```python
from supermarktconnector.jumbo import JumboConnector
connector = JumboConnector()
connector.search_products(query='Smint', size=1, page=0)
```
```json
{
  "products": {
    "data": [
      {
        "id": "70942PAK",
        "title": "Smint Peppermint Sugarfree 100 Stuks 2 x 35g",
        "quantityOptions": [
          {
            "defaultAmount": 1,
            "minimumAmount": 1,
            "amountStep": 1,
            "unit": "pieces",
            "maximumAmount": 99
          }
        ],
        "prices": {
          "price": {
            "currency": "EUR",
            "amount": 365
          },
          "unitPrice": {
            "unit": "kg",
            "price": {
              "currency": "EUR",
              "amount": 5214
            }
          }
        },
        "available": true,
        "productType": "Product",
        "quantity": "2 x 35 g",
        "imageInfo": {
          "primaryView": [
            {
              "url": "https://ish-images-static.prod.cloud.jumbo.com/product_images/240420200540_70942PAK-1_360x360.png",
              "height": 360,
              "width": 360
            }
          ]
        }
      }
    ]
  }
}
```

You can also get the different product-categories:
```python
from supermarktconnector.ah import AHConnector
connector = AHConnector()
connector.get_categories()
```
```json
[
  {
    "id": 6401,
    "name": "Aardappel, groente, fruit",
    "images": [
      {
        "height": 400,
        "width": 600,
        "url": "https://static.ahold.com//cmgtcontent/media//002304400/000/002304468_001_groenten-fruit.png"
      }
    ],
    "nix18": false
  }
]
```

## Deprecated
### X-Digest (Albert Heijn)
The Albert Heijn used a special X-Digest for verifying that the app data traffic was coming from the backend, in the new versions this has been removed.

_This X-Digest is an hashed value that uses SHA1 to check if the request is valid and made by the original android app. The logic behind this hash is:_

`X_DIGEST = URL + PARAMETERS + USERNAME + POST_BODY (Max 1000 bytes) + SECRET_PASSWORD`

### Price differences (Jumbo)
In the past all the the jumbo stores where divided over 5 different categories, with each category a different price for some of the products. The token used for store identification is no longer working in the new versions, It might be handled on the backend.

I created an [interactive map](https://www.google.com/maps/d/u/0/edit?mid=1uPq5t6Ymcjs9TbrNbyAl5uS08sY&ll=51.93466534760809%2C6.304439426712179&z=8) which sorts all the stores by category.

![Jumbo prices](/jumbo-prices.jpg)
