"""AIKO MARIELLE C. BERNARDO"""

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os
import sqlite3

class Course:
    def __init__(self,root):
        self.root = root
        self.root.title("Student Information System")
        self.root.geometry("1220x620")
        self.root.config(bg="light slate gray")
        self.root.resizable(False, False)
        
        CourseCode = StringVar()
        CourseName = StringVar()
        SearchCode = StringVar()
        
        def connect():
            conn = sqlite3.connect("studinfo.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses(CourseCode TEXT PRIMARY KEY,\
                        CourseName TEXT)")
            conn.commit()
            conn.close()
        
        def Add(): #Adds a course
            try: 
                conn = sqlite3.connect("studinfo.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO courses(CourseCode, CourseName) VALUES(?,?)",\
                            (CourseCode.get(),CourseName.get()))     
                conn.commit()
                tkinter.messagebox.showinfo("SSISv2", "Course Has Been Added Successfully!") #When there's no error in adding the course
                displayData()
                Clear()
                conn.close()
            except:
                tkinter.messagebox.showerror("SSISv2","Sorry But Course Already Exist") #If The Course Already Exist

        def displayData(): #Display All the Enrolled Courses
            self.courselist.delete(*self.courselist.get_children())
            conn = sqlite3.connect("studinfo.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", END, text=row[0], values=row[0:])
            conn.commit()   
            conn.close()   

        def Delete(): #A function that deletes courses
            try:
                conn = sqlite3.connect("studinfo.db")
                cur = conn.cursor()
                x = self.courselist.selection()[0]
                id_no = self.courselist.item(x)["values"][0]
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("DELETE FROM courses WHERE CourseCode = ?",(id_no,))
                conn.commit()
                self.courselist.delete(x)
                tkinter.messagebox.showinfo("SSISv2", "Course Has Been Deleted Successfully!")
                conn.close()
            except:
                tkinter.messagebox.showerror("SSISv2","Cannot Delete Course, Student/s Enrolled")
                #This message will appear if there is a student enrolled in a course that you are trying to delete
            
            
        def Search(): #A function that search a course by course code
            CourseCode = SearchCode.get()
            conn = sqlite3.connect("studinfo.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses WHERE CourseCode = ?",(CourseCode,))
            conn.commit()
            self.courselist.delete(*self.courselist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.courselist.insert("", 0, text=row[0], values=row[0:])
            conn.close()
            
        def View():
            displayData()

        def Select():
            x = self.courselist.focus()
            if x == "":
                tkinter.messagebox.showerror("SSISv2", "Please select a record from the table.")
                return
            values = self.courselist.item(x, "values")
            CourseCode.set(values[0])
            CourseName.set(values[1])
        
        def Update(): #a function that updates a course
            for selected in self.courselist.selection():
                conn = sqlite3.connect("studinfo.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET CourseCode = ?,CourseName = ? WHERE CourseCode = ?",
                            (CourseCode.get(),CourseName.get(),self.courselist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo("SSISv2", "Course Has Been Updated Successfully!")
                displayData()
                Clear()
                conn.close()
                
        def Clear():
            CourseCode.set("")
            CourseName.set("")
            SearchCode.set("")
                
        def Exit():
            iExit = tkinter.messagebox.askyesno("SSISv2", "Are you sure you want to exit?")
            if iExit > 0:
                root.destroy()
                return
        
        ''''''''' LABELS AND ENTRY WIDGET '''''''''
        
        dataframe=LabelFrame(self.root,bd=1,width=170,height=400, padx=7, pady= 7, relief=RIDGE,bg="light slate gray",font=('cochin',18,'bold'),fg="honeydew2",text="Course Information:")
        dataframe.place(x=10,y=410)
        
        self.labelSearch = Label(dataframe, font=('cochin', 12, 'bold'),
                               text="Search Course:", fg="honeydew2",
                               bg="light slate gray",padx=2,pady=6, anchor=W)
        self.labelSearch.grid(row=0, column=0, sticky=W)
        self.textSearch = Entry(self.root, font=("cochin", 10, "italic"),
                            fg="skyblue4", textvariable=SearchCode, width=18)
        self.textSearch.place(x=147, y=455)
        self.textSearch.insert(0, '')
        
        self.labelCourseCode = Label(dataframe,font=('cochin',12,'bold'),text="Course Code:",
                             padx=2,pady=6,bg="light slate gray", fg="honeydew2", anchor=W)
        self.labelCourseCode.grid(row=1,column=0,sticky=W)
        self.textCourseCode = Entry(dataframe,font=('cochin',12),textvariable=CourseCode,width=29, fg="skyblue4")
        self.textCourseCode.grid(row=1,column=1)
        
        self.labelCourseName = Label(dataframe,font=('cochin',12,'bold'),text="Course Name:",
                             padx=2,pady=6,bg="light slate gray", fg="honeydew2", anchor=W)
        self.labelCourseName.grid(row=2,column=0,sticky=W)
        self.textCourseName = Entry(dataframe,font=('cochin',12),textvariable=CourseName,width=29, fg="skyblue4")
        self.textCourseName.grid(row=2,column=1)


        ''''''''' TREEVIEW '''''''''
        
        scrollbar = Scrollbar(self.root, orient=VERTICAL)
        scrollbar.place(x=1197,y=400,height=208)

        self.courselist = ttk.Treeview(self.root, columns=("Course Code", "Course Name"),
                                       height = 9, yscrollcommand=scrollbar.set)

        self.courselist.heading("Course Code", text="Course Code", anchor=W)
        self.courselist.heading("Course Name", text="Course Name",anchor=W)
        self.courselist['show'] = 'headings'

        self.courselist.column("Course Code", width=200, anchor=W, stretch=False)
        self.courselist.column("Course Name", width=430, stretch=False)

        self.courselist.place(x=565,y=400)
        scrollbar.config(command=self.courselist.yview)
        
        ''''''''' BUTTONS '''''''''
        
        self.btnSearch = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='SEARCH', fg="skyblue4", command=Search)
        self.btnSearch.place(x=285, y=445)

        self.btnSelect = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='SELECT', fg="skyblue4", command=Select)
        self.btnSelect.place(x=430, y=425)

        self.btnShow = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                              padx=24, width=8, text='VIEW COURSES', fg="skyblue4", command=View)
        self.btnShow.place(x=430, y=472)

        self.btnClear = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                               padx=24, width=8, text='CLEAR', fg="skyblue4", command=Clear)
        self.btnClear.place(x=430, y=524)
        
        self.btnExit = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                              padx=24, width=8, text='EXIT', fg="skyblue4", command=Exit)
        self.btnExit.place(x=430, y=575)
        
        self.btnAddNew = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='ADD', fg="skyblue4", command=Add)
        self.btnAddNew.place(x=10, y=575)

        self.btnUpdate = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='UPDATE', fg="skyblue4", command=Update)
        self.btnUpdate.place(x=150, y=575)

        self.btnDelete = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='DELETE', fg="skyblue4", command=Delete)
        self.btnDelete.place(x=290, y=575)

 
        connect()
        displayData()

