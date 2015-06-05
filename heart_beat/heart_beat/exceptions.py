"""All of the custom exceptions found in heart_beat and what they are used for
"""
class VersionMismatch(Exception):
    """Error that's raised when the version in a ping isn't the one running
    on the server.
    """
    pass

class NonUnixTimestamp(Exception):
    """For when non-unix timestamps are passed to ping."""
    pass

class ESRSNotBool(Exception):
    """For when the EMC Secure Remote Services Value for a ping isn't a
    boolean"""
    pass

class SRNumberNotInt(Exception):
    """For when the service request ID (number) isn't an integer"""
    pass
