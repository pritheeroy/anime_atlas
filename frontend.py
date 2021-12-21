"""
Frontend functions that create tkinter windows and perform manipulations in a visual format
"""
from tkinter import *
import webbrowser

import python_ta

import webscrapping
import io
import tkinter as tk
from pathlib import Path
from PIL import ImageTk, Image
import user
import json
from urllib.request import urlopen

from project2 import token

user_base = []
webscrapping.scrape(user_base)
cc = token.generate_code_challenge()
file = open("code.txt", "r+")
file.truncate(0)
file.close()

cwd = Path.cwd()


def open_url() -> None:
    """Opens tkinter window for log in

    Preconditions:
        - myapp.py is running successfully in the background
        - token.py was successfully imported
    """
    url = token.generate_authorization_url(cc)
    webbrowser.open(url)


def splash_page() -> None:
    """Splash page initialization"""
    global splash_root
    splash_root = tk.Tk()
    splash_root.title('Anime Atlas')
    splash_x = int((splash_root.winfo_screenwidth() / 2) - (800 / 2))
    splash_y = int((splash_root.winfo_screenheight() / 2) - (600 / 2))
    splash_root.geometry(f'{800}x{600}+{splash_x}+{splash_y}')
    splash_root.configure(bg='#2a2a2a')

    # resizing and image formatting to use in the loading screen
    logo = Image.open(f'{cwd}/Anime Atlas Logo.png')
    resized_logo = logo.resize((800, 600), Image.ANTIALIAS)
    splash_logo = ImageTk.PhotoImage(resized_logo)

    # putting the image onto the splash page
    logo_1 = tk.Label(image=splash_logo, bg='#2a2a2a')
    logo_1.pack(side="bottom", fill="both", expand="yes")

    # loading screen lasts for 5000
    splash_root.after(5000, lambda: window())

    splash_root.mainloop()


def window() -> None:
    """Opens the first tkinter page with all GUI elements.

    Preconditions:
        - splash_root() was executed
    """
    splash_root.destroy()

    global root
    root = Tk()

    root.title('Welcome! (Window 1)')
    root_x = int((root.winfo_screenwidth() / 2) - (800 / 2))
    root_y = int((root.winfo_screenheight() / 2) - (600 / 2))
    root.geometry(f'{800}x{600}+{root_x}+{root_y}')
    root.configure(background='#2a2a2a')
    frame = Frame(master=root, width=750, height=550, background='#2a2a2a')
    frame.pack()

    logo_icon = Image.open(f'{cwd}/logo_icon.png')
    resized_logo_icon = logo_icon.resize((120, 138), Image.ANTIALIAS)
    corner_logo = ImageTk.PhotoImage(resized_logo_icon)
    firstlogo = tk.Label(frame, image=corner_logo, bg='#2a2a2a')

    line1 = Label(frame, text='Welcome to Anime Atlas!',
                  fg='#55b3f3', font=('Helvetica', 30), background='#2a2a2a')
    line2 = Label(frame, text='Anime Atlas is a program with four algorithms at your disposal to '
                              'help you, yes you, find anime that fits ',
                  fg='#55b3f3', font=('Helvetica', 16), background='#2a2a2a')
    line3 = Label(frame, text='your taste without having to read and scroll through all '
                              'those anime lists. By using your MyAnimeList',
                  fg='#55b3f3', font=('Helvetica', 16), background='#2a2a2a')
    line4 = Label(frame, text='account or telling us the anime that you have enjoyed, '
                              'we can give you a selection of anime that we think',
                  fg='#55b3f3', font=('Helvetica', 16), background='#2a2a2a')
    line5 = Label(frame, text='you’d like! without having to read and scroll through all those '
                              'anime lists. To refine your search, we have',
                  fg='#55b3f3', font=('Helvetica', 16), background='#2a2a2a')
    line6 = Label(frame, text=' also given you the option to pick the genre and '
                              'number of episodes the recommended anime contains.',
                  fg='#55b3f3', font=('Helvetica', 16), background='#2a2a2a')

    global name_box
    name_box = tk.Entry(frame, bg='#474747', fg='white', width=20)
    name_box_text = tk.Label(frame, text='Please enter your name here: ', fg='white',
                             font=('Helvetica', 18), background='#2a2a2a')

    mal = Button(frame, text='Sign in to My Anime List!', padx=20, pady=6,
                 command=lambda: open_url(), background='white', font=('Helvetica', 15))
    no_anime = Button(frame, text="Don't have an account?", padx=20, pady=6,
                      command=lambda: window2(), background='white', font=('Helvetica', 15))
    nxt = Button(frame, text="Next!", padx=20, pady=6,
                 command=lambda: window3_mal(), background='white', font=('Helvetica', 15))

    firstlogo.place(x=300, y=50)

    line1.place(x=200, y=200)
    line2.place(x=25, y=250)
    line3.place(x=25, y=275)
    line4.place(x=25, y=300)
    line5.place(x=25, y=325)
    line6.place(x=25, y=350)

    name_box.place(x=420, y=420)
    name_box_text.place(x=160, y=420)

    mal.place(x=30, y=500)
    no_anime.place(x=250, y=500)
    nxt.place(x=500, y=500)

    mainloop()


