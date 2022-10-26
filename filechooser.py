# File: filechooser.py
# Version: 0.7 (26-Oct-21)

"""
The filechooser module implements a simple wrapper for the filedialog
class in Tkinter, which is the most common graphics package for use
with Python.
"""

try:
    import tkinter
    try:
        import tkinter.filedialog as tkFileDialog
    except Exception:
        import tkFileDialog
except Exception as e:
    print('Could not load tkinter: ' + str(e))

# Function: choose_input_file

def choose_input_file(dir=".", title="Open File", initialfile=None):
    """
    Opens a file chooser for selecting an input file.
    """
    try:
        tk = tkinter._root
    except AttributeError:
        tk = tkinter.Tk()
        tkinter._root = tk
        tk.withdraw()
    filename = tkFileDialog.askopenfilename(parent=None,
                                            initialdir=dir,
                                            initialfile=initialfile,
                                            title=title)
    tk.update()
    return filename

# Function: choose_output_file

def choose_output_file(dir=".", title="Save File", initialfile=None):
    """
    Opens a file chooser for selecting an output file.
    """
    try:
        tk = tkinter._root
    except AttributeError:
        tk = tkinter.Tk()
        tkinter._root = tk
        tk.withdraw()
    filename = tkFileDialog.asksaveasfilename(parent=None,
                                              initialdir=dir,
                                              initialfile=initialfile,
                                              title=title)
    tk.lift()
    tk.update()
    return filename

# Define camel-case names

chooseOutputFile = choose_output_file
chooseInputFile = choose_input_file

# Check for successful compilation

if __name__ == "__main__":
    print("filechooser.py compiled successfully")
