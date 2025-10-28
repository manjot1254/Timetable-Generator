import tkinter as tk
from tkinter import messagebox

# class for the timer to be instantiated from
class pomodoroTimer:
    def __init__(self, root):
        # creates tkinter window
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.configure(background="papaya whip")
        self.root.geometry("300x150")

        # displays time elapsed
        self.label = tk.Label(root, bg="bisque", text="00:00", font=("Helvetica", 48))
        self.label.pack()

        # initiate attributes (1500 seconds as 25-minute sessions)
        self.timeRemaining = 1500
        self.running = False
        self.pomodorosCompleted = 0

        # buttons to start/stop/reset timer, which link to functions to fulfil purposes
        self.startButton = tk.Button(root, text="Start", command=self.startTimer)
        self.startButton.pack(side=tk.LEFT, padx=35)

        self.stopButton = tk.Button(root, text="Stop", command=self.stopTimer, state=tk.DISABLED)
        self.stopButton.pack(side=tk.LEFT, padx=35)

        self.resetButton = tk.Button(root, text="Reset", command=self.resetTimer)
        self.resetButton.pack(side=tk.LEFT, padx=25)

    # removes one second from the timer every second until it reaches 0 and the break length is determined
    def updateTimer(self):
        if self.running:
            if self.timeRemaining <= 0:
                self.pomodorosCompleted = self.pomodorosCompleted + 1
                # longer break after 4 pomodoros are completed (15 minutes long instead of 5)
                if self.pomodorosCompleted % 4 == 0:
                    self.timeRemaining = 900
                    messagebox.showinfo("Well Done", "Take a 15 minute break!")
                else:
                    self.timeRemaining = 300
                    messagebox.showinfo("Well Done", "Take a 5 minute break!")
            minutes, seconds = divmod(self.timeRemaining, 60)
            time = "{:02d}:{:02d}".format(minutes, seconds)
            self.label.config(text=time)
            self.timeRemaining = self.timeRemaining - 1
            # delay of 1 second (1000 ms) between each reduction of 1 from the timer by calling it recursively
            self.root.after(1000, self.updateTimer)

    def startTimer(self):
        # must be stopped before restarting so can't run if already running
        if not self.running:
            self.running = True
            # calls function to remove 1 second from timer each second /
            self.updateTimer()
            # start button disabled as timer has been started but can now be stopped, so the stop button is enabled
            self.startButton.config(state=tk.DISABLED)
            self.stopButton.config(state=tk.NORMAL)

    def stopTimer(self):
        self.running = False
        self.startButton.config(state=tk.NORMAL)
        self.stopButton.config(state=tk.DISABLED)

    def resetTimer(self):
        self.running = False
        self.timeRemaining = 1500
        self.label.config(text="25:00")
        self.startButton.config(state=tk.NORMAL)
        self.stopButton.config(state=tk.DISABLED)


root = tk.Tk()
timer = pomodoroTimer(root)
root.mainloop()
