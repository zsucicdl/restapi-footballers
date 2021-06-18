from db import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    current_club = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=False)
    preferred_position = db.Column(db.String(50), nullable=False)
    last_modified = db.Column(db.String(50))

    def __init__(self, id, first_name, last_name, current_club, nationality, date_of_birth, preferred_position,
                 last_modified):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.current_club = current_club
        self.nationality = nationality
        self.date_of_birth = date_of_birth
        self.preferred_position = preferred_position
        self.last_modified = last_modified

    @property
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'current_club': self.current_club,
            'nationality': self.nationality,
            'date_of_birth': self.date_of_birth,
            'preferred_position': self.preferred_position,
            'last_modified': self.last_modified
        }
