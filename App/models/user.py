from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .routine import Routine
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    routines = db.relationship('Routine',back_populates=('user'), lazy = 'joined')


    def __init__(self, username, password):
        self.set_username(username)
        self.set_password(password)

    def to_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'routines' : [r.to_json() for r in self.routines]
        }
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def set_username(self,username):
        self.username = username
    
   

    def add_routine(self,routine):
        self.routines.append(routine)

    def remove_routine(self,routine):
        self.routines.remove(routine)

    def __repr__(self):
        return f"<User: {self.id},{self.username},routines:{self.routines}>"