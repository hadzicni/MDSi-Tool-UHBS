import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
from PIL import Image, ImageTk
import subprocess
import webbrowser

Button = tk.Button

def close_window(_event):
    root.destroy()
    exit()



def merge_xml_files(folder_path, output_file, msi_choice):
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
        if msi_choice == "IPS 4K2":
            merged_file.write("        <IPSID>4K2</IPSID>\n")
        elif msi_choice == "IMC 4K3":
            merged_file.write("        <IPSID>4K3</IPSID>\n")
        elif msi_choice == "Manually":
            merged_file.write("        <IPSID></IPSID>\n")
        merged_file.write(f"        <ExpDate>{current_time}</ExpDate>\n")
        merged_file.write(f"        <RowCount>{xml_file_count}</RowCount>\n")
        merged_file.write("    </Header>\n")
        for data in merged_data:
            merged_file.write(data + "\n")
        merged_file.write("</MDSi>\n")

    return merged_data

def callback():
        webbrowser.open_new(r"https://github.com/hadzicni/MDSi-Tool-UHBS")


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
        result_label.config(text="The selected folder does not contain any XML files.")
    elif not folder_path or not output_folder:
        result_label.config(text="Please select the source and target directory.")
    else:
        merged_data = merge_xml_files(folder_path, output_file, ips_choice.get())
        result_label.config(
            text=f"XML files were merged and saved as {output_file}."
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


def auto_fill_filename(*args):
    output_filename_entry.delete(0, tk.END)
    ips_choice_value = ips_choice.get()
    selected_month = dropdownlist.get()
    if selected_month not in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        selected_month = "Monat"

    if ips_choice_value == "IPS 4K2":
        filename_prefix = "MDSi"
    elif ips_choice_value == "IMC 4K3":
        filename_prefix = "MDSimc"
    elif ips_choice_value == "Manually":
        filename_prefix = "manually"
    else:
        filename_prefix = "combined_data"

    output_filename_entry.insert(0, f"{filename_prefix}_{selected_month}")



def update_filename(*args):
    auto_fill_filename()


def get_username():
    try:
        username = os.getlogin()
        return username
    except OSError:
        return "Unknown user"

root = tk.Tk()
root.title("MDSi XML Utility")
root.resizable(width=False, height=False)
root.geometry("660x900")
app_font = ("Archivo", 16)
root.configure(bg='#9B233C')

dropdownlist = ttk.Combobox(root, state="readonly", values=["Please select month", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], width=20)
dropdownlist.set("Please select month")
dropdownlist.pack()
dropdownlist.place(x=260, y=520)

logo = None
logo_path = "uhbs_logo_65_neg.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    logo = logo.resize((350, 60))
    logo = ImageTk.PhotoImage(logo)

logo_label = tk.Label(root, image=logo, bg='#9B233C')
logo_label.pack(pady=50)

user_name = get_username()
welcome_label = tk.Label(root, text=f"{user_name}", font=("Archivo", 14), bg='#9B233C', fg='#E4C6C5')
welcome_label.pack()

title_label = tk.Label(root, text="MDSi XML Utility", font=("Archivo", 26), bg='#9B233C', fg='#E4C6C5')
title_label.pack(pady=15)

input_frame = tk.Frame(root, bg='#9B233C')
input_frame.pack(pady=10)

folder_frame = tk.Frame(input_frame, bg='#9B233C')
folder_frame.pack(side=tk.LEFT, padx=20)

instruction_label = tk.Label(folder_frame, text="Folder with the XML files:", font="Archivo 11 bold", bg='#9B233C', fg='white')
instruction_label.pack()

ips_choice = tk.StringVar()
ips_choice.set("IPS 4K2")

folder_path_entry = tk.Entry(folder_frame, width=40)
folder_path_entry.pack(pady=5)

browse_button = tk.Button(
    folder_frame,
    text="Select",
    command=browse_button_clicked,
    font="Archivo",
    width=20,
    bg='#9B233C',
    fg='white'
)
browse_button.pack(pady=5)

output_frame = tk.Frame(input_frame, bg='#9B233C')
output_frame.pack(side=tk.LEFT, padx=20)

output_folder_label = tk.Label(output_frame, text="Target directory:", font="Archivo 11 bold", bg='#9B233C', fg='white')
output_folder_label.pack()

output_folder_entry = tk.Entry(output_frame, width=40)
output_folder_entry.pack(pady=5)

output_filename_label = tk.Label(root, text="File name:", font="Archivo 15 bold", bg='#9B233C', fg='white')
output_filename_label.pack(pady=10)

output_filename_entry = tk.Entry(root, width=50)
output_filename_entry.pack()
auto_fill_filename()

select_output_folder_button = tk.Button(
    output_frame,
    text="Select",
    command=select_output_folder,
    font="Archivo",
    width=20,
    bg='#9B233C',
    fg='white'
)
select_output_folder_button.pack(pady=5)

ips_choice = tk.StringVar()
ips_choice.set("IPS 4K2")

ips_radio_frame = tk.Frame(root, bg='#9B233C')
ips_radio_frame.pack(pady=60)

ips_label = tk.Label(ips_radio_frame, text="IPS selection:", font=("Archivo", 14, "bold"), bg='#9B233C', fg='white')
ips_label.pack()

ips_radio_font = ("Archivo", 16)

ips_radio_1 = tk.Radiobutton(
    ips_radio_frame,
    text="IPS (4K2)",
    variable=ips_choice,
    value="IPS 4K2",
    font=ips_radio_font,
    bg='#9B233C',
    fg='white',
    selectcolor='#9B233C',
    activeforeground='white',
    activebackground='#9B233C',
    indicatoron=0,
    borderwidth=4,
    highlightthickness=0,
    relief="flat"
)
ips_radio_2 = tk.Radiobutton(
    ips_radio_frame,
    text="IMC (4K3)",
    variable=ips_choice,
    value="IMC 4K3",
    font=ips_radio_font,
    bg='#9B233C',
    fg='white',
    selectcolor='#9B233C',
    activeforeground='white',
    activebackground='#9B233C',
    indicatoron=0,
    borderwidth=4,
    highlightthickness=0,
    relief="flat"
)
ips_radio_3 = tk.Radiobutton(
    ips_radio_frame,
    text="Manuell",
    variable=ips_choice,
    value="Manually",
    font=ips_radio_font,
    bg='#9B233C',
    fg='white',
    selectcolor='#9B233C',
    activeforeground='white',
    activebackground='#9B233C',
    indicatoron=0,
    borderwidth=4,
    highlightthickness=0,
    relief="flat"
)
ips_radio_1.pack(side="left", padx=10)
ips_radio_2.pack(side="left", padx=20)
ips_radio_3.pack(side="left", padx=10)

merge_button = Button(
    root,
    text="Merge XML files",
    command=merge_button_clicked,
    font="Archivo",
    width=50,
    bg='#9B233C',
    fg='white',
    activeforeground='white',
    activebackground='#9B233C',
    borderwidth=4,
    highlightthickness=0,
)
merge_button.pack(pady=25)

link = Button(root, text="GitHub Repository", command=callback, bg='#9B233C', fg='white', font="Archivo")
link.pack(padx=10, pady=10)

def show_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.resizable(width=False, height=False)
    about_window.geometry("250x150")

    about_label = tk.Label(
        about_window, text=f"Author: Hadzic Nikola\nVersion: 3.8\nClient: Petitat Manuel"
    )
    about_label.pack()


about_button = tk.Button(root, text="About", command=show_about_window, bg='#9B233C', fg='white', font="Archivo")
about_button.pack(side="bottom", anchor="se", pady=0)
about_button.place(x=590, y=845)

result_label = tk.Label(root, text="", bg='#9B233C', fg='white')
result_label.pack()

ips_choice.trace("w", auto_fill_filename)
dropdownlist.bind("<<ComboboxSelected>>", auto_fill_filename)

root.bind("<Control-,>", merge_button_clicked)
root.bind("<Escape>", close_window)

root.mainloop()
