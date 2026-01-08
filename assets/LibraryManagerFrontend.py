"""
Program name : LibraryManagerFrontend.py
Author : Cédric
Date : 03.12.2025
Edit : 08.01.2026
Description : The Frontend of the app
Version : V 0.4
"""
#TODO search reload
#TODO borrow
#TODO return
#TODO extend borrow
#TODO add edit delete book
#TODO foreign data
#imports
from customtkinter import *
from tkinter import filedialog, IntVar
from PIL import Image
import os

from assets.database.crud import *

from assets.classes.classes_Author import *
from assets.classes.classes_Book import Book
from assets.classes.classes_Publisher import Publisher
from assets.classes.classes_Worker import Worker
from assets.classes.classes_Customer import Customer
from assets.database.database import *

##############################
#####      Variables     #####
##############################

BOOK_SEARCH_OPTIONS = ["Titre", "Auteur", "Éditeur", "Genre", "Date", "Id"]

BOOK_SEARCH = {"Titre" : "title",
               "Auteur" : "author_id",
               "Éditeur" : "publisher_id",
               "Genre" : "genre",
               "Date" : "publishing_date",
               "Id" : "id"}

btn_navbar = {}

frm_pages = {}

active_user = None # To use for permissions with the active user's rank and for logs

##############################
#####      Functions     #####
##############################


def search(table, by, field, text):
    """
    search in the db
    :param table: the table to look in
    :param by: the field search in
    :param field: the field to display
    :param text: the search text
    :return: a list of the results and the id
    """
    #TODO add foreign data not just id
    result_list = []

    #set the variable to the correct value
    by = by if isinstance(by, str) else BOOK_SEARCH[by.get()]
    text = text if isinstance(text, str) else text.get()

    #get the data in the db
    data = get_by(table, by, text)

    # add results in the results frame
    for i in range(len(data)):
        value = []
        bool_value = True
        for j in field:
            attr = getattr(data[i], j)  # get the attribute from the object
            if isinstance(attr, bool):
                bool_value = attr
                value.append("Oui" if attr else "Non")
            else:
                value.append(str(attr))

        text = " : ".join(value)
        book_id = data[i].id
        result_list.append([book_id, text, bool_value])

    return result_list


def search_display(data, target, on_click, false_is_blocked=False):
    """
    put the search result in the target frame
    """
    for widget in target.winfo_children():
        widget.destroy()

    for i in range(len(data)):
        btn = CTkButton(
            target,
            text=data[i][1],  # assuming the second element is the display text
            font=DEFAULT_FONT,
            **SEARCH_RESULT_STYLE,
            command=lambda d=data[i], b_id=i: on_click(d, b_id)  # capture the item
        )

        if false_is_blocked and not data[i][2]:
            btn.configure(state="disabled"
                                "")
        btn.pack(fill="x", pady=(20, 0), padx=20)


def search_book_display(target, by, text):
    """
    set the results command to book display
    """
    data = search(Book, by,["title", "genre", "author_id", "publisher_id", "publishing_date", "is_avaible"], text)
    search_display(data, target, lambda item, btn: open_book_display(item[0]))


def search_select_move_to(table, field, target, by, text, target_move_to, moved_list):
    """
    set the results command to book move_to
    """
    data = search(table, by, field, text)
    search_display(data, target, lambda item, btn: move_to(item, target_move_to, moved_list), True)


def move_to(data, to_target, moved_items):
    """
    move a result to another frame
    """
    item_id = data[0]
    if item_id in moved_items:
        print(f"Item '{data[1]}' already moved!")
        return  # Skip adding it again

    moved_items.append(item_id)

    btn = CTkButton(
        to_target,
        text=data[1],
        font=DEFAULT_FONT,
        **SEARCH_RESULT_STYLE
    )
    btn.configure(command=lambda b=btn: delete_button(b, item_id, moved_items))
    btn.pack(fill="x", pady=(20, 0), padx=20)


def delete_button(btn, item_id, moved_items):
    btn.destroy()
    moved_items.remove(item_id)


def search_select(table, field, target, by, text, var):
    data = search(table, by, field, text)
    search_display(data, target, lambda item, btn: select(item[0], btn, var, target))


def select(id, b_id, var, target):
    """
    allow to select one of the search result
    :param id: the button id
    :param b_id: the book id
    :param var: the variable containing the selected book
    :param target: the frame where the button in
    """
    var.set(id)
    for i in range(len(target.winfo_children())):
        target.winfo_children()[i].configure(fg_color=["#3a7ebf", "#1f538d"] if i == b_id else ["gray80", "gray24"])


def page_reload(page):
    """
    reload the page
    """
    match page:
        case "search":
            search_book_display(frm_search_results, drp_search_search_by, ent_search_searchbar)
        case "borrow":
            search_select_move_to(Book, ["title", "is_avaible"], frm_borrow_results, drp_borrow_search_by, ent_borrow_searchbar, frm_borrow_selects, borrow_client_selected_list)
            search_select(Customer, ["id"], frm_borrow_client_results, "id", ent_borrow_client_searchbar, borrow_client_selected)
        case "return":
            search_select(Customer, ["id"], frm_return_results, "id", ent_return_searchbar, return_selected)
        case "client":
            search_select(Customer, ["id"], frm_client_results, "id", ent_client_searchbar, client_selected)
        case "manage":
            search_select(Book, ["title"], frm_manage_results, drp_manage_search_by, ent_manage_searchbar, manage_selected)


