# dumpTk
Project with intent to dump Tk GUI toolkit from projects implemented with Tkinter interface and use Qt GUI toolkit instead.

## Main idea of this repository
There will be `middleware.py` and many folders. `middleware.py` should provide interface for Tkinter to use Qt via PyQt. In folders, there will be some examples of Tkinter, which should be using provided interface. If interface from `middleware.py` won't be applicable, there will be own file with interface. Last optional file is implementation of example using PyQt.

### Folder structure
```
└── dumpTk
    ├── README.md
    ├── middleware.py
    ├── requirements.py
    └── {name_of_example}
        ├── {name_of_example}_tkinter.py
        └── {name_of_example}_middleware.py
        └── {name_of_example}_pyqt.py
```

### Virtual envs
There is `requirements.txt` provided by `pip freeze` for each from examples.

## Implemented examples
- *Window* - or simple Frame / QWidget from: https://dm4rnde.com/py-gui-soluts-tkinter-comp-to-pyqt5 

- *Hello world9 - Simple program with buttons and callbacks from Tkinter docs: https://docs.python.org/3/library/tkinter.html  
