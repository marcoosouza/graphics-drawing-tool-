import tkinter as tk
from components.drawing_canvas import DrawingCanvas
from utils.get_image import get_image_path
from components.transform_window import TransformWindow


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Computer Graphics")
        self.resizable(width=False, height=False)

        self.canva = DrawingCanvas(self)
        self.canva.pack(side=tk.BOTTOM)
        self.type_draw = ''

        # BUTTONS

        self.clear_button_image = tk.PhotoImage(
            file=get_image_path("trash.png"))
        self.clear_button = tk.Button(
            self, image=self.clear_button_image, command=self.clear_canvas, width=30, height=30)
        self.clear_button.pack(side=tk.LEFT)

        self.line_button_state = tk.BooleanVar(value=False)
        self.line_button_image = tk.PhotoImage(file=get_image_path("line.png"))
        self.line_button = tk.Button(
            self, image=self.line_button_image, command=self.line_button_toggle, width=30, height=30)
        self.line_button.pack(side=tk.LEFT)

        self.circle_button_state = tk.BooleanVar(value=False)
        self.circle_button_image = tk.PhotoImage(
            file=get_image_path("circle.png"))
        self.circle_button = tk.Button(
            self, image=self.circle_button_image, command=self.circle_button_toggle, width=30, height=30)
        self.circle_button.pack(side=tk.LEFT)

        self.transform_button_image = tk.PhotoImage(
            file=get_image_path('trasnform.png'))
        self.transform_button = tk.Button(
            self, image=self.transform_button_image, command=self.open_trasnform_window, width=30, height=30)
        self.transform_button.pack(side=tk.LEFT)

        self.clipping_button_state = tk.BooleanVar(value=False)
        self.clipping_button_image = tk.PhotoImage(
            file=get_image_path('clipping.png'))
        self.clipping_button = tk.Button(
            self, image=self.clipping_button_image, command=self.clipping_button_toggle, width=30, height=30)
        self.clipping_button.pack(side=tk.LEFT)

        # BUTTONS END

        # MENU

        self.menu_bar = tk.Menu(self)

        self.algorithms_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.rasterization_menu = tk.Menu(self.algorithms_menu, tearoff=0)
        self.rasterization_algorithm = tk.StringVar(value="Bresenham")
        self.rasterization_algorithm.trace_add(
            "write", self.on_change_rasterization)
        self.rasterization_menu.add_radiobutton(
            label="Bresenham", variable=self.rasterization_algorithm, value="Bresenham")
        self.rasterization_menu.add_radiobutton(
            label="DDA", variable=self.rasterization_algorithm, value="DDA")

        self.algorithms_menu.add_cascade(
            label="Rasterização", menu=self.rasterization_menu)

        self.clipping_menu = tk.Menu(self.algorithms_menu, tearoff=0)
        self.clipping_algorithm = tk.StringVar(value="Cohen-Sutherland")
        self.clipping_algorithm.trace_add("write", self.on_change_clipping)
        self.clipping_menu.add_radiobutton(
            label="Cohen-Sutherland", variable=self.clipping_algorithm, value="Cohen-Sutherland")
        self.clipping_menu.add_radiobutton(
            label="Liang-Barsky", variable=self.clipping_algorithm, value="Liang-Barsky")

        self.algorithms_menu.add_cascade(
            label="Recorte", menu=self.clipping_menu)

        self.menu_bar.add_cascade(
            label="Algoritmos", menu=self.algorithms_menu)

        self.config(menu=self.menu_bar)

        # MENU END

    def clear_canvas(self):
        self.canva.clear_canvas()

    def on_change_rasterization(self, *args):
        type_draw = ''
        if self.line_button_state.get():
            type_draw = 'Line'
        elif self.circle_button_state.get():
            type_draw = 'Circle'
        self.canva.set_rasterization_function(
            self.rasterization_algorithm.get(), type_draw)

    def on_change_clipping(self, *args):
        self.canva.set_clipping_function(self.clipping_algorithm.get())

    def line_button_toggle(self):
        if self.clipping_button_state.get():
            self.clipping_button_toggle()
        self.toggle_draw_mode('Line')

    def circle_button_toggle(self):
        if self.clipping_button_state.get():
            self.clipping_button_toggle()
        self.toggle_draw_mode('Circle')

    def clipping_button_toggle(self):
        if self.line_button_state.get():
            self.toggle_draw_mode('Line')
        if self.circle_button_state.get():
            self.toggle_draw_mode('Circle')

        self.clipping_button_state.set(not self.clipping_button_state.get())
        if self.clipping_button_state.get():
            self.clipping_button.config(background='gray')

            self.canva.bind("<ButtonPress-1>", self.canva.get_start_selection)
            self.canva.bind("<B1-Motion>", self.canva.update_selection)
            self.canva.bind("<ButtonRelease-1>", self.canva.end_selection)
        else:
            self.clipping_button.config(background='#d9d9d9')
            self.canva.delete("selection")
            self.canva.unbind("<ButtonPress-1>")
            self.canva.unbind("<B1-Motion>")
            self.canva.unbind("<ButtonRelease-1>")

    def toggle_draw_mode(self, draw_mode):
        if draw_mode == 'Line':
            button_to_toggle = self.line_button
            draw_function = self.canva.drag_line
            self.canva.set_draw_mode(draw_mode)
            rasterization_function = self.canva.line_bresenham_algorithm
        elif draw_mode == 'Circle':
            button_to_toggle = self.circle_button
            draw_function = self.canva.drag_circle
            self.canva.set_draw_mode(draw_mode)
            rasterization_function = self.canva.circle_bresenham_algorithm

        button_state_var = self.line_button_state if draw_mode == 'Line' else self.circle_button_state

        if button_state_var.get():
            button_state_var.set(False)
            if draw_mode == 'Line':
                self.line_button.config(background='#d9d9d9')
            if draw_mode == 'Circle':
                self.circle_button.config(background='#d9d9d9')

            self.canva.unbind("<ButtonPress-1>")
            self.canva.unbind("<B1-Motion>")
            self.canva.unbind("<ButtonRelease-1>")
            return

        else:
            for button, state_var in [(self.line_button, self.line_button_state), (self.circle_button, self.circle_button_state)]:
                if button != button_to_toggle:
                    state_var.set(False)
                    button.config(background='#d9d9d9')
                else:
                    state_var.set(True)
                    button.config(background='gray')

            self.canva.bind("<ButtonPress-1>",
                            self.canva.get_start_coordinates)
            self.canva.bind("<B1-Motion>", draw_function)
            self.canva.bind("<ButtonRelease-1>",
                            self.canva.get_end_coordinates)
            self.canva.set_rasterization_function("Bresenham", draw_mode)
            self.canva.rasterization_function = rasterization_function

    def open_trasnform_window(self):
        transform_window = TransformWindow(self, self.perform_transformation)

    def perform_transformation(self, trasnformations):

        for item in trasnformations:
            if item[0] == 'Translation':
                self.canva.translate_vector(float(item[1]), float(item[2]))
            if item[0] == 'Scale':
                self.canva.scale_vector(float(item[1]), float(item[2]))
            if item[0] == 'Rotation':
                self.canva.rotate_vector(int(item[1]))
            if item[0] == 'Reflection':
                self.canva.reflect_vector(item[1])
