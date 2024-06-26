import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import socket
import json
import tkinter.messagebox
import os


def save_files():
    file_data = []
    for item in files_tree.get_children():
        values = files_tree.item(item, "values")
        file_data.append({"file": values[0], "rotation": values[1]})
    with open("files.json", "w") as file:
        json.dump(file_data, file)

def load_files():
    files_tree.delete(*files_tree.get_children())
    try:
        with open("files.json", "r") as file:
            file_data = json.load(file)
            for data in file_data:
                files_tree.insert("", "end", values=(data["file"], data["rotation"]))
    except FileNotFoundError:
        return


# Функция для сохранения настроек в файл JSON
def save_settings(udp_settings, tcp_settings):
    with open("server_settings.json", "w") as f:
        print(udp_settings, tcp_settings)
        json.dump({"UDP": udp_settings, "TCP": tcp_settings}, f)

# Функция для загрузки настроек из файла JSON
def load_settings():
    try:
        with open("server_settings.json", "r") as f:
            settings = json.load(f)
            return settings.get("UDP", {}), settings.get("TCP", {})
    except FileNotFoundError:
        return {}, {}

def check_address_and_port(address, port):
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.bind((address, port))
        temp_socket.close()
        return True
    except Exception as e:
        print(f"Ошибка при проверке адреса и порта: {e}")
        return False
def ok_click():
    save_files()
    # Собираем настройки UDP и TCP серверов
    udp_settings = {
    "enabled": udp_enable_var.get(),
    "ip_address": udp_ip_entry.get(),
    "port": udp_port_entry.get()
    }
    tcp_settings = {
    "enabled": tcp_enable_var.get(),
    "ip_address": tcp_ip_entry.get(),
    "port": tcp_port_entry.get()
    }
    if check_address_and_port(udp_settings["ip_address"], int(udp_settings["port"])) and \
            check_address_and_port(tcp_settings["ip_address"], int(tcp_settings["port"])):
        save_settings(udp_settings, tcp_settings)
        root.quit()
    else:
        tk.messagebox.showerror("Ошибка", "Невозможно использовать указанный адрес и порт.")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Json files", "*.json")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0,file_path)
    return

def add_file():
    filename = file_entry.get()
    rotation = get_rotation_value()
    files_tree.insert("", "end", values=(os.path.basename(filename), rotation))

def delete_file():
    selected_item = files_tree.selection()
    for item in selected_item:
        files_tree.delete(item)

def cancel_click():
    root.destroy()
    root.quit()

