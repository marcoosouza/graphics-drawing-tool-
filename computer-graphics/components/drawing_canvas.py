import math
import tkinter as tk


class DrawingCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white", width=750, height=750)

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.draws = []
        self.rasterization_function = None
        self.clipping_function = self.cohen_sutherland_algorithm

        self.draw_axes()

    def draw_axes(self):
        canvas_width = 750
        canvas_height = 750

        self.create_line(0, canvas_height / 2, canvas_width,
                         canvas_height / 2, fill="blue", width=2)

        self.create_line(canvas_width / 2, 0, canvas_width /
                         2, canvas_height, fill="blue", width=2)

    def get_start_coordinates(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def drag_line(self, event):
        if self.start_x is not None and self.start_y is not None:
            if self.end_x is not None and self.end_y is not None:
                self.redraw()
            self.end_x = event.x
            self.end_y = event.y
            self.create_line(self.start_x, self.start_y,
                             self.end_x, self.end_y, fill="red", tags="line")

    def drag_circle(self, event):
        if self.start_x is not None and self.start_y is not None:
            if self.end_x is not None and self.end_y is not None:
                self.redraw()
            self.end_x = event.x
            self.end_y = event.y
            radius = max(abs(self.end_x - self.start_x),
                         abs(self.end_y - self.start_y))
            self.circle_bresenham_algorithm(self.start_x, self.start_y, radius)

    def get_end_coordinates(self, event):
        self.end_x = event.x
        self.end_y = event.y

        if self.start_x is not None and self.start_y is not None:
            if self.rasterization_function == self.line_bresenham_algorithm or \
                    self.rasterization_function == self.dda_algorithm:
                self.draws.append(
                    (self.start_x, self.start_y, self.end_x, self.end_y))
            elif self.rasterization_function == self.circle_bresenham_algorithm:
                radius = max(abs(self.end_x - self.start_x),
                             abs(self.end_y - self.start_y))

                center_x = self.start_x
                center_y = self.start_y
                self.draws.append((center_x, center_y, radius))

            self.redraw()

    def get_start_selection(self, event):
        self.selection_start_x = event.x
        self.selection_start_y = event.y
        self.selection_rectangle = self.create_rectangle(
            self.selection_start_x, self.selection_start_y, self.selection_start_x, self.selection_start_y, outline="red", tags="selection")

    def update_selection(self, event):
        self.delete("selection")
        self.selection_end_x = event.x
        self.selection_end_y = event.y
        self.selection_rectangle = self.create_rectangle(
            self.selection_start_x, self.selection_start_y, self.selection_end_x, self.selection_end_y, outline="red", tags="selection")

    def end_selection(self, event):
        self.delete("selection")
        self.selection_end_x = event.x
        self.selection_end_y = event.y
        self.selection_rectangle = self.create_rectangle(
            self.selection_start_x, self.selection_start_y, self.selection_end_x, self.selection_end_y, outline="red", tags="selection")

        self.clip_x_min = min(self.selection_start_x, self.selection_end_x)
        self.clip_x_max = max(self.selection_start_x, self.selection_end_x)
        self.clip_y_min = min(self.selection_start_y, self.selection_end_y)
        self.clip_y_max = max(self.selection_start_y, self.selection_end_y)

        clipped_draws = []

        for item in self.draws:
            if len(item) == 4:
                x1, y1, x2, y2 = item
                clipped_line = self.clipping_function(x1, y1, x2, y2)
                if clipped_line is not None:
                    clipped_draws.append(clipped_line)
            elif len(item) == 3:
                clipped_draws.append(item)

        self.draws = clipped_draws

        self.redraw()

    def translate_vector(self, dx, dy):
        updated_draws = []
        for item in self.draws:
            if len(item) == 4:
                x1, y1, x2, y2 = item
                updated_draws.append((x1 + dx, y1 + dy, x2 + dx, y2 + dy))
            elif len(item) == 3:
                x, y, radius = item
                updated_draws.append((x + dx, y + dy, radius))

        self.draws = updated_draws
        self.redraw()

    def scale_vector(self, factor_x, factor_y):
        updated_draws = []
        for item in self.draws:
            if len(item) == 3:
                x, y, radius = item

                scaled_radius_x = factor_x * radius
                scaled_radius_y = factor_y * radius
                updated_draws.append((x, y, scaled_radius_x))
            else:
                x1, y1, x2, y2 = item

                scaled_x2 = x1 + factor_x * (x2 - x1)
                scaled_y2 = y1 + factor_y * (y2 - y1)
                updated_draws.append((x1, y1, scaled_x2, scaled_y2))

        self.draws = updated_draws
        self.redraw()

    def rotate_vector(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        updated_draws = []
        for item in self.draws:
            if len(item) == 4:
                x1, y1, x2, y2 = item

                translated_x2 = x2 - x1
                translated_y2 = y2 - y1

                rotated_x2 = translated_x2 * \
                    math.cos(angle_radians) - translated_y2 * \
                    math.sin(angle_radians)
                rotated_y2 = translated_x2 * \
                    math.sin(angle_radians) + translated_y2 * \
                    math.cos(angle_radians)

                final_x2 = rotated_x2 + x1
                final_y2 = rotated_y2 + y1
                updated_draws.append((x1, y1, final_x2, final_y2))
            elif len(item) == 3:
                x, y, radius = item
                updated_draws.append((x, y, radius))

        self.draws = updated_draws
        self.redraw()

    def reflect_vector(self, reflection_type):
        updated_draws = []
        canvas_center_x = self.winfo_reqwidth() // 2
        canvas_center_y = self.winfo_reqheight() // 2

        for item in self.draws:
            if len(item) == 4:
                x1, y1, x2, y2 = item
                if "Y" in reflection_type:
                    x1 = 2 * canvas_center_x - x1
                    x2 = 2 * canvas_center_x - x2
                if "X" in reflection_type:
                    y1 = 2 * canvas_center_y - y1
                    y2 = 2 * canvas_center_y - y2
                updated_draws.append((x1, y1, x2, y2))
            elif len(item) == 3:
                x, y, radius = item
                if "Y" in reflection_type:
                    x = 2 * canvas_center_x - x
                if "X" in reflection_type:
                    y = 2 * canvas_center_y - y
                updated_draws.append((x, y, radius))

        self.draws = updated_draws
        self.redraw()

    def redraw(self):
        self.delete("line")
        for item in self.draws:
            if len(item) == 4:
                start_x, start_y, end_x, end_y = item
                if (self.rasterization_function == self.dda_algorithm):
                    self.dda_algorithm(start_x, start_y, end_x, end_y)
                else:
                    self.line_bresenham_algorithm(
                        start_x, start_y, end_x, end_y)
            elif len(item) == 3:
                center_x, center_y, radius = item
                self.circle_bresenham_algorithm(center_x, center_y, radius)

    def set_draw_mode(self, mode):
        if mode == 'Circle':
            self.rasterization_function = self.circle_bresenham_algorithm
        if mode == 'Line':
            self.rasterization_function = self.line_bresenham_algorithm

    def clear_canvas(self):
        self.delete("selection")
        self.delete("line")
        self.draws.clear()

    def set_rasterization_function(self, name, type):
        if name == "DDA":
            self.rasterization_function = self.dda_algorithm
        elif name == "Bresenham":
            if type == 'Line':
                self.rasterization_function = self.line_bresenham_algorithm
            elif type == 'Circle':
                self.rasterization_function = self.circle_bresenham_algorithm

    def set_clipping_function(self, name):
        if name == 'Cohen-Sutherland':
            self.clipping_function = self.cohen_sutherland_algorithm
        elif name == 'Liang-Barsky':
            self.clipping_function = self.liang_barsky_algorithm

    def dda_algorithm(self, start_x, start_y, end_x, end_y):
        dx = end_x - start_x
        dy = end_y - start_y
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            self.create_line(start_x, start_y, start_x, start_y, fill="black")
            return

        increment_x = dx / steps
        increment_y = dy / steps

        x = start_x
        y = start_y

        for _ in range(steps + 1):
            self.create_rectangle(round(x), round(y), round(
                x), round(y), fill="black", width=0, tags="line")
            x += increment_x
            y += increment_y

    def line_bresenham_algorithm(self, start_x, start_y, end_x, end_y):
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        sx = 1 if start_x < end_x else -1
        sy = 1 if start_y < end_y else -1
        err = dx - dy

        while True:
            self.create_rectangle(start_x, start_y, start_x,
                                  start_y, fill="black", width=0, tags="line")
            if abs(start_x - end_x) < 1 and abs(start_y - end_y) < 1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                start_x += sx
            if e2 < dx:
                err += dx
                start_y += sy

    def circle_bresenham_algorithm(self, center_x, center_y, radius):
        x = 0
        y = radius
        d = 3 - 2 * radius

        while x <= y:
            self.create_rectangle(center_x + x, center_y + y, center_x + x,
                                  center_y + y, fill="black", width=0, tags="line")
            self.create_rectangle(center_x - x, center_y + y, center_x - x,
                                  center_y + y, fill="black", width=0, tags="line")
            self.create_rectangle(center_x + x, center_y - y, center_x + x,
                                  center_y - y, fill="black", width=0, tags="line")
            self.create_rectangle(center_x - x, center_y - y, center_x - x,
                                  center_y - y, fill="black", width=0, tags="line")
            self.create_rectangle(center_x + y, center_y + x, center_x + y,
                                  center_y + x, fill="black", width=0, tags="line")
            self.create_rectangle(center_x - y, center_y + x, center_x - y,
                                  center_y + x, fill="black", width=0, tags="line")
            self.create_rectangle(center_x + y, center_y - x, center_x + y,
                                  center_y - x, fill="black", width=0, tags="line")
            self.create_rectangle(center_x - y, center_y - x, center_x - y,
                                  center_y - x, fill="black", width=0, tags="line")

            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    def cohen_sutherland_algorithm(self, x1, y1, x2, y2):
        print("Cohen")
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8

        def compute_outcode(x, y):
            code = 0
            if x < self.clip_x_min:
                code |= LEFT
            elif x > self.clip_x_max:
                code |= RIGHT
            if y < self.clip_y_min:
                code |= BOTTOM
            elif y > self.clip_y_max:
                code |= TOP
            return code

        outcode1 = compute_outcode(x1, y1)
        outcode2 = compute_outcode(x2, y2)

        while True:
            if not (outcode1 | outcode2):
                return (x1, y1, x2, y2)
            elif outcode1 & outcode2:
                return None
            else:

                if outcode1:
                    outcode_out = outcode1
                else:
                    outcode_out = outcode2

                if outcode_out & TOP:
                    x = x1 + (x2 - x1) * (self.clip_y_max - y1) / (y2 - y1)
                    y = self.clip_y_max
                elif outcode_out & BOTTOM:
                    x = x1 + (x2 - x1) * (self.clip_y_min - y1) / (y2 - y1)
                    y = self.clip_y_min
                elif outcode_out & RIGHT:
                    y = y1 + (y2 - y1) * (self.clip_x_max - x1) / (x2 - x1)
                    x = self.clip_x_max
                elif outcode_out & LEFT:
                    y = y1 + (y2 - y1) * (self.clip_x_min - x1) / (x2 - x1)
                    x = self.clip_x_min

                if outcode_out == outcode1:
                    x1, y1 = x, y
                    outcode1 = compute_outcode(x1, y1)
                else:
                    x2, y2 = x, y
                    outcode2 = compute_outcode(x2, y2)

    def liang_barsky_algorithm(self, x1, y1, x2, y2):
        print("Liang")
        dx = x2 - x1
        dy = y2 - y1

        p = [-dx, dx, -dy, dy]
        q = [x1 - self.clip_x_min, self.clip_x_max - x1,
             y1 - self.clip_y_min, self.clip_y_max - y1]

        u1, u2 = 0, 1

        for i in range(4):
            if p[i] == 0 and q[i] < 0:
                return None, None, None, None

            u = q[i] / p[i]

            if p[i] < 0:
                u1 = max(u1, u)
            elif p[i] > 0:
                u2 = min(u2, u)

        if u1 > u2:
            return None, None, None, None

        clipped_x1 = x1 + u1 * dx
        clipped_y1 = y1 + u1 * dy
        clipped_x2 = x1 + u2 * dx
        clipped_y2 = y1 + u2 * dy

        return clipped_x1, clipped_y1, clipped_x2, clipped_y2
