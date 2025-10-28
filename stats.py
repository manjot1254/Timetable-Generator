import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox


class statsSection:
    # constructor method that creates window for stats section
    def __init__(self, root):
        self.root = root
        self.root.title("Stats")
        self.root.geometry("400x400")
        self.root.configure(background="papaya whip")

        # attributes initialised
        file = open("dayStreak.txt", "r")
        currentStreak = file.readline()
        self.daysStreak = int(currentStreak)
        file.close()
        self.pastGrades = []
        self.grade = ""
        self.targetGrade = ""
        self.menuButton = ""
        self.subject = StringVar()

        # labels to display the title name and number of days used
        self.statsLabel = tk.Label(text="Statistics and Analytical Section", background="lemon chiffon")
        self.statsLabel.config(font=("Ariel", 15, "bold"))
        self.statsLabel.pack(pady=15)
        self.daysLabel = tk.Label(text=f"Days Used: {self.daysStreak}", background="lemon chiffon")
        self.daysLabel.config(font=("Ariel", 10, "bold"))
        self.daysLabel.pack(pady=15)

        # buttons to add day, previous grades and show grade trajectories
        self.addDaybutton = tk.Button(text="Check-In", command=self.addDay, background="lemon chiffon")
        self.addDaybutton.pack(pady=5)
        self.addSubject = tk.Button(text="Specify Subject", command=self.addSubject,
                                    background="lemon chiffon")
        self.addSubject.pack(pady=5)
        self.addTargetgrade = tk.Button(text="Add Target Grade", command=self.addTargetgrade,
                                        background="lemon chiffon")
        self.addTargetgrade.pack(pady=5)
        self.addGradebutton = tk.Button(text="Add Previous Grade", command=self.addGrade, background="lemon chiffon")
        self.addGradebutton.pack(pady=5)
        self.calculateTrajectorybutton = tk.Button(text="Calculate Grade Trajectory", command=self.calculateTrajectory,
                                                   background="lemon chiffon")
        self.calculateTrajectorybutton.pack(pady=5)
        self.viewStatsbutton = tk.Button(text="View Stats", command=self.viewStats, background="lemon chiffon")
        self.viewStatsbutton.pack(pady=5)

        self.root.mainloop()

    def addDay(self):
        self.daysStreak = self.daysStreak + 1
        file = open("dayStreak.txt", "w+")
        file.write(str(self.daysStreak))
        file.close()
        self.daysLabel.config(text=f"Days Used: {self.daysStreak}")
        self.addDaybutton.destroy()

    def selectOption(self, option):
        self.targetGrade = option
        messagebox.showinfo("Selected", "Target grade: " + option)
        self.addTargetgrade.destroy()
        self.menuButton.destroy()

    def addTargetgrade(self):
        self.menuButton = tk.Menubutton(root, text="Select grade", borderwidth=1, relief="raised")
        self.menuButton.config(background="lemon chiffon", font=("Ariel", 9))
        self.menuButton.pack()

        optionsMenu = tk.Menu(self.menuButton)
        optionsMenu.add_command(label="A*", command=lambda: self.selectOption("A*"))
        optionsMenu.add_command(label="A", command=lambda: self.selectOption("A"))
        optionsMenu.add_command(label="B", command=lambda: self.selectOption("B"))
        optionsMenu.add_command(label="C", command=lambda: self.selectOption("C"))
        optionsMenu.add_command(label="D", command=lambda: self.selectOption("D"))
        optionsMenu.add_command(label="E", command=lambda: self.selectOption("E"))

        self.menuButton.config(menu=optionsMenu)

    def addGrade(self):
        grade = StringVar()
        options = ['A*', 'A', 'B', 'C', 'D', 'E']
        dropDownmenu = OptionMenu(root, grade, *options)
        dropDownmenu.config(background="lemon chiffon", font=("Ariel", 9))
        dropDownmenu.pack()

        if grade != "":
            self.pastGrades.append(grade)
            return

    def submit(self):
        self.subject = self.subject.get()
        self.newWindow.destroy()
        self.addSubject.destroy()

    def addSubject(self):
        self.newWindow = Tk()
        self.newWindow.title("Timetable Generator")
        self.newWindow.geometry("400x250")
        self.newWindow.configure(background="papaya whip")
        validSubjects = ["Computer Science", "Maths", "Biology", "Chemistry", "Physics", "English", "History",
                         "Law", "Sociology", "Psychology", "Geography"]

        subjectLabel = tk.Label(self.newWindow, text="What subject is this for?", background="lemon chiffon")
        subjectLabel.config(font=("Ariel", 15, "bold"))
        subjectLabel.pack(pady=15)

        dropDownmenu = OptionMenu(self.newWindow, self.subject, *validSubjects)
        dropDownmenu.config(bg="lemon chiffon", font=("Ariel", 9))
        dropDownmenu.pack(pady=14)

        self.submitSubject = tk.Button(self.newWindow, text="Submit", command=self.submit, background="lemon chiffon")
        self.submitSubject.pack(pady=15)

    # function to create graph / database viewer
    def viewStats(self):
        # creates values for both axis / how the plots will look
        xValues = range(len(self.pastGrades))
        plt.plot(xValues, [self.equivalentPoints[grade.get()] for grade in self.pastGrades], marker='o', linestyle='-',
                 markersize=10, markerfacecolor='blue', markeredgecolor='black', alpha=0.7)

        # plots grades / values on each point
        for i, grade in zip(xValues, self.pastGrades):
            plt.annotate(grade.get(), (i, self.equivalentPoints[grade.get()]), textcoords="offset points", xytext=(0, 10),
                         ha='center')

        # establishes x and y values + names of title and axis
        plt.xlim(- 0.5, len(self.pastGrades) - 0.5)
        plt.ylim(0, 60)
        plt.title('Past Grades')
        plt.xlabel('Tests')
        plt.ylabel('UCAS points')

        # only allows integers on the x-axis
        plt.xticks(range(len(self.pastGrades)))

        # creates graph
        plt.show()

        root = Tk()
        root.title("Stats")
        root.geometry("400x100")
        root.configure(bg="lemon chiffon", pady=10, padx=10)

        cursor = sqlite3.connect('stats.db')

        recordSet = cursor.execute('''SELECT subject, targetGrade, currentGrade from stats''')

        i = 0

        headings = ["Subject", "Target Grade", "Current Grade"]

        # add headings
        for d in range(int(len(headings))):
            x = Entry(root, width=20, fg='black', bg='lightgray')
            x.grid(row=1, column=d)
            x.insert(END, headings[d])

            # add user records (subject, target and current grades)
        for y in recordSet:
            for j in range(len(y)):
                e = Entry(root, width=20, fg='black')
                e.grid(row=i+2, column=j)
                e.insert(END, y[j])
            i = i + 1

        root.mainloop()

    def calculateTrajectory(self):
        if len(self.pastGrades) == 0:
            messagebox.showerror("Error", "No grades: Please input grades first")
            self.root.destroy()
            return

        gradesSum = 0
        self.equivalentPoints = {"A*": 56, "A": 48, "B": 40, "C": 32, "D": 24, "E": 16}
        for grade in self.pastGrades:
            if grade.get() in self.equivalentPoints:
                gradesSum += self.equivalentPoints[grade.get()]

        averagePoints = gradesSum / len(self.pastGrades)
        for grade, points in self.equivalentPoints.items():
            if averagePoints >= points:
                messagebox.showinfo("Average", f"Average Grade: {grade}")


                conn = sqlite3.connect("stats.db")
                cursor = conn.cursor()

                # deletes then creates table (resets) but now in comments so this doesn't happen everytime
                cursor.execute("""DROP TABLE stats""")
                cursor.execute("""CREATE TABLE stats (
                              subject text,
                              targetGrade text,
                              currentGrade text
                      )""")
                cursor.execute('INSERT INTO stats VALUES (:subject, :targetGrade, :currentGrade)',
                               {
                                   'subject': self.subject,
                                   'targetGrade': self.targetGrade,
                                   'currentGrade': grade
                               })
                conn.commit()
                conn.close()
                # destroys button as no need to recalculate / add grades and this would flood the database unnecessarily
                self.addGradebutton.destroy()
                self.calculateTrajectorybutton.destroy()

                return


root = Tk()
run = statsSection(root)
