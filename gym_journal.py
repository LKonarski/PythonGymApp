from pydantic import BaseModel, validator
from typing import List
import json

MUSCLES_GROUP = ["Chest", "Triceps", "Shoulders", "Back", "Biceps", "Forearms", "Quads", "Hamstrings", "Glutes", "Calves", "Abs"]
TRAINING_TYPE = ["Push", "Pull", "Legs", "Chest & Back", "Arms & Shoulders", "Upper", "Lower", "Full Body Workout"]


class SetsException(Exception):
    pass

class RepsException(Exception):
    pass

class WeightException(Exception):
    pass

class MuscleException(Exception):
    pass

class TrainingException(Exception):
    pass

class ExerciseEntry(BaseModel):
    exercise: str
    muscles: List[str]
    sets: int
    reps: int 
    weight: float

    @validator('sets')
    def validate_sets(cls, v):
        if v <= 0:
            raise SetsException("I see that you are in debt of some sets to the gym. Value must be positive!")
        elif v > 5:
            raise SetsException("Let some other gymbros exercise!")
        return v

    @validator('reps')
    def validate_reps(cls, v):
        if v <= 0:
            raise RepsException("Going to failure doesnt mean negative reps bro. Value must be positive!")
        elif v > 15:
            raise RepsException("Naaah bro, that's cardio!")
        return v

    @validator('weight')
    def positive_value(cls, v):
        if v <= 0:
            raise WeightException("Do you even lift bro? Value must be positive!")
        return v


class TrainingPlan(BaseModel):
    plan_name: str
    muscles: List[str]
    training_type: str
    exercises: List[str]

    @validator('muscles')
    def validate_muscles(cls, v):
        for muscle in v:
            if muscle not in MUSCLES_GROUP:
                raise MuscleException("Nah mate I dont know what is this but it aint a muscle group. Choose from the provided options.")
        return v

    @validator('training_type')
    def validate_training_type(cls, v):
        if v not in TRAINING_TYPE:
            raise TrainingException("If you type crossfit == Invalid training type. Choose from the provided options.")
        return v


def add_entry():
    exercise = input("Enter the exercise: ")

    print("Muscle Groups:")
    for i, muscle in enumerate(MUSCLES_GROUP, start=1):
        print(f"{i}. {muscle}")

    muscles_choice = input("Enter the muscle group numbers (separated by commas): ")
    muscles = [MUSCLES_GROUP[int(choice) - 1] for choice in muscles_choice.split(",")]

    sets = int(input("Enter the number of sets: "))
    reps = int(input("Enter the number of reps: "))
    weight = float(input("Enter the weight (in kg): "))

    entry = ExerciseEntry(exercise=exercise, muscles=muscles, sets=sets, reps=reps, weight=weight)

    with open("gym_journal.json", "a") as file:
        file.write(entry.json() + "\n")

    print("Entry added successfully!")


def view_entries():
    try:
        with open("gym_journal.json", "r") as file:
            entries = file.readlines()
            print("\n--- Gym Journal Entries ---\n")
            for entry in entries:
                entry_dict = json.loads(entry)
                exercise_entry = ExerciseEntry(**entry_dict)
                print(f"Exercise: {exercise_entry.exercise}")
                print(f"Muscles: {', '.join(exercise_entry.muscles)}")
                print(f"Sets x Reps x Weight: {exercise_entry.sets} sets x {exercise_entry.reps} reps x {exercise_entry.weight} kg\n")
    except FileNotFoundError:
        print("No entries found in the gym journal.")

def delete_entry(exercise_name):
    try:
        with open("gym_journal.json", "r") as file:
            entries = file.readlines()

        with open("gym_journal.json", "w") as file:
            for entry in entries:
                entry_dict = json.loads(entry)
                exercise_entry = ExerciseEntry(**entry_dict)
                if exercise_entry.exercise != exercise_name:
                    file.write(entry)

        print(f"Exercise '{exercise_name}' deleted successfully!")
    except FileNotFoundError:
        print("No entries found in the gym journal.")

