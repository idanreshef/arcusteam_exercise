# Bytes Pattern Finder
Arcusteam exercise

## Description
This application has several modes that handles bytes patterns.
It gets arguments from the user via a CLI and prints an output according to the user's mode choice and other arguments.


## How to execute
Use a linux CLI and make sure that python3 is installed.
In order to run it, just type:

```bash
python3 /THE/FULL/PATH/TO/arcustream_exercise/app.py
```

## The application's modes

1. Basic mode - In this mode, the system gets a path of a binary file and a threshold (number) and returns a json.
Every record in the json represents a binary sequence that repeating in a specific section that it's length is bigger than the threshold.
Example for an output record: {'range': (1008, 1038), 'size': 30, 'repeating_byte': b'\x00'}.
It means that this byte (b'\x00') appears 30 times in a row between 1008 and 1038 indices in the file (the threshold is <= 30 of course).

2. Regex Mode - In this mode, the system gets an expected bytes format and structure.
The current version supports one bytes as a prefix and as many bytes as you want in the structure an hopefully there will be support for
several bytes prefix in the next version ;)
E.g: If I want to get all of the 3 bytes sequences that starts with 'F' - the input will be 'FXX' (without the quote marks).

3. Custom Mode - In this mode, the user provides a dictionary with specific bytes to look for in the file and a mapper to some other string.
The application will return a dictionary with this string and the amount of appearances of it's original key in the file.
Please note that all of the keys must be valid hex strings and that it should include any new line
(you can use copy-paste - but make sure that everything is in the same row!)

## CLI Instructions
- You can type 'help' at any time and go back to the same phase you were in.
- There are three attempts to provide a valid input in each phase: (phase 1 - mode + file, phase 2 - specific arguments per mode).
- A valid input is a numeric option that can be found in the options list, existing file path or other arguments in the expected structure and
format (the mapper should be a valid dict, threshold should be a number etc).
- You SHOULDN'T add any quotes to your arguments (type file_path and not 'file_path')
- Pressing `help` won't have an impact on the attempts number.
- In order to exit the program just press CTRL + C.
