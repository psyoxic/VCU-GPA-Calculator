import customtkinter as ctk
from tkinter import ttk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()

root.title("VCU GPA Calculator")
root.geometry("900x700")
root.configure(fg_color="#171717")

title = ctk.CTkLabel(
    root,
    text="VCU GPA Calculator",
    font=("Arial", 28, "bold"),
    text_color="#F4C430"
)
title.pack(pady=25)

summary_frame = ctk.CTkFrame(root, fg_color="#292929")
summary_frame.pack(fill="x", padx=50, pady=15)

summary_frame.grid_columnconfigure((0, 1, 2), weight=1)

current_gpa_title = ctk.CTkLabel(
    summary_frame,
    text="CURRENT GPA",
    font=("Arial", 12, "bold"),
    text_color="#AAAAAA"
)
current_gpa_title.grid(row=0, column=0, padx=30, pady=10)

current_gpa_display = ctk.CTkLabel(
    summary_frame,
    text="0.00",
    font=("Arial", 26, "bold"),
    text_color="#F4C430"
)
current_gpa_display.grid(row=1, column=0, padx=30, pady=5)

previous_gpa_title = ctk.CTkLabel(
    summary_frame,
    text="PREVIOUS GPA",
    font=("Arial", 12, "bold"),
    text_color="#AAAAAA"
)
previous_gpa_title.grid(row=0, column=1, padx=30, pady=10)

previous_gpa_display = ctk.CTkLabel(
    summary_frame,
    text="0.00",
    font=("Arial", 26, "bold"),
    text_color="#FFFFFF"
)
previous_gpa_display.grid(row=1, column=1, padx=30, pady=5)

total_hours_title = ctk.CTkLabel(
    summary_frame,
    text="TOTAL CREDITS",
    font=("Arial", 12, "bold"),
    text_color="#AAAAAA"
)
total_hours_title.grid(row=0, column=2, padx=30, pady=10)

total_hours_display = ctk.CTkLabel(
    summary_frame,
    text="0",
    font=("Arial", 26, "bold"),
    text_color="#FFFFFF"
)
total_hours_display.grid(row=1, column=2, padx=30, pady =5)

input_container = ctk.CTkFrame(root, fg_color="transparent")
input_container.pack(pady=15)

input_frame = ctk.CTkFrame(input_container, fg_color="#292929")
input_frame.pack(side="left", padx=10, fill="y")

previous_frame = ctk.CTkFrame(input_container, fg_color="#292929")
previous_frame.pack(side="left", padx=10, fill="y")

class_section_title = ctk.CTkLabel(
    input_frame,
    text="ADD A CLASS",
    font=("Arial", 14, "bold"),
    text_color="#F4C430"
)
class_section_title.grid(row=0, column=0, columnspan=2, pady=10)

class_name_label = ctk.CTkLabel(input_frame, text="Class Name:")
class_name_label.grid(row=1, column=0, padx=10, pady=8)

class_name_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Enter class name",
    width=200
)
class_name_entry.grid(row=1, column=1, padx=10, pady=8)

grade_label = ctk.CTkLabel(input_frame, text="Enter Grade:")
grade_label.grid(row=2, column=0, padx=10, pady=8)

grade_entry = ctk.CTkEntry(input_frame, width=200)
grade_entry.grid(row=2, column=1, padx=10, pady=8)

hours_label = ctk.CTkLabel(input_frame, text="Credit Hours:")
hours_label.grid(row=3, column=0, padx=10, pady=8)

hours_entry = ctk.CTkEntry(input_frame, width=200)
hours_entry.grid(row=3, column=1, padx=10, pady=8)

previous_section_title = ctk.CTkLabel(
    previous_frame,
    text="PREVIOUS GPA",
    font=("Arial", 14, "bold"),
    text_color="#F4C430"
)
previous_section_title.grid(row=0, column=0, columnspan=2, pady=10)

previous_gpa_label = ctk.CTkLabel(previous_frame, text="Previous GPA:")
previous_gpa_label.grid(row=1, column=0, padx=10, pady=8)

previous_gpa_entry = ctk.CTkEntry(previous_frame, width=200)
previous_gpa_entry.grid(row=1, column=1, padx=10, pady=8)

previous_hours_label = ctk.CTkLabel(previous_frame, text="Previous Credits:")
previous_hours_label.grid(row=2, column=0, padx=10, pady=8)

previous_hours_entry = ctk.CTkEntry(previous_frame, width=200)
previous_hours_entry.grid(row=2, column=1, padx=10, pady=8)

error_label = ctk.CTkLabel(
    root,
    text="",
    text_color="#FF5555",
    font=("Arial", 12)
)
error_label.pack()


def get_grade_points(grade):
    if grade >= 90:
        return 4.0
    elif grade >= 80:
        return 3.0
    elif grade >= 70:
        return 2.0
    elif grade >= 60:
        return 1.0
    else:
        return 0.0

def get_letter_grade(grade):
    if grade >= 90:
        return "A"
    elif grade >= 80:
        return "B"
    elif grade >= 70:
        return "C"
    elif grade >= 60:
        return "D"
    else:
        return "F"
    
def calculate_gpa():
    total_points = previous_gpa * previous_hours
    total_hours = previous_hours 
    
    for class_name, grade, hours, points in classes:
        total_points += points * hours
        total_hours += hours
    
    if total_hours > 0:
        gpa = total_points / total_hours
        return gpa
    else:
        return 0

