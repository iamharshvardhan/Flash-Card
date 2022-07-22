from tkinter import *
import pandas
import random
import time
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



def next_card():
    global current_card, flip_timer
    windows.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(front_image, image=card_front_image)
    flip_timer = windows.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(front_image, image=card_back_image)


def known_card():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("/data/words_to_learn.csv", index=False)
    next_card()


windows = Tk()
windows.title("Flash Card App")
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
windows.after(3000, func=flip_card)
flip_timer = windows.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
front_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, font=("Ariel", 40, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong.grid(row=1, column=0)

correct_image = PhotoImage(file="images/right.png")
correct = Button(image=correct_image, highlightthickness=0, command=known_card)
correct.grid(row=1, column=1)

next_card()

windows.mainloop()