def header_selection(page):
    """
    header_selection allow to navigate between pages using the header
    :param page: the page to show
    """
    #reset every element to original state
    for i, btn in enumerate(btn_navbar.values()):
        btn.configure(**HEADER_DEFAULT_STYLE)

    for i, frm in enumerate(frm_pages.values()):
        frm.pack_forget()

    #change the chosen page / button
    btn_navbar[page].configure(**HEADER_ACTIVE_STYLE)
    frm_pages[page].pack(expand=True, fill="both", pady=20, padx=20)

    page_reload(page)


def create_client( ent_new_client_surname, ent_new_client_firstname,ent_new_client_birthdate, ent_new_client_address, ent_new_client_phone, ent_new_client_email):
    """
    add a client in the database
    :param ent_new_client_surname: the new client surname
    :param ent_new_client_firstname: the new client first name
    :param ent_new_client_birthdate: the new client birthdate
    :param ent_new_client_address: the new client address
    :param ent_new_client_phone: the new client phone
    :param ent_new_client_email: the new client email
    """

    client_surname = ent_new_client_surname.get()
    client_firstname = ent_new_client_firstname.get()
    client_birthdate = ent_new_client_birthdate.get()
    client_address = ent_new_client_address.get()
    client_phone = ent_new_client_phone.get()
    client_email = ent_new_client_email.get()

    client_list = [client_surname, client_firstname, client_birthdate, client_address, client_phone, client_email]

    create(Customer, firstname=client_list[1], lastname=client_list[0], adress = client_list[3], birthdate = client_list[2],
              phone_number=client_list[4], e_mail=client_list[5], can_borrow=True )


def delete_book():
    """
    delete the selected book
    """
    id = manage_selected.get()
    delete(Book, id)
    #reset frame
    search_select(Book, ["title"], frm_manage_results, drp_manage_search_by, ent_manage_searchbar, manage_selected)


def create_book(ent_title, ent_genre, ent_date, ent_author, ent_editor, ent_state, ent_synopsis, image_name, image_source, parent):
    """
    create a new book
    """
    title = ent_title.get()
    genre = ent_genre.get()
    date = ent_date.get()
    author = ent_author.get()
    editor = ent_editor.get()
    state = ent_state.get()
    synopsis = ent_synopsis.get("1.0", "end-1c")

    # copy image
    if image_source:
        with open(image_source, "rb") as src_file, open("assets/images/" + image_name, "wb") as dest_file:
            dest_file.write(src_file.read())

    create(Book, publishing_date=date, title=title,
            back_cover=synopsis, genre=genre,
            is_avaible=True, front_cover=image_name, status=state,
            author_id=author, publisher_id=editor)

    # reset frame
    search_select(Book, ["title"], frm_manage_results, drp_manage_search_by, ent_manage_searchbar, manage_selected)
    parent.destroy()


def edit_book(id, ent_title, ent__genre, ent_date, ent_author, ent_editor, ent_state, ent_synopsis, image_name, image_source, parent):
    """
    edit the selected book
    """
    title = ent_title.get()
    genre = ent__genre.get()
    date = ent_date.get()
    author = ent_author.get()
    editor = ent_editor.get()
    state = ent_state.get()
    synopsis = ent_synopsis.get("1.0", "end-1c")

    # copy image
    if image_source:
        with open(image_source, "rb") as src_file, open("assets/images/" + image_name, "wb") as dest_file:
            dest_file.write(src_file.read())

    update(Book, id, publishing_date=date, title=title,
            back_cover=synopsis, genre=genre,
            is_avaible=True, front_cover=image_name, status=state,
            author_id=author, publisher_id=editor)

    # reset frame
    search_select(Book, ["title"], frm_manage_results, drp_manage_search_by, ent_manage_searchbar, manage_selected)
    parent.destroy()


##############################
#####    Extra windows   #####
##############################


