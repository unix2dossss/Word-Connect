from tkinter import *
from row_organisation import Generate
from generate_letters_through_JSON import Letters
import random

FONT = ("Helvetica", 12, "bold")

random_gap = ["3", "4"]
random.shuffle(random_gap)

window = Tk()
window.title("Word Connect")
window.geometry("830x500")
window.config(bg="#FFF")

button_slots = []
blank_images = []
slot_spaces = []
all_buttons = []


def cleareverything(*mode_arg):

    global button_slots, blank_images, slot_spaces, nextset_images, slot_images, submitted_words, image_list, letter_buttons, u_word_input_string
    global words_clicked_index, menu_images, control_buttons, strike_buttons, total_strikes

    for buttonOBJ in button_slots:
        if buttonOBJ[0] == len(buttonOBJ[1]):
            for buttonx in buttonOBJ[1]:
                buttonx.destroy()
        else:
            for button_amount in range(len(buttonOBJ[1]) - 1):
                # print(buttonOBJ[1][button_amount])
                buttonOBJ[1][button_amount].destroy()
    for btn in letter_buttons:
        btn.destroy()
    for controlbutton in control_buttons:
        controlbutton.destroy()

    if len(mode_arg) != 0:
        if mode_arg[0] == 0:
            for strikebtn in strike_buttons:
                strikebtn.destroy()
            total_strikes = 0

    slot_spaces = []
    blank_images = []
    button_slots = []
    slot_images = []
    nextset_images = []
    submitted_words = []
    image_list = []
    letter_buttons = []
    u_word_input_string = []
    words_clicked_index = []
    menu_images = []
    control_buttons = []
    strike_buttons = []


def create_level(mode):
    global button_slots, blank_images, slot_spaces, nextset_images, slot_images, submitted_words, image_list, letter_buttons, u_word_input_string
    global words_clicked_index, canvas

    window.geometry("1660x910")
    window.config(bg="#FFF", padx=20, pady=20)

    game_over = False

    if len(button_slots) != 0:
        cleareverything()

    # print(game_over)

    for row in range(3):
        generator = Generate()
        # print(generator.placeholder)
        arrangement = generator.placeholder
        # [3,0,4]

        for a in arrangement:
            slot_spaces.append(a)

        placeholders_placed = 0
        for item in arrangement:  # item = 3
            if item != 0:
                button_set = []
                for word_len in range(item):
                    blank = PhotoImage(file="alphabet/blank.png")
                    blank_images.append(blank)
                    my_button = Button(image=blank, relief="solid", state="active")
                    my_button.grid(row=row, column=placeholders_placed, padx=4, pady=10)
                    placeholders_placed += 1
                    button_set.append(my_button)
                button_slots.append([item, button_set])
            else:

                placeholders_placed += 1

    create_user_buttons(mode)


slot_images = []


def fillButton(word):
    global button_slots, slot_images

    random.shuffle(button_slots)

    for word_slot in button_slots:
        if word_slot[0] == len(word_slot[1]) and word_slot[0] == len(word):
            for o in range(len(word_slot[1])):
                slot_image = PhotoImage(file=f"alphabet/slot/{word[o]}.png")
                slot_images.append(slot_image)
                word_slot[1][o].config(image=slot_image)

            word_slot[1].append("Slot")
            break


image_list = []

u_word_input_string = []
words_clicked_index = []

submitted_words = []


def resetSubmitColor():
    global current_seq_button
    current_seq_button.config(bg="#FBEEFF", text="")


nextset_images = []


def nextset(status, mode):
    global letter_buttons, strike_buttons

    success_set = ["n", "e", "x", "t", "next_set", "s", "e", "t"]
    fail_set = ["n", "i", "c", "e", "retry", "t", "r", "y"]

    for v in range(8):
        if status == "complete":
            next_set_image = PhotoImage(file=f"alphabet/{success_set[v]}.png")
        else:
            next_set_image = PhotoImage(file=f"alphabet/{fail_set[v]}.png")

        nextset_images.append(next_set_image)

        if v != 4:
            letter_buttons[v].config(image=next_set_image, state="disabled")
        else:
            letter_buttons[v].config(
                image=next_set_image, state="normal", borderwidth=3
            )

    current_seq_button.config(state="disabled")
    submit_button.config(state="disabled")
    clear_button.config(state="disabled")


pause_timer = False

