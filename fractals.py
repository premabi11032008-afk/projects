import tkinter as tk
import random
import time

def sub_triangles(corners,lvl):
    a,b,c=corners
    mid_ab,mid_bc,mid_ac=(((a[0]+b[0])//2,(a[1]+b[1])//2),((c[0]+b[0])//2,(c[1]+b[1])//2),
    ((a[0]+c[0])//2,(a[1]+c[1])//2))
    
    return [[mid_bc,mid_ab,mid_ac],
    []]
    

def create_triangle(corners,iteration):
    global corner,iterations    
    v,u=random.random(),random.random()
    if v+u>1:
        u,v=1-u,1-v
        
    starting_point=(corners[0][0]+(v*(corners[1][0]-corners[0][0]))+(u*(corners[2][0]-corners[0][0])),
    corners[0][1]+(v*(corners[1][1]-corners[0][1]))+(u*(corners[2][1]-corners[0][1])))
    
    delay=1
    start=find_nxt(starting_point,corners,delay)
    for _ in range(iteration):
            if _ ==3:
                delay=0.000001
            start=find_nxt(start,corners,delay)
    else:
            mid_ab=((corners[0][0]+corners[1][0])//2,(corners[0][1]+corners[1][1])//2)
            mid_ac=((corners[0][0]+corners[2][0])//2,(corners[0][1]+corners[2][1])//2)
            mid_bc=((corners[2][0]+corners[1][0])//2,(corners[2][1]+corners[1][1])//2)
            corner.append((([mid_ab,mid_bc,mid_ac]),lvl+1))
            corner.append(([((corners[0][0]+mid_ab[0])//2,(corners[0][1]+mid_ab[1])//2),
            ((corners[0][0]+mid_ac[0])//2,(corners[0][1]+mid_ac[1])//2),
            ((mid_ac[0]+mid_ab[0])//2,(mid_ac[1]+mid_ab[1])//2)],lvl+2))
            corner.append(([((corners[1][0]+mid_ab[0])//2,(corners[1][1]+mid_ab[1])//2),
            ((corners[1][0]+mid_bc[0])//2,(corners[1][1]+mid_bc[1])//2),
            ((mid_bc[0]+mid_ab[0])//2,(mid_bc[1]+mid_ab[1])//2)],lvl+2))
            corner.append(([((corners[2][0]+mid_bc[0])//2,(corners[2][1]+mid_bc[1])//2),
            ((corners[2][0]+mid_ac[0])//2,(corners[2][1]+mid_ac[1])//2),
            ((mid_ac[0]+mid_bc[0])//2,(mid_ac[1]+mid_bc[1])//2)],lvl+2))
            
                                                
def find_nxt(start,corners,delay):
    random_corner=random.choice(corners)
    mid=(random_corner[0]+start[0])//2,(random_corner[1]+start[1])//2
    
    r=2
    
    canvas.create_oval(mid[0]-r,mid[1]-r,mid[0]+r,mid[1]+r,fill='black')
    canvas.update()
    
    time.sleep(delay)
    return mid
    

root=tk.Tk()
root.config(bg="grey")
iterations=6000
lvl=0

canvas=tk.Canvas(width=800,height=800,)
canvas.pack(pady=200)

root.update_idletasks()

corner=[([(canvas.winfo_width()//2,15),
(0,canvas.winfo_height()-30),
(canvas.winfo_width(),canvas.winfo_height()-30)],lvl)]

for _ in corner:
    for point in range(len(_[0])):
        canvas.create_line(_[0][point],_[0][point+1 if point+1!=len(_[0]) else 0],width=3)

for tri,lvl in corner:
    create_triangle(tri,(iterations//(2**lvl)))
           
root.mainloop()