def on_tab_change(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "Files":
        load_files()

def get_rotation_value():
    rotation_off = rotation_off_var.get()
    rotation_size = rotation_size_var.get()
    rotation_data = rotation_data_var.get()
    if rotation_off:
        return "off"
    elif rotation_size:
        return f"by size {rotation_size_spinbox.get()} {rotation_size_combobox.get()}, {get_number()}]"
    elif rotation_data:
        return f"by {rotation_data_combobox.get()} {rotation_data_spinbox.get()} hour, {get_number()}]"

def get_number():
    if rotation_name_number_var.get():
        return f"{os.path.basename(file_entry.get())}[1..{rotation_number_spinbox.get()}"
    elif rotation_new_name_var.get():
        return f"{rotation_new_name_entry.get()}[{rotation_number_spinbox.get()}"

def enable_rotation_off():
    rotation_off_var.set(value=True)
    rotation_size_var.set(value=False)
    rotation_data_var.set(value=False)
    rotation_size_checkbox.state(["!disabled"])
    rotation_data_checkbox.state(["!disabled"])
    rotation_name_number_checkbox.state(["disabled"])
    rotation_new_name_checkbox.state(["disabled"])
    rotation_size_spinbox.state(["disabled"])
    rotation_size_combobox.state(["disabled"])
    rotation_data_spinbox.state(["disabled"])
    rotation_data_combobox.state(["disabled"])
    rotation_new_name_entry.state(["disabled"])
    rotation_number_spinbox.state(["disabled"])

def enable_rotation_size():
    rotation_off_var.set(value=False)
    rotation_size_var.set(value=True)
    rotation_data_var.set(value=False)
    rotation_off_checkbox.state(["!disabled"])
    rotation_data_checkbox.state(["!disabled"])
    rotation_name_number_checkbox.state(["!disabled"])
    rotation_new_name_checkbox.state(["!disabled"])
    rotation_size_spinbox.state(["!disabled"])
    rotation_size_combobox.state(["!disabled"])
    rotation_data_spinbox.state(["disabled"])
    rotation_data_combobox.state(["disabled"])
    rotation_new_name_entry.state(["!disabled"])
    rotation_number_spinbox.state(["!disabled"])

def enable_rotation_data():
    rotation_off_var.set(value=False)
    rotation_size_var.set(value=False)
    rotation_data_var.set(value=True)
    rotation_off_checkbox.state(["!disabled"])
    rotation_size_checkbox.state(["!disabled"])
    rotation_name_number_checkbox.state(["!disabled"])
    rotation_new_name_checkbox.state(["!disabled"])
    rotation_size_spinbox.state(["disabled"])
    rotation_size_combobox.state(["disabled"])
    rotation_data_spinbox.state(["!disabled"])
    rotation_data_combobox.state(["!disabled"])
    rotation_new_name_entry.state(["!disabled"])
    rotation_number_spinbox.state(["!disabled"])

def enable_number():
    rotation_name_number_var.set(value=True)
    rotation_new_name_var.set(value=False)

def enable_new():
    rotation_name_number_var.set(value=False)
    rotation_new_name_var.set(value=True)

root = tk.Tk()
root.title("Setup")
root.geometry("490x705")
root.resizable(False, False)

udp_settings, tcp_settings = load_settings()

# Создание вкладок
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Вкладка Main
main_frame = ttk.Frame(notebook)
notebook.add(main_frame, text="Main")

udp_frame = ttk.LabelFrame(main_frame, text="UDP Syslog Server")
udp_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

udp_enable_var = tk.BooleanVar(value=udp_settings.get("enabled", False))
udp_enable_check = ttk.Checkbutton(udp_frame, text="Enable UDP listener", variable=udp_enable_var)
udp_enable_check.grid(row=0, column=0, padx=10, pady=5, sticky="w")

udp_ip_label = ttk.Label(udp_frame, text="IP Address:")
udp_ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
udp_ip_entry = ttk.Combobox(udp_frame, values=["0.0.0.0", "10.255.0.1", "192.168.0.107", "192.168.56.1"])
udp_ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")
udp_ip_entry.insert(0, udp_settings.get("ip_address", ""))

udp_port_label = ttk.Label(udp_frame, text="Port:")
udp_port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
udp_port_entry = ttk.Entry(udp_frame)
udp_port_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")
udp_port_entry.insert(0, udp_settings.get("port", ""))

tcp_frame = ttk.LabelFrame(main_frame, text="TCP Syslog Server")
tcp_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

tcp_enable_var = tk.BooleanVar(value=tcp_settings.get("enabled", False))
tcp_enable_check = ttk.Checkbutton(tcp_frame, text="Enable TCP listener", variable=tcp_enable_var)
tcp_enable_check.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Поле для ввода IP адреса TCP сервера
tcp_ip_label = ttk.Label(tcp_frame, text="IP Address:")
tcp_ip_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
tcp_ip_entry = ttk.Combobox(tcp_frame, values=["0.0.0.0", "10.255.0.1", "192.168.0.107", "192.168.56.1"])
tcp_ip_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")
tcp_ip_entry.insert(0, tcp_settings.get("ip_address", ""))

tcp_port_label = ttk.Label(tcp_frame, text="Port:")
tcp_port_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
tcp_port_entry = ttk.Entry(tcp_frame)
tcp_port_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")
tcp_port_entry.insert(0, tcp_settings.get("port", ""))

# Вкладка Files
files_frame = ttk.Frame(notebook)
notebook.add(files_frame, text="Files")


file_frame = ttk.LabelFrame(files_frame, text="Files")
file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

files_tree = ttk.Treeview(file_frame, columns=("File", "Rotation"), height=5, selectmode="extended")
files_tree.column("#1", width=140)
files_tree.column("#2", width=280)
files_tree.heading("#0", text="ID")
files_tree.heading("File", text="File")
files_tree.heading("Rotation", text="Rotation")
files_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

scrollbar = ttk.Scrollbar(file_frame, orient="vertical", command=files_tree.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
files_tree.configure(yscrollcommand=scrollbar.set)

files_tree.column("#0",width=0,stretch=tk.NO)

button = ttk.Label(file_frame, text="")
button.grid(row=1, column=0, padx=5, pady=5, sticky="we")

add_button = ttk.Button(button, text="Add", command=add_file)
#add_button.pack(side=tk.LEFT, padx=5, pady=5)
add_button.grid(row=1, column=0,padx=5, pady=5)

delete_button = ttk.Button(button, text="Delete", command=delete_file)
#delete_button.pack(side=tk.LEFT, padx=5, pady=5)
delete_button.grid(row=1, column=1,padx=5, pady=5)

files_set_frame = ttk.LabelFrame(files_frame, text="File settings for default file")
files_set_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

set = ttk.Label(files_set_frame, text="")
set.grid(row=1, column=0, padx=5, pady=5, sticky="we")

file_entry_label = ttk.Label(set, text="Name:")
file_entry_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
file_entry = ttk.Entry(set, width=30)
file_entry.grid(row=1, column=0, padx=5, pady=5, sticky="we")

browse_button = ttk.Button(set, text="Browse", command=browse_file)
browse_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

lab = ttk.Label(files_set_frame, text="")
lab.grid(row=2, column=0, padx=5, pady=5, sticky="we")

rotation_off_var = tk.IntVar()
rotation_off_checkbox = ttk.Checkbutton(lab, text="Rotation off", variable=rotation_off_var, command=enable_rotation_off)
rotation_off_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky="w")

rotation_size_var = tk.IntVar()
rotation_size_checkbox = ttk.Checkbutton(lab, text="Rotation by size:", variable=rotation_size_var, command=enable_rotation_size)
rotation_size_checkbox.grid(row=3, column=0, padx=5, pady=5, sticky="w")

rotation_size_spinbox = ttk.Spinbox(lab,from_=1, to=10000, width=5, state=tk.DISABLED)
rotation_size_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky="we")
rotation_size_spinbox.set(1)

