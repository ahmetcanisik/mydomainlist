#!/usr/bin/env python3
import os
import json
import subprocess
from .messagebox import MessageBox
from datetime import datetime
from rich.console import Console
from rich.text import Text

console = Console()

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
    now = datetime.now()
    if type == "info":
        state = "[bold blue][   INFO   ][/bold blue]"
    elif type == "warn":
        state = "[bold yellow][   WARN   ][/bold yellow]"
    elif type == "err":
        state = "[bold red][   ERR    ][/bold red]"
    elif type == "good":
        state = "[bold green][   GOOD   ][/bold green]"
    else:
        state = "[bold][   LOG    ][/bold]"

    timestamp = f"[magenta][    {now}    ][/magenta]"
    msg = f"{timestamp} {state} [cyan]{message}[/cyan]"
    console.print(msg)

    appdata_path = os.getenv('APPDATA')
    if not appdata_path:
        # Fallback for non-Windows systems
        appdata_path = os.path.expanduser('~/.mydomainslist')
        log_file_path = os.path.join(appdata_path, 'log.txt')
    else:
        log_file_path = os.path.join(appdata_path, 'mydomainslist', 'log.txt')
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'a', encoding="utf-8") as log_file:
        log_file.write('\n' + f"{now} {type.upper()} {message}" + '\n')

def get_domains(file_path):
    if not os.path.exists(file_path):
        log(type="err", message=f"file_path:{file_path} not found")
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                log(type="info", message=f"openning... [bold]{file_path}[/bold]")
                data["domains"].append(json.load(file))
                log(type="good", message=f"[bold]{file_path}[/bold] [cyan]successfully readed[/cyan]")
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
            log(type="good", message=f"successfully written to [bold]{file_path}[/bold]")
    except Exception as e:
        log(type="err", message=f"ups! something went wrong [red]{e}[/red]")

def add_github(message="new domain was added", branch="main"):
    try:
        subprocess.run(["git", "checkout", "-b", branch], check=True)
    except subprocess.CalledProcessError as e:
        log(type="err", message=f"Branch creation or migration failed: [red]{e}[/red]")

    try:
        subprocess.run(["git", "branch", "-M", branch], check=True)
        
        subprocess.run(["git", "add", "*"], check=True)
        
        subprocess.run(["git", "commit", "-m", message], check=True)
        
        subprocess.run(["git", "push", "origin", branch], check=True)

        log(type="info", message="The changes have been submitted successfully.")
    except subprocess.CalledProcessError as e:
        log(type="err", message="Command failed!")
        print(e)