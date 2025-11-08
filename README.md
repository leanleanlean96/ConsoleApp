# Console Shell
Python programming course lab #3.
## Description
Interactive console shell build with **typer** that mimics linux terminal commands. Every user action and error is logged to shell.log. History is saved in .history and is saved between the sessions.
___
### Libraries:
- typer
- typer-shell
- os
- shutil
- shlex
- pathlib
- pyfakefs
- unittest
____
### Algorithm
1. User enter the command
2. Command is parsed and checked for correctness by typer
3.  All restrictions required for the command to run are checked
4. If passed all restriction checks, the command is executed and info message is logged
5. Else, the error message is logged
6. If command has output result, it is written in console
7. Back to step 1
___

### Available commands: 
- ls [several sources, -l --long: show detailed info, -a --all: show hidden files]
- cd
- cat
- cp [several sources, -r --recursive: copy recursively]
- mv
- rm [several sources, -r --recursive]
- tar
- untar
- zip
- unzip
- grep [several sources, -r --recursive: search recursively, -i --ignore-case: ignore case of Pattern]
- history
## How to set up?
1. Clone the repo:
```
git clone https://github.com/leanleanlean96/ConsoleApp
```
2. Run the program:
```
python3 -m src.main
```
3. To check command usage rules, type:
 ```
  help
 ```

## Architecture
```
console-app-sample/
├── src/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── cat.py
│   │   ├── cd.py
│   │   ├── command_registrator.py
│   │   ├── cp.py
│   │   ├── grep.py
│   │   ├── history.py
│   │   ├── ls.py
│   │   ├── mv.py
│   │   ├── rm.py
│   │   ├── tar.py
│   │   ├── undo.py
│   │   └── zip.py
│   ├── common/
│   │   ├── __init__.py
│   │   └── errors.py config.py
│   └── errors.py  
│   ├── enums/
│   │   ├── __init__.py
│   │   ├── archive_format.py
│   │   └── file_mode.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── history_service.py
│   │   ├── init_services.py
│   │   └── linux_console.py
│   ├── __init__.py
│   └── main.py
│		 
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_history.py
│   └── test_linux_console.py
│   
└── requirements.txt
```
