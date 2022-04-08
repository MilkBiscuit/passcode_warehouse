import tkinter
from tkinter import *

import pyperclip

import password_generator
import persistent_write

# -------------------- UI setup -------------------- #
root_window = Tk()
root_window.title("Passcode Warehouse")
root_window.config(padx=40, pady=40)


# --- Warehouse --- #
def copy_password_into_clipboard():
    password = password_entry.get()
    pyperclip.copy(password)


def set_store_button_state():
    store_button_enabled = website_var.get() != "" and username_var.get() != "" and password_var.get() != ""
    if store_button_enabled:
        store_button["state"] = NORMAL
    else:
        store_button["state"] = DISABLED


def on_user_input_changed(*args):
    set_store_button_state()


def on_store():
    persistent_write.save(website_var.get(), username_var.get(), password_var.get())


warehouse_label_frame = LabelFrame(root_window, text="Warehouse")
warehouse_label_frame.grid(row=0, column=0, sticky=tkinter.NW)

Label(warehouse_label_frame, text="Website:").grid(row=0, column=0, sticky=tkinter.E)
Label(warehouse_label_frame, text="Username/Email:").grid(row=1, column=0, sticky=tkinter.E)
Label(warehouse_label_frame, text="Password:").grid(row=2, column=0, sticky=tkinter.E)
website_var = StringVar()
username_var = StringVar()
password_var = StringVar()
website_var.trace("w", on_user_input_changed)
username_var.trace("w", on_user_input_changed)
password_var.trace("w", on_user_input_changed)
# TODO: Command + DEL, ALT + DEL don't work
Entry(warehouse_label_frame, textvariable=website_var).grid(row=0, column=1, sticky=tkinter.EW, padx=8)
Entry(warehouse_label_frame, textvariable=username_var).grid(row=1, column=1, columnspan=2, sticky=tkinter.EW, padx=8)
password_entry = Entry(warehouse_label_frame, textvariable=password_var)
password_entry.grid(row=2, column=1, sticky=tkinter.EW, padx=8)
Button(warehouse_label_frame, text="Search").grid(row=0, column=2)
Button(warehouse_label_frame, text="Copy", command=copy_password_into_clipboard).grid(row=2, column=2)
store_button = Button(warehouse_label_frame, text="Store", command=on_store)
store_button.grid(row=3, columnspan=3, sticky=tkinter.EW, padx=40, pady=20)

set_store_button_state()
col_count, row_count = warehouse_label_frame.grid_size()
for row in range(row_count):
    warehouse_label_frame.grid_rowconfigure(row, minsize=30)


# --- Factory --- #
def on_check_custom():
    if custom_var.get() == 1:
        custom_char_entry.grid(row=4, column=1, sticky=tkinter.W)
    else:
        custom_char_entry.grid_remove()


def generate_passcode_and_fill():
    custom_chars: str
    if custom_var.get():
        custom_chars = custom_char_entry.get()
    else:
        custom_chars = ""
    password = password_generator.generate_password(
        lowercase=lowercase_var.get(),
        uppercase=uppercase_var.get(),
        number=number_var.get(),
        custom_chars=custom_chars,
        required_length=required_length.get()
    )
    password_entry.delete(0, END)
    password_entry.insert(END, password)
    copy_password_into_clipboard()


factory_label_frame = LabelFrame(root_window, text="Factory")
factory_label_frame.grid(row=0, column=1, padx=40)

Label(factory_label_frame, text="Use:").grid(row=0, column=0, sticky=tkinter.E)
Label(factory_label_frame, text="Length:").grid(row=5, column=0, sticky=tkinter.E)
lowercase_var = BooleanVar(value=True)
uppercase_var = BooleanVar(value=True)
number_var = BooleanVar(value=True)
custom_var = BooleanVar(value=False)
Checkbutton(factory_label_frame, text="Lowercase", variable=lowercase_var).grid(row=0, column=1, sticky=tkinter.W)
Checkbutton(factory_label_frame, text="Uppercase", variable=uppercase_var).grid(row=1, column=1, sticky=tkinter.W)
Checkbutton(factory_label_frame, text="Number", variable=number_var).grid(row=2, column=1, sticky=tkinter.W)
Checkbutton(factory_label_frame, text="Custom", variable=custom_var, command=on_check_custom)\
    .grid(row=3, column=1, sticky=tkinter.W)
custom_char_entry = Entry(factory_label_frame, width=10)
custom_char_entry.insert(END, "@,.!?#")
on_check_custom()
required_length = tkinter.IntVar(value=10)
length_spinbox = tkinter.Spinbox(factory_label_frame, from_=4, to=50, textvariable=required_length, wrap=True, width=2)
length_spinbox.grid(row=5, column=1, sticky=tkinter.W, pady=8)

generate_button = Button(factory_label_frame, text="Generate", command=generate_passcode_and_fill)
generate_button.grid(row=6, columnspan=2, sticky=tkinter.EW, padx=40, pady=20)


root_window.mainloop()
