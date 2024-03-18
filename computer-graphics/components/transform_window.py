import tkinter as tk


class TransformWindow(tk.Toplevel):
    def __init__(self, parent, transformation_function):
        super().__init__(parent)
        self.title("Transform")
        self.geometry("500x500")
        self.transformation_function = transformation_function

        self.translation_var = tk.BooleanVar()
        self.translation_var.set(False)
        self.translation_checkbox = tk.Checkbutton(
            self, text="Translation", variable=self.translation_var, command=self.toggle_translation)
        self.translation_checkbox.grid(
            row=0, column=0, padx=5, pady=5, sticky="w")

        self.translation_label = tk.Label(self, text="X:")
        self.translation_label.grid(
            row=1, column=0, padx=5, pady=5, sticky="e")
        self.translation_x_entry = tk.Entry(self, state="disabled")
        self.translation_x_entry.grid(row=1, column=1, padx=5, pady=5)
        self.translation_y_label = tk.Label(self, text="Y:")
        self.translation_y_label.grid(
            row=1, column=2, padx=5, pady=5, sticky="e")
        self.translation_y_entry = tk.Entry(self, state="disabled")
        self.translation_y_entry.grid(row=1, column=3, padx=5, pady=5)

        self.scale_var = tk.BooleanVar()
        self.scale_var.set(False)
        self.scale_checkbox = tk.Checkbutton(
            self, text="Scale", variable=self.scale_var, command=self.toggle_scale)
        self.scale_checkbox.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.scale_label = tk.Label(self, text="X:")
        self.scale_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.scale_x_entry = tk.Entry(self, state="disabled")
        self.scale_x_entry.grid(row=3, column=1, padx=5, pady=5)

        self.scale_y_label = tk.Label(self, text="Y:")
        self.scale_y_label.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.scale_y_entry = tk.Entry(self, state="disabled")
        self.scale_y_entry.grid(row=3, column=3, padx=5, pady=5)

        self.rotation_var = tk.BooleanVar()
        self.rotation_var.set(False)
        self.rotation_checkbox = tk.Checkbutton(
            self, text="Rotation", variable=self.rotation_var, command=self.toggle_rotation)
        self.rotation_checkbox.grid(
            row=4, column=0, padx=5, pady=5, sticky="w")

        self.rotation_label = tk.Label(self, text="Angle:")
        self.rotation_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.rotation_entry = tk.Entry(self, state="disabled")
        self.rotation_entry.grid(row=5, column=1, padx=5, pady=5)

        self.reflection_var = tk.BooleanVar()
        self.reflection_var.set(False)
        self.reflection_checkbox = tk.Checkbutton(
            self, text="Reflection", variable=self.reflection_var, command=self.toggle_reflection)
        self.reflection_checkbox.grid(
            row=6, column=0, padx=5, pady=5, sticky="w")

        self.reflection_text_label = tk.Label(self, text="Type:")
        self.reflection_text_label.grid(
            row=7, column=0, padx=5, pady=5, sticky="e")
        self.reflection_text_entry = tk.Entry(self, state="disabled")
        self.reflection_text_entry.grid(
            row=7, column=1, padx=5, pady=5)

        self.transform_button = tk.Button(
            self, text="Transform", command=self.perform_transformation)
        self.transform_button.grid(row=8, columnspan=4, padx=5, pady=5)

    def toggle_translation(self):
        state = self.translation_var.get()
        self.translation_x_entry.config(
            state="normal" if state else "disabled")
        self.translation_y_entry.config(
            state="normal" if state else "disabled")

    def toggle_scale(self):
        state = self.scale_var.get()
        self.scale_x_entry.config(state="normal" if state else "disabled")
        self.scale_y_entry.config(state="normal" if state else "disabled")

    def toggle_rotation(self):
        state = self.rotation_var.get()
        self.rotation_entry.config(state="normal" if state else "disabled")

    def toggle_reflection(self):
        state = self.reflection_var.get()
        self.reflection_text_entry.config(
            state="normal" if state else "disabled")

    def perform_transformation(self):
        transformations = []

        if self.translation_var.get():
            x = self.translation_x_entry.get()
            y = self.translation_y_entry.get()
            transformations.append(("Translation", x, y))
        if self.scale_var.get():
            x_scale = self.scale_x_entry.get()  
            y_scale = self.scale_y_entry.get()  
            transformations.append(("Scale", x_scale, y_scale))
        if self.rotation_var.get():
            angle = self.rotation_entry.get()
            transformations.append(("Rotation", angle))
        if self.reflection_var.get():
            text = self.reflection_text_entry.get()
            transformations.append(("Reflection", text))

        self.transformation_function(transformations)
