import sqlite3
import random
import webbrowser
import tkinter as tk
from tkinter import messagebox
from tkinter import *

global yesVar
global noVar

# for use when potentially changing program colours
darkModevar = False
# establish days and blocks to outline timetable slots for insertion of subjects
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
blocksSchoolhours = ["8:00 AM - 9:00 AM", "9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 AM", "13:00 "
                                                                                                              "PM - "
                                                                                                              "14:00 "
                                                                                                              "PM",
                     "14:00 PM - 15:00 PM", "15:00 PM - 16:00 PM"]
blocksAfterschool = ["16:00 PM - 17:00 PM", "17:00 PM - 18:00 PM", "18:00 PM - 19:00 PM", "19:00 PM - 20:00 PM",
                     "20:00 PM "
                     "- 21:00 "
                     "PM"]
allBlocks = blocksSchoolhours + blocksAfterschool

# stores user subjects and exam boards in a dictionary for use when assigning revision slots
userSubjectsandExamBoards = {
    "subject1": "",
    "subject2": "",
    "subject3": "",
    "subject4": "",
    "examBoard1": "",
    "examBoard2": "",
    "examBoard3": "",
    "examBoard4": ""

}


def partition(array, lower, upper):
    # pivot is set as the last item in the array
    pivot = array[upper]
    i = lower

    for j in range(lower, upper):
        if array[j] < pivot:
            # if current element is smaller than the pivot, swap current and previous item
            temp = array[i]
            array[i] = array[j]
            array[j] = temp
            i += 1

    # swaps the next item and the pivot
    temp = array[i]
    array[i] = array[upper]
    array[upper] = temp
    return i


def quicksort(array, lower, upper):
    if lower < upper:
        # partition function returns index of the pivot
        pivot = partition(array, lower, upper)

        # sort elements recursively
        quicksort(array, lower, pivot - 1)
        quicksort(array, pivot + 1, upper)

# when called, requires parameters of the array to search and the value to find
def binarySearch(array, targetValue):
    # lower and upper bounds established for use in calculating the midpoint
    lower = 0
    upper = len(array) - 1

    # binary search through array
    while lower <= upper:
        midpoint = (lower + upper) // 2
        if array[midpoint] == targetValue:
            return True
        elif array[midpoint] < targetValue:
            lower = midpoint + 1
        else:
            upper = midpoint - 1
    return False


def dropTable():
    # deletes table and creates a new one to refresh it for a new user
    conn = sqlite3.connect("timetable.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE timetableData""")
    cursor.execute("""CREATE TABLE timetableData (
                  id int,
                  day text,
                  subject text,
                  examBoard text,
                  time real
          )""")
    conn.commit()
    conn.close()


def darkMode(root, dropDownmenu1, label):
    root.configure(background="gray10")
    dropDownmenu1.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 10, "bold"))
    label.config(background="MediumPurple4", fg="gray60")


def darkModebutton(button):
    button.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))


class background:
    def __init__(self, root, text):
        self.root = root
        self.root.title("Timetable Generator")
        self.root.geometry("350x250")
        self.root.configure(background="papaya whip")
        self.label = Label(self.root, bg="bisque", text=text)
        self.label.pack()
        self.label.config(font=("Ariel", 10))
        if darkModevar == True:
            self.root.configure(background="gray10")
            self.label.config(background="MediumPurple4", fg="gray60")


