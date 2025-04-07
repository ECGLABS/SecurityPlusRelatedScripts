import tkinter as tk
from tkinter import messagebox, filedialog
import csv

TOTAL_QUESTIONS = 100
TIME_LIMIT_SECONDS = 90 * 60  # 90 minutes in seconds

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Security+ Answer Tracker")
        self.q_index = 1
        self.answers = {}
        self.remaining_time = TIME_LIMIT_SECONDS

        self.timer_label = tk.Label(master, text="", font=("Helvetica", 14), fg="red")
        self.label_num = tk.Label(master, text="", font=("Helvetica", 16, "bold"))
        self.var = tk.StringVar(value="")

        self.radio_buttons = []
        for letter in ["A", "B", "C", "D"]:
            rb = tk.Radiobutton(
                master,
                text=letter,
                variable=self.var,
                value=letter,
                indicatoron=0,
                width=10,
                font=("Helvetica", 14),
                relief="raised",
                bd=2,
                padx=10,
                pady=5,
                bg="lightgray",
                command=self.highlight_selection
            )
            rb.pack(pady=5)
            self.radio_buttons.append(rb)

        self.btn_next = tk.Button(master, text="Next", command=self.next_question, font=("Helvetica", 12))
        self.btn_export = tk.Button(master, text="Export Answers", command=self.export_results, font=("Helvetica", 12))

        self.timer_label.pack(pady=5)
        self.label_num.pack(pady=10)
        self.btn_next.pack(pady=10)
        self.btn_export.pack(pady=5)

        self.load_question()
        self.update_timer()

    def load_question(self):
        self.var.set("")
        self.label_num.config(text=f"Question {self.q_index}")
        for rb in self.radio_buttons:
            rb.config(relief="raised", bg="lightgray", state="normal")

    def highlight_selection(self):
        for rb in self.radio_buttons:
            if rb.cget("value") == self.var.get():
                rb.config(relief="sunken", bg="lightblue")
            else:
                rb.config(relief="raised", bg="lightgray")

    def next_question(self):
        if self.remaining_time <= 0:
            return
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("Missing Answer", "Select A, B, C, or D before moving on.")
            return
        self.answers[self.q_index] = selected
        if self.q_index < TOTAL_QUESTIONS:
            self.q_index += 1
            self.load_question()
        else:
            messagebox.showinfo("Done", "You've completed all questions.")

    def export_results(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Question Number", "Answer"])
                for qnum in sorted(self.answers):
                    writer.writerow([qnum, self.answers[qnum]])
            messagebox.showinfo("Export Complete", "Your answers have been exported.")

    def update_timer(self):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"Time Remaining: {mins:02}:{secs:02}")
            self.remaining_time -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.time_up()

    def time_up(self):
        self.timer_label.config(text="Time's up!")
        self.btn_next.config(state="disabled")
        for rb in self.radio_buttons:
            rb.config(state="disabled")
        messagebox.showinfo("Time's Up", "Your 90 minutes are over. Please export your answers.")
        self.export_results()

root = tk.Tk()
app = QuizApp(root)
root.mainloop()