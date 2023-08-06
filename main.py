import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror
from PIL import ImageTk, Image
from sys import platform

colors = {
    1: '#325AA8',
    2: '#32A852',
    3: '#C42727',
    4: '#0D0A5E',
    5: '#5E300A',
    6: '#A53DB3',
    7: '#B3763D',
    8: '#70007A',
}

w = 1 if platform == 'darwin' else 3
h = 2 if platform == 'darwin' else 1


class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=1, height=2, font='Calibri 16 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False


class MineSweeper:
    window = tk.Tk()
    window.title('MineSweeperPro')
    window.resizable(False, False)
    window.geometry('+400+200')
    icon = tk.PhotoImage(file='pngwing.com-2.png')
    window.iconphoto(False, icon)
    mine_img = ImageTk.PhotoImage(Image.open('pngwing.com-3.png').resize((40, 40)))
    mine_lbl = tk.Label(image=mine_img)
    ROW = 10
    COLUMNS = 10
    MINES = 10
    FIND_MINES = MINES
    GAME_OVER = False
    FIRST_CLICK = True
    SECONDS = 0
    TIME_ID = ''

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROW+2):
            temp = []
            for j in range(MineSweeper.COLUMNS+2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button), width=w, height=h)
                btn.bind('<Button-2>', self.flag)
                btn.bind('<Button-3>', self.flag)
                temp.append(btn)
            self.buttons.append(temp)

    @staticmethod
    def flag(event):
        if MineSweeper.GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal' and MineSweeper.FIND_MINES:
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            cur_btn['disabledforeground'] = 'red'
            MineSweeper.FIND_MINES -= 1
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'
            MineSweeper.FIND_MINES += 1
        MineSweeper.bottom()

    def click(self, clicked_button: MyButton):
        if MineSweeper.GAME_OVER:
            return
        if MineSweeper.FIRST_CLICK:
            self.timer(-1)
            self.insert_mines(clicked_button.number)
            self.count_mines()
            MineSweeper.FIRST_CLICK = False
        if clicked_button.is_mine:
            clicked_button.config(text='*', image=MineSweeper.mine_img, disabledforeground='black', background='red', compound="center")
            clicked_button.is_open = True
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    btn['state'] = tk.DISABLED
                    if btn.is_mine:
                        btn['text'] = '*'
                        btn['image'] = MineSweeper.mine_img
                        btn['disabledforeground'] = 'black'
            MineSweeper.GAME_OVER = True
            MineSweeper.window.after_cancel(MineSweeper.TIME_ID)
            showinfo('BOOM!!!!', 'GAME OVER')
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.b_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)
        not_open = MineSweeper.COLUMNS * MineSweeper.ROW
        for i in self.buttons:
            not_open -= sum([k.is_open for k in i])
        if not_open == MineSweeper.MINES and not_open != 1:
            MineSweeper.GAME_OVER = True
            MineSweeper.window.after_cancel(MineSweeper.TIME_ID)
            showinfo('CONGRATULATIONS!', 'YOU WIN!')

    def b_search(self, btn: MyButton):
        que = [btn]
        while que:
            cur_btn = que.pop()
            if cur_btn['text'] == '🚩':
                MineSweeper.FIND_MINES += 1
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='')
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)
            if not cur_btn.count_bomb:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in que:
                            que.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.FIRST_CLICK = True
        MineSweeper.GAME_OVER = False
        MineSweeper.SECONDS = 0
        MineSweeper.window.after_cancel(MineSweeper.TIME_ID)
        MineSweeper.FIND_MINES = MineSweeper.MINES
        MineSweeper.bottom()

    def settings_window(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.resizable(False, False)
        win_settings.wm_title('Settings')
        win_settings.geometry('+500+300')
        tk.Label(win_settings, text='Number rows:').grid(row=0, column=0, padx=20, pady=10, sticky='w')
        row_entry = tk.Entry(win_settings, width=4)
        row_entry.insert(0, str(MineSweeper.MINES))
        row_entry.grid(row=0, column=1, padx=20, pady=10)
        tk.Label(win_settings, text='Number columns:').grid(row=1, column=0, padx=20, pady=10, sticky='w')
        column_entry = tk.Entry(win_settings, width=4)
        column_entry.insert(0, str(MineSweeper.MINES))
        column_entry.grid(row=1, column=1, padx=20, pady=10)
        tk.Label(win_settings, text='Number mines:').grid(row=2, column=0, padx=20, pady=10, sticky='w')
        mines_entry = tk.Entry(win_settings, width=4)
        mines_entry.insert(0, str(MineSweeper.MINES))
        mines_entry.grid(row=2, column=1, padx=20, pady=10)
        tk.Button(win_settings, text='Confirm', command=lambda: self.confirm_settings(
            row_entry, column_entry, mines_entry)).grid(
            row=3, column=0, padx=20, pady=10)
        tk.Button(win_settings, text='Reset', command=lambda: self.reset_settings(win_settings)).grid(
            row=3, column=1, padx=20, pady=10)

    def reset_settings(self, window):
        window.destroy()
        self.settings_window()

    def confirm_settings(self, row, column, mines):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Error!', 'Numbers only')
            return
        if int(row.get()) < 4 or int(column.get()) < 4:
            showerror('Error!', 'Min cells - 4x4')
            return
        if int(mines.get()) >= int(row.get()) * int(column.get()):
            showerror('Error!', 'Too many mines')
            return
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Start', command=self.reload)
        settings_menu.add_command(label='Settings', command=self.settings_window)
        settings_menu.add_command(label='Exit', command=self.window.destroy)
        menubar.add_cascade(label='Game', menu=settings_menu)
        count = 1
        for i in range(1, MineSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
            for j in range(1, MineSweeper.COLUMNS + 1):
                tk.Grid.columnconfigure(self.window, j, weight=1)
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, sticky='nwes')
                count += 1

    def timer(self, seconds=0):
        MineSweeper.TIME_ID = MineSweeper.window.after(1000, self.timer)
        MineSweeper.SECONDS += 1 + seconds
        self.bottom()

    @staticmethod
    def bottom():
        time_count = tk.Label(MineSweeper.window, text=f'Time: {MineSweeper.SECONDS}',
                              relief=tk.RAISED, borderwidth=1)
        time_count.grid(column=1, row=MineSweeper.ROW + 1, columnspan=MineSweeper.COLUMNS // 2, sticky='ew')
        mine_count = tk.Label(MineSweeper.window, text=f'Mines left: {MineSweeper.FIND_MINES}',
                              relief=tk.RAISED, borderwidth=1)
        mine_count.grid(column=MineSweeper.COLUMNS // 2 + 1, row=MineSweeper.ROW + 1, columnspan=MineSweeper.COLUMNS,
                        sticky='ew')

    def start(self):
        self.create_widgets()
        self.bottom()
        MineSweeper.window.mainloop()

    def insert_mines(self, number: int):
        index_mines = self.get_mines(number)
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbor = self.buttons[i+row_dx][j+col_dx]
                            if neighbor.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines(number: int):
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        indexes.remove(number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


game = MineSweeper()
game.start()
