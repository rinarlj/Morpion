from tkinter import Canvas, Tk, Button, LEFT
from tkinter.messagebox import showerror, showinfo

def on_left_click(canvas, event):
    global board
    x,y = event.x, event.y
    
    i,j = get_board_indexes(x,y,n)

    if not check_possible_move(board, i, j):
        showerror("Non", "Tu ne peux pas")
    else:
        
        if player_turn == 1:
            board[i][j] = player_turn
            draw_circle(canvas, i, j, n)
        elif (player_turn == 2):
            board[i][j] = player_turn
            draw_cross(canvas, i, j, n)

        winning = check_winning(board, n)

        if winning == 0:
            showinfo("Résultat", "Egalité")
        elif (winning == 1):
            showinfo("Résultat", "Joueur 1 a gagné")
        elif (winning == 2):
            showinfo("Résultat", "Joueur 2 a gagné")

        switch_turn()
    
def draw_main_canvas(window, width, height):
    canvas = Canvas(window, width=width, height=height, bg="white")
    canvas.bind("<Button-1>", lambda event: on_left_click(canvas, event))
    canvas.pack(padx=5, pady=5)
    return canvas

def draw_separators(canvas, width, height, n):
    for k in range(1,n):
        canvas.create_line(0, k*width//n, height, k*width//n, fill="black", width=4)    
        canvas.create_line(k*height//n, 0, k*height//n, width, fill="black", width=4)
    
    return canvas

def create_quit_button(window):
    Button(window, text="Quitter", command=window.destroy).pack(side=LEFT, padx=5, pady=5)

    return window

def build_window(width, height):
    window= Tk()
    window.title("Morpion")


    canvas= draw_main_canvas(window, width, height)
    canvas=draw_separators(canvas, width, height, n)

    window = create_quit_button(window)
    return window

def draw_circle(canvas, i, j, n):
    global width
    global height
    x,y = get_central_positions(i,j,n)

    padding_x = width//(2*n) - (width//(2*n))*0.1
    padding_y = height//(2*n) - (height//(2*n))*0.1
    canvas.create_oval(x-padding_x, y-padding_y,x+padding_x, y+padding_y)


def draw_cross(canvas, i, j, n):
    global width
    global height
    x,y = get_central_positions(i,j,n)

    padding_x = width//(2*n) - (width//(2*n))*0.1
    padding_y = height//(2*n) - (height//(2*n))*0.1

    canvas.create_line(x-padding_x,y-padding_y,x+padding_x,y+padding_y)
    canvas.create_line(x+padding_x,y-padding_y,x-padding_x,y+padding_y)

def get_board_indexes(x,y,n):
    """ returns the i,j indexes in the board from the x,y positions
        for eg: x=75, y=150 => i=0, j=1 """
    global width
    global height

    if y < height//n:
        if x < width//n :
            return 0, 0
        for q in range(1, n-1):
            if x > q*(width//n) and x < (q+1)*(width//n):
                return 0, q
        if x > (n-1)*(width//n):
            return 0, n-1
        
    for k in range(1, n-1):
        if y > k*(height//n) and y < (k+1)*(height//n):
            if x < width//n:
                return k, 0
            for q in range(1, n-1):
                if x > q*(width//n) and x < (q+1)*(width//n):
                    return k, q
            if x > (n-1)*(width//n):
                return k, n-1
            
    if y > (n-1)*(height//n):
            if x < width//n:
                return n-1, 0
            for q in range(1, n-1):
                if x > q*(width//n) and x < (q+1)*(width//n):
                    return n-1, q
            if x > (n-1)*(width//n):
                return n-1, n-1

def get_central_positions(i, j, n):
    """Returns the x,y central position for a pair of i,j indexes 
    of the board"""
    global width
    global height

    for k in range(n):
        for q in range(n):
            if i == k:
                if j == q:
                    x = ((2*q)+1)*(width//(2*n))
                    y= ((2*k)+1)*(height//(2*n))
                    return x, y

def check_possible_move(board, i, j):
    """returns True if we can put a mark on board[i][j]
    """
    if board[i][j] == None:
        return True
    #else:
    #   return False

def switch_turn():
    """ Toggles the global 'player_turn' variable"""
    global player_turn
    if player_turn == 1:
        player_turn = 2
        return player_turn
    if player_turn == 2:
        player_turn = 1 
        return player_turn

def check_winning(board, n):
    """returns 
        .None if nothing happens
        .0 if the board is a draw
        .1 if the board is won by player 1
        .2 if the board is won by player 2
    """
    for k in range(n):
        board_sum1,board_sum2 = 0,0
        for q in range(n):
            if board[k][q] == 1 :
                board_sum1 += board[k][q]
                if board_sum1 == n:
                    return 1
            elif board[k][q] == 2 :
                board_sum2 += board[k][q]
                if board_sum2 == 2*n:
                    return 2

        
    for k in range(n):
        board_sum1,board_sum2 = 0,0
        for q in range(n):
            if board[q][k] == 1 :
                board_sum1 += board[q][k]
                if board_sum1 == n:
                    return 1
            elif board[q][k] == 2 :
                board_sum2 += board[q][k]
                if board_sum2 == 2*n:
                    return 2
        
    k=0
    board_sum1,board_sum2 = 0,0
    for q in range(n):
        if k == q:
            if board[k][q] == 1 :
                board_sum1 += board[k][q]
                if board_sum1== n:
                    return 1
            elif board[k][q] == 2 :
                board_sum2 += board[k][q]
                if board_sum2 == 2*n:
                    return 2
        k+=1    
        
    k = 0
    board_sum1,board_sum2 = 0,0
    for q in range(n-1, -1, -1 ):
        if board[k][q] == 1 :
            board_sum1 += board[k][q]
            if board_sum1 == n:
                return 1
        elif board[k][q] == 2 :
            board_sum2 += board[k][q]
            if board_sum2 == 2*n:
                return 2
        k+=1
    

# Main
#board represents the 3*3 grid we are playing with 
# we put 1 on the board for player 1 turn 2 for player 2
n = 3
board = [[None for _ in range(n)] for _ in range(n)]

#1 if it's player 1's turn
#2 if it's player 2's turn 
player_turn = 1
width, height = 600, 600
window = build_window(width, height)

window.mainloop()
