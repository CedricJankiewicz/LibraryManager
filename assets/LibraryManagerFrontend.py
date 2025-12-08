"""
Program name : LibraryManagerFrontend.py
Author : Cédric
Date : 03.12.2025
Edit : 03.12.2025
Description : The Frontend of the app
Version : V 0.1
"""
#imports
from customtkinter import *

##############################
#####      Variable      #####
##############################

##############################
#####      Function      #####
##############################


def header_selection(page):

    for i, btn in enumerate(btn_navbar.values()):
        btn.configure(**HEADER_DEFAULT_STYLE)

    for i, frm in enumerate(frm_pages.values()):
        frm.pack_forget()

    btn_navbar[page].configure(**HEADER_ACTIVE_STYLE)
    frm_pages[page].pack(expand=True, fill="both", pady=20, padx=20)


##############################
#####        Style       #####
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
    "text_color": ["gray14", "gray84"]
}

SEARCH_RESULT_STYLE = {
    "fg_color": ["gray80", "gray24"],
    "text_color": ["gray14", "gray84"],
    "height": 50
}

##############################
#####     Interface      #####
##############################

##### window config #####
window = CTk()
window.geometry("1440x960")

##### header #####
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

##### search window #####
frm_pages["search"] = CTkFrame(window, fg_color="transparent")
frm_pages["search"].pack(expand=True, fill="both", pady=20, padx=20)

frm_search_searching = CTkFrame(frm_pages["search"], fg_color="transparent")
frm_search_searching.pack(fill="x", pady=(0, 20), padx=150)

ent_search_searchbar = CTkEntry(frm_search_searching, placeholder_text="Rechercher...", width=400, font=WIDGET_FONT)
ent_search_searchbar.pack(side="left")

search_options = ["Titre", "Auteur", "Id"]

drp_search_search_by = CTkOptionMenu(frm_search_searching, font=WIDGET_FONT, values=search_options, **DROP_LIST_STYLE)
drp_search_search_by.set("Titre")
drp_search_search_by.pack(side="right")

lbl_search_search_by = CTkLabel(frm_search_searching, text="rechercher par : ", font=WIDGET_FONT)
lbl_search_search_by.pack(side="right")

frm_search_results = CTkScrollableFrame(frm_pages["search"])
frm_search_results.pack(expand=True, fill="both")

btn_search_result = CTkButton(frm_search_results, text="titre : genre : auteur : maison d\'édition : date de parrution : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_search_result.pack(fill="x", pady=20, padx=20)

##### borrow window #####
frm_pages["borrow"] = CTkFrame(window, fg_color="transparent")

for i in range(3):
    frm_pages["borrow"].grid_columnconfigure(i, weight=1)

frm_pages["borrow"].grid_rowconfigure(0, weight=1)

#left
ent_borrow_searchbar = CTkEntry(frm_pages["borrow"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_borrow_searchbar.grid(column=0, row=0, sticky="ewn", padx=(0, 20))

frm_borrow_results = CTkScrollableFrame(frm_pages["borrow"])
frm_borrow_results.grid(column=0, row=0, sticky="ewsn", padx=(0, 20), pady=(60, 0))

btn_borrow_result = CTkButton(frm_borrow_results, text="titre : auteur : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_borrow_result.pack(fill="x", pady=20, padx=20)

#middle

lbl_borrow_search_by = CTkLabel(frm_pages["borrow"], text="rechercher par : ", font=WIDGET_FONT)
lbl_borrow_search_by.grid(column=1, row=0, sticky="wn", padx=(50,0))

search_options = ["Titre", "Auteur", "Id"]

drp_borrow_search_by = CTkOptionMenu(frm_pages["borrow"], font=WIDGET_FONT, values=search_options, **DROP_LIST_STYLE)
drp_borrow_search_by.set("Titre")
drp_borrow_search_by.grid(column=1, row=0, sticky="en", padx=(0, 50))

lbl_borrow_select = CTkLabel(frm_pages["borrow"], text="Livre sélectionés", font=WIDGET_FONT)
lbl_borrow_select.grid(column=1, row=0, sticky="n", pady=(60, 0))

frm_borrow_selects = CTkScrollableFrame(frm_pages["borrow"])
frm_borrow_selects.grid(column=1, row=0, sticky="ewsn", pady=(100, 0), padx=10)

btn_borrow_select = CTkButton(frm_borrow_selects, text="titre : auteur : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_borrow_select.pack(fill="x", pady=20, padx=20)

#right
ent_borrow_client_searchbar = CTkEntry(frm_pages["borrow"], placeholder_text="Rechercher...", font=WIDGET_FONT)
ent_borrow_client_searchbar.grid(column=2, row=0, sticky="ewn", padx=(20, 0))

frm_borrow_client_results = CTkScrollableFrame(frm_pages["borrow"], height=500)
frm_borrow_client_results.grid(column=2, row=0, sticky="ewn", padx=(20, 0), pady=(60, 0))

btn_borrow_client_result = CTkButton(frm_borrow_client_results, text="Prénom : Nom", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_borrow_client_result.pack(fill="x", pady=20, padx=20)

btn_borrow_client_add = CTkButton(frm_pages["borrow"], text="Nouveau Client+", height=90, font=WIDGET_FONT)
btn_borrow_client_add.grid(column=2, row=0, sticky="ews", padx=(20, 0), pady=(0, 150))

btn_borrow = CTkButton(frm_pages["borrow"], text="Emprunter", height=90, font=WIDGET_FONT)
btn_borrow.grid(column=2, row=0, sticky="ews", padx=(20, 0))
window.mainloop()