def open_login():
    """
    open_login open the login window
    """
    def login_user(email, password):
        global active_user

        if len(get_by(Worker, "e_mail", email)) == 1:
            worker = get_by(Worker, "e_mail", email)[0]

            if worker.password == password:
                active_user = worker
                btn_account.configure(text=worker.firstname, command=disconnect_user)
                login.destroy()
                return

        lbl_login_error.configure(text="Email ou mot de passe incorrect", text_color="red")


    login = CTkToplevel(window)

    login.transient(window)  # Keep above the main window
    login.grab_set() # take the control (block action on parent window)

    login.title("LogIn")

    # finding the screen with and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # size of the window
    sizex = 500
    sizey = 500

    # finding the middle of the screen
    posx = screen_width // 2 - (sizex // 2)
    posy = screen_height // 2 - (sizey // 2)

    # place the window in the middle
    login.geometry(f"{sizex}x{sizey}+{posx}+{posy}")

    lbl_login_title = CTkLabel(login, text="LogIn", font=BIG_FONT)
    lbl_login_title.pack(side="top", pady=10)

    lbl_login_email = CTkLabel(login, text="Email", font=WIDGET_FONT)
    lbl_login_email.pack(side="top", anchor="w", padx=50, pady=(10, 0))

    ent_login_email = CTkEntry(login, placeholder_text="Email", font=WIDGET_FONT)
    ent_login_email.pack(side="top", fill="x", padx=50, pady=10)

    lbl_login_password = CTkLabel(login, text="Mot de passe", font=WIDGET_FONT)
    lbl_login_password.pack(side="top", anchor="w", padx=50, pady=(10, 0))

    ent_login_password = CTkEntry(login, placeholder_text="Mot de passe", show="*", font=WIDGET_FONT)
    ent_login_password.pack(side="top", fill="x", padx=50, pady=10)

    lbl_login_error = CTkLabel(login, text="", font=DEFAULT_FONT, text_color="red")
    lbl_login_error.pack(side="top", fill="x", padx=50, pady=10)

    btn_login_connect = CTkButton(login, text="connexion", height=80, font=WIDGET_FONT, command=lambda: login_user(ent_login_email.get(), ent_login_password.get()))
    btn_login_connect.pack(side="top", fill="x", padx=120, pady=30)


def disconnect_user():
    """
    disconnect the user from the app
    """
    def disconnect_confirmed():
        global active_user
        active_user = None
        btn_account.configure(text="Se Connecter", command=open_login)
        disconnect.destroy()

    disconnect = CTkToplevel(window)

    disconnect.transient(window)  # Keep above the main window
    disconnect.grab_set()  # take the control (block action on parent window)

    disconnect.title("Disconnect")

    # finding the screen with and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # size of the window
    sizex = 500
    sizey = 180

    # finding the middle of the screen
    posx = screen_width // 2 - (sizex // 2)
    posy = screen_height // 2 - (sizey // 2)

    # place the window in the middle
    disconnect.geometry(f"{sizex}x{sizey}+{posx}+{posy}")

    lbl_disconnect_confirm = CTkLabel(disconnect, text="Voulez-vous vous déconnecter ?", font=DEFAULT_FONT)
    lbl_disconnect_confirm.pack(side="top", fill="x", padx=50, pady=(30, 0))

    frm_disconnect = CTkFrame(disconnect, fg_color="transparent")
    frm_disconnect.pack(side="bottom", fill="x", padx=50, pady=(0, 30))

    btn_disconnect_yes = CTkButton(frm_disconnect, text="Oui", font=WIDGET_FONT, command=disconnect_confirmed)
    btn_disconnect_yes.pack(side="left")

    btn_disconnect_no = CTkButton(frm_disconnect, text="Non", font=WIDGET_FONT, command=disconnect.destroy)
    btn_disconnect_no.pack(side="right")


def open_book_display(id):
    """
    open_book_display open the book display window
    :param id: the id of the book to display
    """
    #get the book data
    data = get_by(Book, "id", id)[0]

    book_display = CTkToplevel(window)

    book_display.transient(window)  # Keep above the main window
    book_display.grab_set() # take the control (block action on parent window)

    book_display.title("Apercus Livre")

    # finding the screen with and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # size of the window
    sizex = 1160
    sizey = 660

    # finding the middle of the screen
    posx = screen_width // 2 - (sizex // 2)
    posy = screen_height // 2 - (sizey // 2) - 30

    # place the window in the middle
    book_display.geometry(f"{sizex}x{sizey}+{posx}+{posy}")

    frm_book_display_top = CTkFrame(book_display, fg_color="transparent")
    frm_book_display_top.pack(side="top", fill="x")

    #get image and look if it exists
    try:
        image = Image.open(f"assets/images/{data.front_cover}")
    except FileNotFoundError:
        print("Image not found")
        image = Image.open("assets/images/placeholder.jpg")

    book_cover = CTkImage(light_image=image, dark_image=image, size=(266, 400))

    lbl_book_cover_image = CTkLabel(frm_book_display_top, image=book_cover, text="")
    lbl_book_cover_image.pack(side="left", anchor="n", padx=20, pady=20)

    frm_book_display_info_left = CTkFrame(frm_book_display_top, fg_color="transparent")
    frm_book_display_info_left.pack(side="left", anchor="n")

    lbl_book_display_title = CTkLabel(frm_book_display_info_left, text=data.title, font=BIG_FONT)
    lbl_book_display_title.pack(anchor="w", padx=20, pady=(20, 0))

    lbl_book_display_author = CTkLabel(frm_book_display_info_left, text=data.author_id, font=WIDGET_FONT)
    lbl_book_display_author.pack(anchor="w", padx=20, pady=(10, 0))

    lbl_book_display_editor = CTkLabel(frm_book_display_info_left, text=data.publisher_id, font=WIDGET_FONT)
    lbl_book_display_editor.pack(anchor="w", padx=20, pady=(10, 0))

    frm_book_display_info_right = CTkFrame(frm_book_display_top, fg_color="transparent")
    frm_book_display_info_right.pack(side="right", anchor="n")

    lbl_book_display_genre = CTkLabel(frm_book_display_info_right, text=data.genre, font=WIDGET_FONT)
    lbl_book_display_genre.pack(anchor="e", padx=20, pady=(20, 0))

    lbl_book_display_date = CTkLabel(frm_book_display_info_right, text=data.publishing_date, font=WIDGET_FONT)
    lbl_book_display_date.pack(anchor="e", padx=20, pady=(10, 0))

    lbl_book_display_state = CTkLabel(frm_book_display_info_right, text=data.status, font=WIDGET_FONT)
    lbl_book_display_state.pack(anchor="e", padx=20, pady=(10, 0))

    frm_book_display_synopsis = CTkScrollableFrame(book_display)
    frm_book_display_synopsis.pack(side="bottom", fill="x", expand=True, padx=20, pady=(0, 20))

    lbl_book_display_synopsis = CTkLabel(frm_book_display_synopsis, wraplength=700, font=DEFAULT_FONT, text=data.back_cover)
    lbl_book_display_synopsis.pack(fill="x")


