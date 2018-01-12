import logging
from collections import defaultdict

import lob

from utils import pp

logger = logging.getLogger( 'lob-api' )

lobapi_default_config_dict = {
    'file': '<html style="padding-top: 3in; margin: .5in;">{{message}}</html>',
    'description': "Default Configuration",
    'color': True,
    'html_variables': ["message"]
}


class LobApi( object ):
    def __init__(self, key, **lobapi_config_dict):
        lob.api_key = key
        self.config_dict = lobapi_config_dict
        for k, v in lobapi_default_config_dict.items():
            if k not in self.config_dict:
                self.config_dict[k] = v
        logger.info( "Configuration after reading configurations:\n%s", pp( self.config_dict ) )

    def fetch_url(self, to_address, from_address, variable_dict):
        param_dict = defaultdict( dict )
        param_dict.update( self.config_dict )
        for variable in self.config_dict["html_variables"]:
            try:
                param_dict["merge_variables"][variable] = variable_dict[variable]
            except KeyError:
                logger.error( "Mismatch in html_variables specification in input and configuration file: %s", variable )
                exit( 1 )

        del param_dict["html_variables"]
        logger.info( "From Address: %s", from_address )
        logger.info( "To Address: %s", to_address )
        logger.info( "Parameters: \n%s", pp( param_dict ) )
        try:
            letter = lob.Letter.create(
                from_address=from_address._asdict(),
                to_address=to_address._asdict(),
                **param_dict
            )
            return letter.url
        except Exception as e:
            logger.error( "Error: %s", e.message )
            exit( 1 )
