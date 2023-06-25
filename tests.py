import unittest
from unittest.mock import patch
from io import StringIO
import json
from gym_journal import (
    ExerciseEntry,
    SetsException,
    RepsException,
    WeightException,
    MuscleException,
    TrainingException,
    TrainingPlan,
    add_entry,
    view_entries,
    delete_entry,
    clear_entries,
    create_plan,
    view_plans,
    delete_plan,
    clear_plans,
)


class ExerciseEntryTests(unittest.TestCase):
    def test_validate_sets_positive(self):
        entry = ExerciseEntry(
            exercise="Bench Press", muscles=["Chest"], sets=3, reps=10, weight=100.0
        )
        self.assertEqual(entry.sets, 3)

    def test_validate_sets_zero(self):
        with self.assertRaises(SetsException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=0, reps=10, weight=100.0
            )

    def test_validate_sets_negative(self):
        with self.assertRaises(SetsException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=-2, reps=10, weight=100.0
            )

    def test_validate_sets_exceed_limit(self):
        with self.assertRaises(SetsException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=6, reps=10, weight=100.0
            )

    def test_validate_reps_positive(self):
        entry = ExerciseEntry(
            exercise="Bench Press", muscles=["Chest"], sets=3, reps=10, weight=100.0
        )
        self.assertEqual(entry.reps, 10)

    def test_validate_reps_zero(self):
        with self.assertRaises(RepsException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=3, reps=0, weight=100.0
            )

    def test_validate_reps_negative(self):
        with self.assertRaises(RepsException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=3, reps=-5, weight=100.0
            )

    def test_validate_reps_exceed_limit(self):
        with self.assertRaises(RepsException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=3, reps=20, weight=100.0
            )

    def test_positive_value_positive(self):
        entry = ExerciseEntry(
            exercise="Bench Press", muscles=["Chest"], sets=3, reps=10, weight=100.0
        )
        self.assertEqual(entry.weight, 100.0)

    def test_positive_value_zero(self):
        with self.assertRaises(WeightException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=3, reps=10, weight=0.0
            )

    def test_positive_value_negative(self):
        with self.assertRaises(WeightException):
            ExerciseEntry(
                exercise="Bench Press", muscles=["Chest"], sets=3, reps=10, weight=-50.0
            )


class TrainingPlanTests(unittest.TestCase):
    def test_validate_muscles_valid(self):
        plan = TrainingPlan(
            plan_name="Plan1",
            muscles=["Chest", "Back"],
            training_type="Push",
            exercises=["Bench Press", "Pull-ups"],
        )
        self.assertEqual(plan.muscles, ["Chest", "Back"])

    def test_validate_muscles_invalid(self):
        with self.assertRaises(MuscleException):
            TrainingPlan(
                plan_name="Plan1",
                muscles=["Chest", "Shoulders", "Invalid"],
                training_type="Push",
                exercises=["Bench Press", "Shoulder Press"],
            )

    def test_validate_training_type_valid(self):
        plan = TrainingPlan(
            plan_name="Plan1",
            muscles=["Chest", "Back"],
            training_type="Push",
            exercises=["Bench Press", "Pull-ups"],
        )
        self.assertEqual(plan.training_type, "Push")

    def test_validate_training_type_invalid(self):
        with self.assertRaises(TrainingException):
            TrainingPlan(
                plan_name="Plan1",
                muscles=["Chest", "Back"],
                training_type="Invalid",
                exercises=["Bench Press", "Pull-ups"],
            )


