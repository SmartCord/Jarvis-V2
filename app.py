from flask import render_template, Flask, request, jsonify
from flask_socketio import SocketIO
from queue import Queue
from termcolor import colored

import json
import subprocess
import sys
import threading
import time
import logging

import os
import signal

import speech_recognition as sr


processes = {}
app = Flask(__name__)
app.logger.disabled = True
logger = logging.getLogger('werkzeug')
logger.disabled = True

settingsFile = "settings.json"

socket = SocketIO(app)

audio_queue = Queue()
recognizer = sr.Recognizer()

settings_local = {
    "do_listen": True
}

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

def thread(f, args=(), daemon=None):
    threading.Thread(target=f, args=args, daemon=daemon).start()

def botprint(resp):
    print(f"{bot_name} : {resp}")
    os.system(f'{settings()["say_command"]} "{resp}"')

# Load stuff from settings
modules_json = settings()['modules']['filepath']
startup_modules_json = settings()['startup_modules']['filepath']

modules_folder = settings()['modules']['content_folder']
startup_modules_folder = settings()['startup_modules']['content_folder']

bot_name = settings()['name']
recognition = settings()['voice_recognition']
recognizer.energy_threshold = recognition['energy_threshold']
recognizer.pause_threshold = recognition['pause_threshold']
recognizer.dynamic_energy_threshold = recognition['dynamic_energy_threshold']


# Process the given text
def process(text, ignore=None):
    modules = load(modules_json)

    def run(process_name, file, block, args=None, get_output=True):
        out = None
        launches = [settings()['launch'], file]
        if args:
            launches.append(args)

        if not block:
            def dontBlock():
                try:
                    out = subprocess.check_output(launches).decode(sys.stdout.encoding)
                    botprint(out)
                except Exception as e:
                    botprint(str(e))

            if get_output:
                thread(dontBlock)
            else:
                processes[process_name] = subprocess.Popen(launches)

            return

        # Will block
        try:
            if get_output:
                out = subprocess.check_output(launches).decode(sys.stdout.encoding)
                botprint(out)
            else:
                subprocess.call(launches)
        except Exception as e:
            botprint(str(e))

        return out

    for module in sorted(modules['data'], key=lambda k: k['index'], reverse=True):
        block = module['block']
        file = f"{modules_folder}/{module['filename']}"
        get_output = module['get_output']
        process_name = module['process_name']

        if module['process_name'] != ignore:
            for trigger in module['triggers']:
                if module['query']:
                    if text.startswith(trigger['trigger'][:trigger['trigger'].find(" {q}")]):
                        q = text[trigger['trigger'].find("{q}"):]
                        if q:
                            run(process_name, file, block, args=q, get_output=get_output)

                elif trigger['startswith']:
                    if text.startswith(trigger['trigger']):
                        run(process_name, file, block, get_output=get_output)
                else:
                    if trigger['trigger'] == text:
                        run(process_name, file, block, get_output=get_output)


# Routes
@app.route("/processes")
def getProcesses():
    return jsonify({"data": list(processes.keys())})

@app.route("/killprocess/<process>")
def killprocess(process):
    try:
        # os.killpg(os.getpgid(processes[process].pid), signal.SIGTERM)
        processes[process].terminate()
        code = 200
    except KeyError:
        code = 404

    return str(code), code

@app.route("/energy_threshold")
def _energy_threshold():
    new = request.args.get('new')
    updateSettings = request.args.get('updateSettings')

    old = recognizer.energy_threshold
    if new != None:
        recognizer.energy_threshold = int(new)

    if updateSettings == 'yes' and new != None:
        r = settings()
        r['voice_recognition']['energy_threshold'] = int(new)
        write(settingsFile, r)

    data = {
        "old": old,
        "new": int(new) if new != None else None
    }

    return jsonify(data)


def main():
    print(colored("Started startup_modules thread", "blue"))
    # Load startup modules
    for module in load(startup_modules_json)['data']:
        processes[module['process_name']] = subprocess.Popen([settings()['launch'], f"{startup_modules_folder}/{module['filename']}"])
        print(colored(f"Started module : {module['process_name']}", "green"))

def worker():
    print(colored("Started recognizer thread", 'blue'))
    while True:
        audio = audio_queue.get()
        if audio is None: break

        try:
            print(colored("Recognizing...", "yellow"))
            value = recognizer.recognize_google(audio)
            print(colored(f"You said : {value}", "green"))
            process(value)
        except sr.UnknownValueError:
            pass

        audio_queue.task_done()

def listen():
    time.sleep(3)
    print(colored("Started listener thread", "blue"))
    # Wait for your command
    with sr.Microphone() as source:
        try:
            while True:
                audio_queue.put(recognizer.listen(source))
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    thread(main)
    thread(worker, daemon=True)
    thread(listen, daemon=True)

    socket.run(app, port=settings()['port'], use_reloader=settings()['use_reloader'], host=settings()['host'], debug=settings()['debug'])
