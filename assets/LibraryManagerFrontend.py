"""
Program name : LibraryManagerFrontend.py
Author : Cédric
Date : 03.12.2025
Edit : 08.12.2025
Description : The Frontend of the app
Version : V 0.1
"""
#imports
from customtkinter import *

##############################
#####      Variables     #####
##############################

BOOK_SEARCH_OPTIONS = ["Titre", "Auteur", "Éditeur", "Genre", "Date", "Id"]

##############################
#####      Functions     #####
##############################


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


##############################
#####        Styles      #####
##############################

#font
DEFAULT_FONT = ("TkDefaultFont", 25, "bold")
WIDGET_FONT = ("TkDefaultFont", 30, "bold")

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

btn_navbar = {}

btn_navbar["search"] = CTkButton(frm_header, text="Rechercher\nun livre", **HEADER_ACTIVE_STYLE, command=lambda : header_selection("search"))
btn_navbar["borrow"] = CTkButton(frm_header, text="Emprunter\nun livre", **HEADER_DEFAULT_STYLE, command=lambda : header_selection("borrow"))
btn_navbar["return"] = CTkButton(frm_header, text="Rendre\nun livre", **HEADER_DEFAULT_STYLE,command=lambda : header_selection("return"))
btn_navbar["client"] = CTkButton(frm_header, text="Client", **HEADER_DEFAULT_STYLE,command=lambda : header_selection("client"))
btn_navbar["manage"] = CTkButton(frm_header, text="Gestion\nde livre", **HEADER_DEFAULT_STYLE,command=lambda : header_selection("manage"))

for i, btn in enumerate(btn_navbar.values()):
    btn.grid(column=i, row=0, sticky="ew")

btn_account = CTkButton(frm_header, text="Se Connecter", **HEADER_DEFAULT_STYLE).grid(column=5, row=0, sticky="ew")

frm_pages = {}

##############################
#####    search page     #####
##############################
frm_pages["search"] = CTkFrame(window, fg_color="transparent")
frm_pages["search"].pack(expand=True, fill="both", pady=20, padx=20)

frm_search_searching = CTkFrame(frm_pages["search"], fg_color="transparent")
frm_search_searching.pack(fill="x", pady=(0, 20), padx=150)

ent_search_searchbar = CTkEntry(frm_search_searching, placeholder_text="Rechercher...", width=400, font=WIDGET_FONT)
ent_search_searchbar.pack(side="left")

drp_search_search_by = CTkOptionMenu(frm_search_searching, font=WIDGET_FONT, values=BOOK_SEARCH_OPTIONS, **DROP_LIST_STYLE)
drp_search_search_by.set("Titre")
drp_search_search_by.pack(side="right")

lbl_search_search_by = CTkLabel(frm_search_searching, text="rechercher par : ", font=WIDGET_FONT)
lbl_search_search_by.pack(side="right")

frm_search_results = CTkScrollableFrame(frm_pages["search"])
frm_search_results.pack(expand=True, fill="both")

btn_search_result = CTkButton(frm_search_results, text="titre : genre : auteur : maison d\'édition : date de parrution : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_search_result.pack(fill="x", pady=20, padx=20)

##############################
#####    borrow page     #####
##############################
frm_pages["borrow"] = CTkFrame(window, fg_color="transparent")

for i in range(3):
    frm_pages["borrow"].grid_columnconfigure(i, weight=1)

frm_pages["borrow"].grid_rowconfigure(0, weight=1)

#-----left-----
ent_borrow_searchbar = CTkEntry(frm_pages["borrow"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_borrow_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 20))

frm_borrow_results = CTkScrollableFrame(frm_pages["borrow"])
frm_borrow_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

btn_borrow_result = CTkButton(frm_borrow_results, text="titre : auteur : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_borrow_result.pack(fill="x", pady=20, padx=20)

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

btn_borrow_select = CTkButton(frm_borrow_selects, text="titre : auteur : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_borrow_select.pack(fill="x", pady=20, padx=20)

#-----right-----
ent_borrow_client_searchbar = CTkEntry(frm_pages["borrow"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_borrow_client_searchbar.grid(column=2, row=0, sticky="ewn", padx=(20, 0))

frm_borrow_client_results = CTkScrollableFrame(frm_pages["borrow"], height=500)
frm_borrow_client_results.grid(column=2, row=0, sticky="ewn", padx=(20, 0), pady=(60, 0))

btn_borrow_client_result = CTkButton(frm_borrow_client_results, text="Prénom : Nom", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_borrow_client_result.pack(fill="x", pady=20, padx=20)

btn_borrow_client_add = CTkButton(frm_pages["borrow"], text="Nouveau Client", height=90, font=WIDGET_FONT)
btn_borrow_client_add.grid(column=2, row=0, sticky="ews", padx=(20, 0), pady=(0, 150))

btn_borrow = CTkButton(frm_pages["borrow"], text="Emprunter", height=90, font=WIDGET_FONT)
btn_borrow.grid(column=2, row=0, sticky="ews", padx=(20, 0), pady=(0, 25))

##############################
#####    return page     #####
##############################
frm_pages["return"] = CTkFrame(window, fg_color="transparent")

for i in range(3):
    frm_pages["return"].grid_columnconfigure(i, weight=1)

frm_pages["return"].grid_rowconfigure(0, weight=1)

#-----left-----
ent_return_searchbar = CTkEntry(frm_pages["return"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_return_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 20))

frm_return_results = CTkScrollableFrame(frm_pages["return"])
frm_return_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

btn_return_result = CTkButton(frm_return_results, text="Prénom : Nom", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_return_result.pack(fill="x", pady=20, padx=20)

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
ent_client_searchbar = CTkEntry(frm_pages["client"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_client_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 20))

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

btn_client_add = CTkButton(frm_pages["client"], text="Nouveau Client", height=90, font=WIDGET_FONT)
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
ent_manage_searchbar = CTkEntry(frm_pages["manage"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_manage_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 550))

lbl_borrow_search_by = CTkLabel(frm_pages["manage"], text="rechercher par : ", font=WIDGET_FONT)
lbl_borrow_search_by.grid(column=0, row=0, sticky="en", padx=(0, 250))

drp_borrow_search_by = CTkOptionMenu(frm_pages["manage"], font=WIDGET_FONT, values=BOOK_SEARCH_OPTIONS, **DROP_LIST_STYLE)
drp_borrow_search_by.set("Titre")
drp_borrow_search_by.grid(column=0, row=0, sticky="en", padx=(0, 20))

frm_manage_results = CTkScrollableFrame(frm_pages["manage"])
frm_manage_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

btn_manage_result = CTkButton(frm_manage_results, text="titre : auteur : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_manage_result.pack(fill="x", pady=20, padx=20)

#-----right-----
btn_manage_delete = CTkButton(frm_pages["manage"], text="Supprimer le livre", height=90, font=WIDGET_FONT)
btn_manage_delete.grid(column=1, row=0, sticky="ewn", padx=(20, 0), pady=(50, 0))

btn_manage_edit = CTkButton(frm_pages["manage"], text="Modifier le livre", height=90, font=WIDGET_FONT)
btn_manage_edit.grid(column=1, row=0, sticky="ewn", padx=(20, 0), pady=(160, 0))

btn_manage_add = CTkButton(frm_pages["manage"], text="Ajouter un livre", height=90, font=WIDGET_FONT)
btn_manage_add.grid(column=1, row=0, sticky="ewn", padx=(20, 0), pady=(300, 0))

window.mainloop()