def update_dashboard():
    current_gpa = calculate_gpa()
    
    current_gpa_display.configure(text=f"{current_gpa:.2f}")
    
    previous_gpa_display.configure(text=f"{previous_gpa:.2f}")
    
    total_hours = previous_hours + sum(hours for class_name, grade, hours, points in classes)
    
    total_hours_display.configure(text=f"{total_hours:g}")

def save_data():
    data = {
        "previous_gpa": previous_gpa,
        "previous_hours": previous_hours,
        "classes": classes
    }
    
    with open ("gpa_data.json", "w") as file:
        json.dump(data, file, indent=4)
        
    print("Data saved successfully!")
    print(os.path.abspath("gpa_data.json"))
        
def load_data():
    global previous_gpa, previous_hours, classes
    
    try:
        with open("gpa_data.json", "r") as file:
            data = json.load(file)
            print("Data loaded successfully!")
            print(data)
        
        previous_gpa = data["previous_gpa"]
        previous_hours = data["previous_hours"]
        classes = data["classes"]
        
    except FileNotFoundError:
        return
    
    for class_name, grade, hours, points in classes:
        letter = get_letter_grade(grade)
        
        class_list.insert("", "end", values=(
            class_name, f"{grade:g} ({letter})", hours, points
        ))
        
    update_dashboard()

classes = []

previous_gpa = 0.0
previous_hours = 0

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#292929",
    foreground="#FFFFFF",
    fieldbackground="#292929",
    rowheight=30
)

style.configure(
    "Treeview.Heading",
    background="#F4C430",
    foreground="#000000",
    font=("Arial", 12, "bold")
)

style.map("Treeview", background=[("selected", "#555555")])

class_list = ttk.Treeview(
    root,
    columns=("name", "grade", "hours", "points"),
    show="headings",
    height=5
)
class_list.pack(pady=10)

class_list.heading("name", text="Class Name")
class_list.heading("grade", text="Grade")
class_list.heading("hours", text="Credits")
class_list.heading("points", text="Points")

class_list.column("name", width=200)
class_list.column("grade", width=100)
class_list.column("hours", width=100)
class_list.column("points", width=100)

def update_previous_gpa():
    global previous_gpa, previous_hours
    
    try:
        new_gpa = float(previous_gpa_entry.get())
        new_hours = float(previous_hours_entry.get())
    except ValueError:
        error_label.configure(text="Please enter a valid numbers.")
        return
    
    if not 0 <= new_gpa <= 4:
        error_label.configure(text="GPA must be between 0 and 4.")
        return
    
    if not 0 <= new_hours < float("inf"):
        error_label.configure(text="Credit hours must be non-negative and finite.")
        return
    
    previous_gpa = new_gpa
    previous_hours = new_hours
    
    error_label.configure(text="")
    
    update_dashboard()
    save_data()
    
previous_button = ctk.CTkButton(
    previous_frame,
    text="Update GPA",
    command=update_previous_gpa,
    font=("Arial", 12, "bold"),
    fg_color="#F4C430",
    text_color="#000000",
    hover_color="#D4A900"
)
previous_button.grid(row=3, column=0, columnspan=2, pady=10)

button_frame = ctk.CTkFrame(
    root,
    fg_color="transparent"
)
button_frame.pack(pady=15)

def enter_class():
    class_name = class_name_entry.get()
    
    if not class_name.strip():
        error_label.configure(text="Please enter a class name.")
        return
    try:
        grade = float(grade_entry.get())
        hours = float(hours_entry.get())
    except ValueError:
        print ("Please enter a valid grade and credit hours.")
        return
    
    if not 0 <= grade <= 100:
        error_label.configure(text="Grade must be between 0 and 100.")
        return
    
    if not 0 < hours < float ("inf"):
        error_label.configure(text="Credit hours must be a positive number.")
        return
    
    error_label.configure(text="")
    
    points = get_grade_points(grade)
    letter = get_letter_grade(grade)
    
    classes.append((class_name, grade, hours, points))
    
    update_dashboard()
    save_data()
    
    class_list.insert ("", "end", values=(class_name, f"{grade:g} ({letter})", hours, points))
    print (classes)
    
    print ("Grade:", grade)
    print ("Credit Hours:", hours)
    
    class_name_entry.delete(0, "end")
    grade_entry.delete(0, "end")
    hours_entry.delete(0, "end")
    class_name_entry.focus()
    
enter_button = ctk.CTkButton(
    button_frame,
    text="Add Class",
    command=enter_class,
    font=("Arial", 10, "bold"),
    fg_color="#F4C430",
    text_color="#000000",
    hover_color="#D4A900",
    
)
enter_button.pack(side="left", padx=10)

def remove_class():
    selected = class_list.selection()
    
    if selected:
        item = selected[0]
        index = class_list.index(item)
        
        classes.pop(index)
        class_list.delete(item)
        
        update_dashboard()
        save_data()
    
remove_button = ctk.CTkButton(
    button_frame,
    text="Remove Class",
    command=remove_class,
    font=("Arial", 12, "bold"),
    fg_color="#444444",
    text_color="#FFFFFF",
    hover_color="#666666"
)
remove_button.pack(side="left", padx=10)

def clear_classes():
    for item in class_list.get_children():
        class_list.delete(item)
    classes.clear()
    
    update_dashboard()
    save_data()
   
    
clear_button = ctk.CTkButton(
    button_frame,
    text="Clear All",
    command=clear_classes,
    font=("Arial", 12, "bold"),
    fg_color="#444444",
    text_color="#FFFFFF",
    hover_color="#666666"
)
clear_button.pack(side="left", padx=10)





load_data()

root.mainloop()