total_strikes = 0


def strike(strike):
    strike_buttons[strike].config(bg="#F4C7C7", text="X")


def checkword(letter, z, mode):
    global u_word_input_string, words_clicked_index, letter_buttons, current_seq_button, game_over, pause_timer, total_strikes
    # print(z)
    if letter == "clear":
        u_word_input_string = []
        words_clicked_index = []
        letter_buttons[z].config(
            state="normal"
        )  # NOT SURE WHAT THIS DOES. LOOKS USEELESS.

        for btn in letter_buttons:
            btn.config(state="normal")

        current_seq_button.config(text="")

    elif letter == "submit":
        global fullstring
        fullstring = "".join(u_word_input_string).upper()

        if fullstring not in submitted_words:

            letters.CheckWord(u_word_input_string)
            if len(fullstring) in slot_spaces:
                if letters.valid:
                    fillButton(u_word_input_string)
                    letters.CheckWord(u_word_input_string)

                    submitted_words.append(fullstring)
                    current_seq_button.config(bg="#c0fac8")
                    current_seq_button.after(1500, resetSubmitColor)
                    slot_spaces.remove(len(fullstring))

                    if len(slot_spaces) == 3:
                        game_over = True
                        nextset("complete", mode=mode)

                else:
                    if mode == 0:
                        if total_strikes == 2:
                            game_over = True
                            nextset("failed", mode=mode)
                        strike(total_strikes)
                        total_strikes += 1
                    current_seq_button.config(bg="#fac0c0", text=f"Word Doesn't Exist")
                    current_seq_button.after(1500, resetSubmitColor)

            else:
                current_seq_button.config(
                    bg="#fac0c0", text=f"No {len(fullstring)} Lettered Slots"
                )
                current_seq_button.after(1500, resetSubmitColor)
        else:
            current_seq_button.config(bg="#fac0c0", text=f"Already Submitted")
            current_seq_button.after(1500, resetSubmitColor)

        if not game_over:
            for btn in letter_buttons:
                btn.config(state="normal")

        u_word_input_string = []
        words_clicked_index = []

    elif game_over == True and z == 4:
        print('LOL')
        if mode == 0:
            for strikebtn in strike_buttons:
                strikebtn.destroy()
                total_strikes = 0
        elif mode == 1:
            start_timer(60, pause_timer)
        create_level(mode)
        pause_timer = True

    else:

        pause_timer = False

        u_word_input_string.append(letter)
        words_clicked_index.append(z)
        # print(letter_buttons)
        letter_buttons[z].config(state="disabled")
        # print(u_word_input_string)
        currrentstring = "".join(u_word_input_string).upper()
        current_seq_button.config(text=f"{currrentstring} ({len(currrentstring)})")


clear_image = PhotoImage(file=f"alphabet/backspace.png")

control_buttons = []
strike_buttons = []


def start_timer(seconds, timer_state):
    global timerButton, game_over

    # If the user fills in all the slots, pause the timer.
    if game_over:
        return

    if seconds == -1:
        game_over = True
        nextset("failed", 1)
    else:
        timerButton.configure(text=seconds)
        timerButton.after(1000, start_timer, seconds - 1, pause_timer)


