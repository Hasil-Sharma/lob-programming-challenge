import json
import logging
from collections import defaultdict
from optparse import OptionParser

import colorlog
import yaml

from resources import AddressObj
from resources import CivicApi
from resources import LobApi
from utils import validate_config, validate_input, pp

# Setting up Logger
handler = colorlog.StreamHandler()
handler.setFormatter( colorlog.ColoredFormatter( '%(log_color)s[%(levelname)s]:[%(name)s] = %(message)s' ) )
logger = colorlog.getLogger()
logger.addHandler( handler )

parser = OptionParser()
parser.add_option( "-c", "--config", dest="config",
                   help="YAML configuration file containing API key(s) and other configurations" )
parser.add_option( "-g", "--civic-key", dest="civic_key",
                   help="Google Civic API Key (Overrides --config value) (Required in either --config or here)" )
parser.add_option( "-l", "--lob-key", dest="lob_key",
                   help="Lob API Key, (Overrides --config value) (Required in either --config or here)" )
parser.add_option( "-f", "--file", dest="input_file",
                   help="Json file to read input (Mandatory)" )
parser.add_option( "-i", "--html-id", dest="html_id",
                   help="ID of saved HTML template (Overrides --config specified)."
                        "Defaults to default template of single variables {{message}}" )
parser.add_option( "-v", "--verbose", action="store_true", dest="verbose",
                   help="Print verbose messages" )

(options, args) = parser.parse_args()

# Set Verbosity Level
if options.verbose:
    logger.setLevel( logging.INFO )
    logger.info( "Verbose Mode" )

config_dict = defaultdict( dict )

# Reading Configuration File
if options.config:
    logger.info( "Reading from configuration file: %s", options.config )
    try:
        with open( options.config ) as f:
            config_dict.update( yaml.load( f ) )
    except Exception as e:
        logger.error( "Error in reading configuration file: %s : %s", options.config, e.message )
        exit( 1 )
else:
    logger.info( "Using default configurations" )

# Updating default html templated
if options.html_id:
    config_dict["lob-api"]["file"] = options.html_id
    logger.info( "Updated HTML template to %s", options.html_id )

# Updating Google Civic API key
if options.civic_key:
    config_dict["auth"]["civic-key"] = options.civic_key
    logger.info( "Updated civic-key to %s", options.civic_key )

# Updating Lob API key
if options.lob_key:
    config_dict["auth"]["lob-key"] = options.lob_key
    logger.info( "Updated lob-key to %s", options.lob_key )

# Validating Authentication keys
validate_config( config_dict, "auth" )

# Reading Address Input
input_dict = defaultdict( dict )
if options.input_file:
    try:
        with open( options.input_file ) as f:
            input_dict = json.load( f )
    except Exception as e:
        logger.error( "Error in reading input file: %s %s", options.input_file, e.message )
        exit( 1 )
else:
    logger.error( "Must specify input file" )
    exit( 1 )

if 'html_variables' in input_dict:
    pass
elif 'message' in input_dict:
    input_dict["html_variables"]["message"] = input_dict["message"]
else:
    logger.error(
        "html_variables or message not defined in input."
        "Please specify 'message' for default html"
        "template or 'html_variables' as dictionary of custom variables (as per your html template)" )

# Validating Input
validate_input( input_dict )

logger.info( "Final Configurations (Default values used if nothing specified):\n%s", pp( config_dict ) )

# Creating look up address to use with Civic API
from_address = AddressObj.get_address_obj( **input_dict )
lookup_address = from_address.get_lookup_address()

logger.info( "Lookup Address to use with Google Civic API: %s", lookup_address )
civicApi = CivicApi( config_dict["auth"]["civic-key"], **config_dict["civic-api"] )
to_address = civicApi.get_representative_address( lookup_address )
lob_api = LobApi( config_dict["auth"]["lob-key"], **config_dict["lob-api"] )
url = lob_api.fetch_url( to_address, from_address, input_dict["html_variables"] )
print url
