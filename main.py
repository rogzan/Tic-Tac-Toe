from tkinter import *
from functools import partial
from random import randint
import datetime

# Dane startowe
root = Tk()
root.geometry('480x510')
root.resizable(False, False)
root.title("Kółko i krzyżyk")
root.iconbitmap("logo.ico")
photo_1 = PhotoImage(file="logo.png")
clicked = False
counter = 0
nick1 = ""
nick2 = ""
last_move = []
game_works = 0
time = 0


# Funkcja tworząca menu startowe gry.
def gameMenu():
    Label(root, image=photo_1).place(x=345, y=0)
    Label(root, text='Kółko i krzyżyk', fg="dark green", font="Times 32 bold").place(x=30, y=35)
    Label(root, text='Gracz "0":', fg="black", font="Times 16 bold").place(x=20, y=135)
    nick1_menu = Entry(root, width=30, borderwidth=5)
    nick1_menu.place(x=250, y=135)
    Label(root, text='Gracz "X" (Multiplayer):', fg="black", font="Times 16 bold").place(x=20, y=170)
    nick2_menu = Entry(root, width=30, borderwidth=5)
    nick2_menu.place(x=250, y=170)
    Label(root, text='Podaj rozmiar planszy:', fg="black", font="Times 16 bold").place(x=20, y=205)
    size = Entry(root, width=30, borderwidth=5)
    size.place(x=250, y=205)
    size.insert(0, "3")
    Label(root, text='Czas gry:', fg="black", font="Times 16 bold").place(x=20, y=240)
    time_game = Entry(root, width=30, borderwidth=5)
    time_game.place(x=250, y=240)
    time_game.insert(0, "0")
    Label(root, text='Menu', fg="black", font="Times 22 bold").place(x=200, y=270)
    Button(root, text="Graj z komputerem", fg="black", font="Times 16", padx="70",
           command=partial(singleplayer_game, nick1_menu, size, time_game)).place(x=82, y=310)
    Button(root, text="Graj ze znajomym", fg="black", font="Times 16", padx="75",
           command=partial(multiplayer_game, nick1_menu, nick2_menu, size)).place(x=82, y=355)
    Button(root, text="Statystyki", fg="black", font="Times 16", padx="110",
           command=partial(stat_display)).place(x=82, y=400)
    Button(root, text="Wyjdź", fg="black", font="Times 16", padx="123", command=root.quit).place(x=82, y=445)


# Pasem Menu dostępny w każdym momencie gry z podstawowymi opcjami oraz info
def menuToolbar(button=0):
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu, tearoff=0)
    menu.add_cascade(label='Opcje', menu=filemenu)
    filemenu.add_command(label='Cofnij', command=partial(return_click, button))
    filemenu.add_command(label='Reset', command=reset)
    filemenu.add_command(label='Statystyki', command=stat_display)
    filemenu.add_separator()
    filemenu.add_command(label='Wyjdź', command=root.quit)
    infomenu = Menu(menu, tearoff=0)
    menu.add_cascade(label='Info', menu=infomenu)
    infomenu.add_command(label='Autorzy:')
    infomenu.add_separator()
    infomenu.add_command(label='Roksana Cieśla')
    infomenu.add_command(label='Stanisław Dudiak')
    infomenu.add_command(label='Jakub Dębski')
    infomenu.add_command(label='Marcin Brzózka')


# Funkcja resetująca - powrót do menu gry
def reset():
    global clicked
    global counter
    global nick1
    global nick2
    global time
    for widget in root.winfo_children():
        widget.destroy()
    clicked = False
    counter = 0
    nick1 = ""
    nick2 = ""
    time = 0
    menuToolbar()
    gameMenu()


