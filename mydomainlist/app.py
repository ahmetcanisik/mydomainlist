#!/usr/bin/env python3
from frames import *
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        log(type="info", message=f"{terminal_color.BOLD}mydomainlist{terminal_color.ENDC} {terminal_color.OKCYAN}was started...")
        self.title("Convert Domains List to Markdown Table")
        self.geometry("500x600")
        self.grid_columnconfigure(0, weight=1)
        ctk.set_appearance_mode(data["preferences"]["theme"])
        get_domains(data["location"]["json"])

        self.header = Header(self)
        self.header.grid(row=0, column=0, padx=0, pady=0, sticky="new")

        self.main = MainFrame(self)
        self.main.grid(row=1, column=0, padx=0, pady=0, sticky="new")


if __name__ == "__main__":
    app = App()
    app.mainloop()