def window2() -> None:
    """Opens the second tkinter page with all GUI elements.

    Preconditions:
        - window() was executed
        - show_data.json has the correct file path
    """
    global name
    name = name_box.get()

    with open('show_data.json') as f:
        anime_data = json.load(f)

    options = []
    for id in anime_data:
        options.append(anime_data[id][0])

    options2 = options
    options3 = options
    options4 = options
    options5 = options

    root.destroy()

    global root2
    root2 = Tk()

    root2.title('Anime Atlas (Window 2)')
    root2_x = int((root2.winfo_screenwidth() / 2) - (800 / 2))
    root2_y = int((root2.winfo_screenheight() / 2) - (600 / 2))
    root2.geometry(f'{800}x{600}+{root2_x}+{root2_y}')
    root2.configure(background='#2a2a2a')

    frame2 = Frame(master=root2, width=750, height=650, background='#2a2a2a')
    frame2.pack()

    logo_icon = Image.open(f'{cwd}/logo_icon.png')
    resized_logo_icon = logo_icon.resize((120, 138), Image.ANTIALIAS)
    corner_logo = ImageTk.PhotoImage(resized_logo_icon)
    secondlogo = tk.Label(frame2, image=corner_logo, bg='#2a2a2a')

    next_page = Button(frame2, text='Continue', padx=30, pady=10,
                       command=lambda: window3_manual(), background='white', font=('Helvetica', 16))

    intro_text = 'Hello ' + name + "! So you don't have a MyAnimeList account."
    introduction = Label(frame2, text=intro_text,
                         fg='#55b3f3', font=('Helvetica', 22), background='#2a2a2a')
    intro_text1 = "Don't worry, just tell us these details to help us recommend some anime for you!"
    introduction1 = Label(frame2, text=intro_text1,
                          fg='#55b3f3', font=('Helvetica', 18), background='#2a2a2a')

    anime_input_text = Label(frame2, text='Please select your top 5 favorite anime from the'
                                          'dropdown menus below!',
                             fg='white', font=('Helvetica', 18), background='#2a2a2a')

    global selection_tag
    global selection_tag2
    global selection_tag3
    global selection_tag4
    global selection_tag5
    selection_tag = tk.StringVar()
    selection_tag.set('Choose Your Favourite Anime!')
    selection_tag2 = tk.StringVar()
    selection_tag2.set('Choose Your 2nd Favourite Anime!')
    selection_tag3 = tk.StringVar()
    selection_tag3.set('Choose Your 3rd Favourite Anime!')
    selection_tag4 = tk.StringVar()
    selection_tag4.set('Choose Your 4th Favourite Anime!')
    selection_tag5 = tk.StringVar()
    selection_tag5.set('Choose Your 5th Favourite Anime!')

    selection1 = tk.OptionMenu(frame2, selection_tag, *options)
    selection2 = tk.OptionMenu(frame2, selection_tag2, *options2)
    selection3 = tk.OptionMenu(frame2, selection_tag3, *options3)
    selection4 = tk.OptionMenu(frame2, selection_tag4, *options4)
    selection5 = tk.OptionMenu(frame2, selection_tag5, *options5)

    secondlogo.place(x=300, y=40)
    introduction.place(x=30, y=225)
    introduction1.place(x=30, y=250)
    anime_input_text.place(x=30, y=280)
    selection1.place(x=30, y=320)
    selection2.place(x=30, y=350)
    selection3.place(x=30, y=380)
    selection4.place(x=30, y=410)
    selection5.place(x=30, y=440)
    next_page.place(x=300, y=550)

    mainloop()


def window3_mal() -> None:
    """Generates an access token using token.py functions

    Preconditions:
        - splash_root() was executed
        - mal.json file path is correct
        - user.py and token.py are imported correctly
    """
    global name
    name = name_box.get()

    root.destroy()

    global at
    z = token.get_code()
    at = token.generate_new_token(z, cc)
    token.generate_user_json(at, {})

    with open('mal.json') as f:
        data = json.load(f)

    data = [(x[0], x[1]) for x in data['user']]
    global user1
    user1 = user.User(name, data)

    window3()


