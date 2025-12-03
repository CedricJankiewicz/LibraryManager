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


def header_selection(button):

    for i, btn in enumerate(btn_navbar.values()):
        btn.configure(**HEADER_DEFAULT_STYLE)

    btn_navbar[button].configure(**HEADER_ACTIVE_STYLE)


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

##### search window #####
frm_search = CTkFrame(window, fg_color="transparent")
frm_search.pack(expand=True, fill="both", pady=20, padx=20)

frm_search_searching = CTkFrame(frm_search, fg_color="transparent")
frm_search_searching.pack(fill="x", pady=(0, 20), padx=150)

ent_search_searchbar = CTkEntry(frm_search_searching, placeholder_text="Rechercher...", width=400, font=WIDGET_FONT)
ent_search_searchbar.pack(side="left")

search_options = ["Titre", "Auteur", "Id"]

drp_search_search_by = CTkOptionMenu(frm_search_searching, font=WIDGET_FONT, values=search_options, **DROP_LIST_STYLE)
drp_search_search_by.set("Titre")
drp_search_search_by.pack(side="right")

lbl_search_search_by = CTkLabel(frm_search_searching, text="rechercher par : ", font=WIDGET_FONT)
lbl_search_search_by.pack(side="right")

frm_search_results = CTkScrollableFrame(frm_search)
frm_search_results.pack(expand=True, fill="both")

btn_search_result = CTkButton(frm_search_results, text="titre : genre : auteur : maison d\'édition : date de parrution : Disponible", font=DEFAULT_FONT, **SEARCH_RESULT_STYLE)
btn_search_result.pack(fill="x", pady=20, padx=20)

window.mainloop()