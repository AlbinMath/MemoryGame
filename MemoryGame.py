# MemoryGame.py
# A simple memory game implemented in Python using Tkinter.

import tkinter as tk
import random
from tkinter import messagebox

images = ['🍎', '🍌', '🍇', '🍉', '🍓', '🍍', '🍑', '🍒']
images = images * 2  # Duplicate images for pairs

class MemoryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Game")
        self.master.configure(bg='lightblue')
        self.buttons = []
        self.first_selection = None
        self.second_selection = None
        self.first_index = None
        self.second_index = None
        self.matched_pairs = 0
        self.time_left = 120
        self.timer_running = False
        self.is_checking = False
        self.timer_id = None

        # 🔑 Bind 'z' key to close the game window
        self.master.bind('z', self.close_game)

        for i in range(4):
            row = []
            for j in range(4):
                button = tk.Button(master, text='', font=('Arial', 36), width=4, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j),
                                   bg='white', activebackground='lightgray')
                button.grid(row=i, column=j, padx=10, pady=10)
                row.append(button)
            self.buttons.append(row)

        self.restart_button = tk.Button(master, text='Restart', font=('Arial', 24), command=self.restart_game,
                                        bg='lightgreen', activebackground='darkgreen')
        self.restart_button.grid(row=4, column=0, columnspan=4, sticky='ew', padx=10, pady=20)

        self.timer_label = tk.Label(master, text='Time Left: 120', font=('Arial', 24), bg='lightblue')
        self.timer_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        self.restart_game()

    def restart_game(self):
        if self.timer_id is not None:
            self.master.after_cancel(self.timer_id)

        random.shuffle(images)
        self.matched_pairs = 0
        self.first_selection = None
        self.second_selection = None
        self.first_index = None
        self.second_index = None
        self.time_left = 120
        self.timer_running = True
        self.is_checking = False
        self.update_timer()

        for row in self.buttons:
            for button in row:
                button['text'] = ''
                button['bg'] = 'white'

    def update_timer(self):
        if self.timer_running:
            if self.time_left > 0:
                self.timer_label.config(text=f'Time Left: {self.time_left}')
                self.time_left -= 1
                self.timer_id = self.master.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.show_full_board()
                messagebox.showinfo("Time's Up!", "You ran out of time!")

    def show_full_board(self):
        for i in range(4):
            for j in range(4):
                self.buttons[i][j]['text'] = images[i * 4 + j]

    def on_button_click(self, i, j):
        if not self.timer_running or self.is_checking:
            return
        if self.buttons[i][j]['text'] == '' and self.first_selection is None:
            self.buttons[i][j]['text'] = images[i * 4 + j]
            self.first_selection = images[i * 4 + j]
            self.first_index = (i, j)
        elif self.buttons[i][j]['text'] == '' and self.first_selection is not None:
            self.buttons[i][j]['text'] = images[i * 4 + j]
            self.second_selection = images[i * 4 + j]
            self.second_index = (i, j)
            self.is_checking = True
            self.master.after(1000, self.check_for_match)

    def check_for_match(self):
        if self.first_selection == self.second_selection:
            self.matched_pairs += 1
            if self.matched_pairs == len(images) // 2:
                self.timer_running = False
                messagebox.showinfo("Congratulations!", "You've found all pairs!")
        else:
            self.buttons[self.first_index[0]][self.first_index[1]]['bg'] = 'red'
            self.buttons[self.second_index[0]][self.second_index[1]]['bg'] = 'red'
            self.master.after(100, self.reset_buttons)
        self.first_selection = None
        self.second_selection = None
        self.is_checking = False

    def reset_buttons(self):
        self.buttons[self.first_index[0]][self.first_index[1]]['text'] = ''
        self.buttons[self.first_index[0]][self.first_index[1]]['bg'] = 'white'
        self.buttons[self.second_index[0]][self.second_index[1]]['text'] = ''
        self.buttons[self.second_index[0]][self.second_index[1]]['bg'] = 'white'

    # 🔒 Close the game window on pressing 'z'
    def close_game(self, event=None):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
