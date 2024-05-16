import tkinter as tk
import json

class StatsTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stats Tracker")

        self.labels = []
        self.entries = []

        for stat_label, stat_value in self.load_data().items():
            label = tk.Label(self.root, text=stat_label)
            label.grid(row=len(self.labels), column=0, padx=10, pady=5)
            self.labels.append(label)

            entry = tk.Entry(self.root, width=5)
            entry.insert(tk.END, stat_value)
            entry.grid(row=len(self.entries), column=1, padx=10, pady=5)
            self.entries.append(entry)

            up_button = tk.Button(self.root, text="↑", command=lambda index=len(self.labels) - 1: self.update_stat(index, 1))
            up_button.grid(row=len(self.labels) - 1, column=2)

            down_button = tk.Button(self.root, text="↓", command=lambda index=len(self.labels) - 1: self.update_stat(index, -1))
            down_button.grid(row=len(self.labels) - 1, column=3)

        close_button = tk.Button(self.root, text="Close", command=self.close_window)
        close_button.grid(row=len(self.labels) + 1, columnspan=4, pady=10)

        # Save data whenever the application is closed
        root.protocol("WM_DELETE_WINDOW", self.save_data)

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

root = tk.Tk()
app = StatsTracker(root)
root.mainloop()
