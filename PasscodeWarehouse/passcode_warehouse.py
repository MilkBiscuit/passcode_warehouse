import tkinter
import typing
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import *

import pyperclip

import matched_result_popup
import persistent_read
import persistent_write
from password_generator import generate_password
from ui_constants import *

# -------------------- UI setup -------------------- #
root_window = Tk()
root_window.title(APP_NAME)
root_window.config(padx=20, pady=20)


# --- Input Dialog --- #
def pop_dialog_to_ask_backup_passcode(message: str, positive_callable: typing.Any):
    backup_passcode = simpledialog.askstring(title=DIALOG_TITLE_BACKUP_PWD,
                                             prompt=message,
                                             parent=root_window)
    if backup_passcode is None or len(backup_passcode) == 0:
        print("The user didn't set a passcode")
    else:
        positive_callable(backup_passcode)


# --- Import/Export --- #
def on_export_button():
    export_file = filedialog.asksaveasfile(mode="w", defaultextension=".json")
    if export_file is not None:
        persistent_write.export_credentials(export_file)


def on_import_button():
    # TODO: Discarding existing records is not necessary, but there will be potential same-key-conflict
    discard = messagebox.askyesno(title="", message=DIALOG_MESSAGE_CONFIRM_IMPORT)
    if discard:
        persistent_write.clear_all_credentials()
        import_file = filedialog.askopenfile(mode="r", defaultextension=".json")
        if import_file is not None:
            def callback(passcode):
                result = persistent_read.import_credentials(import_file, passcode)
                if result == persistent_read.ImportResult.INHERIT_BACKUP_PASSCODE:
                    messagebox.showinfo(title="", message=f"Your backup passcode is still '{passcode}', because you"
                                                          f" didn't have one before importing.")
                elif result == persistent_read.ImportResult.SUCCESS:
                    messagebox.showinfo(title="", message=DIALOG_MESSAGE_IMPORT_SUCCEED)
                elif result == persistent_read.ImportResult.DECRYPT_PASSCODE_INCORRECT:
                    messagebox.showerror(title="", message=DIALOG_MESSAGE_PASSCODE_INCORRECT)
                else:
                    messagebox.showerror(title="", message=DIALOG_MESSAGE_SOMETHING_WRONG)

            pop_dialog_to_ask_backup_passcode(
                message=DIALOG_MESSAGE_ASK_FOR_BACKUP_PWD,
                positive_callable=callback
            )


backup_label_frame = tkinter.LabelFrame(root_window, text=PROMPT_BACKUP)
backup_label_frame.grid(row=0, column=0, sticky=NSEW)

Button(backup_label_frame, command=on_import_button, text=PROMPT_IMPORT)\
    .grid(row=0, column=0, padx=8, pady=8, sticky=EW)
Button(backup_label_frame, command=on_export_button, text=PROMPT_EXPORT)\
    .grid(row=0, column=1, padx=8, pady=8, sticky=EW)
backup_label_frame.grid_columnconfigure(index=0, weight=1)
backup_label_frame.grid_columnconfigure(index=1, weight=1)


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


def on_username_input_changed(*args):
    set_store_button_state()


def on_website_input_changed(*args):
    set_store_button_state()
    website_value = website_var.get()
    if len(website_value) == 0 or website_value.isspace():
        search_button["state"] = DISABLED
    else:
        search_button["state"] = NORMAL


def on_password_input_changed(*args):
    set_store_button_state()
    password_value = password_var.get()
    if len(password_value) == 0:
        copy_button["state"] = DISABLED
    else:
        copy_button["state"] = NORMAL


def on_store():
    if persistent_read.read_user_backup_passcode() == "":
        pop_dialog_to_ask_backup_passcode(
            message=DIALOG_MESSAGE_INPUT_YOUR_BACKUP_PWD,
            positive_callable=persistent_write.save_user_backup_passcode
        )
        return

    persistent_write.save(website_var.get(), username_var.get(), password_var.get())
    website_var.set("")
    username_var.set("")
    password_var.set("")


def on_website_entry_key_press(event: tkinter.Event):
    if event.keysym == "Return":
        on_search_tapped()
    elif event.keysym == "BackSpace":
        if event.keycode == 864026751:
            # Option + Backspace
            current_website_value = website_var.get()
            last_space_index = current_website_value.rfind(" ")
            if last_space_index == -1:
                website_entry.delete(0, "insert")
            elif not current_website_value[website_entry.index("insert") - 1].isspace():
                website_entry.delete(last_space_index + 1, "insert")
        elif event.keycode == 855638143:
            # Command + Backspace
            website_entry.delete(0, "insert")


def on_search_tapped():
    result = persistent_read.search_and_decrypt(website_var.get())
    matched_result_num = len(result.keys())
    if matched_result_num == 1:
        website_key = next(iter(result))
        username_var.set(result[website_key]["username"])
        password_var.set(result[website_key]["password"])
    else:
        if matched_result_num > 1:
            matched_result_popup.show(root_window, result)
        username_var.set("")
        password_var.set("")