def open_new_client():
    """
    open_new_client open the new client window
    """
    new_client = CTkToplevel()

    new_client.transient(window)  # Keep above the main window
    new_client.grab_set() # take the control (block action on parent window)

    new_client.title("Apercus Livre")

    # finding the screen with and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # size of the window
    sizex = 600
    sizey = 660

    # finding the middle of the screen
    posx = screen_width // 2 - (sizex // 2)
    posy = screen_height // 2 - (sizey // 2) - 30

    # place the window in the middle
    new_client.geometry(f"{sizex}x{sizey}+{posx}+{posy}")

    lbl_new_client_surname = CTkLabel(new_client, text="Nom", font=WIDGET_FONT)
    lbl_new_client_surname.pack(anchor="w", padx=20, pady=(10,0))

    ent_new_client_surname = CTkEntry(new_client, placeholder_text="...", font=WIDGET_FONT)
    ent_new_client_surname.pack(anchor="w", fill="x", padx=20)

    lbl_new_client_firstname = CTkLabel(new_client, text="Prénom", font=WIDGET_FONT)
    lbl_new_client_firstname.pack(anchor="w", padx=20, pady=(10,0))

    ent_new_client_firstname = CTkEntry(new_client, placeholder_text="...", font=WIDGET_FONT)
    ent_new_client_firstname.pack(anchor="w", fill="x", padx=20)

    lbl_new_client_birthdate = CTkLabel(new_client, text="Date de naissance", font=WIDGET_FONT)
    lbl_new_client_birthdate.pack(anchor="w", padx=20, pady=(10,0))

    ent_new_client_birthdate = CTkEntry(new_client, placeholder_text="jj.mm.aaaa", font=WIDGET_FONT)
    ent_new_client_birthdate.pack(anchor="w", fill="x", padx=20)

    lbl_new_client_address = CTkLabel(new_client, text="Adresse", font=WIDGET_FONT)
    lbl_new_client_address.pack(anchor="w", padx=20, pady=(10,0))

    ent_new_client_address = CTkEntry(new_client, placeholder_text="...", font=WIDGET_FONT)
    ent_new_client_address.pack(anchor="w", fill="x", padx=20)

    lbl_new_client_phone = CTkLabel(new_client, text="Numéro de téléphone", font=WIDGET_FONT)
    lbl_new_client_phone.pack(anchor="w", padx=20, pady=(10,0))

    ent_new_client_phone = CTkEntry(new_client, placeholder_text="+00 00 000 00 00", font=WIDGET_FONT)
    ent_new_client_phone.pack(anchor="w", fill="x", padx=20)

    lbl_new_client_email = CTkLabel(new_client, text="E-mail", font=WIDGET_FONT)
    lbl_new_client_email.pack(anchor="w", padx=20, pady=(10,0))

    ent_new_client_email = CTkEntry(new_client, placeholder_text="user@gmail.com", font=WIDGET_FONT)
    ent_new_client_email.pack(anchor="w", fill="x", padx=20)

    btn_new_client_add = CTkButton(new_client, text="Créer le client", height=90, font=WIDGET_FONT,command=lambda: create_client(ent_new_client_surname, ent_new_client_firstname,ent_new_client_birthdate, ent_new_client_address, ent_new_client_phone, ent_new_client_email))
    btn_new_client_add.pack(padx=50, fill="x", pady=20)


