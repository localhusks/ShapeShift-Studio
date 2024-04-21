from App.database import db
from sqlalchemy import event
from .exercise import Exercise
from .routine_exercise import routine_exercise

class Routine(db.Model):
    __tablename__ = 'routine'
    routine_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="routines")
    custom_name = db.Column(db.String(120), nullable=True)
    exercises = db.relationship("Exercise", secondary=routine_exercise, lazy='joined')
    
    def __init__(self, name, user_id):
        self.set_routine_name(name)
        self.user_id = user_id

    def set_routine_name(self, name):
        name_in = name if name != None else f'routine {self.routine_id}:{self.user_id}'
        self.custom_name = name_in

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def remove_exercise(self, exercise):
        self.exercises.remove(exercise)
    
    def __repr__(self):
        return f"<routine: {self.routine_id}>"
    
    def to_json(self):
        return {
            'routine_id': self.routine_id,
            'user_id': self.user_id,
            'exercises': [e.to_json() for e in self.exercises],
            'custom_name': self.custom_name
        }
@event.listens_for(Routine,'after_delete')
def remove_routine_exercise_entries(mapper, connection, target):
    connection.execute(
        routine_exercise.delete().where(routine_exercise.c.routine_id == target.routine_id)
    )    