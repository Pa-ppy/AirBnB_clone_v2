import unittest
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place

class TestHBNBCommandCreate(unittest.TestCase):
    """Test cases for the do_create method."""

    def setUp(self):
        """Set up test environment."""
        self.cli = HBNBCommand()

    def tearDown(self):
        """Clean up storage."""
        storage._FileStorage__objects.clear()

    def test_create_state_with_name(self):
        """Test creating a State with a name attribute."""
        self.cli.onecmd('create State name="California"')
        obj = list(storage.all(State).values())[0]
        self.assertEqual(obj.name, "California")

    def test_create_place_with_multiple_attributes(self):
        """Test creating a Place with multiple attributes."""
        self.cli.onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4')
        obj = list(storage.all(Place).values())[0]
        self.assertEqual(obj.city_id, "0001")
        self.assertEqual(obj.user_id, "0001")
        self.assertEqual(obj.name, "My little house")
        self.assertEqual(obj.number_rooms, 4)

    def test_create_with_invalid_attribute(self):
        """Test creating an object with an invalid attribute."""
        self.cli.onecmd('create State invalid_attr')
        self.assertEqual(len(storage.all(State)), 0)

    def test_create_with_escaped_characters(self):
        """Test creating an object with escaped characters in a string."""
        self.cli.onecmd('create State name="My_\"great\"_state"')
        obj = list(storage.all(State).values())[0]
        self.assertEqual(obj.name, 'My "great" state')

if __name__ == "__main__":
    unittest.main()
