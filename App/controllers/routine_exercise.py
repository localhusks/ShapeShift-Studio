from App.models import Routine
from App.database import db
from App.models import Exercise
from App.models import routine_exercise
from .exercise import get_exercise
from .routine import get_routine
def add_exercise_to_routine(exercise_id,routine_id):
    exercise = get_exercise(exercise_id)
    routine = get_routine(routine_id)
    if exercise and routine:
        routine.add_exercise(exercise)
        db.session.add_all({exercise,routine})
        db.session.commit()
        return routine
    return None

def remove_exercise_from_routine(exercise_id,routine_id):
    exercise = get_exercise(exercise_id)
    routine = get_routine(routine_id)
    if exercise and routine:
        routine.remove_exercise(exercise)
        db.session.add_all({exercise,routine})
        db.session.commit()
        return routine
    return None

# def incrememnt_rep_count(routine_id, exercise_id):
#     query = routine_exercise.update().values(count=routine_exercise.c.count + 1).where(
#         db.and_(routine_exercise.c.routine_id == routine_id, routine_exercise.c.exercise_id == exercise_id)
#     )
#     db.session.execute(query)
#     db.session.commit()

# def decrememnt_rep_count(routine_id, exercise_id):
#     query = routine_exercise.update().values(count=routine_exercise.c.count - 1).where(
#         db.and_(routine_exercise.c.routine_id == routine_id, routine_exercise.c.exercise_id == exercise_id)
#     )
#     db.session.execute(query)
#     db.session.commit()
