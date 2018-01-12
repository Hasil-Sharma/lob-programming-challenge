from collections import namedtuple

Address = namedtuple( "Address", "name, address_line1, address_line2, address_city, address_zip, address_state" )


class AddressObj( Address ):
    def get_lookup_address(self):
        """
        Method to create lookup address to use in Civic API
        :return: str
        """
        return "%s %s %s %s %s".strip() % (self.address_line1,
                                           self.address_line2 if self.address_line2 else '',
                                           self.address_city,
                                           self.address_state,
                                           self.address_zip)

    @classmethod
    def get_address_obj(cls, **kwargs):
        """
        Set parameters passed in as kwargs and None to the parameters not passed
        :return: AddressObj
        """
        nkwargs = {}
        for key in cls._fields:
            value = kwargs.get( key, None )
            if isinstance( value, basestring ):
                nkwargs[key] = value.strip() if value and len( value.strip() ) > 0 else None
            else:
                nkwargs[key] = value
        return cls.__new__( cls, **nkwargs )
