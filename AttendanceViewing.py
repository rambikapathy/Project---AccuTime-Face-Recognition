import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import pandas as pd


def getCSVdetails():
    file_pd = pd.read_csv('attendanceReport.csv')
    #print(file_pd.head())
    name = file_pd['Student Name']
    date = file_pd['Date']
    time = file_pd['Time']
    return name,date,time


def AttendanceTreeView():
    windowTreeview = tk.Tk()
    windowTreeview.title('Accutime Attendance Report')
    windowTreeview.geometry('600x600')

    # define columns
    columns = ('Student Name', 'Date' , 'Time')

    layout = ttk.Treeview(windowTreeview, columns=columns, show='headings')

    # define headings
    layout.heading('Student Name', text='Student Name')
    layout.heading('Date', text='Date')
    layout.heading('Time', text='Time')

    # generate data
    studentName, dateMarked, timeMarked = getCSVdetails()
    student = []
    for i in range(len(studentName)):
        name = studentName[i]
        date = dateMarked[i]
        time = timeMarked[i]
        student.append((f'{name}', f'{date}', f'{time}'))

    # add data to the treeview
    for studentView in student:
        layout.insert('', tk.END, values=studentView)


    def choice(event):
        for i in layout.selection():
            item = layout.item(i)
            data = item['values']
            # show a message
            showinfo(title='Student Details', message=','.join(data))


    layout.bind('<<TreeviewSelect>>', choice)

    layout.grid(row=0, column=0, sticky='nsew')

    sidebar = ttk.Scrollbar(windowTreeview, orient=tk.VERTICAL, command=layout.yview)
    layout.configure(yscroll=sidebar.set)
    sidebar.grid(row=0, column=1, sticky='ns')

    # run the app
    windowTreeview.mainloop()