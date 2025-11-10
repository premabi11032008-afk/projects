from PIL import Image
import tkinter as tk
import time

def shortest_finder(start,end):
    path=[]
    row1,col1=start
    row2,col2=end
    visit=[[False for _ in range(column)]for _ in range(rows)]
    visit[row1][col1]=True
    q=[]
    q.append(start)
    parent={}
   
       
    while q[0]!=end :
         row1,col1=q.pop(0)
         print(row1,col1)
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
            row=1+row1 if row1 <rows-2 else rows-1
            col=col1
            if not visit[row][col]:
                visit[row][col]=True
                q.append((row,col))
                parent[(row,col)]=row1,col1
                canvas.update()
                time.sleep(0.1)
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
            col=1+col1 if col1 < column-2 else column-1
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

def is_wall(x, y, spread, direction):
    black_count = 0
    total = 0
    threshold = 150

    for offset in range(-spread, spread + 1):
        for band in range(-10, 8):  
            if direction == 'x':  
                temp_x = max(0, min(x + offset, img_width - 1))
                temp_y = max(0, min(y + band, img_height - 1))
            else: 
                temp_x = max(0, min(x + band, img_width - 1))
                temp_y = max(0, min(y + offset, img_height - 1))

            pixel = gray_scale.getpixel((temp_x, temp_y))
            if pixel < threshold:
                black_count += 1
            total += 1

    wall_ratio = black_count / total 
    return wall_ratio > 0.593

def check_walls(x1, y1, x2, y2, grid_y, grid_x):
    spread = max(2, min((y2 - y1), (x2 - x1)) // 8)

    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    
    top_y = max(0, min(y1 + 1, img_height - 1))
    walls[grid_y][grid_x]['Top'] = is_wall(mid_x, top_y, spread, 'x')
    
    bottom_y = min(y2 - 1, img_height - 1)
    walls[grid_y][grid_x]['Bottom'] = is_wall(mid_x, bottom_y, spread, 'x')

    if grid_x == 0:
        walls[grid_y][grid_x]['Left'] = True
    else:
        left_x = max(0, min(x1 + 2, img_width - 1))
        walls[grid_y][grid_x]['Left'] = is_wall(left_x, mid_y, spread, 'y')

    if grid_x == column - 1:
        walls[grid_y][grid_x]['Right'] = True
    else:
        right_x = max(0, min(x2 - 2, img_width - 1))
        walls[grid_y][grid_x]['Right'] = is_wall(right_x, mid_y, spread, 'y')


img = Image.open("maze4.jpg")
gray_scale = img.convert("L")
img_height = gray_scale.height
img_width = gray_scale.width
rows, column = 10,10

row_bounds = [round(i * img_height / rows) for i in range(rows + 1)]
col_bounds = [round(i * img_width / column) for i in range(column + 1)]


walls = [[{'Top': None, 'Bottom': None, "Right": None, 'Left': None} 
          for _ in range(column)] for _ in range(rows)]

print(f"Image dimensions: {img_width}x{img_height}")


for i in range(rows):
    for j in range(column):
        if i==8:
            print(x1,x2,y1,y2)
        x1, x2 = col_bounds[j], col_bounds[j + 1]
        y1, y2 = row_bounds[i], row_bounds[i + 1]
        check_walls(x1, y1, x2, y2, i, j)

for i in range(rows):
    for j in range(column):
        cell = walls[i][j]
        walls[i][j] = {
            't': cell['Top'],
            'b': cell['Bottom'],
            'l': cell['Left'],
            'r': cell['Right']
        }

root = tk.Tk()
root.title("Maze Wall Detection")

canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='black')
canvas.pack()

for i in range(rows):
    for j in range(column):
        draw_cell(i, j, 'green')

path=shortest_finder((0,0),(rows-1,column-1))

for row,col in path:
                    draw_cell(row,col,"blue")

root.mainloop()