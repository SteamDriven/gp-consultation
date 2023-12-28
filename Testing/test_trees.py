from tkinter import *
from tkinter import ttk


root = Tk()
root.title = ('Test Tree')
root.geometry('550x500')

my_tree = ttk.Treeview(root)
my_tree['columns'] = ('ID', 'First', 'Surname', 'Status')

my_tree.column('#0', width=0, stretch=NO)
my_tree.column('ID', anchor=CENTER, width=80)
my_tree.column('First', anchor=W, width=120)
my_tree.column('Surname', anchor=W, width=120)
my_tree.column('Status', anchor=W, width=120)

my_tree.heading('#0', text='', anchor=W)
my_tree.heading('ID', text='Patient_ID', anchor=CENTER)
my_tree.heading('First', text='First Name', anchor=W)
my_tree.heading('Surname', text='Last Name', anchor=W)
my_tree.heading('Status', text='Current Status', anchor=W)

my_tree.insert(parent='', index='end', iid=0, text='Parent', values=(1, 'Adriel', 'McBean', 'Waiting'))
my_tree.insert(parent='', index='end', iid=1, text='Parent', values=(2, 'Steph', 'Marufu', 'Waiting'))
my_tree.insert(parent='', index='end', iid=2, text='Parent', values=(3, 'Jack', 'Wilkinson', 'Waiting'))
my_tree.insert(parent='', index='end', iid=3, text='Parent', values=(4, 'Meghan', 'Jacques', 'Waiting'))
my_tree.insert(parent='', index='end', iid=4, text='Parent', values=(5, 'Demi', 'Hodgson', 'Waiting'))
my_tree.insert(parent='', index='end', iid=5, text='Parent', values=(6, 'Teresa', 'Cid', 'Waiting'))


my_tree.pack(pady=20)

root.mainloop()