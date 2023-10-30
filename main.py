import os
import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog
from xml.etree import ElementTree as ET
from datetime import datetime
from PIL import Image, ImageTk
from time import strftime
import subprocess

Button = tk.Button


def close_window(_event):
    root.destroy()
    exit()


def merge_xml_files(folder_path, output_file, ips_choice):
    merged_data = []

    xml_file_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_file_count += 1
            with open(os.path.join(folder_path, filename), "r") as xml_file:
                xml_data = xml_file.read()
                start_tag = "<Row>"
                end_tag = "</Row>"
                start_index = xml_data.find(start_tag)
                end_index = xml_data.rfind(end_tag)
                if start_index != -1 and end_index != -1:
                    data_to_append = xml_data[start_index: end_index + len(end_tag)]
                    merged_data.append(data_to_append.strip())

    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    with open(output_file, "w") as merged_file:
        merged_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        merged_file.write("<MDSi>\n")
        merged_file.write("    <Header>\n")
        if ips_choice == "IPS 4K2":
            merged_file.write("        <IPSID>4K2</IPSID>\n")
        elif ips_choice == "IMC 4K3":
            merged_file.write("        <IPSID>4K3</IPSID>\n")
        elif ips_choice == "Manually":
            merged_file.write("        <IPSID></IPSID>\n")
        merged_file.write(f"        <ExpDate>{current_time}</ExpDate>\n")
        merged_file.write(f"        <RowCount>{xml_file_count}</RowCount>\n")
        merged_file.write("    </Header>\n")
        for data in merged_data:
            merged_file.write(data + "\n")
        merged_file.write("</MDSi>\n")

    return merged_data


def select_output_folder():
    output_folder = filedialog.askdirectory()
    if output_folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, output_folder)


def merge_button_clicked():
    folder_path = folder_path_entry.get()
    output_folder = output_folder_entry.get()
    output_filename = output_filename_entry.get() + ".xml"
    output_file = os.path.join(output_folder, output_filename)

    xml_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".xml")
    ]

    if not xml_files:
        result_label.config(text="Der ausgewählte Ordner enthält keine XML-Dateien.")
    elif not folder_path or not output_folder:
        result_label.config(text="Bitte wählen Sie Quell- und Zielverzeichnis aus.")
    else:
        merged_data = merge_xml_files(folder_path, output_file, ips_choice.get())
        result_label.config(
            text=f"XML-Dateien wurden zusammengeführt und als {output_file} gespeichert."
        )

        if os.name == "nt":
            subprocess.Popen(["explorer", output_folder])
        elif os.name == "posix":
            subprocess.Popen(["open", output_folder])
        else:
            pass

        merged_data = merge_xml_files(folder_path, output_file, ips_choice.get())
        root.after(3000, root.quit)


def browse_button_clicked():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)


def auto_fill_filename():
    output_filename_entry.delete(0, tk.END)
    ips_choice_value = ips_choice.get()
    if ips_choice_value == "IPS 4K2":
        output_filename_entry.insert(0, "combined_data_IPS4K2")
    elif ips_choice_value == "IMC 4K3":
        output_filename_entry.insert(0, "combined_data_IMC4K3")
    elif ips_choice_value == "Manually":
        output_filename_entry.insert(0, "combined_data_manually")


def update_filename(*args):
    auto_fill_filename()


def get_username():
    try:
        username = os.getlogin()
        return username
    except OSError:
        return "Unbekannter Benutzer"


print(os.environ["username"])

root = tk.Tk()
root.title("MDSi XML Utility")
root.resizable(width=False, height=False)
root.geometry("660x800")
app_font = ("Raleway", 12)

logo_path = "usblogo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    logo = logo.resize((400, 83))
    logo = ImageTk.PhotoImage(logo)

logo_label = tk.Label(root, image=logo)
logo_label.pack(pady=60,
                # anchor="nw"
                )

user_name = get_username()
welcome_label = tk.Label(root, text=f"Hallo, {user_name}!", font=("Raleway-Bold", 14))
welcome_label.pack()

title_label = tk.Label(root, text="MDSi XML Utility", font=("Raleway", 18, "bold"))
title_label.pack(pady=15)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

folder_frame = tk.Frame(input_frame)
folder_frame.pack(side=tk.LEFT, padx=20)

instruction_label = tk.Label(folder_frame, text="Ordner mit den XML-Dateien:")
instruction_label.configure(font="Raleway 11 bold")
instruction_label.pack()

ips_choice = tk.StringVar()
ips_choice.set("IPS 4K2")

folder_path_entry = tk.Entry(folder_frame, width=40)
folder_path_entry.pack(pady=5)

browse_button = tk.Button(
    folder_frame,
    text="Auswählen",
    command=browse_button_clicked,
    font="Raleway",
    width=20,
)
browse_button.pack(pady=5)

output_frame = tk.Frame(input_frame)
output_frame.pack(side=tk.LEFT, padx=20)

output_folder_label = tk.Label(output_frame, text="Zielverzeichnis:")
output_folder_label.configure(font="Raleway 11 bold")
output_folder_label.pack()

output_folder_entry = tk.Entry(output_frame, width=40)
output_folder_entry.pack(pady=5)

output_filename_label = tk.Label(root, text="Dateiname:")
output_filename_label.configure(font="Raleway 15 bold")
output_filename_label.pack(pady=10)

output_filename_entry = tk.Entry(root, width=50)
output_filename_entry.pack()
auto_fill_filename()

select_output_folder_button = tk.Button(
    output_frame,
    text="Auswählen",
    command=select_output_folder,
    font="Raleway",
    width=20,
)
select_output_folder_button.pack(pady=5)

ips_choice = tk.StringVar()
ips_choice.set("IPS 4K2")

ips_radio_frame = tk.Frame(root)
ips_radio_frame.pack(pady=10)

ips_label = tk.Label(ips_radio_frame, text="IPS-Auswahl:", font=("Raleway", 14, "bold"))

ips_radio_font = ("Helvetica", 16)
ips_radio_1 = tk.Radiobutton(
    ips_radio_frame,
    text="IPS (4K2)",
    variable=ips_choice,
    value="IPS 4K2",
    font=ips_radio_font,
)
ips_radio_2 = tk.Radiobutton(
    ips_radio_frame,
    text="IMC (4K3)",
    variable=ips_choice,
    value="IMC 4K3",
    font=ips_radio_font,
)
ips_radio_3 = tk.Radiobutton(
    ips_radio_frame,
    text="Manuell",
    variable=ips_choice,
    value="Manually",
    font=ips_radio_font,
)
ips_radio_1.pack()
ips_radio_2.pack()
ips_radio_3.pack()

merge_button = Button(
    root,
    text="XML-Dateien zusammenführen",
    command=merge_button_clicked,
    font="Raleway",
    width=25,
)
merge_button.pack(pady=25)


def show_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About Tool")
    about_window.resizable(width=False, height=False)
    about_window.geometry("250x150")

    about_label = tk.Label(
        about_window, text=f"Autor: Nikola Hadzic\nVersion: 3.0\nHallo, {user_name}!"
    )
    about_label.pack()


about_button = tk.Button(root, text="About", command=show_about_window)
about_button.pack(side="bottom", anchor="se", pady=30)
about_button.place(x=605, y=765)

result_label = tk.Label(root, text="")
result_label.pack()

ips_choice.trace("w", update_filename)

root.bind('<Escape>', close_window)

root.mainloop()
