import datetime

from . import db


class DiagnosticPingData(db.Model):
    """
    Table declarations for the logset self service usage reporting tool. All
    of the data must be present in order for a row to be inserted into the
    database.
    
    ASSUMPTION: A machine is going to send data to the heart_beat flask app
                and as such there will be no malformed data.
    
    ASSUMPTION: heart_beat expects to get client_start_teme and 
                logset_gather_time in a Unix Time format and will convert that
                format into a database ISO 8601 format for humans to read.
    """
    __tablename__ = "diagnostic_ping_data"

    ping_id = db.Column(
            db.Integer,
            primary_key=True,
            nullable=False,
            autoincrement=True)
    db_insert_time = db.Column(
            db.DateTime,
            default=db.func.now(),
            onupdate=db.func.now(),
            nullable=False)
    client_start_time = db.Column(
            db.DateTime,
            nullable=False)
    logset_gather_time = db.Column(
            db.DateTime,
            nullable=False)
    onefs_version = db.Column(db.String(24), nullable=False)
    esrs_enabled = db.Column(db.Boolean, nullable=False)
    tool_version = db.Column(db.String(24), nullable=False)
    sr_number = db.Column(db.Integer(), nullable=False)

    def __init__(
            self,
            client_start_time=None,
            logset_gather_time=None,
            onefs_version=None,
            esrs_enabled=None,
            tool_version=None,
            sr_number=None,):

        client_start_epoch_time = int(client_start_time)
        logset_gather_epoch_time = int(logset_gather_time)

        ISO_8601_client = datetime.datetime.utcfromtimestamp(
            client_start_epoch_time)
        ISO_8601_gather = datetime.datetime.utcfromtimestamp(
            logset_gather_epoch_time)

        self.client_start_time=ISO_8601_client
        self.logset_gather_time=ISO_8601_gather
        self.onefs_version=onefs_version
        self.esrs_enabled=esrs_enabled
        self.tool_version=tool_version
        self.sr_number=sr_number

    def __repr__(self):
        """
        Returns all of the internal attribute values of the DiagnosticPingData
        object __repr__ is called on.
        """
        return ("<DiagnosticPingData db_insert_time={}, client_start_time={}, "
            "logset_gather_time={}, onefs_version={}, esrs_enabled={}, "
            "tool_version={}, sr_number={}>").format(
            self.db_insert_time,
            self.client_start_time,
            self.logset_gather_time,
            self.onefs_version,
            self.esrs_enabled,
            self.tool_version,
            self.sr_number,)
