import tkinter as tk
from tkinter import ttk
import random as rd
import time

def shortest_finder(start,end):
    path=[]
    row1,col1=start
    row2,col2=end
    visit=[[False for _ in range(40)]for _ in range(40)]
    q=[]
    q.append(start)
    parent={}
   
       
    while q[0]!=end :
         row1,col1=q.pop(0)
         direction=[] 
         if not walls[row1][col1]["t"]:
            row=row1-1 if row1>0 else 0
            col=col1
            if not visit[row][col]:
                visit[row][col]=True
                q.append((row,col))
                parent[(row,col)]=row1,col1
                canvas.update()
                time.sleep(0.01)
                draw_cell(row,col,"red")
            
         if not walls[row1][col1]["b"]:
            row=1+row1 if row1 <39 else 40
            col=col1
            if not visit[row][col]:
                visit[row][col]=True
                q.append((row,col))
                parent[(row,col)]=row1,col1
                canvas.update()
                time.sleep(0.01)
                draw_cell(row,col,"red")
                
         if not walls[row1][col1]["l"]:
            col=col1-1 if col1 >0 else 0
            row=row1
            if not visit[row][col]:
                visit[row][col]=True
                q.append((row,col))
                parent[(row,col)]=row1,col1
                canvas.update()
                time.sleep(0.01)
                draw_cell(row,col,"red")
            
       
         if not walls[row1][col1]["r"]:
            col=1+col1 if col1 < 39 else 40
            row=row1
            if not visit[row][col]:
                visit[row][col]=True
                q.append((row,col))
                parent[(row,col)]=row1,col1
                canvas.update()
                time.sleep(0.01)
                draw_cell(row,col,"red")
            
    # Once end is reached, reconstruct path
    r, c = end
    while (r, c) != start:
        path.append((r, c))
        r, c = parent[(r, c)]
    path.append(start)
    path.reverse()
    
    return path
    
def draw_cell(r, c,color):
    x, y = 40 + c * 20, 40 + r * 20
    x1, y1, x2, y2 = x, y, x + 20, y + 20

    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    if walls[r][c]['t']:
        canvas.create_line(x1, y1, x1 + 20, y1, fill='white')
    if walls[r][c]['b']:
        canvas.create_line(x1, y1 + 20, x1 + 20, y1 + 20, fill='white')
    if walls[r][c]['l']:
        canvas.create_line(x1, y1, x1, y1 + 20, fill='white')
    if walls[r][c]['r']:
        canvas.create_line(x1 + 20, y1, x1 + 20, y1 + 20, fill='white')

def cube_generator(row,col,d):
    p_row,p_col=row,col
    if d == 't' and row >0:  # go up
        walls[row][col]['t'] = False
        walls[row-1][col]['b'] = False
        row -= 1
    elif d == 'b' and row<39:  # go down
        walls[row][col]['b'] = False
        walls[row+1][col]['t'] = False
        row += 1
    elif d == 'l' and col>0:  # go left
        walls[row][col]['l'] = False
        walls[row][col-1]['r'] = False
        col -= 1
    elif d == 'r' and col<39:  # go right
        walls[row][col]['r'] = False
        walls[row][col+1]['l'] = False
        col += 1
        
    visited[row][col]=True
    
    draw_cell(p_row,p_col,"green")
    draw_cell(row,col,"green")

     
    return row,col
    
def create_canvas():
    global canvas
    canvas=tk.Canvas(root,width=880,height=880)
    canvas.pack(pady=40,padx=40)
    
    canvas.create_rectangle(40,40,840,840,fill='black')
        
    for i in range(41):
        x = 40 + i * 20
        canvas.create_line(x, 40, x, 840, fill='white', width=2)
        canvas.create_line(40, x, 840, x, fill='white', width=2)
        
    button=tk.Button(text="Refresh",font=('arial',20),command=refresh)
    button.pack(padx=20,pady=20)

def main(start,end):
        global row,col
        directions = []
        if row > 0 and not visited[row-1][col]:
            directions.append('t')
        if row < 39 and not visited[row+1][col]:
            directions.append('b')
        if col > 0 and not visited[row][col-1]:
            directions.append('l')
        if col < 39 and not visited[row][col+1]:
            directions.append('r')
    
        if not directions:
            if  not path:
                path.extend(shortest_finder(start,end))
                for row,col in path:
                    draw_cell(row,col,"blue")
                return
            row,col=path.pop()
        else:
            d = rd.choice(directions)
            
            path.append((row,col))
            row,col=cube_generator(row, col, d)
        
        canvas.update()
        root.after(50,lambda:main(start,end))
        
# --- Start Button ---
def mysterious_function(start,end):
    
    for child in root.winfo_children():
        child.destroy()
    
    create_canvas()
    main(start,end)

def refresh():
        for child in root.winfo_children():
            child.destroy()
        
        start()
        
        
def start():
    # Fullscreen approach (good for mobile)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg="#e9eef6")
    
    lst_value = list(range(40))  # values for maze
    
    def only_numbers(P):
        return P.isdigit() and 0 <= int(P) < 40 if P else True
    
    vcmd = (root.register(only_numbers), '%P')
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TCombobox",
                    fieldbackground="#ffffff",
                    background="#dddddd",
                    font=("Arial", 12))
    
    # --- Title ---
    title_label = tk.Label(root,
                           text="Shortest Distance Finder \nIn a Randomized Maze",
                           font=("Helvetica", 20, "bold"),
                           bg="#e9eef6", fg="#1a1a1a", justify='center')
    title_label.pack(pady=20)
    
    # --- Input Section ---
    def create_input_section(label_text, combo1, combo2):
        frame = tk.Frame(root, bg="#e9eef6")
        frame.pack(pady=10, fill='x', padx=30)
    
        label = tk.Label(frame, text=label_text, font=('Arial', 14, 'bold'), bg="#e9eef6")
        label.pack(anchor='w')
    
        combo_frame = tk.Frame(frame, bg="#e9eef6")
        combo_frame.pack(pady=5)
    
        combo1.config(validate='key', validatecommand=vcmd, width=5)
        combo1.pack(side='left', padx=10)
        combo2.config(validate='key', validatecommand=vcmd, width=5)
        combo2.pack(side='left', padx=10)
    
    # Start
    start_row = ttk.Combobox(root, values=lst_value)
    start_row.current(0)
    start_col = ttk.Combobox(root, values=lst_value)
    start_col.current(0)
    create_input_section("Start Position (row, column):", start_row, start_col)
    
    # End
    end_row = ttk.Combobox(root, values=lst_value)
    end_row.set(39)
    end_col = ttk.Combobox(root, values=lst_value)
    end_col.set(39)
    create_input_section("End Position (row, column):", end_row, end_col)
    
    
    start_btn = tk.Button(root,
                          text="✨ Start Search ✨",
                          font=("Arial", 14, "bold"),
                          bg="#4caf50", fg="white",
                          activebackground="#45a049",
                          relief=tk.RAISED, bd=3,
                          padx=20, pady=10,
                          command=lambda:mysterious_function((int(start_row.get()),int(start_col.get())),(int(end_row.get()),int(end_col.get()))))
    start_btn.pack(pady=30)
        
      
            
walls = [[{'t': True, 'b': True, 'l': True, 'r': True} for _ in range(40)] for _ in range(40)]

visited = [[False for _ in range(40)] for _ in range(40)]
        
row, col = 20,20
visited[row][col]=True
path=[]
lst_value=[i for i in range(41)]


root = tk.Tk()
root.title("Shortest Distance Finder")

if __name__=='__main__':
    start()

root.mainloop()