def window3_manual() -> None:
    a1 = selection_tag.get()
    a2 = selection_tag2.get()
    a3 = selection_tag3.get()
    a4 = selection_tag4.get()
    a5 = selection_tag5.get()

    with open('show_data.json') as f:
        anime_data = json.load(f)

    dicto = {}
    for key in anime_data:
        dicto[anime_data[key][0]] = key

    data = [(dicto[a1], 10), (dicto[a2], 9), (dicto[a3], 9), (dicto[a4], 8), (dicto[a5], 8)]
    print(data)
    global user1
    user1 = user.User(name, data)

    root2.destroy()
    window3()


def window3() -> None:
    """Opens 3rd tkinter page

    Preconditions:
        - window2() was executed
        - genre_tag1.get() != 'Choose Your Preferred Genre!'
        - alg_type.get() != 'Type of Algorithm'
        - num_of_anime.get() != 'Number of Anime'
    """

    global root3
    root3 = Tk()
    root3.title('Anime Atlas')
    root3_x = int((root3.winfo_screenwidth() / 2) - (800 / 2))
    root3_y = int((root3.winfo_screenheight() / 2) - (600 / 2))
    root3.geometry(f'{800}x{600}+{root3_x}+{root3_y}')
    root3.configure(background='#2a2a2a')

    frame3 = Frame(master=root3, width=750, height=550, background='#2a2a2a')
    frame3.pack()

    usrname = tk.Label(frame3, text=f'Welcome {name}!',
                       fg='#55b3f3', font=('Helvetica', 25), background='#2a2a2a')
    or_text = tk.Label(frame3, text='OR',
                       fg='#55b3f3', font=('Helvetica', 20), background='#2a2a2a')
    instructions = tk.Label(frame3,
                            text='Please enter the following info to receive anime '
                                 'recommendations!',
                            fg='#55b3f3', font=('Helvetica', 23), background='#2a2a2a')

    global num_of_anime, num_of_episodes, alg_type

    line1 = tk.Label(frame3, text='Do you want to search for anime of specific genres?',
                     fg='white', font=('Helvetica', 20), background='#2a2a2a')
    genre_btn = Button(frame3, text='Open Genre Pop-up!', padx=6, pady=3,
                       command=lambda: genre_question(), background='white')

    line2 = tk.Label(frame3, text='How many anime would you like recommended?',
                     fg='white', font=('Helvetica', 20), background='#2a2a2a')
    numbers = [x for x in range(1, 11)]
    num_of_anime = tk.IntVar()
    num_of_anime.set('Number of Anime')
    drop2 = tk.OptionMenu(frame3, num_of_anime, *numbers)

    line3 = tk.Label(frame3, text='Do you have any preferences for length of anime?',
                     fg='white', font=('Helvetica', 20), background='#2a2a2a')
    numbers2 = ['No preference', 'movie', 'mini-series (~12 eps)', 'medium series (~50 eps)',
                'long series (~100+ eps)']
    num_of_episodes = tk.StringVar()
    num_of_episodes.set('Number of Episodes')
    drop3 = tk.OptionMenu(frame3, num_of_episodes, *numbers2)

    line4 = tk.Label(frame3, text='Which method of recommendation would you like?',
                     fg='white', font=('Helvetica', 20), background='#2a2a2a')
    algs = ['User Comparison', 'Weighting', 'Similarity', 'Searching']
    alg_type = tk.StringVar()
    alg_type.set('Type of Algorithm')
    drop4 = tk.OptionMenu(frame3, alg_type, *algs)

    def genre_question() -> None:
        """Helper functions that create popup window for genre section"""
        popup = tk.Toplevel()
        popup.title('Anime Atlas')
        popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
        popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
        popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
        popup.configure(background='#2a2a2a')

        popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
        popup_frame.pack()

        line1 = Label(popup_frame, text='Please input the genres from the options:',
                      fg='#55b3f3', font=('Helvetica', 16), background='#2a2a2a')
        line2 = Label(popup_frame, text='Psychological, Supernatural, Seinen, Action, Comedy,',
                      fg='white', font=('Helvetica', 16), background='#2a2a2a')
        line3 = Label(popup_frame, text='Shounen, School, Sci-Fi, Drama, Mecha, Adventure, Fantasy',
                      fg='white', font=('Helvetica', 16), background='#2a2a2a')
        line4 = Label(popup_frame, text='Romance, Sports, Slice of Life, Ecchi, Thriller, Horror',
                      fg='white', font=('Helvetica', 16), background='#2a2a2a')
        example = Label(popup_frame, text='Example input: Action, Comedy, Sports',
                        fg='#55b3f3', font=('Helvetica', 16), background='#2a2a2a')

        line5 = Label(popup_frame, text="If you haven't already selected certain genres, "
                                        "do you want us to",
                      fg='white', font=('Helvetica', 16), background='#2a2a2a')
        line6 = Label(popup_frame, text="select based on which genre we think you'll like?",
                      fg='white', font=('Helvetica', 16), background='#2a2a2a')

        global genre_tag1, genre_tag2, genre_tag3
        genres = ['Action', 'Adventure', 'Comedy', 'Drama', 'Sci-Fi', 'Slice of Life', 'Seinen',
                  'Fantasy', 'Mystery', 'Psych', 'Romance', 'Horror', 'Sports', 'Mecha', 'Ecchi']
        genres2 = genres
        genres3 = genres
        genre_tag1 = tk.StringVar()
        genre_tag1.set('Choose Your Preferred Genre!')
        genre_tag2 = tk.StringVar()
        genre_tag2.set('Choose Your 2nd Preferred Genre!')
        genre_tag3 = tk.StringVar()
        genre_tag3.set('Choose Your 3rd Preferred Genre!')
        selection1 = tk.OptionMenu(popup_frame, genre_tag1, *genres)
        selection2 = tk.OptionMenu(popup_frame, genre_tag2, *genres2)
        selection3 = tk.OptionMenu(popup_frame, genre_tag3, *genres3)
        selection1.place(x=30, y=320)
        selection2.place(x=30, y=350)
        selection3.place(x=30, y=380)

        global choice
        choices = ['Yes!', 'No!']
        choice = tk.StringVar()
        choice.set('Choices')
        drop_c = tk.OptionMenu(popup_frame, choice, *choices)

        btn1 = Button(popup_frame, text='Next!', padx=6, pady=3,
                      command=lambda: popup.withdraw(), background='white')

        line1.place(x=30, y=50)
        line2.place(x=30, y=80)
        line3.place(x=30, y=100)
        line4.place(x=30, y=120)
        example.place(x=30, y=150)
        line5.place(x=30, y=420)
        line6.place(x=30, y=440)
        drop_c.place(x=225, y=480)
        btn1.place(x=225, y=520)

    search = Button(frame3, text='Find Recommendations!', padx=6, pady=3,
                    command=lambda: window4(), background='#2a2a2a', font=('Helvetica', 20))
    compare = Button(frame3, text='Compare your anime tastes with a friend!', padx=6, pady=3,
                     command=lambda: compare_window(), background='#2a2a2a', font=('Helvetica', 16))

    search.place(x=250, y=450)
    compare.place(x=225, y=520)
    usrname.place(x=30, y=50)
    or_text.place(x=340, y=485)
    instructions.place(x=30, y=80)
    line1.place(x=30, y=125)
    genre_btn.place(x=30, y=165)
    line2.place(x=30, y=205)
    drop2.place(x=30, y=245)
    line3.place(x=30, y=285)
    drop3.place(x=30, y=325)
    line4.place(x=30, y=365)
    drop4.place(x=30, y=405)

    mainloop()