def open_new_book(id=None):
    """
    open_new_book open the new book window
    :param id: id of the book to edit if None create new window
    """

    image_name = "placeholder.jpg"
    image_source = None

    def select_image():
        nonlocal image_name, image_source
        image_path = "assets/images"
        image_source = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if image_source:
            image = Image.open(image_source)
            book_cover = CTkImage(light_image=image, dark_image=image, size=(200, 300))
            lbl_new_book_cover_image.configure(image=book_cover, text="")

            #get a unique image name
            # List all items in the folder
            all_items = os.listdir(image_path)

            # Filter only files
            files = [f for f in all_items if os.path.isfile(os.path.join(image_path, f))]

            # Count files
            image_name = f"{len(files)+1}{os.path.splitext(image_source)[1]}"


    new_book = CTkToplevel()

    new_book.transient(window)  # Keep above the main window
    new_book.grab_set()  # take the control (block action on parent window)

    new_book.title("Apercus Livre")

    # finding the screen with and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # size of the window
    sizex = 750
    sizey = 580

    # finding the middle of the screen
    posx = screen_width // 2 - (sizex // 2)
    posy = screen_height // 2 - (sizey // 2) - 30

    # place the window in the middle
    new_book.geometry(f"{sizex}x{sizey}+{posx}+{posy}")

    btn_new_book_confirm = CTkButton(new_book, text="Confirmer", height=90, font=WIDGET_FONT)
    btn_new_book_confirm.pack(side="bottom", fill="x", padx=20, pady=20)

    frm_new_book_left = CTkFrame(new_book, fg_color="transparent")
    frm_new_book_left.pack(side="left", fill="both")

    frm_new_book_info = CTkFrame(frm_new_book_left, fg_color="transparent")
    frm_new_book_info.pack()

    for i in range(4):
        frm_new_book_info.grid_columnconfigure(index=i, weight=1)
    for i in range(3):
        frm_new_book_info.grid_rowconfigure(index=i, weight=1)

    #left
    lbl_new_book_info_title = CTkLabel(frm_new_book_info, text="Titre", font=DEFAULT_FONT)
    lbl_new_book_info_title.grid(column=0, row=0, sticky="e", pady=(20, 10), padx=5)

    ent_new_book_info_title = CTkEntry(frm_new_book_info, placeholder_text="...", font=DEFAULT_FONT)
    ent_new_book_info_title.grid(column=1, row=0, pady=(20, 10), padx=5)

    lbl_new_book_info_genre = CTkLabel(frm_new_book_info, text="Genre", font=DEFAULT_FONT)
    lbl_new_book_info_genre.grid(column=0, row=1, sticky="e", pady=10, padx=5)

    ent_new_book_info_genre = CTkEntry(frm_new_book_info, placeholder_text="...", font=DEFAULT_FONT)
    ent_new_book_info_genre.grid(column=1, row=1, pady=10, padx=5)

    lbl_new_book_info_date = CTkLabel(frm_new_book_info, text="Date", font=DEFAULT_FONT)
    lbl_new_book_info_date.grid(column=0, row=2, sticky="e", pady=10, padx=5)

    ent_new_book_info_date = CTkEntry(frm_new_book_info, placeholder_text="jj.mm.aaaa", font=DEFAULT_FONT)
    ent_new_book_info_date.grid(column=1, row=2, pady=10, padx=5)

    #right
    lbl_new_book_info_author = CTkLabel(frm_new_book_info, text="Auteur", font=DEFAULT_FONT)
    lbl_new_book_info_author.grid(column=2, row=0, sticky="e", pady=(20, 10), padx=5)

    ent_new_book_info_author = CTkEntry(frm_new_book_info, placeholder_text="...", font=DEFAULT_FONT)
    ent_new_book_info_author.grid(column=3, row=0, pady=(20, 10), padx=5)

    lbl_new_book_info_editor = CTkLabel(frm_new_book_info, text="Éditeur", font=DEFAULT_FONT)
    lbl_new_book_info_editor.grid(column=2, row=1, sticky="e", pady=10, padx=5)

    ent_new_book_info_editor = CTkEntry(frm_new_book_info, placeholder_text="...", font=DEFAULT_FONT)
    ent_new_book_info_editor.grid(column=3, row=1, pady=10, padx=5)

    lbl_new_book_info_state = CTkLabel(frm_new_book_info, text="État", font=DEFAULT_FONT)
    lbl_new_book_info_state.grid(column=2, row=2, sticky="e", pady=10, padx=5)

    ent_new_book_info_state = CTkEntry(frm_new_book_info, placeholder_text="x/10", font=DEFAULT_FONT)
    ent_new_book_info_state.grid(column=3, row=2, pady=10, padx=5)

    lbl_new_book_info_synopsis = CTkLabel(frm_new_book_left, text="4em de couverture", font=DEFAULT_FONT)
    lbl_new_book_info_synopsis.pack(anchor="w", pady=10, padx=10)

    tbx_new_book_info_synopsis = CTkTextbox(frm_new_book_left)
    tbx_new_book_info_synopsis.pack(fill="both", pady=10, padx=10)

    frm_new_book_right = CTkFrame(new_book, fg_color="transparent")
    frm_new_book_right.pack(side="right", fill="both")

    lbl_new_book_cover_image = CTkLabel(frm_new_book_right, text="pas d'image", width=200, height=300, fg_color="#888")
    lbl_new_book_cover_image.pack(padx=20, pady=20)

    btn_new_book_image = CTkButton(frm_new_book_right, text="Choisir image", height=70, font=WIDGET_FONT, command=select_image)
    btn_new_book_image.pack(fill="x", padx=20, pady=10)

    #act differently depending to the mode
    if id and not id == -1:
        print(1)
        data = get_by(Book, "id", id)[0]
        ent_new_book_info_title.insert(0, data.title)
        ent_new_book_info_state.insert(0, data.status)
        ent_new_book_info_date.insert(0, data.publishing_date)
        ent_new_book_info_editor.insert(0, data.publisher_id)
        ent_new_book_info_author.insert(0, data.author_id)
        ent_new_book_info_genre.insert(0, data.genre)
        tbx_new_book_info_synopsis.insert("1.0", data.back_cover)

        image = Image.open("assets/images/"+data.front_cover)
        book_cover = CTkImage(light_image=image, dark_image=image, size=(200, 300))
        lbl_new_book_cover_image.configure(image=book_cover, text="")

        btn_new_book_confirm.configure(command=lambda: edit_book(id, ent_new_book_info_title,
                                                                   ent_new_book_info_genre,
                                                                   ent_new_book_info_date,
                                                                   ent_new_book_info_author,
                                                                   ent_new_book_info_editor,
                                                                   ent_new_book_info_state,
                                                                   tbx_new_book_info_synopsis,
                                                                   data.front_cover, image_source, new_book))

    else:
        btn_new_book_confirm.configure(command=lambda: create_book(ent_new_book_info_title,
                                                                   ent_new_book_info_genre,
                                                                   ent_new_book_info_date,
                                                                   ent_new_book_info_author,
                                                                   ent_new_book_info_editor,
                                                                   ent_new_book_info_state,
                                                                   tbx_new_book_info_synopsis,
                                                                   image_name, image_source, new_book))


