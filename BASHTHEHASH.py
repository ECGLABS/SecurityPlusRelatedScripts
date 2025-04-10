
import hashlib
import os
import random
import string
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class HashGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HashMaster: Cryptic Cruncher")
        self.progress = 0
        self.algorithms = ["MD5", "SHA1", "SHA256", "SHA3_256"]
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Enter Text:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_entry = ttk.Entry(self.root, width=40)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Select Algorithm:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.algo_combo = ttk.Combobox(self.root, values=self.algorithms, state="readonly")
        self.algo_combo.current(0)
        self.algo_combo.grid(row=1, column=1, padx=5, pady=5)

        self.salt_var = tk.BooleanVar()
        self.salt_check = ttk.Checkbutton(self.root, text="Use Salt", variable=self.salt_var)
        self.salt_check.grid(row=2, column=1, sticky="w")

        self.hash_button = ttk.Button(self.root, text="Generate Hash", command=self.generate_hash)
        self.hash_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.challenge_button = ttk.Button(self.root, text="Brute Force Challenge", command=self.brute_force_challenge)
        self.challenge_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.puzzle_button = ttk.Button(self.root, text="Solve Hash Puzzle", command=self.hash_puzzle)
        self.puzzle_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.output_box = scrolledtext.ScrolledText(self.root, width=60, height=12, wrap=tk.WORD)
        self.output_box.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.progress_bar = ttk.Progressbar(self.root, length=300, maximum=100, value=self.progress)
        self.progress_bar.grid(row=7, column=0, columnspan=2, pady=10)

        self.save_button = ttk.Button(self.root, text="Save Progress", command=self.save_progress)
        self.save_button.grid(row=8, column=0, columnspan=2, pady=5)

    def generate_salt(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def generate_hash(self):
        user_input = self.input_entry.get()
        if not user_input:
            messagebox.showwarning("Input Required", "Please enter some text.")
            return

        salt = self.generate_salt() if self.salt_var.get() else ""
        full_input = user_input + salt
        algo = self.algo_combo.get()

        try:
            hash_func = getattr(hashlib, algo.lower())
        except AttributeError:
            messagebox.showerror("Algorithm Error", f"Hashing algorithm '{algo}' is not supported.")
            return

        hash_result = hash_func(full_input.encode()).hexdigest()
        result_text = f"Input: {user_input}\nAlgorithm: {algo}\nSalt: {salt if salt else 'None'}\nHash: {hash_result}\n{'-'*60}\n"
        self.output_box.insert(tk.END, result_text)
        self.output_box.see(tk.END)
        self.update_progress(10)

    def brute_force_challenge(self):
        word = random.choice(["cat", "dog", "bat", "123", "sun"])
        hashed = hashlib.sha256(word.encode()).hexdigest()

        guess = simpledialog.askstring("Brute Force Challenge", f"Guess the word for this SHA256 hash:\n{hashed[:12]}...")
        if guess == word:
            messagebox.showinfo("Success", "Correct! You've cracked the hash!")
            self.update_progress(20)
        else:
            messagebox.showinfo("Failed", f"Incorrect. The word was: {word}")

    def hash_puzzle(self):
        options = ["apple", "banana", "carrot", "donut"]
        correct = random.choice(options)
        hash_val = hashlib.sha1(correct.encode()).hexdigest()

        puzzle_text = f"One of these words matches the hash:\n{hash_val[:16]}...\nOptions: {', '.join(options)}"
        guess = simpledialog.askstring("Hash Puzzle", puzzle_text)
        if guess == correct:
            messagebox.showinfo("Well Done!", "Correct guess!")
            self.update_progress(15)
        else:
            messagebox.showinfo("Oops", f"Nope! The answer was: {correct}")

    def update_progress(self, amount):
        self.progress = min(100, self.progress + amount)
        self.progress_bar["value"] = self.progress

    def save_progress(self):
        log_entry = f"[{datetime.now()}] Progress: {self.progress}%\n"
        with open("hash_game_progress.log", "a") as f:
            f.write(log_entry)
        messagebox.showinfo("Progress Saved", "Your progress has been saved.")

if __name__ == "__main__":
    from tkinter import simpledialog
    root = tk.Tk()
    app = HashGameApp(root)
    root.mainloop()