def window4() -> None:
    """Opens 4th tkinter page"""
    if genre_tag1.get() == 'Choose Your Preferred Genre!':
        genre1 = None
    else:
        genre1 = genre_tag1.get()

    if genre_tag2.get() == 'Choose Your 2nd Preferred Genre!':
        genre2 = None
    else:
        genre2 = genre_tag2.get()

    if genre_tag3.get() == 'Choose Your 3rd Preferred Genre!':
        genre3 = None
    else:
        genre3 = genre_tag3.get()

    if num_of_episodes.get() == 'Number of Episodes' or num_of_episodes.get() == 'No preference':
        episodes = None
    else:
        episodes = num_of_episodes.get()

    if episodes == 'medium series (~50 eps)':
        episodes = 'short series (~26 eps)'

    num_anime = num_of_anime.get()
    alg = alg_type.get()

    if choice.get() == 'Choices':
        genre_check = 'No!'
    else:
        genre_check = choice.get()

    genres = [genre1, genre2, genre3]
    genres1 = [gene for gene in genres if gene is not None]

    global shows
    shows = user1.recommend_shows(num_anime, alg, episodes, genres1, genre_check == "Yes!")

    global root4
    root4 = Tk()
    root4.title('Anime Atlas')
    root4_x = int((root4.winfo_screenwidth() / 2) - (800 / 2))
    root4_y = int((root4.winfo_screenheight() / 2) - (600 / 2))
    root4.geometry(f'{800}x{600}+{root4_x}+{root4_y}')
    root4.configure(background='#2a2a2a')

    frame4 = Frame(master=root4, width=750, height=550, background='#2a2a2a')
    frame4.pack()

    if num_anime == 1:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')

        pop_button.place(x=500, y=25)
        anime.place(x=50, y=25)
    elif num_anime == 2:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)

    elif num_anime == 3:
        print(shows)
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)

    elif num_anime == 4:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime_name4 = shows[3][0] + '   score: ' + str(int(shows[3][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')
        anime4 = tk.Label(frame4, text=anime_name4, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')
        pop_button4 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup4(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        anime4.place(x=50, y=175)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)
        pop_button4.place(x=500, y=175)

    elif num_anime == 5:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime_name4 = shows[3][0] + '   score: ' + str(int(shows[3][3]))
        anime_name5 = shows[4][0] + '   score: ' + str(int(shows[4][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')
        anime4 = tk.Label(frame4, text=anime_name4, fg='white', background='#2a2a2a')
        anime5 = tk.Label(frame4, text=anime_name5, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')
        pop_button4 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup4(), background='white')
        pop_button5 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup5(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        anime4.place(x=50, y=175)
        anime5.place(x=50, y=225)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)
        pop_button4.place(x=500, y=175)
        pop_button5.place(x=500, y=225)

    elif num_anime == 6:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime_name4 = shows[3][0] + '   score: ' + str(int(shows[3][3]))
        anime_name5 = shows[4][0] + '   score: ' + str(int(shows[4][3]))
        anime_name6 = shows[5][0] + '   score: ' + str(int(shows[5][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')
        anime4 = tk.Label(frame4, text=anime_name4, fg='white', background='#2a2a2a')
        anime5 = tk.Label(frame4, text=anime_name5, fg='white', background='#2a2a2a')
        anime6 = tk.Label(frame4, text=anime_name6, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')
        pop_button4 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup4(), background='white')
        pop_button5 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup5(), background='white')
        pop_button6 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup6(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        anime4.place(x=50, y=175)
        anime5.place(x=50, y=225)
        anime6.place(x=50, y=275)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)
        pop_button4.place(x=500, y=175)
        pop_button5.place(x=500, y=225)
        pop_button6.place(x=500, y=275)

    elif num_anime == 7:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime_name4 = shows[3][0] + '   score: ' + str(int(shows[3][3]))
        anime_name5 = shows[4][0] + '   score: ' + str(int(shows[4][3]))
        anime_name6 = shows[5][0] + '   score: ' + str(int(shows[5][3]))
        anime_name7 = shows[6][0] + '   score: ' + str(int(shows[6][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')
        anime4 = tk.Label(frame4, text=anime_name4, fg='white', background='#2a2a2a')
        anime5 = tk.Label(frame4, text=anime_name5, fg='white', background='#2a2a2a')
        anime6 = tk.Label(frame4, text=anime_name6, fg='white', background='#2a2a2a')
        anime7 = tk.Label(frame4, text=anime_name7, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')
        pop_button4 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup4(), background='white')
        pop_button5 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup5(), background='white')
        pop_button6 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup6(), background='white')
        pop_button7 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup7(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        anime4.place(x=50, y=175)
        anime5.place(x=50, y=225)
        anime6.place(x=50, y=275)
        anime7.place(x=50, y=325)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)
        pop_button4.place(x=500, y=175)
        pop_button5.place(x=500, y=225)
        pop_button6.place(x=500, y=275)
        pop_button7.place(x=500, y=325)

    elif num_anime == 8:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime_name4 = shows[3][0] + '   score: ' + str(int(shows[3][3]))
        anime_name5 = shows[4][0] + '   score: ' + str(int(shows[4][3]))
        anime_name6 = shows[5][0] + '   score: ' + str(int(shows[5][3]))
        anime_name7 = shows[6][0] + '   score: ' + str(int(shows[6][3]))
        anime_name8 = shows[7][0] + '   score: ' + str(int(shows[7][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')
        anime4 = tk.Label(frame4, text=anime_name4, fg='white', background='#2a2a2a')
        anime5 = tk.Label(frame4, text=anime_name5, fg='white', background='#2a2a2a')
        anime6 = tk.Label(frame4, text=anime_name6, fg='white', background='#2a2a2a')
        anime7 = tk.Label(frame4, text=anime_name7, fg='white', background='#2a2a2a')
        anime8 = tk.Label(frame4, text=anime_name8, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')
        pop_button4 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup4(), background='white')
        pop_button5 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup5(), background='white')
        pop_button6 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup6(), background='white')
        pop_button7 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup7(), background='white')
        pop_button8 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup8(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        anime4.place(x=50, y=175)
        anime5.place(x=50, y=225)
        anime6.place(x=50, y=275)
        anime7.place(x=50, y=325)
        anime8.place(x=50, y=375)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)
        pop_button4.place(x=500, y=175)
        pop_button5.place(x=500, y=225)
        pop_button6.place(x=500, y=275)
        pop_button7.place(x=500, y=325)
        pop_button8.place(x=500, y=375)

    elif num_anime == 9:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime_name4 = shows[3][0] + '   score: ' + str(int(shows[3][3]))
        anime_name5 = shows[4][0] + '   score: ' + str(int(shows[4][3]))
        anime_name6 = shows[5][0] + '   score: ' + str(int(shows[5][3]))
        anime_name7 = shows[6][0] + '   score: ' + str(int(shows[6][3]))
        anime_name8 = shows[7][0] + '   score: ' + str(int(shows[7][3]))
        anime_name9 = shows[8][0] + '   score: ' + str(int(shows[8][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')
        anime4 = tk.Label(frame4, text=anime_name4, fg='white', background='#2a2a2a')
        anime5 = tk.Label(frame4, text=anime_name5, fg='white', background='#2a2a2a')
        anime6 = tk.Label(frame4, text=anime_name6, fg='white', background='#2a2a2a')
        anime7 = tk.Label(frame4, text=anime_name7, fg='white', background='#2a2a2a')
        anime8 = tk.Label(frame4, text=anime_name8, fg='white', background='#2a2a2a')
        anime9 = tk.Label(frame4, text=anime_name9, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')
        pop_button4 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup4(), background='white')
        pop_button5 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup5(), background='white')
        pop_button6 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup6(), background='white')
        pop_button7 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup7(), background='white')
        pop_button8 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup8(), background='white')
        pop_button9 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup9(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        anime4.place(x=50, y=175)
        anime5.place(x=50, y=225)
        anime6.place(x=50, y=275)
        anime7.place(x=50, y=325)
        anime8.place(x=50, y=375)
        anime9.place(x=50, y=425)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)
        pop_button4.place(x=500, y=175)
        pop_button5.place(x=500, y=225)
        pop_button6.place(x=500, y=275)
        pop_button7.place(x=500, y=325)
        pop_button8.place(x=500, y=375)
        pop_button9.place(x=500, y=425)

    elif num_anime == 10:
        anime_name = shows[0][0] + '   score: ' + str(int(shows[0][3]))
        anime_name2 = shows[1][0] + '   score: ' + str(int(shows[1][3]))
        anime_name3 = shows[2][0] + '   score: ' + str(int(shows[2][3]))
        anime_name4 = shows[3][0] + '   score: ' + str(int(shows[3][3]))
        anime_name5 = shows[4][0] + '   score: ' + str(int(shows[4][3]))
        anime_name6 = shows[5][0] + '   score: ' + str(int(shows[5][3]))
        anime_name7 = shows[6][0] + '   score: ' + str(int(shows[6][3]))
        anime_name8 = shows[7][0] + '   score: ' + str(int(shows[7][3]))
        anime_name9 = shows[8][0] + '   score: ' + str(int(shows[8][3]))
        anime_name10 = shows[9][0] + '   score: ' + str(int(shows[9][3]))
        anime = tk.Label(frame4, text=anime_name, fg='white', background='#2a2a2a')
        anime2 = tk.Label(frame4, text=anime_name2, fg='white', background='#2a2a2a')
        anime3 = tk.Label(frame4, text=anime_name3, fg='white', background='#2a2a2a')
        anime4 = tk.Label(frame4, text=anime_name4, fg='white', background='#2a2a2a')
        anime5 = tk.Label(frame4, text=anime_name5, fg='white', background='#2a2a2a')
        anime6 = tk.Label(frame4, text=anime_name6, fg='white', background='#2a2a2a')
        anime7 = tk.Label(frame4, text=anime_name7, fg='white', background='#2a2a2a')
        anime8 = tk.Label(frame4, text=anime_name8, fg='white', background='#2a2a2a')
        anime9 = tk.Label(frame4, text=anime_name9, fg='white', background='#2a2a2a')
        anime10 = tk.Label(frame4, text=anime_name10, fg='white', background='#2a2a2a')

        pop_button = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                               command=lambda: anime_popup1(), background='white')
        pop_button2 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup2(), background='white')
        pop_button3 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup3(), background='white')
        pop_button4 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup4(), background='white')
        pop_button5 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup5(), background='white')
        pop_button6 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup6(), background='white')
        pop_button7 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup7(), background='white')
        pop_button8 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup8(), background='white')
        pop_button9 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                command=lambda: anime_popup9(), background='white')
        pop_button10 = tk.Button(frame4, text='Information about anime', padx=6, pady=3,
                                 command=lambda: anime_popup10(), background='white')

        anime.place(x=50, y=25)
        anime2.place(x=50, y=75)
        anime3.place(x=50, y=125)
        anime4.place(x=50, y=175)
        anime5.place(x=50, y=225)
        anime6.place(x=50, y=275)
        anime7.place(x=50, y=325)
        anime8.place(x=50, y=375)
        anime9.place(x=50, y=425)
        anime10.place(x=50, y=475)
        pop_button.place(x=500, y=25)
        pop_button2.place(x=500, y=75)
        pop_button3.place(x=500, y=125)
        pop_button4.place(x=500, y=175)
        pop_button5.place(x=500, y=225)
        pop_button6.place(x=500, y=275)
        pop_button7.place(x=500, y=325)
        pop_button8.place(x=500, y=375)
        pop_button9.place(x=500, y=425)
        pop_button10.place(x=500, y=475)

    restart_button = Button(frame4, text='Change recommendation options', padx=6, pady=3,
                            command=lambda: root4.destroy(), background='white')
    restart_button.place(x=400, y=520)

    graph_button = Button(frame4, text='Graph 1', padx=6, pady=3,
                          command=lambda: user1.call_visualizer1(), background='white')
    graph_button2 = Button(frame4, text='Graph 2', padx=6, pady=3,
                           command=lambda: user1.call_visualizer2(), background='white')
    graph_button3 = Button(frame4, text='Graph 3', padx=6, pady=3,
                           command=lambda: user1.call_visualizer3(), background='white')
    graph_button.place(x=30, y=520)
    graph_button2.place(x=130, y=520)
    graph_button3.place(x=230, y=520)

    mainloop()


