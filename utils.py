#!/usr/bin/env python3
import os
import json
import subprocess
from messagebox import MessageBox
from datetime import datetime
class terminal_color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

data = {
    "name": "My Domain List",
    "version": "0.0.1",
    "description": "A desktop gui program to create your own domain list.",
    "main": "app.py",
    "repository": "https://github.com/ahmetcanisik/mydomainlist.git",
    "author": "ahmetcanisik <can.isik.business@gmail.com> (https://ahmetcanisik.com)",
    "license": "MIT",
    "preferences": {
        "theme": "system",
        "lang": "English"
    },
    "colors": {
        "header": ("#BED0FF", "#162755"),
        "header_title": ("#06163F", "#ffffff"),
        "main": ("#FFFFFF", "#2C4587"),
        "entry": ("#E6ECFC", "#152449"),
        "entry_text": ("#000000", "#C7D6FF"),
        "entry_border_color": "#000000"
    },
    "img": {
        "settings": ["./assets/vector/settings/light.png", "./assets/vector/settings/dark.png"],
        "world": ["./assets/vector/world/light.png", "./assets/vector/world/dark.png"],
        "file": ["./assets/vector/file/light.png", "./assets/vector/file/dark.png"],
        "clear": ["./assets/vector/clear/light.png", "./assets/vector/clear/dark.png"],
        "add": ["./assets/vector/add/light.png", "./assets/vector/add/dark.png"],
        "push": ["./assets/vector/push/light.png", "./assets/vector/push/dark.png"]
    },
    "location": {
        "json": "domains.json",
        "readme": "README.md"

    },
    "domains": [],
    "category_list": [],
    "selected_category": "without_category",
    "last_added": [],
    "entrys": {
        "domain": "example.com",
        "description": "Domain name that is free to use in projects."
    }
}

def log(type="info", message="your log is here!"):
    state = ""
    if type == "info":
        state = f"{terminal_color.OKBLUE}[   INFO   ]{terminal_color.ENDC}"
    elif type == "warn":
        state = f"{terminal_color.WARNING}[   WARN   ]{terminal_color.ENDC}"
    elif type == "err":
        state = f"{terminal_color.FAIL}[   ERR    ]{terminal_color.ENDC}"
    elif type == "good":
        state = f"{terminal_color.OKGREEN}[   GOOD   ]{terminal_color.ENDC}"

    result = f"{terminal_color.HEADER}[    {datetime.now()}    ]{terminal_color.ENDC} {state} {terminal_color.OKCYAN}{message}{terminal_color.ENDC}"
    print(result)

    appdata_path = os.getenv('APPDATA')
    log_file_path = os.path.join(appdata_path, 'mydomainslist', 'log.txt')

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    with open(log_file_path, 'a', encoding="utf-8") as log_file:
        log_file.write('\n' + result + '\n')

def get_domains(file_path):
    if not os.path.exists(file_path):
        log(type="err", message=f"file_path:{file_path} not found")
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                log(type="info", message=f"openning... {terminal_color.BOLD}{file_path}{terminal_color.ENDC}")
                data["domains"].append(json.load(file))
                log(type="good", message=f"{terminal_color.BOLD}{file_path}{terminal_color.ENDC}{terminal_color.OKCYAN} successfully readed")
                data["category_list"] = list(data["domains"][0].keys())
                log(type="good", message="category list was updated")
            except json.JSONDecodeError as e:
                MessageBox(title="Error", message=f"Error: Could not read JSON file - {e}", icon="cancel")
                log(type="err", message=f"Error: Could not read JSON file - {e}")

def set_domains(domains_list, file_path):
    #if not os.path.exists(file_path):
    #   log(type="err", message=f"file_path:{file_path} not found, ilgili dizinde domains.json dosyası oluşturulyor")"""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(domains_list, file, ensure_ascii=False, indent=4)
            log(type="good", message=f"successfully written to {file_path}")
    except Exception as e:
        log(type="err", message=f"ups! something went wrong {e}")

def add_github(message="new domain was added", branch="main"):
    try:
        subprocess.run(["git", "checkout", "-b", branch], check=True)
    except subprocess.CalledProcessError as e:
        log(type="err", message=f"Branch creation or migration failed: {e}")

    try:
        subprocess.run(["git", "branch", "-M", branch], check=True)
        
        subprocess.run(["git", "add", "*"], check=True)
        
        subprocess.run(["git", "commit", "-m", message], check=True)
        
        subprocess.run(["git", "push", "origin", branch], check=True)

        log(type="info", message="The changes have been submitted successfully.")
    except subprocess.CalledProcessError as e:
        log(type="err", message="Command failed!")
        print(e)