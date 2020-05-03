# SupermarketConnector

An python project for getting products and categories from some major sumpermarkets in the Netherlands.

See [example.py](https://github.com/bartmachielsen/SupermarktConnector/blob/master/example.py) for an simple example.

## Required

This application is written for Python 3 (But should be compatible with Python 2.7)

### Requests

To keep the http-requests simple and not version dependant the requests library is used. Make sure to install this library before running the example:
`python -m install requests`

## Method

For getting the products from the supermarkets the data of the mobile app is analyzed. This app makes use of the public api behind those apps.

## Albert Heijn

The AH makes use of an backend Rest-API that uses multiple security techniques to limit the data to only app users.

The location of the backend:    [```ms.ah.nl/rest/ah/```](ms.ah.nl/rest/ah)

- **Basic authentication**
    _Any request should contain an authentication-key so that the backend knows that the user is valid._

- **X-Digest**
    _This X-Digest is an hashed value that uses SHA1 to check if the request is valid and made by the original android app. The logic behind this hash is:_

    `X_DIGEST = URL + PARAMETERS + USERNAME + POST_BODY (Max 1000 bytes) + SECRET_PASSWORD`

    _This mechanism is copied into this application_

## Jumbo Supermarkten

The jumbo also has an app that makes it possible to search products. By looking at the data communication it is clearly visible that this app does not use any security mechanism. The only key or token that is used is used for setting an given supermarket as the shop that you want to order from. By implementing this **X-jumbo-token** it is possible to switch between different stores and determine the price difference between certain stores.

The backend location:   ```mobileapi.jumbo.com```

All the stores of the jumbo are sorted in 5 different categories, the logic behind which store is more expensive is difficult because it is dependant of which products you are looking for.

I created an [interactive map](https://www.google.com/maps/d/u/0/edit?mid=1uPq5t6Ymcjs9TbrNbyAl5uS08sY&ll=51.93466534760809%2C6.304439426712179&z=8) which sorts all the stores by category.

![Jumbo prices](/jumbo-prices.jpg)