def anime_popup1() -> None:
    """popup window for image and synopsis of 1st recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[0][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image2 = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image2, bg='#2a2a2a')

    synopsis1 = shows[0][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup2() -> None:
    """popup window for image and synopsis of 2nd recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[1][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[1][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup3() -> None:
    """popup window for image and synopsis of 3rd recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[2][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[2][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup4() -> None:
    """popup window for image and synopsis of 4th recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[3][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[3][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup5() -> None:
    """popup window for image and synopsis of 5th recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[4][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[4][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup6() -> None:
    """popup window for image and synopsis of 6th recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[5][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[5][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)

    mainloop()


def anime_popup7() -> None:
    """popup window for image and synopsis of 7th recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[6][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[6][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup8() -> None:
    """popup window for image and synopsis of 8th recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[7][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[7][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup9() -> None:
    """popup window for image and synopsis of 9th recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[8][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[8][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def anime_popup10() -> None:
    """popup window for image and synopsis of 10th recommended anime

    Preconditions:
        - Window4() is running
    """
    popup = tk.Toplevel()
    popup.title('Anime Atlas')
    popup_x = int((popup.winfo_screenwidth() / 2) - (500 / 2))
    popup_y = int((popup.winfo_screenheight() / 2) - (600 / 2))
    popup.geometry(f'{500}x{600}+{popup_x}+{popup_y}')
    popup.configure(background='#2a2a2a')

    popup_frame = Frame(master=popup, width=750, height=550, background='#2a2a2a')
    popup_frame.pack()

    image_url = shows[9][1]
    image_byt = urlopen(image_url).read()
    data_stream = io.BytesIO(image_byt)
    pil_image = Image.open(data_stream)
    resized = pil_image.resize((150, 225), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resized)
    image_label = tk.Label(popup_frame, image=image, bg='#2a2a2a')

    synopsis1 = shows[9][2]
    syn_acc = ''
    for i in range(0, len(synopsis1)):
        syn_acc = syn_acc + synopsis1[i]
        if synopsis1[i] == '.':
            break

    if len(syn_acc) > 55:
        addon = (4 - (len(syn_acc) % 4))
        syn_acc += (addon * ' ')
        line_length = int(len(syn_acc) / 4)
        broken_synacc = [syn_acc[line_length * x: line_length * (x + 1)] for x in range(4)]

        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {broken_synacc[0]}', fg='white',
                                  background='#2a2a2a')
        synopsis_label2 = tk.Label(popup_frame, text=broken_synacc[1], fg='white',
                                   background='#2a2a2a')
        synopsis_label3 = tk.Label(popup_frame, text=broken_synacc[2], fg='white',
                                   background='#2a2a2a')
        synopsis_label4 = tk.Label(popup_frame, text=broken_synacc[3], fg='white',
                                   background='#2a2a2a')
        synopsis_label.place(x=25, y=300)
        synopsis_label2.place(x=25, y=325)
        synopsis_label3.place(x=25, y=350)
        synopsis_label4.place(x=25, y=375)
    else:
        synopsis_label = tk.Label(popup_frame, text=f'Synopsis: {syn_acc}', fg='white',
                                  background='#2a2a2a')
        synopsis_label.place(x=25, y=300)

    image_label.place(x=100, y=25)
    synopsis_label.place(x=25, y=300)

    mainloop()


def compare_window() -> None:
    """Allows user to compare there myanimelist with another users given that user's username

    Preconditions:
        - Window4() is running
        - username is a valid mal username
    """
    global root5
    root5 = tk.Toplevel()
    root5.title('Anime Atlas')
    root5_x = int((root5.winfo_screenwidth() / 2) - (800 / 2))
    root5_y = int((root5.winfo_screenheight() / 2) - (600 / 2))
    root5.geometry(f'{800}x{600}+{root5_x}+{root5_y}')
    root5.configure(background='#2a2a2a')

    frame5 = Frame(master=root5, width=750, height=550, background='#2a2a2a')
    frame5.pack()

    compare_label = Label(frame5, text="You want to compare your anime preferences with a friend "
                                       "with a MyAnimeList account?",
                          fg='white', font=('Helvetica', 16), background='#2a2a2a')
    compare_label2 = Label(frame5, text="Enter your friend's MyAnimeList username: ",
                           fg='white', font=('Helvetica', 16), background='#2a2a2a')

    global compare_user
    compare_user = tk.Entry(frame5, bg='#474747', fg='white', width=20)

    logo_icon = Image.open(f'{cwd}/logo_icon.png')
    resized_logo_icon = logo_icon.resize((120, 138), Image.ANTIALIAS)
    corner_logo = ImageTk.PhotoImage(resized_logo_icon)
    comparelogo = tk.Label(frame5, image=corner_logo, bg='#2a2a2a')

    submit = tk.Button(frame5, text='Submit', padx=6, pady=3,
                       command=lambda: compare_results(), background='white')

    comparelogo.place(x=310, y=50)
    compare_label.place(x=30, y=230)
    compare_label2.place(x=30, y=250)
    compare_user.place(x=270, y=350)
    submit.place(x=330, y=500)

    def compare_results() -> None:
        """Function for calculating similarity value

        Preconditions:
        - every key value pair in user1.mal in AnimeDict, AnimeSet = anime.main()
        - every key value pair in user2.mal in AnimeDict, AnimeSet = anime.main()
        - user1 has a logged in my anime account

        """
        username = compare_user.get()
        user2_mal = {}
        token.generate_user2_json(at, username, user2_mal)

        root5.destroy()

        mal = {}
        token.generate_user_json(at, mal)
        user2 = user.User(username, user2_mal['user'])
        output = user1.compare_user(user2)

        global root6
        root6 = tk.Toplevel()
        root6.title('Anime Atlas')
        root6_x = int((root6.winfo_screenwidth() / 2) - (800 / 2))
        root6_y = int((root6.winfo_screenheight() / 2) - (600 / 2))
        root6.geometry(f'{800}x{600}+{root6_x}+{root6_y}')
        root6.configure(background='#2a2a2a')

        frame6 = Frame(master=root6, width=750, height=550, background='#2a2a2a')
        frame6.pack()

        score = Label(frame6, text=f'{output}',
                      fg='#55b3f3', font=('Helvetica', 40), background='#2a2a2a')
        score_text = Label(frame6, text='Your Comparison Score Is:',
                           fg='white', font=('Helvetica', 25), background='#2a2a2a')
        score.place(x=310, y=250)
        score_text.place(x=200, y=200)

    mainloop()


def main():
    splash_page()


python_ta.check_all(config={
    'extra-imports': [],  # the names (strs) of imported modules
    'allowed-io': [],  # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['E1136']
})
