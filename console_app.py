from database import initialize_db
from clock_service import start_clock
from patient_service import (
    add_patient,
    get_all_patients,
    update_patient,
    delete_patient
)
from medication_service import (
    add_medication,
    get_medications_by_patient,
    update_medication,
    delete_medication
)

# ---------------------
# PATIENT LIST DISPLAY
# ---------------------

def show_patients():
    patients = get_all_patients()

    if not patients:
        print("No patients registered.\n")
        return []

    print("\n=== Patients ===")
    for i, p in enumerate(patients):
        print(f"{i+1}. {p[1]} | Age:{p[2]} | Drawer:{p[3]}")
    print("===============\n")

    return patients


# ---------------------
# REGISTER PATIENT
# ---------------------

def register_patient():
    name = input("Enter patient name: ")

    while True:
        age_input = input("Enter age: ")
        if not age_input.isdigit():
            print("Age must be a number.\n")
            continue
        age = int(age_input)
        break

    drawer = add_patient(name, age)

    if drawer is None:
        print("No available drawers in this unit.\n")
    else:
        print(f"Patient registered in drawer {drawer}.\n")


# ---------------------
# PATIENT MENU
# ---------------------

def patient_menu(patient_id):
    while True:
        print("\n=== Patient Menu ===")
        print("1. Edit Patient")
        print("2. Delete Patient")
        print("3. Manage Medications")
        print("4. Back")

        choice = input("Select option: ")

        if choice == "1":
            current_patients = get_all_patients()
            patient_data = next(
                (p for p in current_patients if p[0] == patient_id),
                None
            )

            if not patient_data:
                print("Patient not found.\n")
                continue

            print(f"Current name: {patient_data[1]}")
            print(f"Current age: {patient_data[2]}")

            new_name = input("New name (leave blank to keep current): ")
            new_age_input = input("New age (leave blank to keep current): ")

            new_age = None
            if new_age_input:
                if new_age_input.isdigit():
                    new_age = int(new_age_input)
                else:
                    print("Invalid age. Skipping age update.")

            if not new_name:
                new_name = None

            update_patient(patient_id, new_name, new_age)
            print("Patient updated.\n")

        elif choice == "2":
            confirm = input("Are you sure? (y/n): ")
            if confirm.lower() == "y":
                delete_patient(patient_id)
                print("Patient deleted.\n")
                break                                                                 

        elif choice == "3":
            medication_menu(patient_id)

        elif choice == "4":
            break

        else:
            print("Invalid option.\n")



# ---------------------
# MEDICATION MENU
# ---------------------

