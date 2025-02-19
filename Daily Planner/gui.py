from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import pandas as pd
import numpy as np
from datetime import date, timedelta 

root = Tk()
root.title('Daily Planner')

root.option_add('*tearOff', FALSE)

#########################  FUNCS  #########################
current_file = None
current_path = None

def open_file():
    global current_file, current_path, df_var

    # if current_file:
    #     save_file()

    try:
        filename = filedialog.askopenfilename()
    except Exception as e:
        messagebox.showerror(message=f'An error has occured: {e}')
    
    current_path = filename

    try:
        current_file = pd.read_csv(filename, dtype=object)
    except Exception as e:
        messagebox.showerror(message=f'An error has occured: {e}')
    
    file_change_housekeeping()

def file_change_housekeeping(): # things we need to do when changing the current_file
    global current_file, df_var, index_cbx
    wipe_viewer() # might as well?
    df_var = np.ndarray(shape = current_file.shape, dtype=StringVar)
    index_cbx['values'] = [i for i in current_file.index]
    update_viewer()

def new_file():
    global current_file, current_path

    # if current_file:
    #     save_file()

    try:
        current_file = pd.DataFrame([[date.today(),],], columns=['Date..ent',])
    except Exception as e:
        messagebox.showerror(message=f'An error has occured: {e}')


def save_file():
    global current_file, current_path
    update_df()

    if not current_path:
        try:
            current_path = filedialog.asksaveasfilename()
        except Exception as e:
            messagebox.showerror(message=f'An error has occured: {e}')
    

    try:
        current_file.to_csv(current_path, index = False)
    except PermissionError:
        messagebox.showerror(message='The file does not have permission to save,\nensure that the file is not open in any other program.')
    except Exception as e:
        messagebox.showerror(message=f'An error has occured: {e}')
    
    print(current_file)

def change_index(x, y, z):
    global index, index_var
    update_df()
    index = index_var.get()
    update_viewer()



def add_col():
    update_df()
    t = Toplevel(root)
    t.title('Add Column')

    def enter():
        global current_file
        current_file[f'{name_ent.get()}..{type_var.get()}'] = {i:'' for i in current_file.index}
        file_change_housekeeping()
        t.destroy()

    name_lbl = Label(t, text='Column Name: ')
    name_ent = Entry(t)

    type_var = StringVar(t, value='ent')
    type_lbl = Label(t, text='Column Type: ')
    ent_rdb = ttk.Radiobutton(t, text='Entry', variable=type_var, value='ent')
    cbx_rdb = ttk.Radiobutton(t, text='Combobox', variable=type_var, value='cbx')

    enter_btn = Button(t, text='Enter', command=enter)
    cancel_btn = Button(t, text='Cancel', command=t.destroy)
    

    
    name_lbl.grid(row=0,column=0)
    name_ent.grid(row=0,column=1)

    type_lbl.grid(row=1,column=0, rowspan=2)
    ent_rdb.grid(row=1,column=1)
    cbx_rdb.grid(row=2,column=1)

    enter_btn.grid(row=3,column=0)
    cancel_btn.grid(row=3,column=1)

def add_row():
    global current_file, index_var
    update_df()
    new_row = {col:'' for col in current_file}
    new_row['Date..ent'] = date.today()
    new_idx = current_file.shape[0]
    current_file.loc[new_idx, :] = new_row
    file_change_housekeeping()
    index_var.set(new_idx)

def edit_col():
    t = Toplevel(root)
    t.title('Edit Column')

    def enter():
        global current_file
        new_col = f'{name_ent.get()}..{type_var.get()}'
        old_col = [col for col in current_file.columns if col.split(sep='..')[0] == col_cbx.get()][0]
        print({old_col:new_col})
        current_file = current_file.rename(columns={old_col:new_col})
        print(current_file)
        file_change_housekeeping()
        wipe_viewer()
        update_viewer()
        t.destroy()

    col_lbl = Label(t, text='Choose Which Column to Edit:')
    col_cbx = ttk.Combobox(t, values=[col.split(sep='..')[0] for col in current_file.columns], state='readonly')
    
    type_var = StringVar(t, value='ent')
    type_lbl = Label(t, text='Type: ')
    ent_rdb = ttk.Radiobutton(t, text='Entry', variable=type_var, value='ent')
    cbx_rdb = ttk.Radiobutton(t, text='Combobox', variable=type_var, value='cbx')

    name_lbl = Label(t, text='Name: ')
    name_ent = Entry(t)

    enter_btn = Button(t, text='Enter', command=enter)
    cancel_btn = Button(t, text='Cancel', command=t.destroy)

    col_lbl.grid(column=0, row=0, columnspan=2)
    col_cbx.grid(column=0, row=1, columnspan=2)

    type_lbl.grid(column=0, row=2, rowspan=2)
    ent_rdb.grid(column=1, row=2)
    cbx_rdb.grid(column=1, row=3)

    name_lbl.grid(column=0, row=4)
    name_ent.grid(column=1, row=4)

    enter_btn.grid(column=0, row=5)
    cancel_btn.grid(column=1, row=5)


