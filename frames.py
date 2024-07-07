from openFileDialog import FileDialogBox
from PIL import Image
import customtkinter as ctk
from converter import ConvertMarkdown
from CTkToolTip import CTkToolTip
from utils import *


class OptionMenuBox(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.category_list = data["category_list"]

        new_category_list = []
        for category in self.category_list:
            new_category_list.append(category.replace('_', ' '))

        self.category_list = new_category_list

        initial = ctk.StringVar(value=data["selected_category"].replace("_", ' '))
        label_font = ctk.CTkFont(size=14, weight="bold")

        self.label = ctk.CTkLabel(self, text="Category", font=label_font)
        self.label.grid(row=0, column=0, sticky="nsew")

        self.combobox = ctk.CTkComboBox(self, values=self.category_list, variable=initial, width=200, height=50, fg_color=data["colors"]["entry"], text_color=data["colors"]["entry_text"], border_color=data["colors"]["entry_border_color"], corner_radius=4,  command=self.combobox_onchange)
        self.combobox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    def combobox_onchange(self, category):
        data["selected_category"] = category.replace(' ', '_')

    def reset(self):
        self.combobox.configure(values=[data["selected_category"]])

class DomainConfigureBox(ctk.CTkFrame):
    def __init__(self, master, name, text, placeholder):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure((0, 1), weight=1)
        self.text = text
        self.name = name
        self.placeholder = placeholder

        label_font = ctk.CTkFont(size=14, weight="bold")

        self.label = ctk.CTkLabel(self, text=self.text, font=label_font)
        self.label.grid(row=0, column=0, sticky="nsew")

        self.entry = ctk.CTkEntry(self, placeholder_text=self.placeholder, width=250, height=50, fg_color=data["colors"]["entry"], text_color=data["colors"]["entry_text"], border_color=data["colors"]["entry_border_color"], corner_radius=4, state="normal")
        self.entry.grid(row=0, column=1, sticky="nsew")

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, ctk.END)

class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=data["colors"]["header"])
        self.grid_columnconfigure((0, 1), weight=1)

        s12_b = ctk.CTkFont(size=12, weight="bold")

        icon_settings = ctk.CTkImage(light_image=Image.open(data["img"]["settings"][0]),
                                     dark_image=Image.open(data["img"]["settings"][1]), size=(24, 24))

        self.title = ctk.CTkLabel(self, text="My Domain List", text_color=data["colors"]["header_title"], font=s12_b)
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.settings_button = ctk.CTkButton(self, image=icon_settings, text="", fg_color="transparent", width=24, command=self.settings_button_clicked)
        self.settings_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    def settings_button_clicked(self):
        msg = MessageBox(title="Very soon!", message="The Settings section will come in later versions.", icon="info")

class Title(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)

        s24_b = ctk.CTkFont(size=24, weight="bold")

        icon_title = ctk.CTkImage(light_image=Image.open(data["img"]["world"][0]),
                                  dark_image=Image.open(data["img"]["world"][1]), size=(24, 24))

        label_image = ctk.CTkLabel(self, image=icon_title, text="")
        label_image.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="ne")

        label_text = ctk.CTkLabel(self, text="Add Domain", font=s24_b)
        label_text.grid(row=0, column=1, padx=0, pady=10, sticky="nw")

class ButtonBox(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.mainframe = master
        self.grid_columnconfigure((0, 1, 2), weight=1)


        clear_icon = ctk.CTkImage(light_image=Image.open(data["img"]["clear"][0]), dark_image=Image.open(data["img"]["clear"][1]), size=(24, 24))
        self.clear_button = ctk.CTkButton(self, image=clear_icon, text="", command=self.clear_domains)
        self.clear_button.grid(row=0, column=0, padx=5, sticky="nsew")
        self.clear_tooltip = CTkToolTip(self.clear_button, message="Clear All Text")

        self.add_icon = ctk.CTkImage(light_image=Image.open(data["img"]["add"][0]), dark_image=Image.open(data["img"]["add"][1]), size=(24, 24))
        self.add_button = ctk.CTkButton(self, image=self.add_icon, text="", command=self.add_domains)
        self.add_button.grid(row=0, column=1, padx=5, sticky="nsew")
        self.add_tooltip = CTkToolTip(self.add_button, message="Add Domain")

        push_icon = ctk.CTkImage(light_image=Image.open(data["img"]["push"][0]),
                                    dark_image=Image.open(data["img"]["push"][1]), size=(24, 24))
        self.push_button = ctk.CTkButton(self, image=push_icon, text="(beta)", command=self.push_github)
        self.push_button.grid(row=0, column=3, padx=5, sticky="nsew")
        self.push_tooltip = CTkToolTip(self.push_button, message="Push Github Your Files")

    def add_domains(self):

        domain = self.mainframe.domain_name.get()
        description = self.mainframe.domain_description.get()

        if not domain or not description:
            error_msg = MessageBox(title="Warning", message="Please make sure you fill in all the boxes!",
                                   icon="warning")
            log(type="warn", message="Please make sure you fill in all the boxes!")
            return

        data["entrys"]["domain"], data["entrys"]["description"] = domain, description
        data["last_added"].append({
            "Domain": domain,
            "Description": description
        })

        
        if data["selected_category"] not in data["domains"][0]:
            data["domains"][0][data["selected_category"]] = []

        data["domains"][0][data["selected_category"]].append({
            "Domain": domain,
            "Description": description
        })

        info = f'Updated domain list: {data["selected_category"]}: {data["domains"][0][data["selected_category"]][:-1]}, {terminal_color.HEADER}{data["domains"][0][data["selected_category"]][-1]}{terminal_color.ENDC}'
        set_domains(data["domains"][0], data["location"]["json"])

        log(type="info", message=info)

        log(type="info", message="Converting domains...")

        ConvertMarkdown(domains_path=data["location"]["json"], title="My Domain List", readme=data["location"]["readme"], domain_check="True")

        log(type="good", message=f"Successfully Converted Domains to Markdown Table... {data['location']['readme']}")

        msg = MessageBox(title="Success!", message='Your domains added!', icon="check")

    def clear_domains(self):
        data["location"]["json"] = "./domains.json"
        data["location"]["readme"] = "./README.md"
        data["entrys"]["domain"] = ""
        data["entrys"]["description"] = ""
        data["domains"] = []
        data["category_list"] = []
        data["selected_category"] = "ozel_alan_adlari"
        self.mainframe.dialog.clear()
        self.mainframe.category_menu.reset()
        self.mainframe.domain_name.clear()
        self.mainframe.domain_description.clear()
        msg = MessageBox(title="Info", message="All Areas was cleared!")
        log(type="info", message="All Areas was cleared!")

    def push_github(self):
        add_github(message=f"added {data["entrys"]["domain"]}", branch="main")
        msg = MessageBox(title="Pushed!", message="Successfully pushed to Github.", icon="check")

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=data["colors"]["main"])

        self.grid_columnconfigure(0, weight=1)

        self.title = Title(self, fg_color="transparent")
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.dialog = FileDialogBox(self, mainframe=self)
        self.dialog.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        self.category_menu = OptionMenuBox(self)
        self.category_menu.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.domain_name = DomainConfigureBox(self, name="domain", text="Domain Name", placeholder="Enter Domain Name...")
        self.domain_name.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.domain_description = DomainConfigureBox(self, name="description", text="Domain Description", placeholder="Enter Domain Description...")
        self.domain_description.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        self.button_box = ButtonBox(self)
        self.button_box.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")