# Fukcja przygotowująca grę ze znajomym
def multiplayer_game(nick1_menu, nick2_menu, size_menu):
    global nick1
    global nick2
    nick1 = nick1_menu.get()
    nick2 = nick2_menu.get()
    size = int(size_menu.get())

    if (size < 3):
        size = 3
    for widget in root.winfo_children():
        widget.destroy()
    button = [[0 for i in range(size)] for j in range(size)]
    menuToolbar(button)

    for i in range(size):
        for j in range(size):
            button[i][j] = Button(root, text=None, font="Times 24 bold",
                                  command=partial(multiplayer_click, button, i, j, size))
            button[i][j].grid(row=i, column=j, sticky="nsew")
            Grid.rowconfigure(root, i, weight=1)
            Grid.columnconfigure(root, j, weight=1)


# Funkcja gry ze znajomym
def multiplayer_click(button, i, j, size):
    global clicked
    global counter
    global last_move
    if (button[i][j]['text'] == "" and clicked):
        button[i][j]['text'] = "X"
        clicked = False
        counter += 1
        win(button, size)
        last_move.append((i, j))
    elif (button[i][j]['text'] == "" and not clicked):
        button[i][j]['text'] = "O"
        clicked = True
        counter += 1
        win(button, size)
        last_move.append((i, j))


# Pomocnicza do funkcji określającej ruch komputera
def empty_cells(board, size):
    empty = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                empty.append((i, j))
    return empty


# Pomocnicza do funkcji określającej ruch komputera
def countWins(board, size, x):
    count = 0
    empty = empty_cells(board, size)
    for (i, j) in empty:
        copy = board[i][j]
        board[i][j] = x
        count += win2(board, size, x)
        board[i][j] = copy
    return count


# Pomocnicza do funkcji określającej ruch komputera
def win2(board, size, x):
    for i in range(size - 2):
        for j in range(size - 2):
            if (board[i][j] == board[i + 1][j] == board[i + 2][j] == x) \
                    or (board[i][j + 1] == board[i + 1][j + 1] == board[i + 2][j + 1] == x) \
                    or (board[i][j + 2] == board[i + 1][j + 2] == board[i + 2][j + 2] == x) \
                    or (board[i][j] == board[i][j + 1] == board[i][j + 2] == x) \
                    or (board[i + 1][j] == board[i + 1][j + 1] == board[i + 1][j + 2] == x) \
                    or (board[i + 2][j] == board[i + 2][j + 1] == board[i + 2][j + 2] == x) \
                    or (board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == x) \
                    or (board[i][j + 2] == board[i + 1][j + 1] == board[i + 2][j] == x):
                return 1
            else:
                return 0


# Funcja określająca ruch komputera
def get_move(board, size):
    empty = empty_cells(board, size)
    length = len(empty)

    if length == 1:
        i, j = empty[0]
        return i, j

    for i, j in empty:
        copy = board[i][j]
        board[i][j] = "X"

        if win2(board, size, "X"):
            board[i][j] = "X"
            return i, j

        board[i][j] = copy

    for i, j in empty:
        copy = board[i][j]
        board[i][j] = "O"

        if win2(board, size, "O"):
            board[i][j] = "X"
            return i, j

        board[i][j] = copy

    wins2 = []
    l = 0

    for i, j in empty:
        copy = board[i][j]
        board[i][j] = 'X'
        if countWins(board, size, 'X') > 1:
            l += 1
            r = [i, j]
            wins2.append(r)

        board[i][j] = copy

    if l:
        m = wins2[randint(0, l - 1)]
        board[m[0]][m[1]] = 'X'
        return m[0], m[1]

    centers = [(i, j) for i in range(size) for j in range(size)
               if ((i in [0, size - 1]) == (j in [0, size - 1]) == False) and ((i, j) in empty)]

    if len(centers) > 0:
        r = centers[randint(0, len(centers) - 1)]
        board[r[0]][r[1]] = "X"
        return r[0], r[1]

    pos_edges = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
    edges = [(i, j) for i in pos_edges
             if ((i, j) in empty)]

    if len(edges) > 0:
        r = edges[randint(0, len(edges) - 1)]
        board[r[0]][r[1]] = "X"
        return r[0], r[1]

    middles = [(i, j) for i in range(size) for j in range(size) if
               (i in [0, size - 1]) != (j in [0, size - 1]) and ((i, j) in empty)]

    r = middles[randint(0, len(middles) - 1)]
    board[r[0]][r[1]] = "X"
    return r[0], r[1]


