import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.controllers.routine import get_routine
from App.main import create_app
from App.database import db, create_db
from App.models import User, Exercise, Routine, exercise, routine
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    add_routine_to_user,
    remove_routine_from_user,
    create_exercise,
    get_exercise,
    get_all_exercises_json,
    get_all_exercises_by_difficulty,
    get_all_exercises_by_target_muscle,
    get_all_exercises_by_equipment,
    create_routine,
    get_routine,
    get_routine_by_name,
    get_all_routines_for_user_json,
    delete_routine,
    add_exercise_to_routine,
    remove_exercise_from_routine,


)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User(
            username="bob", 
            password="bobpass"
            )
        assert user.username == "bob"
    def test_add_routine(self):
        routine = Routine(
            name = None,
            user_id=None
        )
        user = User("bob", "bobpass")
        user.add_routine(routine)
        self.assertIn(routine,user.routines)
    def test_remove_routine(self):
        routine = Routine(
            name = None,
            user_id=None
        )
        user = User("bob", "bobpass")
        user.add_routine(routine=routine)
        user.remove_routine(routine=routine)
        self.assertNotIn(routine,user.routines)

    def test_to_json(self):
        user = User("bob", "bobpass")
        user_json = user.to_json()
        self.assertDictEqual(user_json, {
            "id":None, 
            "username":"bob",
            "routines" : []
            })
    
    def test_hashed_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class ExerciseUnitTests(unittest.TestCase):
    def test_create_exercise(self):
        exercise = Exercise(
            name="body weight squats",
            difficulty= "lower",
            equip="body weight",
            target_muscle = "thighs"
        )
        assert exercise.name == "body weight squats"
    
    def test_to_json(self):
        exercise = Exercise(
            name="body weight squats",
            difficulty= "lower",
            equip="body weight",
            target_muscle = "thighs"
        )
        exercise_json = exercise.to_json()
        self.assertDictEqual(exercise_json,{
            'exercise_id' : None,
            'name':"body weight squats",
            'targeted_muscle':"thighs",
            'equipment':"body weight",
            'difficulty':"lower"
        })

class RoutineUnitTests(unittest.TestCase):
    def test_create_routine_no_custom(self):
        
        no_custom_routine = Routine(
            name = None,
            user_id=None
        )
        assert no_custom_routine.custom_name == "routine None:None"

    def test_create_routine_custom_name(self):
        
        custom_name_routine = Routine(
            name = "testing name",
            user_id=None
        )
        assert custom_name_routine.custom_name == "testing name"

    def test_add_exercise(self):
        exercise = Exercise(
            name="body weight squats",
            difficulty= "lower",
            equip="body weight",
            target_muscle = "thighs"
        )
        routine = Routine(
            name = "testing add exercise",
            user_id=None
        )
        routine.add_exercise(exercise=exercise)
        self.assertIn(exercise, routine.exercises)

    def test_remove_exercise(self):
        exercise = Exercise(
            name="body weight squats",
            difficulty= "lower",
            equip="body weight",
            target_muscle = "thighs"
        )
        routine = Routine(
            name = "testing remove exercise",
            user_id=None
        )
        routine.add_exercise(exercise=exercise)
        routine.remove_exercise(exercise=exercise)
        self.assertNotIn(exercise, routine.exercises)

    def test_to_json(self):
        exercise = Exercise(
            name="body weight squats",
            difficulty= "lower",
            equip="body weight",
            target_muscle = "thighs"
        )
        routine = Routine(
            name = "testing to json",
            user_id=None
        )
        routine.add_exercise(exercise=exercise)
        routine_json = routine.to_json()
        self.assertDictEqual(routine_json,{
            'routine_id': None,
            'user_id': None,
            'exercises': [
                {
                    'exercise_id' : None,
                    'name':"body weight squats",
                    'targeted_muscle':"thighs",
                    'difficulty':"lower",
                    'equipment' : "body weight"
                }
            ],
            'custom_name': "testing to json"
        })