##############################
#####        Styles      #####
##############################

#font
DEFAULT_FONT = ("TkDefaultFont", 25, "bold")
WIDGET_FONT = ("TkDefaultFont", 30, "bold")
BIG_FONT = ("TkDefaultFont", 50, "bold")
XBIG_FONT = ("TkDefaultFont", 80, "bold")

#widget style
HEADER_DEFAULT_STYLE = {
    "fg_color": ["gray92", "gray14"],
    "text_color": ["gray14", "gray84"],
    "corner_radius": 0,
    "border_width": 1,
    "height": 80,
    "font": WIDGET_FONT
}

HEADER_ACTIVE_STYLE = {
    "fg_color": ["gray92", "gray14"],
    "text_color": ["gray14", "gray84"],
    "corner_radius": 0,
    "border_width": 0,
    "height": 80,
    "font": WIDGET_FONT
}

DROP_LIST_STYLE = {
    "fg_color": ["gray86", "gray20"],
    "button_color": ["gray82", "gray24"],
    "text_color": ["gray14", "gray84"],
    "anchor": "center",
    "width": 200
}

SEARCH_RESULT_STYLE = {
    "fg_color": ["gray80", "gray24"],
    "text_color": ["gray14", "gray84"],
    "height": 50
}

##############################
#####     Interface      #####
##############################

#-----window config-----#
window = CTk()
window.title("Library Manager")

# finding the screen with and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# size of the window
sizex = 1440
sizey = 960

# finding the middle of the screen
posx = screen_width // 2 - (sizex // 2)
posy = screen_height // 2 - (sizey // 2) - 30

# place the window in the middle
window.geometry(f"{sizex}x{sizey}+{posx}+{posy}")

#-----header-----#
frm_header = CTkFrame(window, fg_color="transparent")
frm_header.pack(side="top", fill="x")

for i in range(6):
    frm_header.grid_columnconfigure(i, weight=1)

btn_navbar["search"] = CTkButton(frm_header, text="Rechercher\nun livre", **HEADER_ACTIVE_STYLE, command=lambda : header_selection("search"))
btn_navbar["borrow"] = CTkButton(frm_header, text="Emprunter\nun livre", **HEADER_DEFAULT_STYLE, command=lambda : header_selection("borrow"))
btn_navbar["return"] = CTkButton(frm_header, text="Rendre\nun livre", **HEADER_DEFAULT_STYLE,command=lambda : header_selection("return"))
btn_navbar["client"] = CTkButton(frm_header, text="Client", **HEADER_DEFAULT_STYLE,command=lambda : header_selection("client"))
btn_navbar["manage"] = CTkButton(frm_header, text="Gestion\nde livre", **HEADER_DEFAULT_STYLE,command=lambda : header_selection("manage"))

for i, btn in enumerate(btn_navbar.values()):
    btn.grid(column=i, row=0, sticky="ew")

btn_account = CTkButton(frm_header, text="Se Connecter", command=open_login, **HEADER_DEFAULT_STYLE)
btn_account.grid(column=5, row=0, sticky="ew")

##############################
#####    search page     #####
##############################
frm_pages["search"] = CTkFrame(window, fg_color="transparent")
frm_pages["search"].pack(expand=True, fill="both", pady=20, padx=20)

frm_search_searching = CTkFrame(frm_pages["search"], fg_color="transparent")
frm_search_searching.pack(fill="x", pady=(0, 20), padx=150)

ent_search_searchbar = CTkEntry(frm_search_searching, placeholder_text="Rechercher...", width=400, font=WIDGET_FONT)
ent_search_searchbar.pack(side="left")

ent_search_searchbar.bind("<KeyRelease>",lambda event:
search_book_display(frm_search_results, drp_search_search_by, ent_search_searchbar))

drp_search_search_by = CTkOptionMenu(frm_search_searching, font=WIDGET_FONT, values=BOOK_SEARCH_OPTIONS, **DROP_LIST_STYLE)
drp_search_search_by.set("Titre")
drp_search_search_by.pack(side="right")

lbl_search_search_by = CTkLabel(frm_search_searching, text="rechercher par : ", font=WIDGET_FONT)
lbl_search_search_by.pack(side="right")

