from . import db


class DiagnosticPingData(db.Model):
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
    one_fs_version = db.Column(db.String(24), nullable=False)
    esrs_enabled = db.Column(db.Boolean, nullable=False)
    tool_version = db.Column(db.String(24), nullable=False)
    sr_number = db.Column(db.Integer(14), nullable=False)
