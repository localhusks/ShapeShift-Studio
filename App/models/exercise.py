from App.database import db
# from .routine_exercise import routine_exercise

class Exercise(db.Model):
    __tablename__ = 'exercise'
    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(120), nullable=False)
    equipment = db.Column(db.String(120), nullable=False)
    target_muscle = db.Column(db.String(120), nullable=False)

    def __init__(self, name, difficulty, equip, target_muscle):
        self.name = name
        self.difficulty = difficulty
        self.equipment = equip
        self.target_muscle = target_muscle

    def __repr__(self):
        return f"<exercise: {self.exercise_id}, {self.name}, {self.difficulty}, {self.equipment}, {self.target_muscle}>"
    
    def to_json(self):
        return {
            'exercise_id': self.exercise_id,
            'name': self.name,
            'targeted_muscle': self.target_muscle,
            'equipment': self.equipment,
            'difficulty': self.difficulty,
        }