# Przygotowanie gry z komputerem
def singleplayer_game(nick1_menu, size_menu, time_game):
    global nick1
    global nick2
    global game_works
    game_works = 1

    # Licznik czasu dla gry z komputerem
    time = int(time_game.get())
    start_game = datetime.datetime.now()

    def remaining_time():
        global game_works
        x = datetime.datetime.now()
        time_difference = x - start_game

        if(int(time_difference.total_seconds()) <= time and game_works == 1 ):
            root.after(1000, remaining_time)

        if((int(time_difference.total_seconds())) > time):
            for widget in root.winfo_children():
                widget.destroy()
            menuToolbar()
            Label(root, text="Remis", fg="dark green", font="Times 42 bold").place(x=165, y=100)
            Label(root, text="Koniec czasu", fg="dark green", font="Times 42 bold").place(x=85, y=200)
            Button(root, text="Menu", fg="black", font="Times 16", padx="123", command=reset).place(x=82, y=350)
            game_works = 0

    if (time != 0):
        root.after(1000, remaining_time)

    nick1 = nick1_menu.get()
    nick2 = "Komputer"
    size = int(size_menu.get())

    if (size < 3):
        size = 3
    for widget in root.winfo_children():
        widget.destroy()
    menuToolbar()
    button = [[0 for i in range(size)] for j in range(size)]

    for i in range(size):
        for j in range(size):
            button[i][j] = Button(root, text=None, font="Times 24 bold",
                                  command=partial(singleplayer_click, button, i, j, size))
            button[i][j].grid(row=i, column=j, sticky="nsew")
            Grid.rowconfigure(root, i, weight=1)
            Grid.columnconfigure(root, j, weight=1)


# Gra z komputerem
def singleplayer_click(button, i, j, size):
    global clicked
    global counter
    board = [[button[y][x]['text'] for x in range(size)] for y in range(size)]

    if (button[i][j]['text'] == "" and not clicked):
        button[i][j]['text'] = "O"
        board[i][j] = "O"
        clicked = True
        counter += 1
        win(button, size)
        while (clicked):
            computer_move = get_move(board, size)
            computer_i = computer_move[0]
            computer_j = computer_move[1]
            if (button[computer_i][computer_j]['text'] == ""):
                button[computer_i][computer_j]['text'] = "X"
                clicked = False
                counter += 1
                win(button, size)