'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_user(self):
        user = get_user(1)
        assert user.username == "bob"

    def test_get_user_by_username(self):
        user =  get_user_by_username("bob")
        assert user.id == 1

    def test_get_all_users_json(self):

        users_json = get_all_users_json()
        self.assertListEqual([
            {
                "id":1, 
                "username":"bob",
                "routines" : []
            }, 
            {
                "id":2, 
                "username":"rick",
                "routines" : []
            }
            ], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    # def test_add_routine(self):
    #     #adding routine to bob
    #     user = get_user_by_username("bob")
    #     routine = 
    #     add_routine_to_user(user.id, )

    # def test_remove_routine(self):
    #     #adding routine to bob
    #     user = get_user_by_username("bob")
    #     routine = 
    #     add_routine_to_user(user.id, )

class ExerciseIntegrationTests(unittest.TestCase):
    def test_create_exercise(self):
        exercise = create_exercise(
            name="body weight squats",
            difficulty= "lower",
            equipment="body weight",
            target_muscle = "thighs"
        )
        assert exercise.name == "body weight squats"
    def test_get_exercies(self):
        exercise = get_exercise(1)
        assert exercise.name == "body weight squats"
    def test_get_all_exercises(self):
        exercise_2 = create_exercise(
            name="plank",
            difficulty= "waist",
            equipment="body weight",
            target_muscle = "abdominals"
        )
        
        exercises_json = get_all_exercises_json()
        self.assertListEqual(
            [
                {
                    'exercise_id' : 1,
                    'name':"body weight squats",
                    'targeted_muscle':"thighs",
                    'equipment':"body weight",
                    'difficulty':"lower"
                },
                {
                    'exercise_id' : 2,
                    'name':"plank",
                    'targeted_muscle':"abdominals",
                    'equipment':"body weight",
                    'difficulty':"waist"
                }
            ],
            exercises_json
        )   

    def test_get_exercises_by_body(self):
        filtered = get_all_exercises_by_difficulty("waist")
        self.assertListEqual(filtered,[{
                    'exercise_id' : 2,
                    'name':"plank",
                    'targeted_muscle':"abdominals",
                    'equipment':"body weight",
                    'difficulty':"waist"
                }
            ]
        )
    def test_get_exercises_target_muscle(self):
        filtered = get_all_exercises_by_target_muscle("thighs")
        self.assertListEqual(filtered,[{
                    'exercise_id' : 1,
                    'name':"body weight squats",
                    'targeted_muscle':"thighs",
                    'equipment':"body weight",
                    'difficulty':"lower"
                }
            ]
        )
    def test_get_exercises_equipment(self):
        filtered = get_all_exercises_by_equipment("body weight")
        self.assertListEqual(filtered,[
            {
                'exercise_id' : 1,
                'name':"body weight squats",
                'targeted_muscle':"thighs",
                'equipment':"body weight",
                'difficulty':"lower"
            },
            {
                'exercise_id' : 2,
                'name':"plank",
                'targeted_muscle':"abdominals",
                'equipment':"body weight",
                'difficulty':"waist"
            }
            ]
        )

class RoutineIntegrationTests(unittest.TestCase):     
    def test_create_routine(self):
        user = create_user("maki","zenin")
        routine = create_routine("maki's workout",user.id)
        self.assertListEqual(user.routines, [routine]) and routine.custom_name == "maki's workout"

    def test_get_routine_by_name(self):
        routine = get_routine_by_name("maki's workout")
        user = get_user_by_username("maki")
        assert routine.user_id == user.id

    def test_get_all_routines_for_user(self):
        maki_user = get_user_by_username("maki")
        new_routine = create_routine("cardio",maki_user.id)
        routines = get_all_routines_for_user_json(maki_user.id)
        self.assertListEqual([
            {
                'routine_id': 1,
                'user_id' : maki_user.id,
                'exercises': [],
                'custom_name': "maki's workout"
            },
            {
                'routine_id': 2,
                'user_id' : maki_user.id,
                'exercises': [],
                'custom_name': "cardio"
            }
        ],routines)

    def test_routine_new_exercise(self):
        routine = get_routine_by_name("maki's workout")
        exercise = create_exercise(
            name="Barbell Curls",
            difficulty= "arms",
            equipment="50kg Barbell",
            target_muscle = "biceps"
        )
        add_exercise_to_routine(
            exercise_id=exercise.exercise_id,
            routine_id=routine.routine_id
        )
        self.assertIn(exercise,routine.exercises)
        
   
    def test_ryoutines_all(self):
        routine = get_routine_by_name("cardio")
        maki_user = get_user_by_username("maki")
        exercise = create_exercise(
            name="Burpees",
            difficulty= "core",
            equipment="body weight",
            target_muscle = "abdominals"
        )
        add_exercise_to_routine(
            exercise_id=exercise.exercise_id,
            routine_id=routine.routine_id
        )
        routines = get_all_routines_for_user_json(maki_user.id)
        self.assertListEqual([
            {
                'routine_id': 1,
                'user_id' : maki_user.id,
                'exercises': [],
                'custom_name': "maki's workout"
            },
            {
                'routine_id': 2,
                'user_id' : maki_user.id,
                'exercises': [{
                    'exercise_id' : exercise.exercise_id,
                    'name' : "Burpees",
                    'targeted_muscle':"abdominals",
                    'equipment':"body weight",
                    'difficulty':"core"

                }],
                'custom_name': "cardio"
            }
        ],routines)
    def test_routine_rem_exercise(self):
        routine = get_routine_by_name("maki's workout")
        exercise = routine.exercises[-1]
        remove_exercise_from_routine(
            exercise_id=exercise.exercise_id,
            routine_id=routine.routine_id
        )
        self.assertNotIn(exercise,routine.exercises)

    def test_rzemove_routine(self):
        routine = get_routine_by_name("maki's workout")
        delete_routine(routine.routine_id)
        user = get_user_by_username("maki")
        routines = get_all_routines_for_user_json(user.id)
        self.assertNotIn(routine.to_json(),routines)