# main subroutine, which recursively calls connect() to add records to database for timetable
def createTimetable():
    global numOfsubjects

    # when "darkModebutton" is clicked, toggles dark mode by changing variables and colours
    def darkMode():
        global darkModevar
        if darkModevar == False:
            darkModevar = True
            root.configure(background="gray10")
            label.config(background="MediumPurple4", fg="gray60")
            dropDownmenu.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))
            darkModebutton.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))
            confirmButton.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))

        elif darkModevar == True:
            darkModevar = False
            root.configure(background="papaya whip")
            label.config(background="lemon chiffon", fg="black")
            dropDownmenu.config(bg="lemon chiffon", fg="black")
            darkModebutton.config(bg="lemon chiffon", fg="black")
            confirmButton.config(bg="lemon chiffon", fg="black")

    def closeNumberwindow():
        root.destroy()

    # creates window, same colours used as sign-up and log-in for consistency
    root = Tk()
    root.title("Timetable Generator")
    root.geometry("400x250")
    root.configure(background="papaya whip")

    # label so user knows what the drop-down menu is for
    label = Label(root, text="How many subjects do you take?", background="lemon chiffon")
    label.pack(pady=15)
    label.config(font=("Ariel", 15, "bold"))

    darkModebutton = tk.Button(root, text="Dark Mode" u"\u263E", command=darkMode, bg="lemon chiffon",
                               font=("Ariel", 10))
    darkModebutton.pack()

    options = [4, 3, 2, 1]
    numOfsubjects = IntVar()
    numOfsubjects.set(3)

    # drop down menu of how many subjects so that all are taken in
    dropDownmenu = OptionMenu(root, numOfsubjects, *options)
    dropDownmenu.config(bg="lemon chiffon", font=("Ariel", 9))
    dropDownmenu.pack(pady=14)

    # button to confirm number and close window
    confirmButton = tk.Button(root, text="Confirm", command=closeNumberwindow, bg="lemon chiffon", font=("Ariel", 10))
    confirmButton.pack()

    # creates window
    root.mainloop()

    for i in range(numOfsubjects.get()):
        def closeSubjectswindow():
            y = 0
            if userSubjectsandExamBoards.get("examBoard1") == '':
                y = 1
            elif userSubjectsandExamBoards.get("examBoard2") == '':
                y = 2
            elif userSubjectsandExamBoards.get("examBoard3") == '':
                y = 3
            elif userSubjectsandExamBoards.get("examBoard4") == '':
                y = 4

            subject = subjectInput.get()
            examBoard = examBoardInput.get()

            # allows for validation of input subjects/exam boards by checking they exist in these two lists
            validSubjects = ["Computer Science", "Maths", "Biology", "Chemistry", "Physics", "English", "History",
                             "Law", "Sociology", "Psychology", "Geography"]
            validExamboards = ["AQA", "OCR", "PEARSON", "WJEC EDUQAS"]

            # sorts each list first via the quicksort, which is a precondition of the binary search
            quicksort(validSubjects, 0, len(validSubjects) - 1)
            quicksort(validExamboards, 0, len(validExamboards) - 1)

            # searches through valid subjects + exam boards arrays to ensure inputs are valid
            if binarySearch(validSubjects, subject.title()):
                userSubjectsandExamBoards.update({"subject" + str(y): subject.title()})
            else:
                messagebox.showerror("Error", "Invalid subject!\nPlease double-check and re-enter subject.")
                root.destroy()
                createTimetable()

            if binarySearch(validExamboards, examBoard.upper()):
                userSubjectsandExamBoards.update({"examBoard" + str(y): examBoard.upper()})
            else:
                messagebox.showerror("Error", "Invalid exam board!\nPlease double-check and re-enter exam board.")
                root.destroy()
                createTimetable()

            # only begins to calculate blocks and add to database if inputted subjects and exam boards are valid
            if y == numOfsubjects.get():
                connect()
                return

            root.destroy()

        root = tk.Tk()
        root.title("Timetable Generator")
        root.configure(background="papaya whip")
        root.geometry("350x250")

        subjectLabel = tk.Label(root, bg="bisque", text="What subject do you take?")
        subjectLabel.pack()
        subjectInput = Entry(root, bg="linen", width=20)
        subjectInput.pack()

        examBoardlabel = tk.Label(root, bg="bisque", text="What exam board?")
        examBoardlabel.pack()

        examBoardInput = Entry(root, bg="linen", width=20)
        examBoardInput.pack()

        confirmButton = tk.Button(root, text="Confirm", command=closeSubjectswindow, bg="lemon chiffon", font=("Ariel", 10))
        confirmButton.pack()

        # changes colours to darker colour scheme if dark mode was toggled at the main screen
        if darkModevar == True:
            root.configure(background="gray10")
            subjectLabel.config(background="MediumPurple4", fg="gray60")
            examBoardlabel.config(background="MediumPurple4", fg="gray60")
            subjectInput.config(background="MediumPurple4", fg="gray60")
            examBoardInput.config(background="MediumPurple4", fg="gray60")
            confirmButton.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))
        root.mainloop()