def clear_entries():
    confirm = input("Are you sure you want to clear all entries? (y/n): ")
    if confirm.lower() == "y":
        with open("gym_journal.json", "w") as file:
            file.write("")
        print("All entries cleared successfully!")


def create_plan():
    plan_name = input("Enter the name of the training plan: ")

    print("Muscle Groups:")
    for i, muscle in enumerate(MUSCLES_GROUP, start=1):
        print(f"{i}. {muscle}")

    muscles_choice = input("Enter the muscle group numbers (separated by commas): ")
    muscles = [MUSCLES_GROUP[int(choice) - 1] for choice in muscles_choice.split(",")]

    print("Training Types:")
    for i, training_type in enumerate(TRAINING_TYPE, start=1):
        print(f"{i}. {training_type}")

    training_type_choice = int(input("Enter the training type number: "))
    training_type = TRAINING_TYPE[training_type_choice - 1]

    exercises = []
    print("Enter the exercises for the plan (enter 'x' to finish): ")
    while True:
        exercise = input("Exercise: ")
        if exercise.lower() == "x":
            break
        exercises.append(exercise)

    plan = TrainingPlan(plan_name=plan_name, muscles=muscles, training_type=training_type, exercises=exercises)

    with open("training_plans.json", "a") as file:
        file.write(plan.json() + "\n")

    print("Training plan created successfully!")


def view_plans():
    try:
        with open("training_plans.json", "r") as file:
            plans = file.readlines()
            print("\n--- Training Plans ---\n")
            for plan in plans:
                plan_dict = json.loads(plan)
                training_plan = TrainingPlan(**plan_dict)
                print(f"Plan Name: {training_plan.plan_name}")
                print(f"Muscles: {', '.join(training_plan.muscles)}")
                print(f"Training Type: {training_plan.training_type}")
                print(f"Exercises: {', '.join(training_plan.exercises)}\n")
    except FileNotFoundError:
        print("No training plans found.")

def delete_plan(plan_name):
    try:
        with open("training_plans.json", "r") as file:
            plans = file.readlines()

        with open("training_plans.json", "w") as file:
            for plan in plans:
                plan_dict = json.loads(plan)
                training_plan = TrainingPlan(**plan_dict)
                if training_plan.plan_name != plan_name:
                    file.write(plan)
        print(f"Training plan '{plan_name}' deleted successfully!")
    except FileNotFoundError:
        print("No training plans found.")

def clear_plans():
    confirm = input("Are you sure you want to clear all training plans? (y/n): ")
    if confirm.lower() == "y":
        with open("training_plans.json", "w") as file:
            file.write("")
        print("All training plans cleared successfully!")


def main():
    print("Welcome to Gym Journal!")

    while True:
        print("\nMenu:")
        print("1. Exercises")
        print("2. Training Plans")
        print("3. Quit")

        section_choice = input("Enter your choice (1-3): ")

        if section_choice == "1":
            while True:
                print("\nExercise Menu:")
                print("1. Add an entry")
                print("2. View all entries")
                print("3. Delete an entry")
                print("4. Clear all entries")
                print("5. Back to main menu")

                exercise_choice = input("Enter your choice (1-5): ")

                if exercise_choice == "1":
                    add_entry()
                elif exercise_choice == "2":
                    view_entries()
                elif exercise_choice == "3":
                    exercise_name = input("Enter the name of the exercise to delete: ")
                    delete_entry(exercise_name)
                elif exercise_choice == "4":
                    clear_entries()
                elif exercise_choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif section_choice == "2":
            while True:
                print("\nTraining Plan Menu:")
                print("1. Create a training plan")
                print("2. View all training plans")
                print("3. Delete a plan")
                print("4. Clear all training plans")
                print("5. Back to main menu")

                plan_choice = input("Enter your choice (1-5): ")

                if plan_choice == "1":
                    create_plan()
                elif plan_choice == "2":
                    view_plans()
                elif plan_choice == "3":
                    plan_name = input("Enter the name of the plan to delete: ")
                    delete_plan(plan_name)
                elif plan_choice == "4":
                    clear_plans()
                elif plan_choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif section_choice == "3":
            print("See ya!")
            break

        else:
            print("Invalid choice. Please try again.")

main()