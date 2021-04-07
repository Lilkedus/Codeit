from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from sys import platform
import subprocess
import os

compiler = Tk()
compiler.title("CodeIt")
compiler.attributes("-fullscreen", False)
compiler.configure(bg="#111111")

file_path = ""
outputStr = ""
file_name = ""


def set_file_path(path):
    global file_path
    file_path = path


def open_file(_):
    path = askopenfilename(filetypes=[("Python files", "*.py")])
    with open(path, "r") as file:
        code = file.read()
        editor.delete("1.0", END)
        file_name = os.path.basename(path)
        text = Label(text=file_name, bg="#111111",
                     fg="white", font=(get_font()), padx=12, pady=123)
        editor.insert("1.0", code)
        set_file_path(path)
        text.pack()


def save_as(_):
    if file_path == "":
        path = asksaveasfilename(filetypes=[("Python files", "*.py")])
    else:
        path = file_path
    with open(path, "w") as file:
        code = editor.get("1.0", END)
        file.write(code)
        set_file_path(path)


def run(_):
    if file_path == "":
        save_prompt = Toplevel()
        text = Label(save_prompt, text="Please save your code")
        text.pack()
        return
    code_output.delete("1.0", END)
    command = f"python {file_path}"
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    global outputStr
    outputStr = output
    code_output.insert("1.0", output)
    code_output.insert("1.0", error)


def run_new_window(_):
    if file_path == "":
        warning_prompt = Toplevel()
        warning_prompt.geometry('300x200-100+100')
        text = Label(warning_prompt, text="Please save your work")
        text.pack()
        return
    print(outputStr)
    # Render the content from the terminal
    command = f"python {file_path}"
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    terminal_prompt = Toplevel()
    terminal_prompt.geometry("300x200")
    terminal = Label(terminal_prompt, text=output)
    terminal.pack()
    print(file_path)


def get_font():
    if platform == "darwin":
        return "Menlo"
    elif platform == "win32" or platform == "win64":
        return "Consolas"
    elif platform == "linux" or platform == "linux2":
        return "Ubuntu Monospace"


def render_file_name():
    if not file_path:
        return "Welcome"
    else:
        print(os.path.basename(file_path))


def shortcut_based_on_os(letter):
    if platform == "darwin":
        return f"<Command-{letter}>"
    elif platform == "win32":
        return "<Control-{letter}>"
    elif platform == "linux" or platform == "linux2":
        return "<Control-{letter}>"


def accelerator_basesd_on_os(letter):
    if platform == "darwin":
        return f"cmd+{letter}"
    elif platform == "win32":
        return f"ctrl+{letter}"
    elif platform == "linux" or platform == "linux2":
        return f"ctrl+{letter}"


menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file,
                      accelerator=accelerator_basesd_on_os("o"))
file_menu.add_command(label="Save", command=save_as,
                      accelerator=accelerator_basesd_on_os("s"))
file_menu.add_command(label="Save As", command=save_as,
                      accelerator=accelerator_basesd_on_os("shit+s"))
file_menu.add_command(label="Exit", command=exit,
                      accelerator=accelerator_basesd_on_os("w"))
menu_bar.add_cascade(label="File", menu=file_menu)


run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label="Run", command=run,
                    accelerator=accelerator_basesd_on_os("r"))
run_bar.add_command(label="Run in a seperate window",
                    command=run_new_window, accelerator=accelerator_basesd_on_os("shift+r"))
menu_bar.add_cascade(label="Run", menu=run_bar)

compiler.config(menu=menu_bar, pady=10)

text = Label(text=file_name, bg="#111111", fg="white", font=(get_font()))
text.pack()


editor = Text(width=1000, height=40, highlightthickness=0, bg="#111111", fg="white",
              font=(get_font(), 0), padx=10, pady=10, insertbackground="red")
editor.pack()

# Shortcuts
compiler.bind(shortcut_based_on_os("r"), run)
compiler.bind(shortcut_based_on_os("Shift-r"), run_new_window)
compiler.bind("<Command-o>", open_file)
compiler.bind(shortcut_based_on_os("s"), save_as)
compiler.bind(shortcut_based_on_os("Shift-s"), save_as)
compiler.bind(shortcut_based_on_os("w"), exit)


# Terminal
code_output = Text(height=10, width=1000, highlightthickness=0,
                   bg="#1e1e1e", fg="white", relief=GROOVE, borderwidth=1, padx=10, pady=10)
# code_output.place(re)
code_output.pack(side=BOTTOM)

compiler.mainloop()