# called recursively to insert records into database for timetable
def connect():
    # iterate as many times as subjects chosen/input of hours needed to complete
    global days

    def close():
        root = tk.Tk()
        root.geometry("300x150")
        root.configure(background="papaya whip")
        weeklyHours = tk.IntVar()
        weeklyHours.set(15)
        options = [20, 15, 10, 5]

        label = Label(root, text="How many hours a week do you want to revise?", bg="lemon chiffon")
        label.pack()

        # drop-down menu to select a number of hours, preventing invalid inputs
        dropDownmenu1 = OptionMenu(root, weeklyHours, *options)
        dropDownmenu1.config(bg="lemon chiffon", font=("Ariel", 9))
        dropDownmenu1.pack()

        # calls subroutine to change colours, saves rewriting code
        if darkModevar:
            darkMode(root, dropDownmenu1, label)

        def next():
            for i in range(weeklyHours.get()):
                conn = sqlite3.connect("timetable.db")
                cursor = conn.cursor()
                used_ids = set()
                id = 0

                # increments id, calculate days + times
                num = random.randrange(1, 4)
                dayPicker = random.randrange(0, len(days))
                day = days[dayPicker]
                if day == "Monday":
                    id = id
                if day == "Tuesday":
                    id = id + 10000
                if day == "Wednesday":
                    id = id + 20000
                if day == "Thursday":
                    id = id + 30000
                if day == "Friday":
                    id = id + 40000
                if day == "Saturday":
                    id = id + 50000
                if day == "Sunday":
                    id = id + 60000

                subjectInput = userSubjectsandExamBoards["subject" + str(num)]
                examBoardInput = userSubjectsandExamBoards["examBoard" + str(num)]

                # cannot add sessions when users are in school, removes blocks after assigned to prevent duplicates
                if day == "Monday" or day == "Tuesday" or day == "Wednesday" or day == "Thursday" or day == "Friday":
                    time = random.choice(blocksAfterschool)
                    add = time[0]
                    add = add + time[1]
                    add = int(add)
                    if time[1] == int:
                        add = add + time[1]
                    if time[6] == "P":
                        add = add + 1000
                    id = id + add
                else:
                    time = random.choice(allBlocks)
                    add = time[0]
                    add = add + time[1]
                    add = int(add)
                    if time[1] == int:
                        add = add + time[1]
                    if time[6] == "P":
                        add = add + 1000
                    id = id + add

                day = random.choice(days)
                random.choice()
                time = random.choice(blocksAfterschool)

                # begins inserting blocks
                cursor.execute('INSERT INTO timetableData VALUES (:id, :day, :subject, :examBoard, :time)',
                               {
                                   'id': id,
                                   'day': day,
                                   'subject': subjectInput,
                                   'examBoard': examBoardInput,
                                   'time': time,
                               })
                conn.commit()

                cursor.execute("SELECT * FROM timetableData ORDER BY id DESC LIMIT 1")
            root.destroy()

            display()

        button = tk.Button(root, text="Continue", command=next, bg="lemon chiffon", font=("Ariel", 10))
        button.pack()
        if darkModevar:
            darkModebutton(button)

    root = Tk()
    text = "Do you have a job?"
    background(root, text)

    # working days aren't considered to prevent clashing
    def work(workDay=tk.StringVar()):
        label = Label(root, text="How many day(s) do you work?", bg="lemon chiffon")
        label.pack()
        numOfdays = tk.IntVar()
        numOfdays.set(2)
        options = [4, 3, 2, 1]
        dropDownmenu1 = OptionMenu(root, numOfdays, *options)
        dropDownmenu1.config(bg="lemon chiffon", font=("Ariel", 9))
        dropDownmenu1.pack()

        # calls subroutine to change colours, saves rewriting code
        darkMode(root, dropDownmenu1, label)

        def choosedays():
            # so a day can be selected per number of working days
            for i in range(numOfdays.get()):
                dropDownmenu = OptionMenu(root, workDay, *days)
                dropDownmenu.config(bg="lemon chiffon", font=("Ariel", 9))
                dropDownmenu.pack(pady=14)
                workDays = []
                workDays.append(workDay.get())

                if darkModevar == True:
                    dropDownmenu.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 10, "bold"))

            # ensures all working days removed
            for x in workDays:
                if x in days:
                    days.remove(x)

        button = tk.Button(root, text="Choose days", command=choosedays, bg="lemon chiffon", font=("Ariel", 10))
        button.pack()
        if darkModevar:
            darkModebutton(button)

        button = tk.Button(root, text="Continue", command=close, bg="lemon chiffon", font=("Ariel", 10))
        button.pack()
        if darkModevar:
            darkModebutton(button)

    def noWork():
        button = tk.Button(root, text="Continue", command=close, bg="lemon chiffon", font=("Ariel", 10))
        button.pack()
        if darkModevar:
            darkModebutton(button)

    # buttons that call subroutines to add working days first (if yes) and/or then continue with generator (if no)
    yesBox = tk.Checkbutton(root, text="Yes", bg="lemon chiffon", onvalue=1, offvalue=0, command=work)
    noBox = tk.Checkbutton(root, text="No", bg="lemon chiffon", onvalue=1, offvalue=0, command=noWork)
    yesBox.pack()
    noBox.pack()

    if darkModevar == True:
        yesBox.config(bg="MediumPurple4", fg="gray60")
        noBox.config(bg="MediumPurple4", fg="gray60")

    root.mainloop()


