import logging

logger = logging.getLogger( 'Validation' )


def validate_config(conf_dict, key):
    def check_key(_conf_dict, _key, msg):
        if _key not in _conf_dict:
            logger.error( msg )
            exit( 1 )

    def check_extra_keys(msg, *args):
        set_args = map( set, args )
        diff = reduce( lambda x, y: x ^ y, set_args )
        if len( diff ) != 0:
            logger.error( msg, key, ", ".join( diff ) )
            exit( 1 )

    if key == 'auth':
        # Check if keys and sub-key are present
        possible_subkeys = ["civic-key", "lob-key"]

        logger.info( "Checking for 'auth' specification" )
        check_key( conf_dict, key, "civic-api key and lob-api key not specified properly. Please specify in"
                                   " configuration file or pass via --civic-key and --lob-key" )

        logger.info( "Checking for civic-api key specification" )
        check_key( conf_dict["auth"], possible_subkeys[0], "civic-api key not specified. Please specify it "
                                                           "in configuration file or pass via --civic-key" )

        logger.info( "Checking for lob-api key specification" )
        check_key( conf_dict["auth"], possible_subkeys[1], "lob-api key not specified. Please specify it in "
                                                           "configuration file or pass via --lob-key" )

        # Checking for extra key specification
        logger.info( "Checking for extra keys specified in configuration file" )
        check_extra_keys( "Unknown key(s) specified in %s: %s", possible_subkeys, conf_dict["auth"].keys() )


def validate_input(input_dict):
    logger.info( "Validating Input File" )

    def checker(key):
        if key not in input_dict:
            logger.error( "Required Field not not specified in input: %s", key )
            exit( 1 )

    required_variables = ["name", "address_line1", "address_city", "address_state", "address_zip"]
    map( checker, required_variables )
