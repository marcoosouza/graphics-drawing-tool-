import tkinter as tk
from components.main_window import MainWindow
from PIL import Image


# image = Image.open("coupon_617242.png")
# new_width = 20
# new_height = 20
# resized_image = image.resize((new_width, new_height))
# resized_image.save("clipping.png")

def main():
    root = MainWindow()

    root.mainloop()


if __name__ == "__main__":
    main()
