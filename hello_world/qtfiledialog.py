from PyQt5.QtWidgets import QFileDialog

# ---------------------------------------------

file_dialog_translate = {
    'askopenfilename': 'getOpenFileName',
    'asksaveasfilename': 'getSaveFileName',
    'askopenfilenames': 'getOpenFileNames',
    'askopenfile': 'TODO', # TODO: Need to make my own function ...?
    'askopenfiles': 'TODO', # TODO: Need to make my own function ...?
    'asksaveasfile': 'TODO', # TODO: Need to make my own function ...?
    'askdirectory': 'getExistingDirectory', # TODO: Additional keyword option: mustexist - determines if selection must be an existing directory.
}

# ---------------------------------------------

def exec_dialog(func, **options):
    # TODO: Solve options
    dialog = QFileDialog()
    return getattr(dialog, file_dialog_translate[func])()

def askopenfilename(**options):
    return exec_dialog('askopenfilename',**options) 


def asksaveasfilename(**options):
    return exec_dialog('asksaveasfilename',**options) 


def askopenfilenames(**options):
    return exec_dialog('asksaveasfilename',**options) 


def askopenfile(mode = "r", **options):
    return exec_dialog('asksaveasfilename',**options) 


def askopenfiles(mode = "r", **options):
    return exec_dialog('asksaveasfilename',**options) 


def asksaveasfile(mode = "w", **options):
    return exec_dialog('asksaveasfilename',**options) 


def askdirectory (**options):
    return exec_dialog('asksaveasfilename',**options) 