class GymJournalTests(unittest.TestCase):
    def setUp(self):
        self.mock_file = StringIO()

    @patch("builtins.input", side_effect=["Bench Press", "1", "3", "10", "100.0"])
    @patch("builtins.open", create=True)
    def test_add_entry(self, mock_file_open, mock_input):
        from gym_journal import add_entry

        mock_file = mock_file_open.return_value
        add_entry()

        mock_file.write.assert_called_once()
        entry_dict = json.loads(mock_file.write.call_args[0][0])
        self.assertEqual(entry_dict["exercise"], "Bench Press")
        self.assertEqual(entry_dict["muscles"], ["Chest"])
        self.assertEqual(entry_dict["sets"], 3)
        self.assertEqual(entry_dict["reps"], 10)
        self.assertEqual(entry_dict["weight"], 100.0)

    @patch("builtins.print")
    @patch("builtins.open", create=True)
    def test_view_entries(self, mock_file_open, mock_print):
        from gym_journal import view_entries

        mock_file = mock_file_open.return_value
        mock_file.readlines.return_value = [
            '{"exercise": "Bench Press", "muscles": ["Chest"], "sets": 3, "reps": 10, "weight": 100.0}\n',
            '{"exercise": "Squats", "muscles": ["Quads"], "sets": 4, "reps": 12, "weight": 150.0}\n',
        ]
        view_entries()

        mock_file.readlines.assert_called()
        mock_print.assert_called_with(
            "\n--- Gym Journal Entries ---\n"
            "Exercise: Bench Press\n"
            "Muscles: Chest\n"
            "Sets x Reps x Weight: 3 sets x 10 reps x 100.0 kg\n"
        )

    @patch("builtins.input", return_value="Bench Press")
    @patch("builtins.print")
    @patch("builtins.open", create=True)
    def test_delete_entry(self, mock_file_open, mock_print):
        from gym_journal import delete_entry

        mock_file = mock_file_open.return_value
        mock_file.readlines.return_value = [
            '{"exercise": "Bench Press", "muscles": ["Chest"], "sets": 3, "reps": 10, "weight": 100.0}\n',
            '{"exercise": "Squats", "muscles": ["Quads"], "sets": 4, "reps": 12, "weight": 150.0}\n',
        ]
        delete_entry()

        mock_file.readlines.assert_called()
        mock_file.seek.assert_called()
        mock_file.write.assert_called()
        deleted_entry = json.loads(mock_file.write.call_args[0][0])
        self.assertEqual(deleted_entry["exercise"], "Bench Press")
        self.assertEqual(deleted_entry["muscles"], ["Chest"])
        self.assertEqual(deleted_entry["sets"], 3)
        self.assertEqual(deleted_entry["reps"], 10)
        self.assertEqual(deleted_entry["weight"], 100.0) \
     \

    @patch("builtins.open", create=True)
    def test_clear_entries(self, mock_file_open):
        from gym_journal import clear_entries

        mock_file = mock_file_open.return_value
        clear_entries()

        mock_file.truncate.assert_called()

    @patch("builtins.input", side_effect=["Plan1", "Chest, Back", "Push", "Bench Press, Pull-ups"])
    @patch("builtins.open", create=True)
    def test_create_plan(self, mock_file_open, mock_input):
        from gym_journal import create_plan

        mock_file = mock_file_open.return_value
        create_plan()

        mock_file.write.assert_called_once()
        plan_dict = json.loads(mock_file.write.call_args[0][0])
        self.assertEqual(plan_dict["plan_name"], "Plan1")
        self.assertEqual(plan_dict["muscles"], ["Chest", "Back"])
        self.assertEqual(plan_dict["training_type"], "Push")
        self.assertEqual(plan_dict["exercises"], ["Bench Press", "Pull-ups"])

    @patch("builtins.print")
    @patch("builtins.open", create=True)
    def test_view_plans(self, mock_file_open, mock_print):
        from gym_journal import view_plans

        mock_file = mock_file_open.return_value
        mock_file.readlines.return_value = [
            '{"plan_name": "Plan1", "muscles": ["Chest", "Back"], "training_type": "Push", "exercises": ["Bench Press", "Pull-ups"]}\n',
            '{"plan_name": "Plan2", "muscles": ["Legs"], "training_type": "Pull", "exercises": ["Squats", "Deadlifts"]}\n',
        ]
        view_plans()

        mock_file.readlines.assert_called()
        mock_print.assert_called_with(
            "\n--- Training Plans ---\n"
            "Plan Name: Plan1\n"
            "Muscles: Chest, Back\n"
            "Training Type: Push\n"
            "Exercises: Bench Press, Pull-ups\n"
        )

    @patch("builtins.input", return_value="Plan1")
    @patch("builtins.print")
    @patch("builtins.open", create=True)
    def test_delete_plan(self, mock_file_open, mock_print, mock_input):
        from gym_journal import delete_plan

        mock_file = mock_file_open.return_value
        mock_file.readlines.return_value = [
            '{"plan_name": "Plan1", "muscles": ["Chest", "Back"], "training_type": "Push", "exercises": ["Bench Press", "Pull-ups"]}\n',
            '{"plan_name": "Plan2", "muscles": ["Legs"], "training_type": "Pull", "exercises": ["Squats", "Deadlifts"]}\n',
        ]
        delete_plan()

        mock_file.readlines.assert_called()
        mock_file.seek.assert_called()
        mock_file.write.assert_called()
        deleted_plan = json.loads(mock_file.write.call_args[0][0])
        self.assertEqual(deleted_plan["plan_name"], "Plan1")
        self.assertEqual(deleted_plan["muscles"], ["Chest", "Back"])
        self.assertEqual(deleted_plan["training_type"], "Push")
        self.assertEqual(deleted_plan["exercises"], ["Bench Press", "Pull-ups"])


unittest.main()

