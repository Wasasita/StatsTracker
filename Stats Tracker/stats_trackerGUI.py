import tkinter as tk
import json
import multiprocessing

class StatsTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stats Tracker")
        self.root.configure(bg="#051033")  # Set background color

        self.labels = []
        self.entries = []

        bold_font = ("Game Over", 10, "bold")  # Define a bold font (anchor='w' TO ALIGN LEFT)
        arrow = ("Game Over", 12, "bold")

        for stat_label, stat_value in self.load_data().items():
            label = tk.Label(self.root, text=stat_label, bg="#051033", fg="#c4f0ff", font=bold_font)  # Set label background color ("bold")
            label.grid(row=len(self.labels), column=0, padx=(0, 10), pady=(1, 1), sticky="nsew")  # Adjust padding
            self.labels.append(label)

            entry = tk.Entry(self.root, width=5, bg="#030e2b", fg="#c4f0ff", highlightthickness=0.4, highlightbackground="#54d1ff")  # Set text color of entry and add colored outline
            # entry = tk.Entry(self.root, width=5, bg="#00A6F0")
            entry.insert(tk.END, stat_value)
            entry.grid(row=len(self.entries), column=1, padx=(0, 10), pady=(1, 1), sticky="nsew")  # Adjust padding
            self.entries.append(entry)

            up_button = tk.Button(self.root, text="↑", command=lambda index=len(self.labels) - 1: self.update_stat(index, 1), bg="#030e2b", fg="#c4f0ff", font=arrow)
            up_button.grid(row=len(self.labels) - 1, column=2, padx=(0, 5), pady=(1, 1), sticky="nsew")

            down_button = tk.Button(self.root, text="↓", command=lambda index=len(self.labels) - 1: self.update_stat(index, -1), bg="#030e2b", fg="#c4f0ff", font=arrow)
            down_button.grid(row=len(self.labels) - 1, column=3, padx=(0, 5), pady=(1, 1), sticky="nsew")

        close_button = tk.Button(self.root, text="Close", command=self.close_window, bg="#030e2b", font=bold_font, fg="#c4f0ff", highlightthickness=1, highlightbackground="#54d1ff")  # Set button background color
        close_button.grid(row=len(self.labels), columnspan=4, pady=(5, 5), sticky="nsew")  # Adjust button placement
        
        # Configure row and column weights to expand proportionally with window resizing
        for i in range(len(self.labels) + 1):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        
        # Save data whenever the application is closed
        root.protocol("WM_DELETE_WINDOW", self.close_window)

    def load_data(self):
        try:
            with open('stats_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                "Strength": 0,
                "Resistance": 0,
                "Recovery": 0,
                "Intelligence": 0,
                "Focus": 0,
                "Memory": 0,
                "Punctuality": 0,
                "Discipline": 0,
                "Completion": 0
            }

    def update_stat(self, index, value):
        current_value = int(self.entries[index].get())
        new_value = max(0, current_value + value)  # Ensure value doesn't go negative
        self.entries[index].delete(0, tk.END)
        self.entries[index].insert(tk.END, new_value)

    def save_data(self):
        stats = {}
        # Update stats from entries
        for i, label in enumerate(self.labels):
            stats[label.cget("text")] = int(self.entries[i].get())

        # Save stats to file
        with open('stats_data.json', 'w') as file:
            json.dump(stats, file)

    def close_window(self):
        self.save_data()
        self.root.quit()

def run_stats_tracker():
    root = tk.Tk()
    app = StatsTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    multiprocessing.Process(target=run_stats_tracker).start()
