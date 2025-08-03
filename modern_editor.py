import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from configparser import ConfigParser
from ttkbootstrap import Style

class TerrificEditor:
    def __init__(self):
        # Initialize theme and main window
        self.style = Style(theme=self._load_theme())
        self.root = self.style.master
        self.root.title("Terrific Editor")
        self.file_path = None
        self.current_theme = self._load_theme()
        
        # Setup window geometry
        self._setup_window()
        
        # Create main container frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create widgets
        self._create_widgets()
        self._build_menu()
        self._setup_bindings()
        
        # Initialize line numbers
        self.update_line_numbers()
        
        self.root.mainloop()

    def _setup_window(self):
        """Configure main window geometry"""
        width, height = 800, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def _create_widgets(self):
        """Create and arrange all widgets"""
        # Create line numbers text widget
        self.line_numbers = tk.Text(
            self.main_frame,
            width=4,
            padx=4,
            pady=4,
            takefocus=0,
            border=0,
            background='lightgrey',
            foreground='black',
            state='disabled',
            wrap=tk.NONE,
            font=('Consolas', 12)
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Create vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create main text area
        self.text_area = tk.Text(
            self.main_frame,
            yscrollcommand=self._on_text_scroll,
            wrap=tk.WORD,
            undo=True,
            font=('Consolas', 12),
            padx=5,
            pady=5
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbar
        self.scrollbar.config(command=self._sync_scroll)

    def _build_menu(self):
        """Create complete menu bar with all submenus"""
        menubar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=lambda: self.open_file(), accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self._save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self._undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self._redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self._cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self._copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self._paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self._select_all, accelerator="Ctrl+A")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Theme Menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        themes = {
            'Flatly': 'flatly',
            'Darkly': 'darkly',
            'Cosmo': 'cosmo',
            'Superhero': 'superhero',
            'Minty': 'minty',
            'Solar': 'solar'
        }
        for name, theme in themes.items():
            theme_menu.add_command(
                label=name,
                command=lambda t=theme: self._change_theme(t)
            )
        menubar.add_cascade(label="Theme", menu=theme_menu)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def _setup_bindings(self):
        """Configure all keyboard/mouse bindings"""
        # File operations
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self._save_as())
        
        # Edit operations
        self.root.bind("<Control-z>", self._undo)
        self.root.bind("<Control-y>", self._redo)
        self.root.bind("<Control-x>", self._cut)
        self.root.bind("<Control-c>", self._copy)
        self.root.bind("<Control-v>", self._paste)
        self.root.bind("<Control-a>", self._select_all)
        
        # Text area bindings
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self._on_mousewheel)
        self.text_area.bind("<Configure>", self.update_line_numbers)
        
        # Line numbers protection
        self.line_numbers.bind("<Button-1>", lambda e: "break")

    def _on_text_scroll(self, *args):
        """Handle text area scrolling"""
        self.scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])

    def _sync_scroll(self, *args):
        """Sync scrolling between widgets"""
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.delta:
            self.text_area.yview_scroll(-1*(event.delta//120), "units")
        else:
            self.text_area.yview_scroll(1 if event.num == 5 else -1, "units")
        return "break"

    def update_line_numbers(self, event=None):
        """Update the line numbers display with pixel-perfect alignment"""
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
    
        # Get font metrics from both widgets
        text_font = tk.font.Font(font=self.text_area['font'])
        line_font = tk.font.Font(font=self.line_numbers['font'])
    
        # Calculate line height difference
        text_height = text_font.metrics('linespace')
        line_height = line_font.metrics('linespace')
        height_ratio = text_height / line_height
    
        # Get visible range
        first_visible = self.text_area.index("@0,0")
        last_visible = self.text_area.index(f"@0,{self.text_area.winfo_height()}")
    
        start_line = int(first_visible.split('.')[0])
        end_line = int(last_visible.split('.')[0]) + 1
    
        # Add line numbers with adjusted spacing
        for line in range(1, end_line  ): 
            self.line_numbers.insert(tk.END, f"{line}\n")
    
        # Apply vertical spacing adjustment
        self.line_numbers.config(spacing3=int((height_ratio - 1) * text_height))
    
        # Adjust width
        max_line = int(self.text_area.index('end-1c').split('.')[0])
        width = len(str(max_line)) + 1
        self.line_numbers.config(width=max(3, width))
    
        self.line_numbers.config(state=tk.DISABLED)
    
        # Force synchronous scrolling
        self._sync_scroll('moveto', self.text_area.yview()[0])

    def new_file(self, event=None):
        """Create new file"""
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Untitled - Terrific Editor")
        self.update_line_numbers()

    def open_file(self, event=None):
        """Open existing file"""
        file_path = filedialog.askopenfilename(
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, f.read())
                self.file_path = file_path
                self.root.title(f"{os.path.basename(file_path)} - Terrific Editor")
                self.update_line_numbers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")

    def save_file(self, event=None):
        """Save current file"""
        if self.file_path:
            try:
                with open(self.file_path, 'w') as f:
                    f.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Saved", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
        else:
            self._save_as()

    def _save_as(self, event=None):
        """Save file with new name"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            self.file_path = file_path
            self.save_file()
            self.root.title(f"{os.path.basename(file_path)} - Terrific Editor")

    def _undo(self, event=None):
        """Undo last action"""
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass
        return "break"

    def _redo(self, event=None):
        """Redo last undone action"""
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass
        return "break"

    def _cut(self, event=None):
        """Cut selected text"""
        self.text_area.event_generate("<<Cut>>")
        return "break"

    def _copy(self, event=None):
        """Copy selected text"""
        self.text_area.event_generate("<<Copy>>")
        return "break"

    def _paste(self, event=None):
        """Paste from clipboard"""
        self.text_area.event_generate("<<Paste>>")
        self.update_line_numbers()
        return "break"

    def _select_all(self, event=None):
        """Select all text"""
        self.text_area.tag_add('sel', '1.0', 'end')
        return "break"

    def _change_theme(self, theme_name):
        """Change the application theme"""
        self.style.theme_use(theme_name)
        self.current_theme = theme_name
        self._save_theme_preference(theme_name)
        
        # Update specific widget colors
        self.line_numbers.config(
            background='lightgrey' if theme_name in ['flatly', 'cosmo', 'minty'] else 'gray20',
            foreground='black' if theme_name in ['flatly', 'cosmo', 'minty'] else 'white'
        )

    def _save_theme_preference(self, theme_name):
        """Save theme preference to config file"""
        parser = ConfigParser()
        parser.read('config.ini')
        if not parser.has_section('theme_colour'):
            parser.add_section('theme_colour')
        parser.set('theme_colour', 'colour', theme_name)
        with open('config.ini', 'w') as f:
            parser.write(f)

    def _load_theme(self):
        """Load saved theme from config"""
        parser = ConfigParser()
        parser.read('config.ini')
        return parser.get('theme_colour', 'colour', fallback='flatly')

    def _show_about(self):
        """Show about dialog"""
        about_text = (
            "Terrific Editor\n\n"
            "Created by Salay Abdul Muhaimin Kanton in June 2023\n\n"
            "Contributors:\n"
            "Hariharasudhan Rajendiran 2025\n"
            "Version 2.0\n"
            f"Current Theme: {self.current_theme.title()}\n\n"
        )
        messagebox.showinfo("About Terrific Editor", about_text)

if __name__ == "__main__":
    TerrificEditor()