def create_user_buttons(mode):
    global letter_buttons, game_over, current_seq_button, submit_button, clear_button, letters, user_letters, clear_image, timerButton

    letters = Letters()
    user_letters = letters.user_letters
    letter_buttons = []

    game_over = False

    for z in range(8):
        character_image = PhotoImage(file=f"alphabet/{user_letters[z]}.png")
        image_list.append(character_image)
        new_button = Button(
            relief="solid",
            image=character_image,
            borderwidth=2,  # COULD LOOK GOOD WITH RAISED RELIEF BUTTON
            bg="white",
            command=lambda l=[user_letters[z], z]: checkword(l[0], l[1], mode),
        )
        new_button.grid(row=5, column=z, pady=14)
        letter_buttons.append(new_button)

    current_seq_button = Button(
        text="", relief="solid", width=21, height=2, bg="#FBEEFF", borderwidth=2
    )
    current_seq_button.grid(row=6, column=0)
    control_buttons.append(current_seq_button)

    submit_button = Button(
        text="SUBMIT",
        relief="solid",
        width=21,
        height=2,
        bg="#EBCBFF",
        borderwidth=2,
        command=lambda j=["submit", z]: checkword(j[0], j[1], mode),
    )
    submit_button.grid(row=6, column=1, columnspan=3, padx=55, sticky="W")
    control_buttons.append(submit_button)

    clear_button = Button(
        relief="solid",
        bg="#FBEEFF",
        image=clear_image,
        borderwidth=2,
        command=lambda j=["clear", z]: checkword(j[0], j[1], mode),
    )
    clear_button.grid(row=6, column=1, sticky="W", padx=2)
    control_buttons.append(clear_button)

    burger_image = PhotoImage(file=f"menu_graphics/burgermenu.png")

    menu_images.append(burger_image)

    e = "destroy"
    canvas_exists = False

    burgermenu_button = Button(
        image=burger_image,
        relief="solid",
        borderwidth=2,
        highlightthickness=0,
        command=lambda: create_game_menu(e, canvas_exists, mode=mode),
    )
    burgermenu_button.grid(row=6, column=7, sticky="E")
    control_buttons.append(burgermenu_button)

    if mode == 1:
        timerButton = Button(
            text="65",
            width=3,
            height=2,
            highlightthickness=0,
            borderwidth=2,
            relief="solid",
            bg="#D6B8E8",
        )
        timerButton.grid(row=6, column=2, sticky="W", padx=48)
        control_buttons.append(timerButton)
        start_timer(60, pause_timer)
    elif mode == 0:
        for strike in range(3):
            StrikeButton = Button(
                text="",
                width=3,
                height=2,
                highlightthickness=0,
                borderwidth=2,
                relief="solid",
                bg="#C7F4CA",
            )
            StrikeButton.grid(
                row=6, column=2, columnspan=3, sticky="W", padx=(60 + strike * 58)
            )
            strike_buttons.append(StrikeButton)


menu_images = []

howtwo_active = True

menu_images = []


def menu_button_click(button):
    global menu_images, burgermenu_button

    for mbutton in menu_buttons:
        mbutton.destroy()

    if button == 2:

        window.geometry("830x500")
        # window.config(bg='#FFF', padx=20, pady=20)
        window.config(bg="#FFF", padx=0, pady=0)

        howtoplaybg = PhotoImage(file="menu_graphics/howto.png")
        menu_images.append(howtoplaybg)
        canvas.itemconfig(menu_background, image=howtoplaybg)

        q = "don't_destroy"
        canvas_exists = True

        burger_image = PhotoImage(file=f"menu_graphics/burgermenu.png")
        menu_images.append(burger_image)
        burgermenu_button = Button(
            canvas,
            image=burger_image,
            relief="solid",
            borderwidth=2,
            highlightthickness=0,
            command=lambda: create_game_menu(q, canvas_exists, mode=button),
        )
        burgermenu_button.place(x=775, y=448)
        menu_buttons.append(burgermenu_button)
    elif button == 1:
        create_level(1)
        canvas.destroy()
    else:
        create_level(0)
        canvas.destroy()


def create_game_menu(q, canvas_exists, mode):
    global menu_buttons, canvas, menu_background
    global button_slots, blank_images, slot_spaces, nextset_images, slot_images, submitted_words, image_list, letter_buttons, u_word_input_string
    global words_clicked_index, burgermenu_button

    if q == "destroy":
        cleareverything(mode)

    window.geometry("830x500")
    window.config(bg="#FFF", padx=0, pady=0)

    bg_image = PhotoImage(file="menu_graphics/bgmenu.png")
    menu_images.append(bg_image)

    menu_buttons = []

    if canvas_exists == False:
        canvas = Canvas(window)
        canvas.config(width=830, height=500)
        canvas.grid(column=0, row=0)

        menu_background = canvas.create_image(0, 0, image=bg_image, anchor="nw")
    else:
        canvas.itemconfig(menu_background, image=bg_image)
        burgermenu_button.destroy()

    coordinates = [35, 296, 556]

    for m in range(3):

        button_image = PhotoImage(file=f"menu_graphics/{m}.png")
        menu_images.append(button_image)
        menu_button = Button(
            canvas,
            image=button_image,
            relief="solid",
            borderwidth=2,
            highlightthickness=0,
            command=lambda b=m: menu_button_click(b),
        )
        menu_button.place(x=coordinates[m], y=230)
        menu_buttons.append(menu_button)


create_game_menu("don't_destroy", False, 2)

window.mainloop()
