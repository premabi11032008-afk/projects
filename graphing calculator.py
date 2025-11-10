import tkinter as tk
from tkinter import font, messagebox
import os
import ast
import matplotlib.pyplot as mp
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

results_dict = {}
figure = mp.Figure()
ax = figure.add_subplot(1, 1, 1)
stored_functions=[]

if not os.path.exists("storage.txt"):
    with open("storage.txt", "w") as file:
        pass

with open("storage.txt") as file:
    content=file.read()

if content:
    while "[" in content and "]" in content:
        start, end = content.find("["), content.find("]")
        func_code = content[start+1:end]
        exec(func_code, globals())  # adds function to globals

        # Safely get function name
        tree = ast.parse(func_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                stored_functions.append(node.name)

        content = content[end+1:]


window = tk.Tk()
window.title("Graph Calculator & Custom Function Creator")
window.geometry("700x600")
window.config(bg="#f0f0f5")

title_font = font.Font(family="Helvetica", size=20, weight="bold")
label_font = font.Font(family="Comic Sans MS", size=12)
button_font = font.Font(family="Helvetica", size=12, weight="bold")


def return_to_main():
    for widget in window.winfo_children():
      widget.destroy()
    main()

def create_function():
    function_name = entry_function_name.get().strip()
    variable_name = entry_variable_name.get().strip()
    function_body = text_function_body.get("1.0", tk.END).strip()
    if not function_name or not variable_name or not function_body:
        result_label.config(text="All fields must be filled!", fg="red")
        return
    
    full_function = f"def {function_name}({variable_name}):\n"
    for line in function_body.splitlines():
        full_function += f"    {line}\n"

    try:
        tree = ast.parse(full_function)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
              if node.func.id in ['open', 'exec', 'eval']:
                 raise ValueError("Function contains restricted operations.")
              
        exec(full_function, globals())
        result_label.config(text=f"Function '{function_name}' created successfully!", fg="green")

        # Create Store button  
        store_button = tk.Button(text=f"Store {function_name} Results", command=lambda: store_results(function_name), bg="#4CAF50", fg="white", font=button_font)  
        store_button.pack(pady=10)  
            
            # Prompt to store function permanently  
        save_function = messagebox.askyesno("Store Permanently?", f"Do you want to store '{function_name}' permanently?")  
        if save_function:  
            with open("storage.txt", "a") as file:  
                file.write("["+full_function + "]\n")  

    except SyntaxError as e:  
        result_label.config(text=f"Syntax Error: {e}", fg="red")  
    except ValueError as e:  
        result_label.config(text=f"Error: {e}", fg="red")  
    except Exception as e:  
        result_label.config(text=f"Error: {str(e)}", fg="red")

def store_results(function_name):
    try:
        x_values = list(range(-10, 11))
        user_function = globals().get(function_name)
        if user_function:
            results = {x: user_function(x) for x in x_values}
            results_dict[function_name] = results
            result_label.config(text=f"Results stored for '{function_name}'!", fg="blue")
            return_to_main()
        else:
            result_label.config(text="Function not found.", fg="red")
    except Exception as e:
        result_label.config(text=f"Error in function execution: {str(e)}", fg="red")

def view_stored_functions():
    slide_frame = tk.Frame(window, width=200, bg="#e6e6fa", padx=10, pady=10, relief="groove", bd=3)
    slide_frame.place(x=window.winfo_width(), y=0, height=window.winfo_height())

    def slide(step=20):
        x = slide_frame.winfo_x()
        target_x = window.winfo_width() - 200
        if x > target_x:
            slide_frame.place(x=max(x - step, target_x), y=0)
            window.after(10, slide)
        else:
            slide_frame.place(x=target_x, y=0)

    slide()
    tk.Label(slide_frame, text="Stored Functions:", font=label_font, bg="#e6e6fa").pack(pady=10)

    for function in stored_functions:
        button = tk.Button(slide_frame, text=function+"(x)", command=lambda f=function: fill_function(f), bg="#4CAF50", fg="white", font=button_font)
        button.pack(pady=5)

    return_button = tk.Button(slide_frame, text="Close", command=slide_frame.destroy, bg="#FF9800", fg="white", font=button_font)
    return_button.pack(pady=10)

def fill_function(function_name):
    if function_name.split("(x")[0] in globals():
        def delayed_fill():
            entry_graph.delete(0, tk.END)
            entry_graph.insert(0, function_name+"(x)")
            on_graph()
        return_to_main()
        window.after(50, delayed_fill)  # small delay ensures main() finishes


    else:
        result_label1.config(text=f"Function '{function_name}' not defined.", fg="red")

def on_graph():
    function_name = entry_graph.get().strip()

    if not function_name:
        result_label1.config(text="Function name cannot be empty!", fg="red")
        return
    try:
        x_min = int(entry_x_min.get())
        x_max = int(entry_x_max.get())
        y_min = int(entry_y_min.get())
        y_max = int(entry_y_max.get())
        graph(function_name, x_range=(x_min, x_max), y_range=(y_min, y_max))
    except ValueError:
        result_label1.config(text="Please enter valid numerical ranges.", fg="red")

def graph(entry_list, x_range=(-100, 100), y_range=(-100, 100)):
    global canvas
    values = []


    e1 = entry_list.replace("x", "(x)")
    x_values=np.linspace(x_range[0],x_range[1],400)

    for i in x_values:
        try:
            result = eval(e1.replace("x",str(i)))
            if y_range[0] <= result <= y_range[1]:
                values.append((i, result))
        except:
            continue

    plot_graph(values, entry_graph.get())
    canvas.draw()

def plot_graph(values, function_name):
    ax.clear()
    if values:
        x_value, y_value = zip(*values)
        ax.axhline(y=0, color="black")
        ax.axvline(x=0, color="black")
        ax.plot(x_value, y_value, label=function_name, color="#2196F3")
        ax.set_xlim(min(x_value), max(x_value))
        ax.set_ylim(min(y_value), max(y_value))
        ax.legend()
        ax.set_title(f"Graph of {function_name}", fontsize=14)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")

def create_custom_function_window():
    for widget in window.winfo_children():
        widget.destroy()

    global entry_function_name, entry_variable_name, text_function_body, result_label

    title_label = tk.Label(window, text="Custom Function Creator",
                           font=title_font, bg="#f0f0f5", fg="#333399")
    title_label.pack(pady=20)

    frame = tk.Frame(window, bg="#e6e6fa", padx=20, pady=20, relief="groove", bd=3)
    frame.pack(pady=20)

    tk.Label(frame, text="Enter Function Name:", font=label_font, bg="#e6e6fa").pack(anchor="w", pady=5)
    entry_function_name = tk.Entry(frame, width=30, font=label_font)
    entry_function_name.pack(pady=5)

    tk.Label(frame, text="Enter Variable Name:", font=label_font, bg="#e6e6fa").pack(anchor="w", pady=5)
    entry_variable_name = tk.Entry(frame, width=30, font=label_font)
    entry_variable_name.pack(pady=5)

    tk.Label(frame, text="Enter Function Body (Python code):", font=label_font, bg="#e6e6fa").pack(anchor="w", pady=5)
    text_function_body = tk.Text(frame, height=10, width=50, relief="sunken", bd=2, font=label_font)
    text_function_body.pack(pady=10)

    button_create_function = tk.Button(frame, text="Create Function", command=create_function,
                                       bg="#4CAF50", fg="white", font=button_font, relief="raised", bd=3)
    button_create_function.pack(pady=10)

    result_label = tk.Label(window, text="", font=label_font, bg="#f0f0f5", fg="red")
    result_label.pack(pady=5)

    button_return = tk.Button(window, text="Return", command=return_to_main,
                              bg="#FF9800", fg="white", font=button_font, relief="raised", bd=3)
    button_return.pack(pady=10)


def main():
    for widget in window.winfo_children():
        widget.destroy()

    global entry_graph, entry_x_min, entry_x_max, entry_y_min, entry_y_max, canvas, result_label1

    title_label = tk.Label(window, text="Graph Calculator & Custom Function Creator",
                           font=title_font, bg="#f0f0f5", fg="#333399")
    title_label.pack(pady=20)

    input_frame = tk.Frame(window, bg="#e6e6fa", padx=20, pady=20, relief="groove", bd=3)  
    input_frame.pack(pady=20)  

    tk.Label(input_frame, text="Enter function name:", font=label_font, bg="#e6e6fa").grid(row=0, column=0, sticky="w", pady=5)  
    entry_graph = tk.Entry(input_frame, width=20, font=label_font)  
    entry_graph.grid(row=0, column=1, pady=5)  

    tk.Label(input_frame, text="X Min:", font=label_font, bg="#e6e6fa").grid(row=1, column=0, sticky="w", pady=5)  
    entry_x_min = tk.Entry(input_frame, width=10, font=label_font)  
    entry_x_min.grid(row=1, column=1, sticky="w", pady=5)  
    entry_x_min.insert(0, "-10")  

    tk.Label(input_frame, text="X Max:", font=label_font, bg="#e6e6fa").grid(row=1, column=2, sticky="w", pady=5)  
    entry_x_max = tk.Entry(input_frame, width=10, font=label_font)  
    entry_x_max.grid(row=1, column=3, sticky="w", pady=5)  
    entry_x_max.insert(0, "10")  

    tk.Label(input_frame, text="Y Min:", font=label_font, bg="#e6e6fa").grid(row=2, column=0, sticky="w", pady=5)  
    entry_y_min = tk.Entry(input_frame, width=10, font=label_font)  
    entry_y_min.grid(row=2, column=1, sticky="w", pady=5)  
    entry_y_min.insert(0, "-10")  

    tk.Label(input_frame, text="Y Max:", font=label_font, bg="#e6e6fa").grid(row=2, column=2, sticky="w", pady=5)  
    entry_y_max = tk.Entry(input_frame, width=10, font=label_font)  
    entry_y_max.grid(row=2, column=3, sticky="w", pady=5)  
    entry_y_max.insert(0, "10")

    frame = tk.Frame(window)
    frame.pack(pady=10)

    button_graph = tk.Button(frame, text="Plot Graph", command=on_graph,
                             bg="#4CAF50", fg="white", font=button_font, relief="raised", bd=3)
    button_graph.pack(side="left", padx=10)

    button_create_function = tk.Button(frame, text="Create Custom Function",
                                       command=create_custom_function_window, bg="#2196F3",
                                       fg="white", font=button_font, relief="raised", bd=3)
    button_create_function.pack(side="left", padx=10)

    button_view_stored = tk.Button(frame, text="View Stored Functions", command=view_stored_functions,
                                   bg="#FF9800", fg="white", font=button_font, relief="raised", bd=3)
    button_view_stored.pack(side="left", padx=10)

    result_label1 = tk.Label(window, text="", font=label_font, bg="#f0f0f5", fg="red")
    result_label1.pack(pady=5)

    canvas_frame = tk.Frame(window, bg="#f0f0f5")
    canvas_frame.pack(fill="both", expand=True)

    canvas = FigureCanvasTkAgg(figure, master=canvas_frame)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, canvas_frame)
    toolbar.update()
    toolbar.pack(fill="x", side="bottom")

    canvas.get_tk_widget().pack(fill="both", expand=True)





main()
window.mainloop()