class Student:
    def __init__(self,root):
        self.root = root
        self.root.title("Student Information System")
        self.root.geometry("1220x620")
        self.root.config(bg="light slate gray")
        self.root.resizable(False, False)
        
        StudentID = StringVar()
        StudentName = StringVar()
        Course = StringVar()
        YearLevel = StringVar()
        Gender = StringVar()
        Search = StringVar()
        
        def connect():
            conn = sqlite3.connect("studinfo.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_key = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students(StudentID TEXT PRIMARY KEY, \
                        StudentName TEXT, CourseCode TEXT, YearLevel TEXT, Gender TEXT, \
                        FOREIGN KEY(CourseCode) REFERENCES courses(CourseCode) ON UPDATE CASCADE)")
            conn.commit()
            conn.close()
        
        def addData(): #Adds a student that should input all the information before it will be added
            if StudentID.get() == "" or StudentName.get() == "" or Course.get() == "" or YearLevel.get() == "" or Gender.get() == "": 
                tkinter.messagebox.showinfo("SSISv2", "Please fill in the box")
            else:  
                ID = StudentID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("SSISv2", "Sorry But Invalid ID Number")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("SSISv2", "Sorry But Invalid ID Number")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("SSISv2", "Sorry But Invalid ID Number")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("SSISv2", "Sorry But Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("SSISv2", "Sorry But Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("studinfo.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO students(StudentID, StudentName, CourseCode, YearLevel, Gender) VALUES(?,?,?,?,?)",
                                             (StudentID.get(),StudentName.get(),Course.get(), YearLevel.get(),Gender.get()))                                        
                                    conn.commit() 
                                    tkinter.messagebox.showinfo("SSISv2", "Student Has Been Recorded Successfully")
                                    Clear()
                                    displayData()
                                    conn.close()
                                except:
                                    tkinter.messagebox.showerror("SSISv2", "Sorry But Course Unavailable")
                    else:
                        tkinter.messagebox.showerror("SSISv2", "Sorry But Invalid ID")
                else:
                    tkinter.messagebox.showerror("SSISv2", "Sorry But Invalid ID")
            
        def displayData():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("studinfo.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", END, text=row[0], values=row[0:])
            conn.commit()
            conn.close()   

        def deleteData():
            conn = sqlite3.connect("studinfo.db")
            cur = conn.cursor()
            x = self.studentlist.selection()[0]
            id_no = self.studentlist.item(x)["values"][0]
            cur.execute("DELETE FROM students WHERE StudentID = ?",(id_no,))
            conn.commit()
            self.studentlist.delete(x)
            tkinter.messagebox.showinfo("SSISv2", "Student Has Been Deleted Successfully!")
            conn.close()

        def searchData():
            StudentID = Search.get()
            conn = sqlite3.connect("studinfo.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students WHERE StudentID = ?",(StudentID,))
            conn.commit()
            self.studentlist.delete(*self.studentlist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", 0, text=row[0], values=row[0:])
            conn.close()  

        def ViewData():
            displayData()

        def editData():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("SSISv2", "Please select a record from the table.")
                return
            values = self.studentlist.item(x, "values")
            StudentID.set(values[0])
            StudentName.set(values[1])
            Course.set(values[2])
            YearLevel.set(values[3])
            Gender.set(values[4])
        
        def updateData():
            for selected in self.studentlist.selection():
                conn = sqlite3.connect("studinfo.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE students SET StudentID = ?,StudentName = ?, CourseCode = ?,\
                            YearLevel = ?, Gender = ? WHERE StudentID = ?",\
                            (StudentID.get(),StudentName.get(),Course.get(),
                             YearLevel.get(),Gender.get(),self.studentlist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo("SSISv2", "Student has beeen successfully updated")
                displayData()
                Clear()
                conn.close()
                
        def Clear():
            StudentID.set("")
            StudentName.set("")
            Course.set("")
            YearLevel.set("")
            Gender.set("")
            Search.set("")
        
        '''''''''FRAMES'''''''''

        title=Label(self.root,bd=8,padx=50,pady=8,font=('cochin',30,'bold', 'italic','underline'),text="S T U D E N T   I N F O R M A T I O N   S Y S T E M",fg="honeydew2", bg="light slate gray")
        title.place(x=100,y=10)

        dataframeleft=LabelFrame(self.root,bd=1,width=150,height=400, padx=6, pady= 6, relief=RIDGE,bg="light slate gray",font=('cochin',18,'bold'),fg="honeydew2",text="Student's Information:")
        dataframeleft.place(x=10,y=100)


        '''''''''LABELS AND ENTRY WIDGET'''''''''

        self.labelSearch = Label(dataframeleft, font=('cochin', 12, 'bold'),
                               text="Search ID:", fg="honeydew2",
                               bg="light slate gray",padx=2,pady=6, anchor=W)
        self.labelSearch.grid(row=0, column=0, sticky=W)
        self.textSearch = Entry(self.root, font=("cochin", 10, "italic"),
                            fg="skyblue4", textvariable=Search, width=18)
        self.textSearch.place(x=125, y=145)
        self.textSearch.insert(0, '')
        
        self.labelID = Label(dataframeleft,font=('cochin',12,'bold'),text="ID Number:",
                             padx=2,pady=6,bg="light slate gray", fg="honeydew2", anchor=W)
        self.labelID.grid(row=1,column=0,sticky=W)
        self.textID = Entry(dataframeleft,font=('cochin',12),textvariable=StudentID,width=30, fg="skyblue4")
        self.textID.grid(row=1,column=1)

        self.labelFname = Label(dataframeleft,font=('cochin',12,'bold'),text="Full Name:",
                                padx=2,pady=6,bg="light slate gray", fg="honeydew2", anchor=W)
        self.labelFname.grid(row=2,column=0,sticky=W)
        self.labelFName = Label(dataframeleft, font=('cochin', 10, 'italic', 'bold'),
                                 text="Firstname                  MI                  Lastname",
                                 bg="light slate gray", fg="honeydew2", bd=10, anchor=W)
        self.labelFName.grid(row=3, column=1, sticky=W)
        self.textFname = Entry(dataframeleft,font=('cochin',12),textvariable=StudentName,width=30, fg="skyblue4")
        self.textFname.grid(row=2,column=1)
        
        self.labelCourse = Label(dataframeleft,font=('cochin',12,'bold'),text="Course:",
                                 padx=2,pady=6,bg="light slate gray", fg="honeydew2", anchor=W)
        self.labelCourse.grid(row=4,column=0,sticky=W)
        self.textCourse = Entry(dataframeleft,font=('cochin',12),textvariable=Course ,width=30, fg="skyblue4")
        self.textCourse.grid(row=4,column=1)

        self.labelYearLevel = Label(dataframeleft, font=('cochin', 12, 'bold'), text="Year Level:",
                                  fg="honeydew2", bg="light slate gray",padx=2,pady=6, anchor=W)
        self.labelYearLevel.grid(row=5, column=0, sticky=W)
        self.labelYearLevel = ttk.Combobox(dataframeleft, font=('cochin', 10),
                                         state='readonly', width=36, textvariable=YearLevel)
        self.labelYearLevel['values'] = ('', '1st Year', '2nd Year', '3rd Year', '4th Year')
        self.labelYearLevel.current(0)
        self.labelYearLevel.grid(row=5, column=1)

        self.labelGender = Label(dataframeleft, font=('cochin', 12, 'bold'), text="Gender:",
                               fg="honeydew2", bg="light slate gray", padx=2,pady=6, anchor=W)
        self.labelGender.grid(row=6, column=0, sticky=W)
        self.labelGender = ttk.Combobox(dataframeleft, font=('cochin', 10),
                                      state='readonly', width=36, textvariable=Gender)
        self.labelGender['values'] = ('', 'Female', 'Male')
        self.labelGender.current(0)
        self.labelGender.grid(row=6, column=1)

        ''''''''' TREEVIEW '''''''''
        
        scrollbar = Scrollbar(self.root, orient=VERTICAL)
        scrollbar.place(x=1195,y=105,height=287)

        self.studentlist = ttk.Treeview(self.root, columns=("ID Number", "Name", "Course", "Year Level", "Gender"),
                                        height = 13, yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID Number", text="ID Number", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course", text="Course",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID Number", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)

        self.studentlist.place(x=563,y=105)
        scrollbar.config(command=self.studentlist.yview)
        
        ''''''''' BUTTONS '''''''''

        self.btnSearch = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='SEARCH', fg="skyblue4", command=searchData)
        self.btnSearch.place(x=275, y=135)

        self.btnSelect = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='SELECT', fg="skyblue4", command=editData)
        self.btnSelect.place(x=430, y=120)

        self.btnShow = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                              padx=24, width=8, text='VIEW STUDENTS', fg="skyblue4", command=ViewData)
        self.btnShow.place(x=430, y=168)

        self.btnAddNew = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='ADD', fg="skyblue4", command=addData)
        self.btnAddNew.place(x=430, y=216)

        self.btnUpdate = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='UPDATE', fg="skyblue4", command=updateData)
        self.btnUpdate.place(x=430, y=264)

        self.btnDelete = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                                padx=24, width=8, text='DELETE', fg="skyblue4", command=deleteData)
        self.btnDelete.place(x=430, y=312)

        self.btnClear = Button(self.root, pady=1, bd=4, font=('cochin', 10, 'bold'),
                               padx=24, width=8, text='CLEAR', fg="skyblue4", command=Clear)
        self.btnClear.place(x=430, y=360)

 
        connect()
        displayData()
        
if __name__ == '__main__':
    root = Tk()
    application = Course(root)
    application = Student(root)
    root.mainloop()