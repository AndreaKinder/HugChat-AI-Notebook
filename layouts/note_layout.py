import customtkinter as ctk
import asyncio
from tkinter import Entry, Text, WORD, END, filedialog

from chatbot_configs.import_api import import_text_response
from logs.check_log import check_file_log


class MyFrameNote(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        self.my_entry = Entry(self)
        self.my_entry.grid(row=1, column=1, padx=40, pady=2, ipady=10, sticky='ew')

        self.response_text = Text(self, wrap=WORD, height=25, width=35)
        self.response_text.grid(row=2, column=1, padx=20, pady=5, sticky='ew')
        self.response_text.config(state="disabled")

        self.my_entry.bind('<Return>', lambda event: self.master.after(0, self.print_response_layout))

    def create_text_response_init(self):
        response_update = self.my_entry.get()
        response_init = asyncio.run(self.proceso(entrada=response_update))
        return response_init

    def print_response_layout(self):
        response = self.create_text_response_init()
        self.my_entry.delete(0, END)
        self.response_text.config(state="normal")
        self.response_text.insert(END, response)
        self.response_text.config(state="disabled")

    @staticmethod
    async def proceso(entrada):
        if check_file_log():
            response = await import_text_response(text=entrada)
            return response

    def export_markdown_note(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        if file_path:
            text_to_export = self.response_text.get("1.0", END)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_to_export)

#TODO Add Export Text and Storage Text
#TODO Optiomizar tkinter