def reschedule(i, connection, cursor):
    connection.commit()
    cursor.close()
    def databaseChange():
        connection = sqlite3.connect('timetable.db')
        cursor = connection.cursor()

        newDay = str(dayChangeto.get())
        newTime = str(timeChangeto.get())

        cursor.execute('''SELECT subject FROM (SELECT subject, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM 
        timetableData) AS subquery WHERE row_num = ?''', (i,))
        subject = cursor.fetchone()
        subject = str(subject)
        subject = subject[2:-3]
        cursor.execute('''SELECT examBoard FROM (SELECT examBoard, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM 
        timetableData) AS subquery WHERE row_num = ?''', (i,))
        examBoard = cursor.fetchone()
        examBoard = str(examBoard)
        examBoard = examBoard[2:-3]
        cursor.execute('''SELECT day FROM (SELECT day, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM timetableData) 
        AS subquery WHERE row_num = ?''', (i,))
        oldDay = cursor.fetchone()
        oldDay = str(oldDay)
        cursor.execute('''SELECT time FROM (SELECT time, ROW_NUMBER() OVER (ORDER BY id) AS row_num FROM 
        timetableData) AS subquery WHERE row_num = ?''', (i,))
        oldTime = cursor.fetchone()
        oldTime = str(oldTime)

        cursor.execute('''UPDATE timetableData SET subject="", examBoard="" WHERE subject=? AND examBoard=? AND day=? 
        AND time=?''', (subject, examBoard, oldDay, oldTime))
        cursor.execute('''UPDATE timetableData SET subject=?, examBoard=? WHERE day=? AND time=?''',
                       (subject, examBoard, newDay, newTime))
        connection.commit()
        cursor.close()

    # create window and establish size and colour
    root = tk.Tk()
    root.geometry("400x150")
    root.configure(bg="lemon chiffon")

    # label to ask question as this function is for rescheduling slots
    questionLabel = tk.Label(root, bg="bisque",
                             text="What day and time would you like to change this study session to?")
    questionLabel.config(font=("Ariel", 9, "bold"))
    questionLabel.pack()

    # gives users the option to select a day and time via drop-down menus
    dayChangeto = tk.StringVar()
    dayChangeto.set("Monday")
    dropDownmenu2 = OptionMenu(root, dayChangeto, *days)
    dropDownmenu2.config(bg="lemon chiffon", font=("Ariel", 9))
    dropDownmenu2.pack()
    timeChangeto = tk.StringVar()
    timeChangeto.set("8:00 AM - 9:00 AM")
    dropDownmenu3 = OptionMenu(root, timeChangeto, *allBlocks)
    dropDownmenu3.config(bg="lemon chiffon", font=("Ariel", 9))
    dropDownmenu3.pack()

    confirmButton = tk.Button(root, text="Continue", command=databaseChange, bg="lemon chiffon", font=("Ariel", 10))
    confirmButton.pack()

    # changes colours to darker colour scheme if dark mode was selected at the start
    if darkModevar == True:
        root.configure(background="gray10")
        questionLabel.config(background="MediumPurple4", fg="gray60")
        dropDownmenu2.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))
        dropDownmenu3.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))
        confirmButton.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))


