import random
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog as fd
from Backend import *
import re
import os
import platform
from Objects import *
from random import randint


class PyGUI:
    def __init__(self):
        # Make and name TK GUI
        self.root = Tk()
        self.root.title("Project 3 AI")

        self.button_pressed = ""
        self.attr_file = ""
        self.con_file = ""
        self.logics_file = ""
        self.files = []

        self.attributes = []
        self.constraints = []
        self.Logics = []
        self.penalties = []
        self.possibilistics = []
        self.qualitatives = []
        self.feasibles = []


        # Create tab controller
        self.tab_notebook = ttk.Notebook(self.root)
        self.tab_notebook.pack(pady=5)

        # Call all tab creation function
        self.make_input_tab()
        self.make_exist_tab()
        self.make_exemp_tab()
        self.make_opti_tab()
        self.make_omni_tab()

        self.root.mainloop()

    # Displays Binary Attributes values
    def display_attributes(self):
        for a in self.attributes:
            self.tree_attr.insert(parent='', index='end', iid=a.numop1, values=(a.numop1, a.name, a.op1, a.op2))

    # Displays Hard Constraints variables
    def display_constraints(self):
        i = 1
        for c in self.constraints:
            if c.input == "":
                break
            self.tree_con.insert(parent='', index='end', iid=i, values=(i, c.input))
            i += 1

    # Displays Penalty Logic variables
    def display_penalty(self):
        i = 0
        p = self.Logics[0]
        while i < len(p):
            self.tree_pen.insert(parent='', index='end', iid=i, values=(i+1, p[i].input_as_words[0], p[i].pen))
            i += 1

    # Displays Possibilistic Logic variables
    def display_possibilistic(self):
        i = 0
        p = self.Logics[1]
        while i < len(p):
            self.tree_possib.insert(parent='', index='end', iid=i, values=(i+1, p[i].input_as_words[0], p[i].tol))
            i += 1

    # Displays Qualitative Form Logic variables
    def display_qualitative(self):
        i = 0
        while i < len(self.Logics[2]):
            self.tree_qual.insert(parent='', index='end', iid=i, values=(i+1, self.qualitatives[i].input))
            i += 1

    def call_parse_attributes(self):
        self.attr_file = fd.askopenfilename()
        self.attributes = parse_attributes_file(self.attr_file, self.attributes)
        self.files.append(self.attr_file)
        self.display_attributes()
        self.button_con['state'] = NORMAL

    def call_parse_constraints(self):
        self.con_file = fd.askopenfilename()
        self.constraints = parse_constraints_file(self.con_file, self.attributes, self.constraints)
        self.files.append(self.con_file)
        self.display_constraints()
        self.button_logic['state'] = NORMAL

    def call_parse_logics(self):
        self.logics_file = fd.askopenfilename()
        self.Logics = parse_logic_file(self.logics_file,
                                       self.penalties,
                                       self.possibilistics,
                                       self.qualitatives,
                                       self.attributes)
        self.display_penalty()
        self.display_possibilistic()
        self.display_qualitative()
        self.files.append(self.logics_file)
        self.feasibles = Backend(self.files)
        self.GUI_output()


    # Create page for all input variables
    def make_input_tab(self):
        # Create input tab
        self.tab_input = Frame(self.tab_notebook)
        self.tab_input.pack()
        self.tab_notebook.add(self.tab_input, text="Input")

        # Left Input Frame
        self.frm_left = tk.LabelFrame(self.tab_input, text="", labelanchor=N, padx=100, pady=50)
        self.frm_left.grid(column=0, row=0)

        # Right Input Frame
        self.frm_right = LabelFrame(self.tab_input, text="", padx=100, pady=46)
        self.frm_right.grid(column=1, row=0)

        # Attribute Label
        self.lbl_attr = Label(self.frm_left, text="Binary Attributes")
        self.lbl_attr.pack()

        # Make tree view table for attributes
        self.tree_attr = ttk.Treeview(self.frm_left, height=10)
        self.tree_attr['columns'] = ("Attr #", "Attribute", "Option 1", "Option 2")
        self.tree_attr.column("#0", width=0)
        self.tree_attr.column("Attr #", width=100, minwidth=50, anchor=CENTER)
        self.tree_attr.column("Attribute", width=100, minwidth=50, anchor=CENTER)
        self.tree_attr.column("Option 1", width=100, minwidth=50, anchor=CENTER)
        self.tree_attr.column("Option 2", width=100, minwidth=50, anchor=CENTER)

        # Attribute tree headers
        self.tree_attr.heading("Attr #", text="Attr #", anchor=CENTER)
        self.tree_attr.heading("Attribute", text="Attribute", anchor=CENTER)
        self.tree_attr.heading("Option 1", text="Option 1", anchor=CENTER)
        self.tree_attr.heading("Option 2", text="Option 2", anchor=CENTER)

        # Show tree
        self.tree_attr.pack()

        # Make button to open attribute Files
        self.button_attr = tk.Button(self.frm_left, text='Open File', command=self.call_parse_attributes)
        self.button_attr.pack()

        # Constraints Label
        self.lbl_con = Label(self.frm_left, text="Hard Constraints")
        self.lbl_con.pack()

        # Make Constraints tree
        self.tree_con = ttk.Treeview(self.frm_left, height=10)
        self.tree_con['columns'] = ("Const #", "Constraint")
        self.tree_con.column("#0", width=0)
        self.tree_con.column("Const #", width=100, minwidth=20, anchor=CENTER)
        self.tree_con.column("Constraint", width=300, minwidth=50, anchor=CENTER)

        # Constraints tree headers
        self.tree_con.heading("Const #", text="Const #", anchor=CENTER)
        self.tree_con.heading("Constraint", text="Constraint", anchor=CENTER)

        # Show tree
        self.tree_con.pack()

        # Make button to open constraint Files
        self.button_con = tk.Button(self.frm_left,
                                    text='Open File',
                                    command=self.call_parse_constraints,
                                    state=DISABLED)
        self.button_con.pack()

        # Penalty Logic Label
        self.lbl_pen = Label(self.frm_right, text="Penalty Logic")
        self.lbl_pen.pack()

        # Make tree view table for Penalty Logic
        self.tree_pen = ttk.Treeview(self.frm_right, height=6)
        self.tree_pen['columns'] = ("Pref #", "Preference", "Penalty")
        self.tree_pen.column("#0", width=0)
        self.tree_pen.column("Pref #", width=100, anchor=CENTER)
        self.tree_pen.column("Preference", width=250, anchor=CENTER)
        self.tree_pen.column("Penalty", width=100, anchor=CENTER)

        # Penalty Logic tree headers
        self.tree_pen.heading("Pref #", text="Pref #", anchor=CENTER)
        self.tree_pen.heading("Preference", text="Preference", anchor=CENTER)
        self.tree_pen.heading("Penalty", text="Penalty", anchor=CENTER)

        # Show tree
        self.tree_pen.pack()


        # Possibilistic Logic Label
        self.lbl_possib = Label(self.frm_right, text="Possibilistic Logic")
        self.lbl_possib.pack()

        # Make tree view table for possibilistic logics
        self.tree_possib = ttk.Treeview(self.frm_right, height=6)
        self.tree_possib['columns'] = ("Pref #", "Preference", "Tolerance")
        self.tree_possib.column("#0", width=0)
        self.tree_possib.column("Pref #", width=100, anchor=CENTER)
        self.tree_possib.column("Preference", width=250, anchor=CENTER)
        self.tree_possib.column("Tolerance", width=100, anchor=CENTER)

        # Possibilistic tree headers
        self.tree_possib.heading("Pref #", text="Pref #", anchor=CENTER)
        self.tree_possib.heading("Preference", text="Preference", anchor=CENTER)
        self.tree_possib.heading("Tolerance", text="Tolerance", anchor=CENTER)

        # Show tree
        self.tree_possib.pack()

        # Qualitative Form Logic Label
        self.lbl_qual = Label(self.frm_right, text="Qualitative Choice Logic")
        self.lbl_qual.pack()

        # Make tree view table for attributes
        self.tree_qual = ttk.Treeview(self.frm_right, height=6)
        self.tree_qual['columns'] = ("Pref #", "Preference")
        self.tree_qual.column("#0", width=0)
        self.tree_qual.column("Pref #", width=100, anchor=CENTER)
        self.tree_qual.column("Preference", width=350, anchor=CENTER)

        # Attribute tree headers
        self.tree_qual.heading("Pref #", text="Pref #", anchor=CENTER)
        self.tree_qual.heading("Preference", text="Preference", anchor=CENTER)

        # Show tree
        self.tree_qual.pack()

        # Make button to open Logic Files
        self.button_logic = tk.Button(self.frm_right, text='Open File', command=self.call_parse_logics, state=DISABLED)
        self.button_logic.pack()


    # Call store_feasible_objects from Backend to display in Treeview
    def display_feasible_output(self):
        i = 0
        f = self.feasibles
        while i < len(f):
            self.tree_exist.insert(parent='', index='end', iid=i, values=(i + 1, f[i].name_as_num, f[i].name))
            i += 1


    # Create Page for Feasible objects
    def make_exist_tab(self):
        # Create Existence Tab
        self.tab_exist = Frame(self.tab_notebook)
        self.tab_exist.pack()
        self.tab_notebook.add(self.tab_exist, text="Existence")

        # Create frame for left side of exist tab
        self.frm_exist_left = Frame(self.tab_exist, padx=15)
        self.frm_exist_left.pack()


        # Create and show Title label for left exist tab
        self.lbl_exist = Label(self.frm_exist_left, text="Feasible Objects")
        self.lbl_exist.pack(pady=15)

        # Create TreeView for Feasible Objects
        self.tree_exist = ttk.Treeview(self.frm_exist_left, height=20)

        # Create tree columns
        self.tree_exist['columns'] = ("Obj #", "CLASP", "Object")
        self.tree_exist.column("#0", width=0)
        self.tree_exist.column("Obj #", width=100, minwidth=50, anchor=CENTER)
        self.tree_exist.column("CLASP", width=200, minwidth=50, anchor=CENTER)
        self.tree_exist.column("Object", width=300, minwidth=50, anchor=CENTER)

        # Add column headers
        self.tree_exist.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_exist.heading("CLASP", text="CLASP", anchor=CENTER)
        self.tree_exist.heading("Object", text="Object", anchor=CENTER)

        # Show tree
        self.tree_exist.pack()



    # Create page for 2 feasible objects exemplification output
    def make_exemp_tab(self):
        # Create Exemplification Tab
        self.tab_exemp = Frame(self.tab_notebook)
        self.tab_exemp.pack()
        self.tab_notebook.add(self.tab_exemp, text="Exemplification")

        # Make exemplification Frame
        self.frm_exemp = Frame(self.tab_exemp)
        self.frm_exemp.pack()

        # Make exemplification label
        self.lbl_exemp = Label(self.frm_exemp, text="Exemplification")
        self.lbl_exemp.pack()

        # Create Treeview for exemplification tab
        self.tree_exemp = ttk.Treeview(self.frm_exemp, height=10)

        # Create tree columns
        self.tree_exemp['columns'] = ("Obj #", "Object", "Penalty", "Possibilistic", "Qualitative")
        self.tree_exemp.column("#0", width=0)
        self.tree_exemp.column("Obj #", width=100, minwidth=50, anchor=CENTER)
        self.tree_exemp.column("Object", width=200, minwidth=50, anchor=CENTER)
        self.tree_exemp.column("Penalty", width=200, minwidth=50, anchor=CENTER)
        self.tree_exemp.column("Possibilistic", width=200, minwidth=50, anchor=CENTER)
        self.tree_exemp.column("Qualitative", width=200, minwidth=50, anchor=CENTER)

        # Add column headers
        self.tree_exemp.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_exemp.heading("Object", text="Object", anchor=CENTER)
        self.tree_exemp.heading("Penalty", text="Penalty", anchor=CENTER)
        self.tree_exemp.heading("Possibilistic", text="Possibilistic", anchor=CENTER)
        self.tree_exemp.heading("Qualitative", text="Qualitative", anchor=CENTER)

        # Show tree
        self.tree_exemp.pack()


    # Create page for single optimization output
    def make_opti_tab(self):
        # Create Optimization Tab
        self.tab_opti = Frame(self.tab_notebook)
        self.tab_opti.pack()
        self.tab_notebook.add(self.tab_opti, text="Optimization")

        # Make left side of optimization tab
        self.frm_opti_left = Frame(self.tab_opti, padx=15)
        self.frm_opti_left.grid(column=0, row=0)

        # Make right side of optimization tab
        self.frm_opti_right = Frame(self.tab_opti)
        self.frm_opti_right.grid(column=1, row=0)

        # Call logicss for left side of opti tab
        self.display_opti_pen(self.frm_opti_left)
        self.display_opti_possib(self.frm_opti_left)
        self.display_opti_qual(self.frm_opti_left)

        # Call logics for right side of opti tab
        # self.display_penalty_output(self.frm_opti_right)
        # self.display_possib_output(self.frm_opti_right)
        # self.display_qualitative_output(self.frm_opti_right)


    # Create page for omni optimization output
    def make_omni_tab(self):
        # Create Omni-Optimization Tab
        self.tab_omni = Frame(self.tab_notebook)
        self.tab_omni.pack()
        self.tab_notebook.add(self.tab_omni, text="Omni-Optimization")

        # Make left side of omni optimization tab
        self.frm_omni_left = Frame(self.tab_omni, padx=15)
        self.frm_omni_left.grid(column=0, row=0)

        # Make right side of omni optimization tab
        self.frm_omni_right = Frame(self.tab_omni)
        self.frm_omni_right.grid(column=1, row=0)

        # Call logics for left side of omni tab
        self.display_omni_pen(self.frm_omni_left)
        self.display_omni_possib(self.frm_omni_left)
        self.display_omni_qual(self.frm_omni_left)

        # Call logics for right side of omni tab
        self.display_penalty_output(self.frm_omni_right)
        self.display_possib_output(self.frm_omni_right)
        self.display_qualitative_output(self.frm_omni_right)



    def display_penalty_output(self, input_frame):
        # Label for penalty output
        self.lbl_penaltyo = Label(input_frame, text="Penalty Logic")
        self.lbl_penaltyo.pack()

        # Make Treeview widget for penalty output
        self.tree_penaltyo = ttk.Treeview(input_frame, height=7)
        self.tree_penaltyo.pack()

        # Make Treeview columns for penalty output
        self.tree_penaltyo['columns'] = ("Obj #", "Pref 1", "Pref 2", "Pref 3", "Total")
        self.tree_penaltyo.column("#0", width=0)
        self.tree_penaltyo.column("Obj #", width=100, minwidth=50, anchor=CENTER)
        self.tree_penaltyo.column("Pref 1", width=100, minwidth=50, anchor=CENTER)
        self.tree_penaltyo.column("Pref 2", width=100, minwidth=50, anchor=CENTER)
        self.tree_penaltyo.column("Pref 3", width=100, minwidth=50, anchor=CENTER)
        self.tree_penaltyo.column("Total", width=100, minwidth=50, anchor=CENTER)

        # Make Treeview headers for columns
        self.tree_penaltyo.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_penaltyo.heading("Pref 1", text="Pref 1", anchor=CENTER)
        self.tree_penaltyo.heading("Pref 2", text="Pref 2", anchor=CENTER)
        self.tree_penaltyo.heading("Pref 3", text="Pref 3", anchor=CENTER)
        self.tree_penaltyo.heading("Total", text="Total", anchor=CENTER)

        # Show tree
        self.tree_penaltyo.pack()


    def display_possib_output(self, input_frame):
        # Label for penalty output
        self.lbl_possibo = Label(input_frame, text="Possibilistic Logic")
        self.lbl_possibo.pack()

        # Make Treeview widget for penalty output
        self.tree_possibo = ttk.Treeview(input_frame, height=7)
        self.tree_possibo.pack()

        # Make Treeview columns for penalty output
        self.tree_possibo['columns'] = ("Obj #", "Pref 1", "Pref 2", "Pref 3", "Total")
        self.tree_possibo.column("#0", width=0)
        self.tree_possibo.column("Obj #", width=100, minwidth=50, anchor=CENTER)
        self.tree_possibo.column("Pref 1", width=100, minwidth=50, anchor=CENTER)
        self.tree_possibo.column("Pref 2", width=100, minwidth=50, anchor=CENTER)
        self.tree_possibo.column("Pref 3", width=100, minwidth=50, anchor=CENTER)
        self.tree_possibo.column("Total", width=100, minwidth=50, anchor=CENTER)

        # Make Treeview headers for columns
        self.tree_possibo.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_possibo.heading("Pref 1", text="Pref 1", anchor=CENTER)
        self.tree_possibo.heading("Pref 2", text="Pref 2", anchor=CENTER)
        self.tree_possibo.heading("Pref 3", text="Pref 3", anchor=CENTER)
        self.tree_possibo.heading("Total", text="Total", anchor=CENTER)

        # Show tree
        self.tree_possibo.pack()


    def display_qualitative_output(self, input_frame):
        # Label for penalty output
        self.lbl_qualo = Label(input_frame, text="Qualitative Choice Logic")
        self.lbl_qualo.pack()

        # Make Treeview widget for penalty output
        self.tree_qualo = ttk.Treeview(input_frame, height=7)
        self.tree_qualo.pack()

        # Make Treeview columns for penalty output
        self.tree_qualo['columns'] = ("Obj #", "Pref 1", "Pref 2", "Pref 3", "Total")
        self.tree_qualo.column("#0", width=0)
        self.tree_qualo.column("Obj #", width=100, minwidth=50, anchor=CENTER)
        self.tree_qualo.column("Pref 1", width=100, minwidth=50, anchor=CENTER)
        self.tree_qualo.column("Pref 2", width=100, minwidth=50, anchor=CENTER)
        self.tree_qualo.column("Pref 3", width=100, minwidth=50, anchor=CENTER)
        self.tree_qualo.column("Total", width=100, minwidth=50, anchor=CENTER)

        # Make Treeview headers for columns
        self.tree_qualo.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_qualo.heading("Pref 1", text="Pref 1", anchor=CENTER)
        self.tree_qualo.heading("Pref 2", text="Pref 2", anchor=CENTER)
        self.tree_qualo.heading("Pref 3", text="Pref 3", anchor=CENTER)
        self.tree_qualo.heading("Total", text="Total", anchor=CENTER)

        # Show tree
        self.tree_qualo.pack()


    def display_opti_pen(self, input_frame):
        # Label for optimization penalty output
        self.lbl_opti_pen = Label(input_frame, text="Optimal Penalty Objects")
        self.lbl_opti_pen.pack()

        # Make Treeview widget for Optimal penalty output
        self.tree_opti_pen = ttk.Treeview(input_frame, height=6)
        self.tree_opti_pen.pack()

        # Make columns for Treeview
        self.tree_opti_pen['columns'] = ("Obj #", "CLASP", "Object")
        self.tree_opti_pen.column("#0", width=0)
        self.tree_opti_pen.column("Obj #", width=100, anchor=CENTER)
        self.tree_opti_pen.column("CLASP", width=200, anchor=CENTER)
        self.tree_opti_pen.column("Object", width=300, anchor=CENTER)

        # Make column headers for Treeview
        self.tree_opti_pen.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_opti_pen.heading("CLASP", text="CLASP", anchor=CENTER)
        self.tree_opti_pen.heading("Object", text="Object", anchor=CENTER)

        # Show tree
        self.tree_opti_pen.pack()


    def display_opti_possib(self, input_frame):
        # Label for optimization penalty output
        self.lbl_opti_possib = Label(input_frame, text="Optimal Possibilistic Objects")
        self.lbl_opti_possib.pack()

        # Make Treeview widget for Optimal penalty output
        self.tree_opti_possib = ttk.Treeview(input_frame, height=6)
        self.tree_opti_possib.pack()

        # Make columns for Treeview
        self.tree_opti_possib['columns'] = ("Obj #", "CLASP", "Object")
        self.tree_opti_possib.column("#0", width=0)
        self.tree_opti_possib.column("Obj #", width=100, anchor=CENTER)
        self.tree_opti_possib.column("CLASP", width=200, anchor=CENTER)
        self.tree_opti_possib.column("Object", width=300, anchor=CENTER)

        # Make column headers for Treeview
        self.tree_opti_possib.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_opti_possib.heading("CLASP", text="CLASP", anchor=CENTER)
        self.tree_opti_possib.heading("Object", text="Object", anchor=CENTER)

        # Show tree
        self.tree_opti_possib.pack()


    def display_opti_qual(self, input_frame):
        # Label for optimization penalty output
        self.lbl_opti_qual = Label(input_frame, text="Optimal Qualitative Choice Objects")
        self.lbl_opti_qual.pack()

        # Make Treeview widget for Optimal penalty output
        self.tree_opti_qual = ttk.Treeview(input_frame, height=6)
        self.tree_opti_qual.pack()

        # Make columns for Treeview
        self.tree_opti_qual['columns'] = ("Obj #", "CLASP", "Object")
        self.tree_opti_qual.column("#0", width=0)
        self.tree_opti_qual.column("Obj #", width=100, anchor=CENTER)
        self.tree_opti_qual.column("CLASP", width=200, anchor=CENTER)
        self.tree_opti_qual.column("Object", width=300, anchor=CENTER)

        # Make column headers for Treeview
        self.tree_opti_qual.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_opti_qual.heading("CLASP", text="CLASP", anchor=CENTER)
        self.tree_opti_qual.heading("Object", text="Object", anchor=CENTER)

        # Show tree
        self.tree_opti_qual.pack()


    def display_omni_pen(self, input_frame):
        # Label for optimization penalty output
        self.lbl_omni_pen = Label(input_frame, text="Optimal Penalty Objects")
        self.lbl_omni_pen.pack()

        # Make Treeview widget for Optimal penalty output
        self.tree_omni_pen = ttk.Treeview(input_frame, height=6)
        self.tree_omni_pen.pack()

        # Make columns for Treeview
        self.tree_omni_pen['columns'] = ("Obj #", "CLASP", "Object")
        self.tree_omni_pen.column("#0", width=0)
        self.tree_omni_pen.column("Obj #", width=100, anchor=CENTER)
        self.tree_omni_pen.column("CLASP", width=200, anchor=CENTER)
        self.tree_omni_pen.column("Object", width=300, anchor=CENTER)

        # Make column headers for Treeview
        self.tree_omni_pen.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_omni_pen.heading("CLASP", text="CLASP", anchor=CENTER)
        self.tree_omni_pen.heading("Object", text="Object", anchor=CENTER)

        # Show tree
        self.tree_omni_pen.pack()


    def display_omni_possib(self, input_frame):
        # Label for optimization penalty output
        self.lbl_omni_possib = Label(input_frame, text="Optimal Possibilistic Objects")
        self.lbl_omni_possib.pack()

        # Make Treeview widget for Optimal penalty output
        self.tree_omni_possib = ttk.Treeview(input_frame, height=6)
        self.tree_omni_possib.pack()

        # Make columns for Treeview
        self.tree_omni_possib['columns'] = ("Obj #", "CLASP", "Object")
        self.tree_omni_possib.column("#0", width=0)
        self.tree_omni_possib.column("Obj #", width=100, anchor=CENTER)
        self.tree_omni_possib.column("CLASP", width=200, anchor=CENTER)
        self.tree_omni_possib.column("Object", width=300,anchor=CENTER)

        # Make column headers for Treeview
        self.tree_omni_possib.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_omni_possib.heading("CLASP", text="CLASP", anchor=CENTER)
        self.tree_omni_possib.heading("Object", text="Object", anchor=CENTER)

        # Show tree
        self.tree_omni_possib.pack()


    def display_omni_qual(self, input_frame):
        # Label for optimization penalty output
        self.lbl_omni_qual = Label(input_frame, text="Optimal Qualitative Choice Objects")
        self.lbl_omni_qual.pack()

        # Make Treeview widget for Optimal penalty output
        self.tree_omni_qual = ttk.Treeview(input_frame, height=6)
        self.tree_omni_qual.pack()

        # Make columns for Treeview
        self.tree_omni_qual['columns'] = ("Obj #", "CLASP", "Object")
        self.tree_omni_qual.column("#0", width=0)
        self.tree_omni_qual.column("Obj #", width=100, anchor=CENTER)
        self.tree_omni_qual.column("CLASP", width=200, anchor=CENTER)
        self.tree_omni_qual.column("Object", width=300, anchor=CENTER)

        # Make column headers for Treeview
        self.tree_omni_qual.heading("Obj #", text="Obj #", anchor=CENTER)
        self.tree_omni_qual.heading("CLASP", text="CLASP", anchor=CENTER)
        self.tree_omni_qual.heading("Object", text="Object", anchor=CENTER)

        # Show tree
        self.tree_omni_qual.pack()


    # Fills tables with penalty output, calls cross_reference_penalty
    def fill_penalty(self):
        i = 0
        f = self.feasibles
        while i < len(f):
            self.tree_penaltyo.insert(parent='', index='end', iid=i, values=(f[i].name_as_num,
                                                                             f[i].penalty_list[0],
                                                                             f[i].penalty_list[1],
                                                                             f[i].penalty_list[2],
                                                                             f[i].pen_total))
            i += 1

    # Fills tables with possibilistic output, calls cross_reference_possibilistic
    def fill_possibilistic(self):
        i = 0
        f = self.feasibles
        while i < len(f):
            self.tree_possibo.insert(parent='', index='end', iid=i, values=(f[i].name_as_num,
                                                                            f[i].poss_list[0],
                                                                            f[i].poss_list[1],
                                                                            f[i].poss_list[2],
                                                                            f[i].tolerance))
            i += 1



    def fill_omni_pen(self):
        i = 1
        list_of_optimal = []
        f = self.feasibles
        min = f[0].pen_total
        while i < len(f):
            if f[i].pen_total < min:
                min = f[i].pen_total
            i += 1
        i = 0
        while i < len(f):
            if f[i].pen_total == min:
                list_of_optimal.append(i)
            i += 1
        i = 0
        while i < len(list_of_optimal):
            self.tree_omni_pen.insert(parent='', index='end', iid=i, values=(list_of_optimal[i]+1,
                                                                             f[list_of_optimal[i]].name_as_num,
                                                                             f[list_of_optimal[i]].name))
            i += 1


    def fill_omni_possib(self):
        i = 1
        list_of_optimal = []
        f = self.feasibles
        max = f[0].tolerance
        while i < len(f):
            if f[i].tolerance > max:
                max = f[i].tolerance
            i += 1
        i = 0
        j = 0
        while i < len(f):
            if f[i].tolerance == max:
                list_of_optimal.append(i)
            i += 1
        i = 0
        while i < len(list_of_optimal):
            self.tree_omni_possib.insert(parent='', index='end', iid=i, values=(list_of_optimal[i] + 1,
                                                                                   f[list_of_optimal[i]].name_as_num,
                                                                                   f[list_of_optimal[i]].name))
            i += 1

    def fill_opti_pen(self):
        i = 1
        f = self.feasibles
        min = f[0].pen_total
        min_index = 0
        while i < len(f):
            if f[i].pen_total < min:
                min = f[i].pen_total
                min_index = i
            i += 1
        self.tree_opti_pen.insert(parent='', index='end', iid=i, values=(min_index+1,
                                                                         f[min_index].name_as_num,
                                                                         f[min_index].name))

    def fill_opti_possib(self):
        i = 1
        f = self.feasibles
        max = f[0].tolerance
        max_index = 0
        while i < len(f):
            if f[i].tolerance > max:
                max = f[i].tolerance
                max_index = i
            i += 1
        self.tree_opti_possib.insert(parent='', index='end', iid=i, values=(max_index + 1,
                                                                         f[max_index].name_as_num,
                                                                         f[max_index].name))

    def fill_exemplification(self):
        f_input = exemplification(self.feasibles)
        self.tree_exemp.insert(parent='', index='end', iid=1, values=(f_input[0].name_as_num,
                                                                      f_input[0].name,
                                                                      f_input[0].penalty_exemp,
                                                                      f_input[0].poss_exemp))
        self.tree_exemp.insert(parent='', index='end', iid=2, values=(f_input[1].name_as_num,
                                                                      f_input[1].name,
                                                                      f_input[1].penalty_exemp,
                                                                      f_input[1].poss_exemp))


    # Display all outputs on GUI
    def GUI_output(self):
        self.display_feasible_output()

        self.fill_penalty()
        self.fill_possibilistic()

        self.fill_exemplification()

        self.fill_opti_pen()
        self.fill_opti_possib()
        self.fill_omni_pen()
        self.fill_omni_possib()