# Funkcja sprawdzania zwycięzcy
def win(button, size):
    global nick1
    global nick2
    global game_works

    for i in range(size - 2):
        for j in range(size - 2):
            if (button[i][j]['text'] == button[i + 1][j]['text'] == button[i + 2][j]['text'] == "O") \
                    or (button[i][j + 1]['text'] == button[i + 1][j + 1]['text'] == button[i + 2][j + 1]['text'] == "O") \
                    or (button[i][j + 2]['text'] == button[i + 1][j + 2]['text'] == button[i + 2][j + 2]['text'] == "O") \
                    or (button[i][j]['text'] == button[i][j + 1]['text'] == button[i][j + 2]['text'] == "O") \
                    or (button[i + 1][j]['text'] == button[i + 1][j + 1]['text'] == button[i + 1][j + 2]['text'] == "O") \
                    or (button[i + 2][j]['text'] == button[i + 2][j + 1]['text'] == button[i + 2][j + 2]['text'] == "O") \
                    or (button[i][j]['text'] == button[i + 1][j + 1]['text'] == button[i + 2][j + 2]['text'] == "O") \
                    or (button[i][j + 2]['text'] == button[i + 1][j + 1]['text'] == button[i + 2][j]['text'] == "O"):
                game_works = 0
                for widget in root.winfo_children():
                    widget.destroy()
                menuToolbar()
                stat(nick1, nick2)
                Label(root, text="Wygrał", fg="dark green", font="Times 42 bold").pack()
                Label(root, text=nick1, fg="dark green", font="Times 42 bold").pack()
                Button(root, text="Menu", fg="black", font="Times 16", padx="123", command=reset).place(x=82, y=350)

            elif (button[i][j]['text'] == button[i + 1][j]['text'] == button[i + 2][j]['text'] == "X") \
                    or (button[i][j + 1]['text'] == button[i + 1][j + 1]['text'] == button[i + 2][j + 1]['text'] == "X") \
                    or (button[i][j + 2]['text'] == button[i + 1][j + 2]['text'] == button[i + 2][j + 2]['text'] == "X") \
                    or (button[i][j]['text'] == button[i][j + 1]['text'] == button[i][j + 2]['text'] == "X") \
                    or (button[i + 1][j]['text'] == button[i + 1][j + 1]['text'] == button[i + 1][j + 2]['text'] == "X") \
                    or (button[i + 2][j]['text'] == button[i + 2][j + 1]['text'] == button[i + 2][j + 2]['text'] == "X") \
                    or (button[i][j]['text'] == button[i + 1][j + 1]['text'] == button[i + 2][j + 2]['text'] == "X") \
                    or (button[i][j + 2]['text'] == button[i + 1][j + 1]['text'] == button[i + 2][j]['text'] == "X"):
                game_works = 0
                for widget in root.winfo_children():
                    widget.destroy()
                menuToolbar()
                stat(nick2, nick1)
                Label(root, text="Wygrał", fg="dark green", font="Times 42 bold").pack()
                Label(root, text=nick2, fg="dark green", font="Times 42 bold").pack()
                Button(root, text="Menu", fg="black", font="Times 16", padx="123", command=reset).place(x=82, y=350)

            elif (counter == size * size):
                game_works = 0
                for widget in root.winfo_children():
                    widget.destroy()
                stat_draw(nick1, nick2)
                Label(root, text="Remis", fg="dark green", font="Times 42 bold").place(x=165, y=100)
                Button(root, text="Menu", fg="black", font="Times 16", padx="123", command=reset).place(x=82, y=350)


# Funkcja zapisywania zwycięztwa
def stat(winer, loser):
    with open(r"Statystyki.txt", 'a') as file:
        x = datetime.datetime.now()
        date = x.strftime("%d/%m/%Y %H:%M:%S")
        text = f"{date} - Wygrany: {winer}, Przegrany: {loser}\n"
        file.write(text)


# Funkcja zapisywania remisu
def stat_draw(p1, p2):
    with open(r"Statystyki.txt", 'a') as file:
        x = datetime.datetime.now()
        date = x.strftime("%d/%m/%Y %H:%M:%S")
        text = f"{date} - Remis pomiędzy {p1} i {p2}\n"
        file.write(text)


# Funkcja odpowiedzialna za wyświetlanie statystyk
def stat_display():
    for widget in root.winfo_children():
        widget.destroy()
    menuToolbar()
    file = open(r"Statystyki.txt", "r")
    list = [" "] * 17
    list_of_stats = file.readlines()
    list_of_stats.reverse()
    if(len(list_of_stats) > 17):
        length = 17
    else:
        length = len(list_of_stats)

    for i in range(length):
        list[i] = list_of_stats[i]
    for i in range(17):
        Label(root, text=list[i], fg="black", font="Times 13 bold").place(x=0, y=i * 24)
    Button(root, text="Wróć do menu", fg="black", font="Times 16", padx="10", command=reset).place(x=170, y=420)


# Funkcja cofania ruchu
def return_click(button):
    global counter
    global clicked
    global last_move
    if last_move != []:
        if (clicked == True):
            clicked = False
        else:
            clicked = True
        counter -= 1
        button[last_move[-1][0]][last_move[-1][1]]['text'] = ""
        last_move.pop(-1)


#Uruchomienie gry
menuToolbar()
gameMenu()
root.mainloop()