rotation_size_combobox = ttk.Combobox(lab, values=["MBs", "KBs", "GBs"], width=5, state=tk.DISABLED)
rotation_size_combobox.grid(row=3, column=2, padx=5, pady=5, sticky="w")
rotation_size_combobox.set("MBs")

rotation_data_var = tk.IntVar()
rotation_data_checkbox = ttk.Checkbutton(lab, text="Rotation by data:", variable=rotation_data_var, command=enable_rotation_data)
rotation_data_checkbox.grid(row=4, column=0, padx=5, pady=5, sticky="w")

rotation_data_combobox = ttk.Combobox(lab, values=["Week", "Month", "Day", "Year"], width=5, state=tk.DISABLED)
rotation_data_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="we")
rotation_data_combobox.set("Week")

rotation_data_spinbox = ttk.Spinbox(lab, from_=0, to=23, width=5, state=tk.DISABLED)
rotation_data_spinbox.grid(row=4, column=2, padx=5, pady=5, sticky="w")
rotation_data_spinbox.set(0)

hour_label = ttk.Label(lab, text="hour")
hour_label.grid(row=4, column=3, padx=5, pady=5, sticky="we")

hour = ttk.Label(files_set_frame, text="")
hour.grid(row=5, column=0, padx=5, pady=5, sticky="we")

rename_label = ttk.Label(hour, text="After rotation rename file to:")
rename_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

rotation_name_number_var = tk.IntVar(value=True)
rotation_name_number_checkbox = ttk.Checkbutton(hour, text="Name + number", variable=rotation_name_number_var, state=tk.DISABLED, command=enable_number)
rotation_name_number_checkbox.grid(row=6, column=0, padx=5, pady=5, sticky="w")

label = ttk.Label(files_set_frame, text="")
label.grid(row=7, column=0, padx=5, pady=5, sticky="we")


rotation_new_name_var = tk.IntVar()
rotation_new_name_checkbox = ttk.Checkbutton(label, text="New name:", variable=rotation_new_name_var, state=tk.DISABLED, command=enable_new)
rotation_new_name_checkbox.grid(row=7, column=0, padx=5, pady=5, sticky="w")

rotation_new_name_entry = ttk.Entry(label, width=30, state=tk.DISABLED)
rotation_new_name_entry.grid(row=7, column=1, padx=5, pady=5, sticky="we")

l = ttk.Label(files_set_frame, text="")
l.grid(row=8, column=0, padx=5, pady=5, sticky="we")

rotation_number_label = ttk.Label(l, text="Number of file:")
rotation_number_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

rotation_number_spinbox = ttk.Spinbox(l, from_=1, to=10000, width=5, state=tk.DISABLED)
rotation_number_spinbox.grid(row=8, column=1, padx=5, pady=5, sticky="we")
rotation_number_spinbox.set(1)

# Кнопки OK и Cancel
ok_button = ttk.Button(root, text="OK", command=ok_click)
ok_button.pack(side=tk.LEFT, padx=10, pady=10)

cancel_button = ttk.Button(root, text="Cancel", command=cancel_click)
cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

# Применение настроек по умолчанию
enable_rotation_off()

notebook.bind("<<NotebookTabChanged>>", on_tab_change)
root.mainloop()