frm_search_results = CTkScrollableFrame(frm_pages["search"])
frm_search_results.pack(expand=True, fill="both")

search_book_display(frm_search_results, drp_search_search_by, ent_search_searchbar)

##############################
#####    borrow page     #####
##############################
frm_pages["borrow"] = CTkFrame(window, fg_color="transparent")

for i in range(3):
    frm_pages["borrow"].grid_columnconfigure(i, weight=1)

frm_pages["borrow"].grid_rowconfigure(0, weight=1)

#-----left-----

borrow_client_selected_list = []

ent_borrow_searchbar = CTkEntry(frm_pages["borrow"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_borrow_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 20))

ent_borrow_searchbar.bind("<KeyRelease>",lambda event:
search_select_move_to(Book, ["title", "is_avaible"], frm_borrow_results, drp_borrow_search_by, ent_borrow_searchbar, frm_borrow_selects, borrow_client_selected_list))

frm_borrow_results = CTkScrollableFrame(frm_pages["borrow"])
frm_borrow_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

#-----middle-----

lbl_borrow_search_by = CTkLabel(frm_pages["borrow"], text="rechercher par : ", font=WIDGET_FONT)
lbl_borrow_search_by.grid(column=1, row=0, sticky="wn", padx=(10,0))

drp_borrow_search_by = CTkOptionMenu(frm_pages["borrow"], font=WIDGET_FONT, values=BOOK_SEARCH_OPTIONS, **DROP_LIST_STYLE)
drp_borrow_search_by.set("Titre")
drp_borrow_search_by.grid(column=1, row=0, sticky="en", padx=(0, 10))

lbl_borrow_select = CTkLabel(frm_pages["borrow"], text="Livre sélectionés", font=WIDGET_FONT)
lbl_borrow_select.grid(column=1, row=0, sticky="n", pady=(70, 0))

frm_borrow_selects = CTkScrollableFrame(frm_pages["borrow"])
frm_borrow_selects.grid(column=1, row=0, sticky="ewsn", pady=(120, 0), padx=10)

#-----right-----

borrow_client_selected = IntVar()
borrow_client_selected.set(-1)

