# dumpTk
Project with intent to dump Tk GUI toolkit from projects implemented with Tkinter interface and use Qt GUI toolkit instead.

### Virtual envs
There is `requirements.txt` provided by `pip freeze` for instalation of your virtualenv.

## Implemented examples
- *Hello world* - Simple program with buttons and callbacks from Tkinter docs: https://docs.python.org/3/library/tkinter.html . Run by `python hello_world_tkinter.py` in your virtualenv.
- *Menu* - Simple program with only menu available. Run by `python menu.py` in your virtualenv.
- *All widgets example* - Simple program with more classes. Sourced from https://runestone.academy/runestone/books/published/thinkcspy/GUIandEventDrivenProgramming/03_widgets.html. Run by `python all_user_input_widgets.py` in your virtualenv.

## Own example
- In your file (needs to be in directory of this project, until pip) you could use this program just by importing `qtinter` instead of `tkinter`.
- Few examples:
  - Change `import tkinter as tk` to `import qtinter as tk`
  - Change `from tkinter import *` to `from qtinter import *`
  - Change `from tkinter import ttk` to `from qtinter import ttk`
  - Change `from tkinter.filedialog import filedialog` to `import qtfiledialog as filedialog` (yes, this needs submodule to work the same way)

## Currenct version main files
- *qtinter.py* - Main file with `Tk` class which inherits from original `Tk` tkinter class. Each call is wrapped by `TkWrapeer` and sent to the `Implementer`.
- *implementer.py* - File with `Implementer` class. Parses Tcl command to recognize Tcl class, which translates to PyQt class. Then according to more options from Tcl command translates these options with functions from `tktoqt.py`.
- *tktoqt.py* - Has set of functions to solve mapping Tcl command parameters to according methods (of parameters of those methods) of PyQt objects according to mapping.
- *parameters_mapping.py* - Defines mapping from Tcl options (and values) to methods (and parameters) of PyQt objects.
- *layouter.py* - Solves layouts of PyQt objects according to their settings in Tcl. Used by `Implementer` class.
- *qtfiledialog.py* - Standalone file supling now for filedialogs from Tkinter.

## How to improve
- Implement new Tcl object
  - Add translation of Tcl object to `translate_class_dict` dictionary in the begining of `implementer.py`.
- Implement new Tcl option (value) of object
  - Add translation of Tcl option (value) translation to `translate_class_dict` (`parameters_values_mapping`) in `parameters_mapping.py`

