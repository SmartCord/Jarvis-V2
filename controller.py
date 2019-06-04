import json

from termcolor import colored
from pprint import pprint

settingsFile = "settings.json"

def load(jf):
    with open(jf) as f:
        r = json.load(f)
        f.close()

    return r

def settings():
    return load(settingsFile)

def write(fp, new):
    with open(fp, 'w+') as f:
        f.seek(0)
        json.dump(new, f, indent=4)
        f.close()

modules_json = settings()['modules']['filepath']
startup_modules_json = settings()['startup_modules']['filepath']


# this thing is incomplete and not tested so don't use it unless you wanna fuck up your modules.json file.

while True:
    text = input("Command : ")
    if text.startswith("new module"):
        name = text[11:]
        if not name:
            print(colored("missing required argument : <name>", "red"))
        else:
            process_name = input("Process Name : ")
            file_name = input("File Name : ")
            action = input("Action (Description) : ")
            block = input("Block (true/false) : ")

            if block == "true":
                block = True
            elif block == "false":
                block = False

            query = input("Query(true/false) : ")
            if query == "true":
                query = True
            elif query == "false":
                query = False

            get_output = input("Get Output(true/false) : ")
            if get_output == "true":
                get_output = True
            elif get_output == "false":
                get_output = False

            triggers = []

            print(colored("Time to add some triggers.\nOnce you're done adding triggers just type TRIGGERS_DONE", "yellow"))
            while True:
                startswith = input(f"Startswith(true/false) : ")
                if startswith == "true":
                    startswith = True
                elif startswith == "false":
                    startswith = False
                elif startswith == "TRIGGERS_DONE":
                    break

                trigger = input(f"Trigger : ")
                if trigger == "TRIGGERS_DONE":
                    break

                data = {
                    "startswith": startswith,
                    "trigger": trigger
                }
                triggers.append(data)

            data = {
                "index": 0,
                "module_name": name,
                "process_name": process_name,
                "filename": file_name,
                "action": action,
                "block": block,
                "query": query,
                "get_output": get_output,
                "triggers": triggers
            }

            r = load(modules_json)
            r['data'].append(data)
            write(modules_json, r)

            print(colored(f"Successfully created module : {name}", "green"))
            pprint(data)
            print("")
    else:
        print(colored("Invalid Command, Type help for a list of commands.", "red"))