ent_borrow_client_searchbar = CTkEntry(frm_pages["borrow"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_borrow_client_searchbar.grid(column=2, row=0, sticky="ewn", padx=(20, 0))

ent_borrow_client_searchbar.bind("<KeyRelease>",lambda event:
#TODO change when foreign data is available
search_select(Customer, ["id"], frm_borrow_client_results, "id", ent_borrow_client_searchbar, borrow_client_selected))

frm_borrow_client_results = CTkScrollableFrame(frm_pages["borrow"], height=500)
frm_borrow_client_results.grid(column=2, row=0, sticky="ewn", padx=(20, 0), pady=(60, 0))

btn_borrow_client_add = CTkButton(frm_pages["borrow"], text="Nouveau Client", height=90, font=WIDGET_FONT, command=open_new_client)
btn_borrow_client_add.grid(column=2, row=0, sticky="ews", padx=(20, 0), pady=(0, 150))

btn_borrow = CTkButton(frm_pages["borrow"], text="Emprunter", height=90, font=WIDGET_FONT, command=lambda : print(borrow_client_selected.get(), borrow_client_selected_list))
btn_borrow.grid(column=2, row=0, sticky="ews", padx=(20, 0), pady=(0, 25))

##############################
#####    return page     #####
##############################
frm_pages["return"] = CTkFrame(window, fg_color="transparent")

for i in range(3):
    frm_pages["return"].grid_columnconfigure(i, weight=1)

frm_pages["return"].grid_rowconfigure(0, weight=1)

#-----left-----

return_selected = IntVar()
return_selected.set(-1)

ent_return_searchbar = CTkEntry(frm_pages["return"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_return_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 20))

ent_return_searchbar.bind("<KeyRelease>",lambda event:
#TODO change when foreign data is available
search_select(Customer, ["id"], frm_return_results, "id", ent_return_searchbar, return_selected))

frm_return_results = CTkScrollableFrame(frm_pages["return"])
frm_return_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

#-----middle-----
lbl_return_borrowed = CTkLabel(frm_pages["return"], text="Livres empruntés", font=WIDGET_FONT)
lbl_return_borrowed.grid(column=1, row=0, sticky="ewn", pady=(10, 0))

frm_return_borrowed_results = CTkScrollableFrame(frm_pages["return"])
frm_return_borrowed_results.grid(column=1, row=0, sticky="ewsn", padx=10, pady=(60, 0))

btn_return_borrowed_result = CTkButton(frm_return_borrowed_results, text="titre : auteur : retard?", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_return_borrowed_result.pack(fill="x", pady=20, padx=20)

#-----right-----
lbl_return_select = CTkLabel(frm_pages["return"], text="Livres sélectionés", font=WIDGET_FONT)
lbl_return_select.grid(column=2, row=0, sticky="ewn", pady=(10, 0))

frm_return_select_results = CTkScrollableFrame(frm_pages["return"])
frm_return_select_results.grid(column=2, row=0, sticky="ewsn", padx=(20, 0), pady=(60, 120))

btn_return_select_result = CTkButton(frm_return_select_results, text="titre : auteur : retard?", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_return_select_result.pack(fill="x", pady=20, padx=20)

btn_borrow = CTkButton(frm_pages["return"], text="Rendre", height=90, font=WIDGET_FONT)
btn_borrow.grid(column=2, row=0, sticky="ews", padx=(20, 0), pady=(0, 10))

##############################
#####    client page     #####
##############################
frm_pages["client"] = CTkFrame(window, fg_color="transparent")

for i in range(3):
    frm_pages["client"].grid_columnconfigure(i, weight=1)

frm_pages["client"].grid_rowconfigure(0, weight=1)

#-----left-----

client_selected = IntVar()
client_selected.set(-1)

ent_client_searchbar = CTkEntry(frm_pages["client"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_client_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 20))

ent_client_searchbar.bind("<KeyRelease>",lambda event:
#TODO change when foreign data is available
search_select(Customer, ["id"], frm_client_results, "id", ent_client_searchbar, client_selected))

frm_client_results = CTkScrollableFrame(frm_pages["client"])
frm_client_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

btn_client_result = CTkButton(frm_client_results, text="Prénom : Nom", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_client_result.pack(fill="x", pady=20, padx=20)
#-----middle-----
lbl_client_borrowed = CTkLabel(frm_pages["client"], text="Historique des emprunts", font=WIDGET_FONT)
lbl_client_borrowed.grid(column=1, row=0, sticky="ewn", pady=(10, 0))

frm_client_borrowed_results = CTkScrollableFrame(frm_pages["client"])
frm_client_borrowed_results.grid(column=1, row=0, sticky="ewsn", padx=10, pady=(60, 0))

btn_client_borrowed_result = CTkButton(frm_client_borrowed_results, text="titre : auteur\n date début : date fin : retard?", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_client_borrowed_result.pack(fill="x", pady=20, padx=20)

#-----right-----
btn_client_borrow = CTkButton(frm_pages["client"], text="Étendre l'emprunt", height=90, font=WIDGET_FONT)
btn_client_borrow.grid(column=2, row=0, sticky="ewn", padx=(20, 0), pady=(20, 0))

btn_client_add = CTkButton(frm_pages["client"], text="Nouveau Client", height=90, font=WIDGET_FONT, command=open_new_client)
btn_client_add.grid(column=2, row=0, sticky="ewn", padx=(20, 0), pady=(130, 0))

lbl_client_fine = CTkLabel(frm_pages["client"], text="Amende", font=WIDGET_FONT)
lbl_client_fine.grid(column=2, row=0, sticky="ewn", pady=(250, 0))

frm_client_fine_results = CTkScrollableFrame(frm_pages["client"])
frm_client_fine_results.grid(column=2, row=0, sticky="ewsn", padx=(20, 0), pady=(290, 0))

btn_client_fine_result = CTkButton(frm_client_fine_results, text="date : prix", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_client_fine_result.pack(fill="x", pady=20, padx=20)

##############################
#####    manage page     #####
##############################
frm_pages["manage"] = CTkFrame(window, fg_color="transparent")

frm_pages["manage"].grid_columnconfigure(0, weight=2)
frm_pages["manage"].grid_columnconfigure(1, weight=1)

frm_pages["manage"].grid_rowconfigure(0, weight=1)

#-----left-----

manage_selected = IntVar()
manage_selected.set(-1)

ent_manage_searchbar = CTkEntry(frm_pages["manage"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_manage_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 550))

ent_manage_searchbar.bind("<KeyRelease>",lambda event:
search_select(Book, ["title"], frm_manage_results, drp_manage_search_by, ent_manage_searchbar, manage_selected))

lbl_manage_search_by = CTkLabel(frm_pages["manage"], text="rechercher par : ", font=WIDGET_FONT)
lbl_manage_search_by.grid(column=0, row=0, sticky="en", padx=(0, 250))

drp_manage_search_by = CTkOptionMenu(frm_pages["manage"], font=WIDGET_FONT, values=BOOK_SEARCH_OPTIONS, **DROP_LIST_STYLE)
drp_manage_search_by.set("Titre")
drp_manage_search_by.grid(column=0, row=0, sticky="en", padx=(0, 20))

frm_manage_results = CTkScrollableFrame(frm_pages["manage"])
frm_manage_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

#-----right-----
btn_manage_delete = CTkButton(frm_pages["manage"], text="Supprimer le livre", height=90, font=WIDGET_FONT, command=delete_book)
btn_manage_delete.grid(column=1, row=0, sticky="ewn", padx=(20, 0), pady=(50, 0))

btn_manage_edit = CTkButton(frm_pages["manage"], text="Modifier le livre", height=90, font=WIDGET_FONT, command= lambda : open_new_book(manage_selected.get()))
btn_manage_edit.grid(column=1, row=0, sticky="ewn", padx=(20, 0), pady=(160, 0))

btn_manage_add = CTkButton(frm_pages["manage"], text="Ajouter un livre", height=90, font=WIDGET_FONT, command=open_new_book)
btn_manage_add.grid(column=1, row=0, sticky="ewn", padx=(20, 0), pady=(300, 0))

window.mainloop()