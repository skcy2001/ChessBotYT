import tkinter as tk
from tkinter import *
from tkinter import font, PhotoImage, ttk 
from threading import *
from collections import defaultdict
import urllib, PIL.Image, PIL.ImageTk, sys, re, pytchat, os

id = "5qap5aO4i9A"
image = []
image2 = []
chat = pytchat.create(video_id=id)
votes = defaultdict(int)
voters = defaultdict(list)
item = ''
banwords = []

# Function to check for a valid chess move and register it in left and middle pannel
def register(c):
    global image, votes, voters
    txt = c.message.lower().strip()
    moves = re.findall(# Currently set to any word for testing purposes
        r"\b([nbrqk])*([a-h])*([1-8])*(x)*([a-h][1-8])+(=[nbrqk])*(\+|#)*|\b(o-o)+(-o)*|(^$.+)|(.)",
        txt, 
    )
    if(len(moves) > 0):
        san = "".join(moves[0]).strip("!")
        name = "thumbnail.png"
        try:
            urllib.request.urlretrieve(c.author.imageUrl, name)
            img = PIL.Image.open(name).resize((20, 20))
            image.append(PIL.ImageTk.PhotoImage(img))
        except: pass
        votes[san] += 1
        voters[san].append(c)     
        TV.insert(
            "",
            0,
            text="",
            image=image[-1],
            values=(c.author.name, san),
            tags=len(image) % 2,
        )
        
        res = {val[0] : val[1] for val in sorted(votes.items(), key = lambda x: (-x[1], x[0]))}
        
        if not TV2.exists(san):
            TV2.insert("","end",text="", iid = san, value=(san,res[san]))
        else:
            TV2.set(san,'Count',votes[san])
            if not TV2.index(san) == list(res.keys()).index(san):
                TV2.move(san, TV2.parent(san), list(res.keys()).index(san))
    else:
        pass

# Function to extract url from given link 
def urlstart():
    global idx, image, chat
    url2 = url.get()
    id = re.findall(
        r"(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*)", url2
    )
    try:
        id = id[0][1]
        url.set(id)
        chat = pytchat.create(video_id=id)
        B1['state'] = 'disabled'
        E1['state'] = 'disabled'
        L2.config(text="")
        thread(chat_update)
    except:
        url.set('')
        L2.config(text="Enter Valid URL")
        pass

# threading function for multithreading
def thread(func):
    t1 = Thread(target=func)
    t1.daemon=True
    t1.start()

# function to start registering
def chat_update():
    global chat, reset_flag
    while True:
        for c in chat.get().sync_items():
            register(c)
                
#tkinter gui bug-fixing
def fixed_map(option):
    # Returns the style map for 'option' with any styles starting with
    # ("!disabled", "!selected", ...) filtered out

    # style.map() returns an empty list for missing options, so this should
    # be future-safe
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]

# function to reset the panels
def reset():
    global votes,voters
    for item in TV2.get_children():
            TV2.delete(item)
    for item in TV.get_children():
            TV.delete(item)
    for item in TV3.get_children():
            TV3.delete(item)
            
    votes.clear()
    voters.clear()

# threading function for right panel
def ODC(e):
    t1 = Thread(target=ODCt)
    t1.daemon=True
    t1.start()

# on-double-click action for a row in left pannel
def ODCt():
    global voters, image2
    move = TV2.item(TV2.focus(), 'values')[0]
    if LB3['text'] == f'People who said "{move}"':
        sys.exit()
    LB3.config(text = f'People who said "{move}"')
    i = 0
    try:
        while move == TV2.item(TV2.focus(), 'values')[0]:
            for x in voters[move]:
                if not move == TV2.item(TV2.focus(), 'values')[0]:
                    break
                if not TV3.exists(x.datetime):
                    name = "thumbnail2.png"
                    try:
                        urllib.request.urlretrieve(x.author.imageUrl, name)
                        img2 = PIL.Image.open(name).resize((20, 20))
                        image2.append(PIL.ImageTk.PhotoImage(img2))
                    except: pass

                    TV3.insert(
                        "",
                        'end',
                        iid = x.datetime,
                        text="",
                        image=image2[-1],
                        values=(x.author.name,x.datetime),
                        tag = i % 2
                    )
                    i += 1
    except:
        pass            
    for item in TV3.get_children():
        TV3.delete(item)

# to be developed banning mechanism
def ban(e):
    global banwords
    banwords.append(TV2.item(TV2.focus(), 'values')[0])

root = tk.Tk()

# Fonts and colour theme configuration
title_font = font.Font(size=10, family="Calibri", weight="bold")
body_font = font.Font(size=10, family="Calibri")
basec = '#f0f0f0'
lightc = '#ffffff'
accent1c = '#fefefe'
accent2c = '#eeeeee'
font1c = '#010101'
font2c = '#010101'

style = ttk.Style()
style.map("Treeview", 
          foreground=fixed_map("foreground"),
          background=fixed_map("background"),
          fieldbackground=fixed_map("fieldbackground")
          )
style.configure(
    "Treeview",
    font=body_font,
    background=lightc,
    foreground=font1c,
    fieldbackground=lightc,
    rowheight=27,
)

# Tkinter window configuration    
root.geometry("900x490")
root.title("Youtube Chatbot")
root.configure(padx=5, pady=5, bg= basec)
root.iconbitmap('Icon.ico')