warehouse_label_frame = tkinter.LabelFrame(root_window, text=PROMPT_WAREHOUSE)
warehouse_label_frame.grid(row=1, column=0, sticky=NSEW)

Label(warehouse_label_frame, text=PROMPT_WEBSITE).grid(row=0, column=0, sticky=E)
Label(warehouse_label_frame, text=PROMPT_USERNAME).grid(row=1, column=0, sticky=E)
Label(warehouse_label_frame, text=PROMPT_PASSWORD).grid(row=2, column=0, sticky=E)
website_var = StringVar()
username_var = StringVar()
password_var = StringVar()
website_var.trace("w", on_website_input_changed)
username_var.trace("w", on_username_input_changed)
password_var.trace("w", on_password_input_changed)
website_entry = Entry(warehouse_label_frame, textvariable=website_var)
website_entry.grid(row=0, column=1, sticky=EW, padx=8)
website_entry.bind(sequence="<Return>", func=on_website_entry_key_press)
website_entry.bind(sequence="<Option-BackSpace>", func=on_website_entry_key_press)
website_entry.bind(sequence="<Command-BackSpace>", func=on_website_entry_key_press)
Entry(warehouse_label_frame, textvariable=username_var).grid(row=1, column=1, columnspan=2, sticky=EW, padx=8)
password_entry = Entry(warehouse_label_frame, textvariable=password_var)
password_entry.grid(row=2, column=1, sticky=EW, padx=8)
search_button = Button(warehouse_label_frame, text=PROMPT_SEARCH, command=on_search_tapped)
search_button.grid(row=0, column=2, padx=8)
copy_button = Button(warehouse_label_frame, text=PROMPT_COPY, command=copy_password_into_clipboard)
copy_button.grid(row=2, column=2, padx=8)
# Just for spacing
Label(warehouse_label_frame).grid(row=3, column=0)
warehouse_label_frame.grid_rowconfigure(index=3, weight=1)
store_button = Button(warehouse_label_frame, text="Store", command=on_store)
store_button.grid(row=4, columnspan=3, padx=40, pady=(0, 8), sticky=EW)
warehouse_label_frame.grid_rowconfigure("all", minsize=30)

on_website_input_changed()
on_username_input_changed()
on_password_input_changed()


# --- Factory --- #
def on_custom_checked():
    if custom_var.get():
        custom_char_entry["state"] = NORMAL
    else:
        custom_char_entry["state"] = DISABLED


def generate_passcode_and_fill():
    custom_chars: str
    if custom_var.get():
        custom_chars = custom_char_entry.get()
    else:
        custom_chars = ""
    password = generate_password(
        lowercase=lowercase_var.get(),
        uppercase=uppercase_var.get(),
        number=number_var.get(),
        custom_chars=custom_chars,
        required_length=required_length.get()
    )
    password_entry.delete(0, END)
    password_entry.insert(END, password)
    copy_password_into_clipboard()


factory_label_frame = tkinter.LabelFrame(root_window, text=PROMPT_FACTORY)
factory_label_frame.grid(row=0, column=1, rowspan=2, padx=(20, 0), sticky=NSEW)

Label(factory_label_frame, text=PROMPT_USE).grid(row=0, column=0, sticky=E)
Label(factory_label_frame, text=PROMPT_LENGTH).grid(row=5, column=0, sticky=E)
lowercase_var = BooleanVar(value=True)
uppercase_var = BooleanVar(value=True)
number_var = BooleanVar(value=True)
custom_var = BooleanVar(value=False)
Checkbutton(factory_label_frame, text=PROMPT_LOWERCASE, variable=lowercase_var).grid(row=0, column=1, sticky=W)
Checkbutton(factory_label_frame, text=PROMPT_UPPERCASE, variable=uppercase_var).grid(row=1, column=1, sticky=W)
Checkbutton(factory_label_frame, text=PROMPT_NUMBER, variable=number_var).grid(row=2, column=1, sticky=W)
Checkbutton(factory_label_frame, text=PROMPT_CUSTOM, variable=custom_var, command=on_custom_checked) \
    .grid(row=3, column=1, sticky=W)
custom_char_entry = Entry(factory_label_frame, width=10)
custom_char_entry.insert(END, DEFAULT_CUSTOM_CHARACTERS)
custom_char_entry.grid(row=4, column=1, sticky=W)
on_custom_checked()
required_length = IntVar(value=10)
length_spinbox = Spinbox(factory_label_frame, from_=4, to=50, textvariable=required_length, wrap=True, width=2)
length_spinbox.grid(row=5, column=1, sticky=W, pady=8)
# Just for spacing
Label(factory_label_frame).grid(row=6, column=0)
factory_label_frame.grid_rowconfigure(index=6, weight=1)
generate_button = Button(factory_label_frame, text=PROMPT_GENERATE, command=generate_passcode_and_fill)
generate_button.grid(row=7, columnspan=2, padx=40, pady=(0, 8), sticky=EW)

menubar = Menu(root_window)
root_window.config(menu=menubar)
root_window.grid_rowconfigure(index=1, weight=1)
root_window.mainloop()
