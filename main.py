from tkinter import *
from ttkbootstrap import Style
from configparser import ConfigParser
from tkinter import messagebox, filedialog
import os

root = Tk()
root.title('Terrific Editor')
# root.iconbitmap('images/icon.ico')
root_width = 600
root_height = 400

text_area = Text(root, font=('Consolas 12'))
file_name = None

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

left = (screenwidth / 2) - (root_width / 2)
top = (screenheight / 2) - (root_height / 2)

root.geometry('%dx%d+%d+%d' % (root_width, root_height, left, top))

root.grid_rowconfigure(0,weight=1)
root.grid_columnconfigure(0,weight=1)

parser = ConfigParser()
parser.read('config.ini')

saved_theme_colour = parser.get('theme_colour', 'colour')

url = ""

def new_file(event= None):
    global url
    url=""
    text_area.delete(1.0, END)
    root.title("Untitled - Terrific Piece")

def save_file():
    global file_name
    if file_name == None:
            #save as new file
            file_name = filedialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])

            if file_name == "":
                file_name = None
            else:
                #try to save the file
                fr = open(file_name,"w")
                fr.write(text_area.get(1.0,END))
                fr.close()
                #change the window title
                root.title(os.path.basename(file_name) + " - Terrific Piece")
    else:
        fr = open(file_name, "w")
        fr.write(text_area.get(1.0,END))
        fr.close()

def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(("Text File", "*.txt"),("All Files", "*.*")))
    try:
        with open(url, "r") as fr:
            text_area.delete(1.0, root.END)
            text_area.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    root.title(os.path.basename(url)+ 'Terrific Piece')

def save_as():
    pass

def undo():
    text_area.event_generate("<<Undo>>")

def redo():
    text_area.event_generate("<<Redo>>")
    return "break"

def copy():
    text_area.event_generate("<<Copy>>")

def cut():
    text_area.event_generate("<<Cut>>")

def about():
    messagebox.showinfo('Terrific Editor', 'Terrific Editor was created by Salay Abdul Muhaimin Kanton in June 2023')

def theme_flatly():
    parser = ConfigParser()
    parser.read('config.ini')
    parser.set('theme_colour', 'colour','flatly')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    messagebox.showinfo('Terrific Editor', 'Terrific Editor needs a restart before a theme can be applied')


def theme_darkly():
    parser = ConfigParser()
    parser.read('config.ini')
    parser.set('theme_colour', 'colour', 'darkly')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    messagebox.showinfo('Terrific Editor', 'Terrific Editor needs a restart before a theme can be applied')
    

def theme_cosmo():
    parser = ConfigParser()
    parser.read('config.ini')
    parser.set('theme_colour', 'colour', 'cosmo')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    messagebox.showinfo('Terrific Editor', 'Terrific Editor needs a restart before a theme can be applied')
    

def theme_superhero():
    parser = ConfigParser()
    parser.read('config.ini')
    parser.set('theme_colour', 'colour', 'superhero')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    messagebox.showinfo('Terrific Editor', 'Terrific Editor needs a restart before a theme can be applied')
    
def theme_minty():
    parser = ConfigParser()
    parser.read('config.ini')
    parser.set('theme_colour', 'colour', 'minty')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    messagebox.showinfo('Terrific Editor', 'Terrific Editor needs a restart before a theme can be applied')
    

def theme_solar():
    parser = ConfigParser()
    parser.read('config.ini')
    parser.set('theme_colour', 'colour', 'solar')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    messagebox.showinfo('Terrific Editor', 'Terrific Editor needs a restart before a theme can be applied')
    
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar)
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file, accelerator="Ctrl+N")
file_menu.add_separator()
file_menu.add_command(label='Open', command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label='Save', command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label='Save As', command=save_as, accelerator="Ctrl+Shift+S")

file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit, accelerator="Ctrl+W")

edit_menu = Menu(menu_bar)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Undo', command=undo, accelerator="Ctrl+Z")
edit_menu.add_command(label='Redo', command=redo, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label='Copy', command=copy, accelerator="Ctrl+C")
edit_menu.add_command(label='Cut', command=cut, accelerator="Ctrl+X")

theme_menu = Menu(menu_bar)
menu_bar.add_cascade(label='Theme', menu=theme_menu)
theme_menu.add_command(label='Flatly Theme', command=theme_flatly)
theme_menu.add_command(label='Cosmo Theme', command=theme_cosmo)
theme_menu.add_command(label='Minty Theme', command=theme_minty)
theme_menu.add_separator()
theme_menu.add_command(label='Darkly Theme', command=theme_darkly)
theme_menu.add_command(label='Super Hero Theme', command=theme_superhero)
theme_menu.add_separator()
theme_menu.add_command(label='Solar Theme', command=theme_solar)

help_menu = Menu(menu_bar)
menu_bar.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=about)

line_numbers = Text(root, font=('Consolas 12'), bg="lightgrey", fg="black", width=6)
line_numbers.insert(1.0, "1 \n")
line_numbers.configure(state="disabled")
line_numbers.pack(side=LEFT, fill=Y)


def scroll_text_and_line_numbers(*args):
    try:
        # from scrollbar
        text_area.yview_moveto(args[1])
        line_numbers.yview_moveto(args[1])
    except IndexError:
        #from MouseWheel
        event = args[0]
        if event.delta:
            move = -1*(event.delta/120)
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

        text_area.yview_scroll(int(move), "units")
        line_numbers.yview_scroll(int(move), "units")

    return "break"

scrollbar = Scrollbar(root, orient="vertical", command=scroll_text_and_line_numbers)
scrollbar.config(command=text_area.yview)
scrollbar.pack(side=RIGHT,fill=Y)
text_area.config(yscrollcommand=scrollbar.set)
text_area.pack(expand=1, fill=BOTH)

text_area.bind("<Control-y>", redo)
text_area.bind("<Control-z>", undo)

def skip_event():
    return "break"

line_numbers.bind("<MouseWheel>", skip_event)
line_numbers.bind("<Button-4>", skip_event)
line_numbers.bind("<Button-5>", skip_event)



# LINE NUMBERS
def update_line_numbers():
    line_numbers.configure(state="normal")
    line_numbers.delete(1.0, END)
    number_of_lines = text_area.index(END).split(".")[0]
    line_number_string = "\n".join(str(no+1) for no in range(int(number_of_lines)))
    line_numbers.insert(1.0, line_number_string)
    line_numbers.configure(state="disabled")
    

def paste():
    text_area.event_generate("<<Paste>>")
    update_line_numbers()

#Paste command
edit_menu.add_command(label='Paste', command=paste, accelerator="Ctrl+V")

def on_key_release(event=None):
    if event.keysym in ("Return", "Delete", "BackSpace", "Up", "Down", "Escape"):
        update_line_numbers()

def tag_all_lines():
    final_index = text_area.index(END)
    final_line_number = int(final_index.split(".")[0])

    for line_number in range(final_line_number):
        line_to_tag = ".".join([str(line_number), "0"])
        tag_keywords(None, line_to_tag)

    update_line_numbers()

text_area.bind("<KeyRelease>", on_key_release)

Style(theme=saved_theme_colour)
root.mainloop()