from App.database import db

routine_exercise = db.Table(
    'routine_exercise',
    db.Column('routine_id', db.Integer, db.ForeignKey('routine.routine_id',ondelete='CASCADE')),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.exercise_id',ondelete='CASCADE'))
)