def medication_menu(patient_id):
    while True:
        print("\n=== Medication Menu ===")
        print("1. View Medications")
        print("2. Add Medication")
        print("3. Manage Schedules")
        print("4. Edit Medication")
        print("5. Delete Medication")
        print("6. Back")

        choice = input("Select option: ")

        if choice == "1":
            meds = get_medications_by_patient(patient_id)

            if not meds:
                print("No medications found.\n")
            else:
                for i, m in enumerate(meds):
                    print(f"{i+1}. {m[1]} | Dosage: {m[2]}")

        elif choice == "2":
            name = input("Medication name: ").strip()
            dosage = input("Dosage: ").strip()

            if not name:
                print("Medication name cannot be empty.\n")
                continue

            result = add_medication(patient_id, name, dosage)

            if result:
                print("Medication added successfully.\n")

                add_schedule_option = input("Would you like to add schedules now? (y/n): ")
                if add_schedule_option.lower() == "y":
                    meds = get_medications_by_patient(patient_id)
                    schedule_menu(meds[-1][0])

            else:
                print("⚠ This medication already exists for this patient.\n")

        elif choice == "3":
            meds = get_medications_by_patient(patient_id)

            if not meds:
                print("No medications to manage schedules for.\n")
                continue

            print("\nSelect medication:")
            for i, m in enumerate(meds):
                print(f"{i+1}. {m[1]} | Dosage: {m[2]}")

            selection = input("Select medication number or B to go back: ")

            if selection.lower() == "b":
                continue

            if not selection.isdigit():
                print("Invalid selection.\n")
                continue

            index = int(selection) - 1

            if 0 <= index < len(meds):
                med_id = meds[index][0]
                schedule_menu(med_id)
            else:
                print("Selection out of range.\n")


        elif choice == "4":
            meds = get_medications_by_patient(patient_id)

            if not meds:
                print("No medications to edit.\n")
                continue

            for i, m in enumerate(meds):
                print(f"{i+1}. {m[1]} | Dosage: {m[2]}")

            selection = input("Select medication number: ")

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(meds):
                    med_id = meds[index][0]

                    new_name = input("New name (leave blank to keep current): ")
                    new_dosage = input("New dosage (leave blank to keep current): ")

                    if not new_name:
                        new_name = None
                    if not new_dosage:
                        new_dosage = None

                    update_medication(med_id, new_name, new_dosage)
                    print("Medication updated.\n")

        elif choice == "5":
            meds = get_medications_by_patient(patient_id)

            if not meds:
                print("No medications to delete.\n")
                continue

            for i, m in enumerate(meds):
                print(f"{i+1}. {m[1]} | Dosage: {m[2]}")

            selection = input("Select medication number to delete: ")

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(meds):
                    med_id = meds[index][0]
                    delete_medication(med_id)
                    print("Medication deleted.\n")

        elif choice == "6":
            break

        else:
            print("Invalid option.\n")

# ---------------------
# SCHEDULE MENU
# ---------------------

from medication_service import (
    add_schedule,
    get_schedules_by_medication,
    delete_schedule
)

def schedule_menu(medication_id):
    while True:
        print("\n=== Schedule Menu ===")
        print("1. View Schedules")
        print("2. Add Schedule")
        print("3. Delete Schedule")
        print("4. Back")

        choice = input("Select option: ")

        if choice == "1":
            schedules = get_schedules_by_medication(medication_id)
            if not schedules:
                print("No schedules found.\n")
            else:
                for i, s in enumerate(schedules):
                    print(f"{i+1}. {s[1]}")

        elif choice == "2":
            time_str = input("Enter time (HH:MM format): ")

            # Validación básica de formato
            import re
            if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_str):
                print("Invalid time format. Use HH:MM.\n")
                continue

            add_schedule(medication_id, time_str)
            print("Schedule added.\n")

        elif choice == "3":
            schedules = get_schedules_by_medication(medication_id)
            if not schedules:
                print("No schedules to delete.\n")
                continue

            for i, s in enumerate(schedules):
                print(f"{i+1}. {s[1]}")

            selection = input("Select schedule to delete: ")

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(schedules):
                    schedule_id = schedules[index][0]
                    delete_schedule(schedule_id)
                    print("Schedule deleted.\n")
                else:
                    print("Selection out of range.\n")
            else:
                print("Invalid selection.\n")



        elif choice == "4":
            break

        else:
            print("Invalid option.\n")


# ---------------------
# MAIN MENU
# ---------------------

def main_menu():
    while True:
        print("==== SMART MED SYSTEM ====")
        print("1. View Patients")
        print("2. Add Patient")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            patients = show_patients()

            if not patients:
                continue

            selection = input("Choose number or B to go back: ")

            if selection.lower() == "b":
                continue

            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(patients):
                    patient_id = patients[index][0]
                    patient_menu(patient_id)

        elif choice == "2":
            register_patient()

        elif choice == "3":
            print("System closed.")
            break

        else:
            print("Invalid option.\n")


def medication_has_schedules(medication_id):
    schedules = get_schedules_by_medication(medication_id)
    return len(schedules) > 0

def medication_has_schedules(medication_id):
    schedules = get_schedules_by_medication(medication_id)
    return len(schedules) > 0



initialize_db()
start_clock() 
main_menu()
import tkinter as tk
from database import initialize_db
from ui.main_window import MainWindow
