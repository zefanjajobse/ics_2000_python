
class InvalidAuthException(Exception):
    """When the authentication failed"""
    
class InvalidHomeException(Exception):
    """When selected home does not exist as a option"""

class InvalidMacOrAuthException(Exception):
    """When the auth or mac address is not set"""

class NoHomeSelectedException(Exception):
    """When no home is selected"""