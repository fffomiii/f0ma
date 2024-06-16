import json
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

class HighlightingSettings(tk.Tk):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Highlighting Settings")
        self.geometry("760x420")

        self.color_mapping = {}
        self.load_color_mapping()

        self.facility_values = ["All", "Kernel", "User", "Mail", "Daemon", "Auth", "Syslog", "LPR", "News", "UUCP", "Cron", "Authpriv", "FTP", "NTP", "Log Audit", "Log Alert", "Clock Daemon", "Local0", "Local1", "Local2", "Local3", "Local4", "Local5", "Local6", "Local7"]
        self.severity_values = ["All", "Emergency", "Alert", "Critical", "Error", "Warning", "Notice", "Informational", "Debug"]

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.Frame(self)
        input_frame.pack(side="top", fill="x", padx=10, pady=5)

        i = ttk.Frame(input_frame)
        i.pack(side="top", fill="x", padx=10, pady=5)

        facility_label = ttk.Label(i, text="Facility", anchor="w")
        facility_label.pack(side="left", padx=(0,5))

        self.facility_var = tk.StringVar()
        self.facility_var.set("All")
        self.facility_combobox = ttk.Combobox(i, textvariable=self.facility_var, values=self.facility_values)
        self.facility_combobox.pack(side="left", padx=(0,5))

        severity_label = ttk.Label(i, text="Severity", anchor="w")
        severity_label.pack(side="left", padx=(20,5))

        self.severity_var = tk.StringVar()
        self.severity_var.set("All")
        self.severity_combobox = ttk.Combobox(i, textvariable=self.severity_var, values=self.severity_values)
        self.severity_combobox.pack(side="left", padx=(0,5))

        self.a = ttk.Frame(input_frame)
        self.a.pack(side="left", padx=10)

        self.color_button = ttk.Button(self.a, text="Color", command=self.choose_color)
        self.color_button.grid(row=0, column=4)

        self.tlabel = ttk.Label(self.a, text="", anchor="w", width=2)
        self.tlabel.grid(row=0, column=2)

        self.text_contains_label = ttk.Label(self.a, text="Text contains", anchor="w")
        self.text_contains_label.grid(row=0, column=0, padx=(0,5))

        self.text_contains_entry = ttk.Entry(self.a, width=47)
        self.text_contains_entry.grid(row=0, column=1)

        self.color_table_frame = ttk.LabelFrame(self, text="Visual")
        self.color_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.color_table = ttk.Treeview(self.color_table_frame, columns=("Facility", "Severity", "Text contains"), show="headings")
        self.color_table.heading("Facility", text="Facility")
        self.color_table.column("Facility", width=120, minwidth=50, stretch=tk.NO)
        self.color_table.heading("Severity", text="Severity")
        self.color_table.column("Severity", width=120, minwidth=50, stretch=tk.NO)
        self.color_table.heading("Text contains", text="Text contains")
        self.color_table.column("Text contains", width=450, minwidth=50, stretch=tk.YES)
        self.color_table.pack(side="left", fill="both", expand=True)

        self.color_scrollbar = ttk.Scrollbar(self.color_table_frame, orient="vertical", command=self.color_table.yview)
        self.color_scrollbar.pack(side="right", fill="y")
        self.color_table.configure(yscrollcommand=self.color_scrollbar.set)

        self.update_color_table()

        ok_button = ttk.Button(self, text="OK", command=self.save_and_quit)
        ok_button.pack(side="left", padx=10, pady=10)

        cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)
        cancel_button.pack(side="right", padx=10, pady=10)

        remove_button = ttk.Button(self, text="Remove", command=self.remove_selected_row)
        remove_button.pack(side="right", padx=10, pady=10)

        move_up_button = ttk.Button(self, text="Move Up", command=self.move_selected_row_up)
        move_up_button.pack(side="right", padx=10, pady=10)

        move_down_button = ttk.Button(self, text="Move Down", command=self.move_selected_row_down)
        move_down_button.pack(side="right", padx=10, pady=10)

    def choose_color(self):
        chosen_color = colorchooser.askcolor()[1]
        if chosen_color:
            print("cvet vybran", chosen_color)
            facility = self.facility_combobox.get()
            severity = self.severity_combobox.get()
            text_contains = self.text_contains_entry.get()
            facility_severity = f"{facility}_{severity}_{text_contains}" if facility and severity else facility or severity
            self.color_mapping[facility_severity] = chosen_color
            self.update_color_table()

    def save_and_quit(self):
        self.save_mappings()
        self.destroy()

    def save_mappings(self):
        with open("highlighting_settings.json", "w") as file:
            json.dump(self.color_mapping, file)

    def load_color_mapping(self):
        try:
            with open("highlighting_settings.json", "r") as file:
                self.color_mapping = json.load(file)
        except FileNotFoundError:
            self.color_mapping = {}

    def update_color_table(self):
        self.color_table.delete(*self.color_table.get_children())
        for facility_severity, color in self.color_mapping.items():
            if color:
                facility, severity, text_contains = facility_severity.split("_") if "_" in facility_severity else (facility_severity, "")
                facility = facility if facility else ""
                severity = severity if severity else ""
                text_contains = text_contains if text_contains else ""
                self.color_table.insert("", "end", values=(facility, severity, text_contains), tags=(facility_severity,))
                self.color_table.tag_configure(facility_severity, background=color)

    def remove_selected_row(self):
        selected_item = self.color_table.selection()[0]
        facility_severity = self.color_table.item(selected_item)['tags'][0]
        if facility_severity in self.color_mapping:
            del self.color_mapping[facility_severity]
            self.update_color_table()

    def move_selected_row_up(self):
        selected_item = self.color_table.selection()[0]
        current_index = int(self.color_table.index(selected_item))
        if current_index > 0:
            self.color_table.move(selected_item, "", current_index - 1)
            self.update_color_mapping_order()

    def move_selected_row_down(self):
        selected_item = self.color_table.selection()[0]
        current_index = int(self.color_table.index(selected_item))
        if current_index < len(self.color_table.get_children()) - 1:
            self.color_table.move(selected_item, "", current_index + 1)
            self.update_color_mapping_order()

    def update_color_mapping_order(self):
        new_mapping = {}
        for item_id in self.color_table.get_children():
            facility_severity = self.color_table.item(item_id)['tags'][0]
            tag_config = self.color_table.tag_configure(facility_severity)
            color = tag_config['background']
            new_mapping[facility_severity] = color
        self.color_mapping = new_mapping

if __name__ == "__main__":
    app = HighlightingSettings(None)
    app.mainloop()