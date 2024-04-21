import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Exercise, Routine
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
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
            body_area= "lower",
            equip="body weight",
            muscle = "thighs"
        )
        assert exercise.name == "body weight squats"
    
    def test_to_json(self):
        exercise = Exercise(
            name="body weight squats",
            body_area= "lower",
            equip="body weight",
            muscle = "thighs"
        )
        exercise_json = exercise.to_json()
        self.assertDictEqual(exercise_json,{
            'exercise_id' : None,
            'name':"body weight squats",
            'targeted_muscle':"thighs",
            'equipment':"body weight",
            'body_part':"lower"
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
            body_area= "lower",
            equip="body weight",
            muscle = "thighs"
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
            body_area= "lower",
            equip="body weight",
            muscle = "thighs"
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
            body_area= "lower",
            equip="body weight",
            muscle = "thighs"
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
            'exercises': [{
                'exercise_id' : None,
            'name':"body weight squats",
            'targeted_muscle':"thighs",
            'equipment':"body weight",
            'body_part':"lower"
            }],
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

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