# Pane layout configuration
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)
root.columnconfigure(2, weight=6)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=15)
root.rowconfigure(2, weight=1)


""" PANE 1 STARTs HERE """

pane1 = tk.Frame(root,bg=basec)
pane1.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=2.5,padx=100)

url = StringVar(root)

L2 = tk.Label(pane1, text="", font=body_font, foreground='red',bg=basec)
L2.pack(fill = 'x')

L1 = tk.Label(pane1, text="Enter Video URL:", foreground=font1c,font=title_font,bg=basec)
L1.pack(side=LEFT)

E1 = tk.Entry(pane1, bd=2, textvariable=url, foreground=font1c,font=body_font,bg=lightc)
E1.pack(expand=True, side=LEFT, fill="x",ipady=2,padx=5)

B1 = tk.Button(pane1, text=" Go ", font=body_font, foreground=font1c, command=urlstart,bg=basec)
B1.pack(side=LEFT,ipady=0)

""" PANE 2 STARTs HERE """

pane2 = tk.Frame(root, relief="groove", bd=2,bg=basec)
pane2.grid(row=1, column=0, sticky="nsew", pady=2.5, padx=2.5)

LB3 = tk.Label(pane2,text='Summary',font=title_font, foreground=font1c, bg=basec)
LB3.pack(side=TOP,fill='x')

TV2 = ttk.Treeview(pane2, columns=("Move","Count"), style = 'Treeview', padding=5, show = 'tree')
TV2.column("#0", width = 0, stretch = NO, anchor="w")
TV2.column("Move", minwidth = 0, width = 30, anchor="w")
TV2.column("Count", minwidth = 0, width = 30, anchor="e")
TV2.heading("Move", text="Name", anchor=CENTER)
TV2.bind("<Double-1>", ODC)

TV2.pack(side=LEFT, fill="both", padx=7, pady=7, expand=True)

SB2 = Scrollbar(pane2, command=TV2.yview,bg=basec,activebackground=basec)
SB2.pack(side=RIGHT, fill="y")
TV2.config(yscrollcommand=SB2.set)

""" PANE 3 STARTs HERE """

pane3 = tk.Frame(root, relief="groove", bd=2,bg=basec)
pane3.grid(row=1, column=1, sticky="nsew", pady=2.5, padx=2.5)

LB2 = tk.Label(pane3,text='Live feed',font=title_font, foreground=font1c, bg=basec)
LB2.pack(side=TOP,fill='x')

TV = ttk.Treeview(pane3, columns=("Name", "Message"), style = 'Treeview', padding=5, show = 'tree')
TV.column("#0", width=45, minwidth = 0, stretch=NO, anchor="e")
TV.column("Name", width=60, minwidth = 0)
TV.column("Message", width=55, minwidth = 0, anchor="e", stretch=NO)
TV.heading("Name", text="Name", anchor=CENTER)
TV.heading("Message", text="Move", anchor=CENTER)

TV.pack(side=LEFT, fill="both", padx=7, pady=7, expand=True)

TV.tag_configure(0, background=accent1c)
TV.tag_configure(1, background=accent2c)

SB = Scrollbar(pane3, command=TV.yview,bg=basec,activebackground=basec)
SB.pack(side=RIGHT, fill="y")
TV.config(yscrollcommand=SB.set)

""" PANE 4 STARTs HERE """

pane4 = tk.Frame(root,bg=basec)
pane4.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=2.5, padx=2.5)

B2 = tk.Button(pane4, text="Reset", font=body_font, foreground=font1c, command=reset,bg=basec)
B2.pack(side=RIGHT,ipady=0,padx = 2)

B3 = tk.Button(pane4, text="Quit", font=body_font, foreground=font1c, command=sys.exit,bg=basec)
B3.pack(side=RIGHT,ipady=0, padx = 2)

#B4 = tk.Button(pane4, text="Restart", font=body_font, foreground=font1c, command=restart_program,bg=basec)
#B4.pack(side=RIGHT,ipady=0, padx = 2)

""" PANE 5 STARTs HERE """

pane5 = tk.Frame(root,bg=basec, bd=2, relief='groove')
pane5.grid(row=1, column=2, sticky="nsew", pady=2.5, padx=2.5)

LB3 = tk.Label(pane5,text='Commentors',font=title_font, foreground=font1c, bg=basec)
LB3.pack(side=TOP,fill='x')

TV3 = ttk.Treeview(pane5, columns=("Names","Timestamp"), style = 'Treeview', padding=5, show = 'tree')
TV3.column("#0", width = 45, stretch = NO, anchor="w")
TV3.column("Names", minwidth = 0, width = 40, anchor="w")
TV3.column("Timestamp", minwidth = 0, width = 40, anchor="e")
TV3.heading("Names", text="Names", anchor=CENTER)

TV3.tag_configure(0, background=accent1c)
TV3.tag_configure(1, background=accent2c)


TV3.pack(side=LEFT, fill="both", padx=7, pady=7, expand=True)

SB3 = Scrollbar(pane5, command=TV3.yview,bg=basec,activebackground=basec)
SB3.pack(side=RIGHT, fill="y")
TV3.config(yscrollcommand=SB3.set)

root.mainloop()
sys.exit()