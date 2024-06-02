from tkinter import *
from tkinter.colorchooser import askcolor
import time

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        self.brush_size = 1
        self.brush_color = "black"
        self.gradient_color = "white"
        self.brush_mode = "solid"
        self.last_x, self.last_y = None, None
        self.x1, self.y1 = None, None
        self.actions = []
        self.redo_stack = []

        self.canvas = Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.paint_start)
        self.canvas.bind("<B1-Motion>", self.paint)

        button_frame = Frame(self.root)
        button_frame.pack(fill=X)

        button_brush_color = Button(button_frame, text="Change Brush Color", command=self.change_brush_color)
        button_brush_color.pack(side=LEFT)

        button_bg_color = Button(button_frame, text="Change Background Color", command=lambda: self.change_bg_color(self.canvas))
        button_bg_color.pack(side=LEFT)

        brush_size_slider = Scale(button_frame, from_=1, to=20, orient=HORIZONTAL, label="Brush Size", command=self.change_brush_size)
        brush_size_slider.set(self.brush_size)
        brush_size_slider.pack(side=LEFT)

        button_solid = Button(button_frame, text="Solid Brush", command=lambda: self.set_brush_mode("solid"))
        button_solid.pack(side=LEFT)

        button_dotted = Button(button_frame, text="Dotted Brush", command=lambda: self.set_brush_mode("dotted"))
        button_dotted.pack(side=LEFT)

        button_gradient_color = Button(button_frame, text="Change Gradient Color", command=self.change_gradient_color)
        button_gradient_color.pack(side=LEFT)

        button_undo = Button(button_frame, text="Undo", command=self.undo)
        button_undo.pack(side=LEFT)

        button_redo = Button(button_frame, text="Redo", command=self.redo)
        button_redo.pack(side=LEFT)

    def change_brush_size(self, new_size):
        self.brush_size = int(new_size)

    def change_bg_color(self, canvas):
        bg_color = askcolor()
        if bg_color[1]:
            canvas.config(bg=bg_color[1])

    def change_brush_color(self):
        color = askcolor()[1]
        if color:
            self.brush_color = color

    def set_brush_mode(self, mode):
        self.brush_mode = mode
        if self.brush_mode == "solid":
            self.canvas.bind("<B1-Motion>", self.paint)
        elif self.brush_mode == "dotted":
            self.canvas.bind("<B1-Motion>", self.dotted_paint)
        elif self.brush_mode == "gradient":
            self.canvas.bind("<B1-Motion>", self.gradient_paint)

    def paint_start(self, event):
        self.x1, self.y1 = event.x, event.y

    def paint(self, event):
        self.x2, self.y2 = event.x, event.y
        line = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.brush_color, width=self.brush_size)
        self.actions.append(line)
        self.x1, self.y1 = self.x2, self.y2

    def dotted_paint(self, event):
        spacing = 10
        if self.last_x is not None and self.last_y is not None:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance >= spacing:
                oval = self.canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, fill="black", outline="black")
                self.actions.append(oval)
                self.last_x, self.last_y = event.x, event.y
        else:
            self.last_x, self.last_y = event.x, event.y

    def change_gradient_color(self):
        color = askcolor()[1]
        if color:
            self.gradient_color = color

    def gradient_paint(self, event):
        x2, y2 = event.x, event.y
        line_length = ((x2 - self.x1) ** 2 + (y2 - self.y1) ** 2) ** 0.5
        steps = int(line_length)
        if steps == 0:
            steps = 1
        r1, g1, b1 = self.canvas.winfo_rgb(self.brush_color)
        r2, g2, b2 = self.canvas.winfo_rgb(self.gradient_color)
        r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
        r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256
        for i in range(steps):
            r = r1 + (r2 - r1) * i // steps
            g = g1 + (g2 - g1) * i // steps
            b = b1 + (b2 - b1) * i // steps
            color = f'#{r:02x}{g:02x}{b:02x}'
            line = self.canvas.create_line(self.x1 + (x2 - self.x1) * i // steps, self.y1 + (y2 - self.y1) * i // steps,
                                           self.x1 + (x2 - self.x1) * (i + 1) // steps, self.y1 + (y2 - self.y1) * (i + 1) // steps,
                                           fill=color, width=self.brush_size)
            self.actions.append(line)
        self.x1, self.y1 = x2, y2

    def undo(self):
        if self.actions:
            last_action = self.actions.pop()
            self.redo_stack.append(last_action)
            self.canvas.delete(last_action)

    def redo(self):
        if self.redo_stack:
            last_action = self.redo_stack.pop()
            self.actions.append(last_action)
            self.canvas.addtag_all(last_action)

if __name__ == "__main__":
    root = Tk()
    app = PaintApp(root)
    root.mainloop()
