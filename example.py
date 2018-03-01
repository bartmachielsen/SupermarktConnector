from Connector.AHConnector import AHConnector
from Connector.JumboConnector import JumboConnector
import json

def use_connector(connector, file_name):
    categorys = connector.get_categorys() # get all the categorys
    result = connector.get_products(categorys[0]["id"]) # just select the first one
    
    with open(file_name, "w") as example_file:
        example_file.write(json.dumps(result)) # convert to json and save
    

if __name__ == "__main__":
    use_connector(AHConnector(), "ah-example.json")
    use_connector(JumboConnector(), "jumbo-example.json")