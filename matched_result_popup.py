from tkinter import Toplevel, Text, END, DISABLED

from prettytable import PrettyTable

from ui_constants import PROMPT_WEBSITE, PROMPT_PASSWORD, PROMPT_USERNAME, PROMPT_MATCHED_RESULTS


def show(root_window, matched_result: dict):
    # TODO: Better UI design
    pretty_table = PrettyTable()
    pretty_table.field_names = [PROMPT_WEBSITE, PROMPT_USERNAME, PROMPT_PASSWORD]
    pretty_table.align[PROMPT_WEBSITE] = "l"
    pretty_table.align[PROMPT_USERNAME] = "l"
    pretty_table.align[PROMPT_PASSWORD] = "l"
    for key, value in matched_result.items():
        pretty_table.add_row([key, value["username"], value["password"]])

    popup_top = Toplevel(root_window)
    popup_top.config(padx=10, pady=10)
    popup_top.title(PROMPT_MATCHED_RESULTS)
    pretty_format_result: str = pretty_table.get_string()
    first_line_length = len(pretty_format_result.splitlines()[0])
    result_text = Text(popup_top, width=first_line_length, bg=popup_top.cget('bg'),
                       borderwidth=0, highlightthickness=0, font='TkFixedFont')
    result_text.insert(END, pretty_format_result)
    result_text.configure(state=DISABLED)
    result_text.pack()
