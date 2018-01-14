import logging

import requests
from utils import validate_config
from _helperclass import AddressObj
from utils import pp

logger = logging.getLogger('civic-api')

civicapi_default_config_dict = {
    "url": "https://www.googleapis.com/civicinfo/v2/representatives",
    "fields": "officials(name, address(city, state, zip, line1, line2))",
}


class CivicApi(object):
    def __init__(self, key, **civicapi_config_dict):
        self.config_dict = civicapi_config_dict

        if 'fields' in self.config_dict:
            logger.warn("Using custom 'field' value not recommended !!!")
        for k, v in civicapi_default_config_dict.items():
            if k not in self.config_dict:
                self.config_dict[k] = v
        self.config_dict["key"] = key
        logger.info("Configuration after reading configurations and adding defaults:\n%s", pp(self.config_dict))
        validate_config(self.config_dict, "civic-api")

    def get_representative_address(self, address):
        parameter_dict = self.config_dict.copy()
        parameter_dict["address"] = address
        del parameter_dict["url"]
        response = requests.get(self.config_dict["url"], params=parameter_dict)
        logger.info("Requesting URL: %s", self.config_dict["url"])
        logger.info("Request Parameters:\n%s", pp(parameter_dict))
        try:
            response_dict = response.json()
            logger.info("Response from Google:\n%s", pp(response_dict))

            if response.status_code != 200:
                logger.error("Google Civic API didn't return success:\n%s", pp(response_dict))
                exit(1)

            if "officials" in response_dict:
                # Using the last legislator of all the legislators returned
                official_dict = response_dict["officials"][-1]
                _address_dict = {"address_%s" % k: v for k, v in official_dict["address"][0].items()}
                _address_dict["name"] = official_dict["name"]
                address_obj = AddressObj.get_address_obj(**_address_dict)
                return address_obj
            else:
                logger.error("Civic API didn't return any legislator")
                exit(1)
        except ValueError:
            logger.error("Civic API: unable to decode response json")
            exit(1)
