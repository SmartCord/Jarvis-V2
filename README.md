# Incomplete and confusing documentation
can a native english speaker write a documentation for me lol

# Setup
- Install python 3.6+ from [here](https://python.org)
-  Clone repository `git clone https://github.com/SmartCord/Jarvis-V2.git`
- Install all the requirements by doing `pip install -r requirements.txt`

### Configuration
It is required to configure the assistant first before using it.

settings.json
```
{
    "modules": {
        "filepath": "/path/to/modules.json",
        "content_folder": "/path/to/modules_folder"
    },
    "startup_modules": {
        "filepath": "/path/to/startup_modules.json",
        "content_folder": "/path/to/startup_modules_folder"
    },
    "name": "Jarvis",
    "launch": "python",
    "voice_recognition": {
        "energy_threshold": 2500,
        "pause_threshold": 1.0,
        "dynamic_energy_threshold": false
    },
    "say_command": "say",
    "port": 5000,
    "host": "127.0.0.1",
    "debug": false,
    "use_reloader": false
}
```
|Key|Description  | Default Value|
|--|--|--|
| modules.filepath |File path to modules.json  |none	 |
|modules.content_folder| Path to where all the modules are | none
| startup_modules.filepath |File path to startup_modules.json  |none	 |
|startup_modules.content_folder| Path to where all the startup_modules are | none
|name|The name of the assistant|Jarvis
|launch|Launch command used, normally it's python| python
|voice_recognition.energy_threshold| Represents the energy level threshold for sounds. Values below this threshold are considered silence, and values above this threshold are considered speech.| 2500
|voice_recognition.pause_threshold| Represents the minimum length of silence (in seconds) that will register as the end of a phrase. | 0.8
|voice_recognition.dynamic_energy_threshold|Represents whether the energy level threshold sounds should be automatically adjusted based on the currently ambient noise level while listening.|false
|say_command| Command used to make the assistant speak, normally it's 'say' for macos. Might be different for windows.| say
|port| Port to run on| 5000
|host| Host to use | 127.0.0.1
|debug| Use flask debug | false
|use_reloader| Automatically reload server when making changes to app.py| false

# Modules
### How does it work?
Each module contains at least one trigger.
Think of a trigger as a word/sentence you have to say to make the assistant do something.

#### Example 1
Let's say there's a module called Time Check which tells you what time is it
The trigger is "what time is it"
When you say "what time is it" the module's file will be executed and that file contains the answer to your question.

modules.json
```
{
    "data": [
        {
            "index": 0,
            "module_name": "Time Check",
            "process_name": "time_check",
            "filename": "time_check.py",
            "action": "Gives you the current time",
            "block": true,
            "query": false,
            "get_output": true,
            "triggers": [
                {
                    "startswith": true,
                    "trigger": "time check"
                },
                {
                    "startswith": true,
                    "trigger": "what time is it"
                }
            ]
        },
        {
            "index": 0,
            "module_name": "Google Search Text",
            "process_name": "google_search_text",
            "filename": "google_search_text.py",
            "action": "Google Search",
            "block": false,
            "query": true,
            "get_output": false,
            "triggers": [
                {
                    "startswith": true,
                    "trigger": "google {q}"
                },
                {
                    "startswith": true,
                    "trigger": "can you google {q}"
                }
            ]
        }
    ]
}

```
