#!/usr/bin/python3
"""Unit tests for the console command interpreter."""
import unittest
import os
import io
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place

IS_DB = os.getenv("HBNB_TYPE_STORAGE") == "db"


def run_cmd(cmd_str):
    """Run a console command and return its printed output.

    Args:
        cmd_str (str): The console command string to execute.

    Returns:
        str: The stripped stdout output of the command.
    """
    with patch('sys.stdout', new_callable=io.StringIO) as mock_out:
        HBNBCommand().onecmd(cmd_str)
        return mock_out.getvalue().strip()


class TestConsoleCreate(unittest.TestCase):
    """Tests for the console do_create command."""

    def test_create_no_class(self):
        """Test create with no class name prints error."""
        output = run_cmd("create")
        self.assertEqual(output, "** class name missing **")

    def test_create_invalid_class(self):
        """Test create with invalid class name prints error."""
        output = run_cmd("create MyFakeClass")
        self.assertEqual(output, "** class doesn't exist **")

    @unittest.skipIf(IS_DB, "FileStorage create test only")
    def test_create_state_returns_id(self):
        """Test that create State prints a valid id (FileStorage)."""
        output = run_cmd('create State name="TestCreate"')
        self.assertEqual(len(output), 36)  # UUID length
        key = "State.{}".format(output)
        self.assertIn(key, storage.all())
        # Clean up
        del storage.all()[key]
        storage.save()

    @unittest.skipIf(IS_DB, "FileStorage only — string param test")
    def test_create_with_string_param(self):
        """Test that string params are correctly set (FileStorage)."""
        output = run_cmd('create State name="California"')
        key = "State.{}".format(output)
        obj = storage.all().get(key)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, "California")
        del storage.all()[key]
        storage.save()

    @unittest.skipIf(IS_DB, "FileStorage only — underscore-to-space test")
    def test_create_with_underscore_in_string(self):
        """Test that underscores in strings become spaces (FileStorage)."""
        output = run_cmd('create State name="My_little_state"')
        key = "State.{}".format(output)
        obj = storage.all().get(key)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, "My little state")
        del storage.all()[key]
        storage.save()

    @unittest.skipIf(IS_DB, "FileStorage only — integer param test")
    def test_create_with_integer_param(self):
        """Test that integer params are correctly parsed (FileStorage)."""
        output = run_cmd(
            'create Place city_id="0001" user_id="0001" '
            'name="House" number_rooms=4'
        )
        key = "Place.{}".format(output)
        obj = storage.all().get(key)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.number_rooms, 4)
        self.assertIsInstance(obj.number_rooms, int)
        del storage.all()[key]
        storage.save()

    @unittest.skipIf(IS_DB, "FileStorage only — float param test")
    def test_create_with_float_param(self):
        """Test that float params are correctly parsed (FileStorage)."""
        output = run_cmd(
            'create Place city_id="0001" user_id="0001" '
            'name="House" latitude=37.773972'
        )
        key = "Place.{}".format(output)
        obj = storage.all().get(key)
        self.assertIsNotNone(obj)
        self.assertAlmostEqual(obj.latitude, 37.773972, places=4)
        self.assertIsInstance(obj.latitude, float)
        del storage.all()[key]
        storage.save()

    @unittest.skipIf(IS_DB, "FileStorage only — invalid param skipped")
    def test_create_skips_invalid_params(self):
        """Test that invalid params are silently skipped (FileStorage)."""
        output = run_cmd('create State name="Valid" bad_param no_equals')
        key = "State.{}".format(output)
        obj = storage.all().get(key)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.name, "Valid")
        self.assertFalse(hasattr(obj, "bad_param"))
        del storage.all()[key]
        storage.save()

    @unittest.skipIf(not IS_DB, "DBStorage create test only")
    def test_create_state_db(self):
        """Test that create State works with DBStorage."""
        output = run_cmd('create State name="DBState"')
        self.assertEqual(len(output), 36)
        key = "State.{}".format(output)
        self.assertIn(key, storage.all())
        obj = storage.all()[key]
        storage.delete(obj)
        storage.save()


class TestConsoleShow(unittest.TestCase):
    """Tests for the console do_show command."""

    def test_show_no_class(self):
        """Test show with no class name prints error."""
        output = run_cmd("show")
        self.assertEqual(output, "** class name missing **")

    def test_show_invalid_class(self):
        """Test show with invalid class name prints error."""
        output = run_cmd("show FakeClass")
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_no_id(self):
        """Test show with no id prints error."""
        output = run_cmd("show State")
        self.assertEqual(output, "** instance id missing **")

    def test_show_invalid_id(self):
        """Test show with non-existent id prints error."""
        output = run_cmd("show State 1234-fake-id")
        self.assertEqual(output, "** no instance found **")


class TestConsoleAll(unittest.TestCase):
    """Tests for the console do_all command."""

    def test_all_invalid_class(self):
        """Test all with invalid class name prints error."""
        output = run_cmd("all FakeModel")
        self.assertEqual(output, "** class doesn't exist **")

    def test_all_no_class(self):
        """Test all with no class returns a list string."""
        output = run_cmd("all")
        self.assertTrue(output.startswith("["))


class TestConsoleDestroy(unittest.TestCase):
    """Tests for the console do_destroy command."""

    def test_destroy_no_class(self):
        """Test destroy with no class name prints error."""
        output = run_cmd("destroy")
        self.assertEqual(output, "** class name missing **")

    def test_destroy_invalid_class(self):
        """Test destroy with invalid class name prints error."""
        output = run_cmd("destroy FakeClass")
        self.assertEqual(output, "** class doesn't exist **")

    def test_destroy_no_id(self):
        """Test destroy with no id prints error."""
        output = run_cmd("destroy State")
        self.assertEqual(output, "** instance id missing **")


if __name__ == "__main__":
    unittest.main()
