import tkinter as tk
from tkinter import ttk
import re

from patient_service import (
    get_all_patients,
    add_patient,
    update_patient,
    delete_patient
)

from medication_service import (
    get_medications_by_patient,
    add_medication,
    update_medication,
    delete_medication
)

from schedule_service import (
    get_schedules_by_medication,
    add_schedule,
    delete_schedule
)


FONT_MAIN = ("Helvetica", 12)


class PatientPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.selected_patient = None
        self.selected_med = None
        self.selected_schedule = None

        self.build_ui()
        self.load_patients()

    # ===============================
    # UI
    # ===============================

    def build_ui(self):

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)

        # ======================
        # TOP - PATIENT SECTION
        # ======================

        patient_frame = tk.LabelFrame(self, text="PATIENTS", font=("Helvetica", 14, "bold"))
        patient_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        patient_frame.columnconfigure(0, weight=1)
        patient_frame.rowconfigure(0, weight=1)

        self.patient_list = tk.Listbox(patient_frame, font=FONT_MAIN, height=4)
        self.patient_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.patient_list.bind("<<ListboxSelect>>", self.select_patient)

        form_frame = tk.Frame(patient_frame)
        form_frame.grid(row=1, column=0, sticky="ew", padx=5)

        tk.Label(form_frame, text="Name", font=FONT_MAIN).grid(row=0, column=0)
        self.patient_name = tk.Entry(form_frame, font=FONT_MAIN)
        self.patient_name.grid(row=0, column=1)

        tk.Label(form_frame, text="Age", font=FONT_MAIN).grid(row=1, column=0)
        self.patient_age = tk.Entry(form_frame, font=FONT_MAIN)
        self.patient_age.grid(row=1, column=1)

        tk.Button(form_frame, text="Save", font=FONT_MAIN,
                command=self.save_patient).grid(row=2, column=0, pady=5)

        tk.Button(form_frame, text="Delete", font=FONT_MAIN,
                command=self.remove_patient).grid(row=2, column=1, pady=5)

        # ======================
        # BOTTOM SECTION
        # ======================

        bottom_frame = tk.Frame(self)
        bottom_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        # ----------------------
        # MEDICATION FRAME
        # ----------------------

        med_frame = tk.LabelFrame(bottom_frame, text="MEDICATIONS", font=("Helvetica", 14, "bold"))
        med_frame.grid(row=0, column=0, sticky="nsew", padx=5)

        med_frame.columnconfigure(0, weight=1)
        med_frame.rowconfigure(0, weight=1)

        self.med_list = tk.Listbox(med_frame, font=FONT_MAIN)
        self.med_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.med_list.bind("<<ListboxSelect>>", self.select_med)

        tk.Label(med_frame, text="Name", font=FONT_MAIN).grid(row=1, column=0)
        self.med_name = tk.Entry(med_frame, font=FONT_MAIN)
        self.med_name.grid(row=2, column=0, sticky="ew", padx=5)

        tk.Label(med_frame, text="Dosage", font=FONT_MAIN).grid(row=3, column=0)
        self.med_dosage = tk.Entry(med_frame, font=FONT_MAIN)
        self.med_dosage.grid(row=4, column=0, sticky="ew", padx=5)

        tk.Button(med_frame, text="Save", font=FONT_MAIN,
                command=self.save_med).grid(row=5, column=0, pady=5)

        tk.Button(med_frame, text="Delete", font=FONT_MAIN,
                command=self.remove_med).grid(row=6, column=0, pady=5)

        # ----------------------
        # SCHEDULE FRAME
        # ----------------------

        schedule_frame = tk.LabelFrame(bottom_frame, text="SCHEDULES", font=("Helvetica", 14, "bold"))
        schedule_frame.grid(row=0, column=1, sticky="nsew", padx=5)

        schedule_frame.columnconfigure(0, weight=1)
        schedule_frame.rowconfigure(0, weight=1)

        self.schedule_list = tk.Listbox(schedule_frame, font=FONT_MAIN)
        self.schedule_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.schedule_list.bind("<<ListboxSelect>>", self.select_schedule)

        tk.Label(schedule_frame, text="Time (HH:MM)", font=FONT_MAIN).grid(row=1, column=0)
        self.schedule_time = tk.Entry(schedule_frame, font=FONT_MAIN)
        self.schedule_time.grid(row=2, column=0, sticky="ew", padx=5)

        tk.Button(schedule_frame, text="Add Time", font=FONT_MAIN,
                command=self.add_time).grid(row=3, column=0, pady=5)

        tk.Button(schedule_frame, text="Delete Time", font=FONT_MAIN,
                command=self.remove_time).grid(row=4, column=0, pady=5)

    # ===============================
    # PATIENT LOGIC
    # ===============================

    def load_patients(self):
        self.patient_list.delete(0, tk.END)
        self.patient_data = get_all_patients()

        for p in self.patient_data:
            self.patient_list.insert(tk.END, f"{p[1]} | Age:{p[2]} | Drawer:{p[3]}")

    def select_patient(self, event):
        selection = self.patient_list.curselection()
        if not selection:
            return

        index = selection[0]
        self.selected_patient = self.patient_data[index]

        self.patient_name.delete(0, tk.END)
        self.patient_name.insert(0, self.selected_patient[1])

        self.patient_age.delete(0, tk.END)
        self.patient_age.insert(0, self.selected_patient[2])

        self.load_medications()

    def save_patient(self):
        name = self.patient_name.get().strip()
        age = self.patient_age.get().strip()

        if not name or not age.isdigit():
            return

        if self.selected_patient:
            update_patient(self.selected_patient[0], name, int(age))
        else:
            add_patient(name, int(age))

        self.selected_patient = None
        self.patient_name.delete(0, tk.END)
        self.patient_age.delete(0, tk.END)

        self.load_patients()

   
    def remove_patient(self):
        if self.selected_patient:
            delete_patient(self.selected_patient[0])

            self.selected_patient = None
            self.selected_med = None
            self.selected_schedule = None

            self.patient_name.delete(0, tk.END)
            self.patient_age.delete(0, tk.END)

            self.med_list.delete(0, tk.END)
            self.schedule_list.delete(0, tk.END)

            self.load_patients()

    # ===============================
    # MEDICATION LOGIC
    # ===============================

    def load_medications(self):
        self.med_list.delete(0, tk.END)

        if not self.selected_patient:
            return

        self.med_data = get_medications_by_patient(self.selected_patient[0])

        for m in self.med_data:
            self.med_list.insert(tk.END, f"{m[1]} | {m[2]}")

    def select_med(self, event):
        selection = self.med_list.curselection()
        if not selection:
            return

        index = selection[0]
        self.selected_med = self.med_data[index]

        self.med_name.delete(0, tk.END)
        self.med_name.insert(0, self.selected_med[1])

        self.med_dosage.delete(0, tk.END)
        self.med_dosage.insert(0, self.selected_med[2])

        self.load_schedules()

    def save_med(self):
        name = self.med_name.get().strip()
        dosage = self.med_dosage.get().strip()

        if not name or not dosage or not self.selected_patient:
            return

        if self.selected_med:
            update_medication(self.selected_med[0], name, dosage)
        else:
            add_medication(self.selected_patient[0], name, dosage)

        self.selected_med = None
        self.med_name.delete(0, tk.END)
        self.med_dosage.delete(0, tk.END)

        self.load_medications()

   
    def remove_med(self):
        if self.selected_med:
            delete_medication(self.selected_med[0])

            self.selected_med = None
            self.selected_schedule = None

            self.med_name.delete(0, tk.END)
            self.med_dosage.delete(0, tk.END)

            self.schedule_list.delete(0, tk.END)

            self.load_medications()

    # ===============================
    # SCHEDULE LOGIC
    # ===============================

    def load_schedules(self):
        self.schedule_list.delete(0, tk.END)

        if not self.selected_med:
            return

        self.schedule_data = get_schedules_by_medication(self.selected_med[0])

        for s in self.schedule_data:
            self.schedule_list.insert(tk.END, s[1])

    def select_schedule(self, event):
        selection = self.schedule_list.curselection()
        if not selection:
            return

        index = selection[0]
        self.selected_schedule = self.schedule_data[index]

        self.schedule_time.delete(0, tk.END)
        self.schedule_time.insert(0, self.selected_schedule[1])

    def add_time(self):
        time = self.schedule_time.get()

        if not self.selected_med:
            return

        # Validación HH:MM 24 horas
        pattern = r"^([01]\d|2[0-3]):([0-5]\d)$"

        if not re.match(pattern, time):
            return

        add_schedule(self.selected_med[0], time)
        self.load_schedules()

    def remove_time(self):
        if self.selected_schedule:
            delete_schedule(self.selected_schedule[0])

            self.selected_schedule = None
            self.schedule_time.delete(0, tk.END)

            self.load_schedules()