# display timetable contents
def display():
    def resources():
        # function to open link using web browser module
        def openLink(url):
            webbrowser.open_new_tab(url)

        # subject and exam board passed as parameters, used to create a label for each subject
        def createLabel(subject, examBoard):
            flashcardsLink = Label(root, text=subject + " flashcards")
            flashcardsLink.pack(pady=10)
            flashcardsLink.config(font=("Ariel", 10, "bold"))
            flashcardsLink.bind("<Button-1>",
                                lambda x: openLink("https://quizlet.com/search?query=a-level-" + subject + "-" +
                                                   examBoard + "&type=all"))
            pastPapersLink = Label(root, text=subject + " past papers")
            pastPapersLink.pack()
            pastPapersLink.config(font=("Ariel", 10, "bold"))
            pastPapersLink.bind("<Button-1>",
                                lambda x: openLink("https://www.physicsandmathstutor.com/past-papers/a-level-"
                                                   + subject + "/"))

        # creates window with specific text passed as a parameter
        root = Tk()
        text = "Relevant resources hyperlinked below:"
        background(root, text)
        y = 1

        # ensures all subjects have a related label
        while y <= numOfsubjects.get():
            subject = userSubjectsandExamBoards.get("subject" + str(y))
            subject = str(subject)

            examBoard = userSubjectsandExamBoards.get("examBoard" + str(y))
            examBoard = str(examBoard)

            # calls subroutine to create labels
            createLabel(subject, examBoard)

            y = y + 1

    # creates window and sets colour/dimensions
    root = tk.Tk()
    root.geometry("600x460")
    root.configure(bg="lemon chiffon", pady=10, padx=10)

    # sorted chronologically, by earliest days and times first
    connection = sqlite3.connect('timetable.db')
    cursor = connection.cursor()

    recordSet = cursor.execute('''SELECT day, subject, examBoard, time from timetableData ORDER BY id''')

    i = 0
    # displays each record in the data set
    for id in recordSet:
        for j in range(len(id)):
            e = Entry(root, width=19, fg='black')
            e.grid(row=i, column=j)
            e.insert(END, id[j])
        i = i + 1
        button = tk.Button(root, bg="lavender blush", text="Reschedule", command=lambda: reschedule(i, connection, cursor))
        button.grid(row=i - 1, column=j + 1)

        # switches colour scheme if dark mode was selected at start
        if darkModevar:
            root.configure(background="gray10")
            button.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 9, "bold"))

    connection.commit()
    cursor.close()



    # creates button for revision resources, linked to relevant subroutine
    resourcesButton = tk.Button(root, text="Revision Resources 🔨", command=resources, bg="lemon chiffon",
                                font=("Ariel", 10, "bold"))
    if darkModevar:
        resourcesButton.config(bg="MediumPurple4", fg="gray60", font=("Ariel", 10, "bold"))
    resourcesButton.grid(column=2)
    root.mainloop()


dropTable()
createTimetable()
display()
