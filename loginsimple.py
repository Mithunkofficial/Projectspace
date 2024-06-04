import subprocess

from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Entry, messagebox


window = Tk()
window.geometry("987x577")
window.configure(bg = "#000000")
window.title("Login")
ti = PhotoImage(file='assets\\title\log.png')
window.iconphoto(False, ti)

#Login Validaation function
def login():

    userid = name_entry.get()
    password = pass_entry.get()

    if userid == "trevor" and password == "enter":
        subprocess.run(["python", "guidark.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


canvas = Canvas(
    window,
    bg = "#000000",
    height = 577,
    width = 987,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)

#Adding Images
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    759.0,
    288.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    273.0,
    296.0,
    image=image_image_2
)

#Adding Login Button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    bg="#113A61",
    highlightthickness=0,
    command=login,
    relief="flat"
)
button_1.place(
    x=86.0,
    y=391.0,
    width=381.0,
    height=68.0
)

#Entry Fields
name_entry =Entry(window, font=('Lato',17,'normal'),
                  width =26,
                  borderwidth=0,
                  background="#D9D9D9",
                  fg="black",
                  border=None
                  )
name_entry.place(x=110, y=185)

pass_entry =Entry(window, font=('Lato',17,'normal'),
                  width =26,
                  borderwidth=0,
                  background="#D9D9D9",
                  show='*',
                  fg="black",
                  border=None
                  )
pass_entry.place(x=110, y=310)

window.mainloop()