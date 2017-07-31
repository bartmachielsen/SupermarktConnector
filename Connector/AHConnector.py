import requests
import hashlib
import base64
import json
from Connector.WebConnector import Connector, parameterize_url, succes

class AHConnector(Connector):
    """The AH connector is the class that is responsable for connecting to the webserver of Albert Heijn
    It uses the AH Rest service for getting products/details and other information
    The AH uses this rest service for its mobile clients"""

    # The secret digest is a key used for creating a x_digest. It could be that this changes over time.
    # It can be found in the mobile app called Appie
    SECRET_DIGEST = "G00gMo81L"

    # The host address of the AH website
    HOST = "https://ms.ah.nl"

    GEN_PASSWORD = "/rest/ah/v1/member-util/generate-password"

    @property
    def host(self):
        return AHConnector.HOST

    @property
    def products_category(self):
        return "/rest/ah/taxonomy/categories/{CATEGORY_ID}/products"

    @property
    def categorys(self):
        return "/rest/ah/taxonomy/categories"

    @staticmethod
    def calculate_xdigest(url, body, username):
        """Function is used for calculating the SHA1 X-digest that is used to securely check if the user is valid
        Needed by AH websites to check
        The url is used without the host details!"""

        url_bytes = bytearray(url, 'UTF-8')
        body_bytes = bytearray()
        if body is not None:
            body_bytes = bytearray(body, 'UTF-8')[0:1000]
        member_bytes = bytearray(username, 'UTF-8')
        digest_bytes = bytearray(AHConnector.SECRET_DIGEST, 'UTF-8')
        total_bytes = bytearray()
        total_bytes.extend(url_bytes)
        total_bytes.extend(body_bytes)
        total_bytes.extend(member_bytes)
        total_bytes.extend(digest_bytes)
        return hashlib.sha1(total_bytes).hexdigest()

    def __init__(self):
        """Constructor for creating a AHConnector object. the username and password are filled"""

        Connector.__init__(self)
        self.password = AHConnector.request_password()
        self.username = AHConnector.request_username(self.password)

    @staticmethod
    def request_password():
        """It requests a password from the ah server.."""

        response = requests.get(AHConnector.HOST + AHConnector.GEN_PASSWORD)
        if succes(response.status_code):
            return str(response.json()['password'])

    @staticmethod
    def request_username(password):
        """This function is responsable for requesting the username from the ah website.
        The other data that is given is not used (like address)"""

        response = requests.post(AHConnector.HOST + "/rest/ah/v1/members",json.dumps({"password":password}),headers={'Content-Type':'application/json'})
        if succes(response.status_code):
            return str(response.json()['memberId'])

    def request(self, method, host, url, parameters=None, body=None):
        """This method is used when you created a AHConnector object and you want to request pages.
        The reason why this method exists is to fill the username and password. It also checks if those are available
        The method is GET,POST,PUT ... or the corresponding objects in Connector.GET (it is a string)
        The parameters and body are optional WARNING! body is always used when given!"""

        if self.username is not None and self.password is not None:
            return AHConnector.response(method, host,url, parameters, body,self.username, self.password)

    @staticmethod
    def response(method, host, url, parameters, body, username, password):
        """This function is responsable for executing the requested method on the given host with the url as path.
        Parameters and body are optional and can be None. WARNING! body is always used when given!
        The username and password are requested when creating the AHConnector."""

        headers = {
            # "Accept": "application/vnd.ah.taxonomy.category.product.withfilters+json", # header not needed
            "Content-Type": "application/json", # header needed
            "Deliver-Errors-In-Json": "true",   # header optional
            "X-ClientName": "android",          # header needed
            "X-ClientVersion": "5.2.1",         # header needed
            "X-Digest":
                AHConnector.calculate_xdigest(parameterize_url(url, parameters), body, username),   # header needed
            "User-Agent": "android/5.2.1 Model/phone Android/6.0.1-API23 Member/"+username, # header needed
            "Authorization":
                "Basic "+
                base64.b64encode(bytes("{}:{}".format(username, password))).decode("UTF-8"), # header needed
            "Host": "ms.ah.nl", # header needed
            # "Connection": "Keep-Alive", # header not needed
            # "Accept-Encoding": "gzip"   # header not needed
        }
        try:
            result = requests.request(method, host+url,
                                  params=parameters, headers=headers)

            if succes(result.status_code): # check if not failed!
                return result.json()
        except Exception as e:
            print e


    def get_categorys(self, head_category=None):
        categories = []
        response = Connector.get_categorys(self, head_category)

        if response is None:
            return categories
        for category in response["levelFilterElementCommands"]:
            categories.append({"title":category["title"], "id":category["value"]})
        return categories

