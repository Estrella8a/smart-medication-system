import tkinter as tk
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

class MedicationPanel(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#F7F7F7")

        self.patient_id = None
        self.selected_med = None
        self.selected_schedule = None

        self.create_widgets()

    def create_widgets(self):

        # ---------- MEDICATION LIST ----------
        tk.Label(self, text="Medications", font=("Helvetica", 14, "bold")).pack()

        self.med_list = tk.Listbox(self)
        self.med_list.pack(fill="both", expand=True)
        self.med_list.bind("<<ListboxSelect>>", self.select_med)

        # ---------- MEDICATION FORM ----------
        tk.Label(self, text="Name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Dosage").pack()
        self.dosage_entry = tk.Entry(self)
        self.dosage_entry.pack()

        tk.Button(self, text="Save Medication", command=self.save_med).pack()
        tk.Button(self, text="Delete Medication", command=self.remove_med).pack()

        # ---------- SCHEDULE LIST ----------
        tk.Label(self, text="Schedules", font=("Helvetica", 14, "bold")).pack(pady=5)

        self.schedule_list = tk.Listbox(self)
        self.schedule_list.pack(fill="both", expand=True)
        self.schedule_list.bind("<<ListboxSelect>>", self.select_schedule)

        # ---------- SCHEDULE FORM ----------
        tk.Label(self, text="Time (HH:MM)").pack()
        self.time_entry = tk.Entry(self)
        self.time_entry.pack()

        tk.Button(self, text="Add Hour", command=self.add_hour).pack()
        tk.Button(self, text="Delete Hour", command=self.delete_hour).pack()

    # ===============================
    # LOAD DATA
    # ===============================

    def load_medications(self, patient_id):
        self.patient_id = patient_id
        self.med_list.delete(0, tk.END)
        meds = get_medications_by_patient(patient_id)

        self.med_data = meds

        for m in meds:
            self.med_list.insert(tk.END, f"{m[1]} | {m[2]}")

    def select_med(self, event):
        selection = self.med_list.curselection()
        if not selection:
            return

        index = selection[0]
        self.selected_med = self.med_data[index]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.selected_med[1])

        self.dosage_entry.delete(0, tk.END)
        self.dosage_entry.insert(0, self.selected_med[2])

        self.load_schedules(self.selected_med[0])

    def save_med(self):
        name = self.name_entry.get()
        dosage = self.dosage_entry.get()

        if not name or not dosage:
            return

        if self.selected_med:
            update_medication(self.selected_med[0], name, dosage)
        else:
            add_medication(self.patient_id, name, dosage)

        self.load_medications(self.patient_id)

    def remove_med(self):
        if self.selected_med:
            delete_medication(self.selected_med[0])
            self.load_medications(self.patient_id)

    # ===============================
    # SCHEDULES
    # ===============================

    def load_schedules(self, med_id):
        self.schedule_list.delete(0, tk.END)
        self.schedule_data = get_schedules_by_medication(med_id)

        for s in self.schedule_data:
            self.schedule_list.insert(tk.END, s[1])

    def select_schedule(self, event):
        selection = self.schedule_list.curselection()
        if not selection:
            return

        index = selection[0]
        self.selected_schedule = self.schedule_data[index]

        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, self.selected_schedule[1])

    def add_hour(self):
        if not self.selected_med:
            return

        time = self.time_entry.get()

        if len(time) != 5 or ":" not in time:
            return

        add_schedule(self.selected_med[0], time)
        self.load_schedules(self.selected_med[0])

    def delete_hour(self):
        if self.selected_schedule:
            delete_schedule(self.selected_schedule[0])
            self.load_schedules(self.selected_med[0])