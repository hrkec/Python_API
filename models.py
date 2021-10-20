import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FootballPlayerModel(db.Model):
    """
    Defines the football player model
    """

    __tablename__ = "footballplayer"

    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String)
    last_name = db.Column("last_name", db.String)
    current_club = db.Column("current_club", db.String)
    nationality = db.Column("nationality", db.String)
    dob = db.Column("dob", db.Date)
    last_modified = db.Column("last_modified", db.DateTime)

    def __init__(self, id, first_name, last_name, club, nationality, dob):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.current_club = club
        self.nationality = nationality
        self.dob = dob
        self.last_modified = datetime.datetime.now()

    def __repr__(self):
        return f"<Player {self.first_name} {self.last_name}>"

    @property
    def serialize(self):
        """
        Return item in serializeable format
        """
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "current_club": self.current_club,
                "nationality": self.nationality,
                "dob": self.dob.strftime('%Y-%m-%d'),
                "last_modified": self.last_modified
                }
