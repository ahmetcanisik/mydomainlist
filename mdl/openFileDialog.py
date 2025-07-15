#!/usr/bin/env python3
import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image
from .utils import data, get_domains
class OpenFileDialogBox(ctk.CTkFrame):
    def __init__(self, master, mainframe, placeholder, name):
        super().__init__(master, fg_color="transparent")
        self.name = name
        self.placeholder = placeholder
        self.mainframe = mainframe
        self.grid_columnconfigure((0, 1), weight=1)

        self.entry = ctk.CTkEntry(self, state="normal", width=250, height=50, fg_color=data["colors"]["entry"], text_color=data["colors"]["entry_text"], border_color=data["colors"]["entry_border_color"], corner_radius=4)
        self.entry.grid(row=0, column=0, sticky="e")
        self.entry.insert(0, self.placeholder)

        file_icon = ctk.CTkImage(light_image=Image.open(data["img"]["file"][0]), dark_image=Image.open(data["img"]["file"][1]), size=(16, 16))

        self.button = ctk.CTkButton(self, image=file_icon, text="", width=48, height=48, command=self.button_clicked)
        self.button.grid(row=0, column=1, padx=0, pady=0, sticky="w")

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, ctk.END)

    def button_clicked(self):
        data["location"][self.name] = filedialog.askopenfilename()
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, data["location"][self.name])

        if (self.name == "json"):
            get_domains(data["location"]["json"])
            self.mainframe.category_menu.combobox.configure(values=data["category_list"])
            
class FileDialogBox(ctk.CTkFrame):
    def __init__(self, master, mainframe):
        super().__init__(master, fg_color="transparent", width=300)
        self.mainframe = mainframe
        self.grid_columnconfigure((0, 1), weight=1)

        label_font = ctk.CTkFont(size=14, weight="bold")

        self.label_json = ctk.CTkLabel(self, font=label_font, text="List (.json)")
        self.label_json.grid(row=0, column=0, pady=10, sticky="nsew")

        self.open_json_box = OpenFileDialogBox(self, mainframe=self.mainframe, placeholder="./domains.json", name="json")
        self.open_json_box.grid(row=0, column=1, pady=10, sticky="nsew")

        self.label_readme = ctk.CTkLabel(self, font=label_font, text="Output (.md)")
        self.label_readme.grid(row=1, column=0, pady=10, sticky="nsew")

        self.open_readme_box = OpenFileDialogBox(self, mainframe=self.mainframe, placeholder="./readme.md", name="readme")
        self.open_readme_box.grid(row=1, column=1, pady=10, sticky="nsew")

    def clear(self):
        self.open_json_box.clear()
        self.open_readme_box.clear()