######################### MENUBAR #########################

menubar = Menu(root)
root['menu'] = menubar

menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menu_file.add_command(label = 'New', command = new_file)
menu_file.add_command(label = 'Save', command = save_file)
menu_file.add_command(label = 'Open', command = open_file)


menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_edit, label='Edit')
menu_edit.add_command(label = 'Add Column', command = add_col)
menu_edit.add_command(label = 'Add Row', command = add_row)
menu_edit.add_command(label = 'Edit Column', command = edit_col)

######################### RIBBON #########################

ribbon = ttk.Frame(root)

index_var = IntVar(value=0)
index_lbl = Label(ribbon, text='Index: ')
index_cbx = ttk.Combobox(ribbon, textvariable=index_var, values=[0,], width=3, state='readonly')
index_var.trace_add(mode='write', callback=change_index)

addcol_btn = Button(ribbon, text='Add\nColumn', command=add_col, width = 10)
addrow_btn = Button(ribbon, text='Add\nRow', command=add_row, width = 10)
editcol_btn = Button(ribbon, text='Edit\nColumn', command=edit_col, width = 10)

index_lbl.grid(row=0, column=0)
index_cbx.grid(row=0,column=1)

addcol_btn.grid(row=0, column=2)
addrow_btn.grid(row=0, column=3)
editcol_btn.grid(row=0, column=4)

######################### VIEWER #########################
new_file()

viewer = ttk.Frame(root, relief='solid', borderwidth=3, padding = "3 3")

index = 0

df_var = np.ndarray(shape = current_file.shape, dtype=StringVar)


# current_file = pd.read_csv('C:/Users/theis/Documents/GitHub/Personal-Projects/Daily Planner/test.csv', dtype=object) #TEMP
# file_change_housekeeping() # TEMP

def wipe_viewer():
    global viewer
    viewer.destroy()
    viewer = ttk.Frame(root, relief='solid', borderwidth=3, padding = "3 3")
    viewer.grid(column = 0, row = 1, sticky=(N, W))


def update_viewer():
    global viewer, df_var
    
    count = 0
    for col in current_file:
        name, typeof = col.split(sep='..')
        label = Label(viewer, text=name)
        label.grid(row = 0, column = count)
        
        
        variable = StringVar(viewer)
        if typeof == 'ent':
            widget = Entry(viewer, textvariable = variable)
            widget.grid(row = 1, column = count)
        elif typeof == 'cbx':
            widget = ttk.Combobox(viewer, textvariable = variable, values=pd.unique(current_file[col]).tolist())
            widget.grid(row = 1, column = count)

        df_var[index, count] = variable

        count += 1
    set_column()

def file_to_var(index: int, column: int) -> None: # takes the value from current_file and maps it to the correspondign StringVar in df_var
    global current_file, df_var
    df_var[index, column].set(current_file.iat[index, column])

def set_column(): # uses file_to_var() for every col in active index
    global index
    [file_to_var(index, j) for j in range(current_file.shape[1])] 

def update_df(): # pushes StringVar values in df_var to current_file, to be called when index changed, file saved, new col added
    global current_file, index
    new_row = {col:var.get() for var, col in zip(df_var[index,:], current_file.columns)}
    current_file.loc[index,:] = new_row



update_viewer()

#########################  #########################

ribbon.grid(column = 0, row = 0, sticky=(N, W))
viewer.grid(column = 0, row = 1, sticky=(N, W))

root.mainloop()


### TODO
# let it import normal .csv files and add functionality on top
# add date stepper
# variable entry/cbx width based on max len *2
# make index selector a spinbox (or just add up and down arrows)