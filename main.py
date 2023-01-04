from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import random
from tkinter import *
lahto = 'https://en.wikipedia.org'
sites = []
used_hrefs = [] 
i = 0
times = 0
urli = ''

# Setting up web scraping things
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# This is where the magic happens
def get_random_wiki():
    global times,i,lahto,used_hrefs,sites,urli
    i += 1
    wiki = session.get(urli).text
    souped_wiki = g_soup(wiki)  
    sites.append(souped_wiki.find(id="firstHeading").text)
    hrefs = []
    for a in souped_wiki.find_all('a', href=True):
        if a['href'][0:6] == '/wiki/' and not any(x in a['href'] for x in [':','#']) and 'Main_Page' not in a['href'] and '(identifier)' not in a['href'] and 'commons.wikimedia.org' not in a['href'] and 'species.wikimedia.org' not in a['href'] and 'Wikisitaatit' not in a['href'] and 'identifier' not in a['href']:
            hrefs.append(a['href'])
    hrefs_removed_already_used_ones = [x for x in hrefs if x not in used_hrefs]
    if i < times:
        try:              
            urli = lahto + random.choice(hrefs_removed_already_used_ones)
            used_hrefs.append('/wiki/' + urli.split('/')[-1])
        except:
            urli = lahto + used_hrefs[-1]
    else:
        sites.pop(0)
        site = random.choice(sites)
        path = sites[:sites.index(site)+1]
        print('\nPath:')
        for xx in path:
            print(xx)   
        print('\nResult:\n', site) 
    print(f"Done: {int(i/times*100)}%")

# Setting the depth (how many links down will get from seed)
def set_depth():
    global times
    times = int(depth_Input.get())

# Refreshing variables for multiple uses and starting the process
def start():
    global sites,used_hrefs,i,urli
    sites = []
    used_hrefs = [] 
    i = 0
    urli = seed_Input.get()
    for x in range(times):
        get_random_wiki()

# Setting languages
def finnish():
    global lahto
    lahto = 'https://fi.wikipedia.org'

def english():
    global lahto
    lahto = 'https://en.wikipedia.org'


def vaihda(e_f):
    global lahto
    if e_f == 0:
        lahto = 'https://en.wikipedia.org'
    else:
        lahto = 'https://fi.wikipedia.org'   

# Souping
def g_soup(text):
    soup = BeautifulSoup(text, 'lxml')
    return soup

# For info window
def New_Window():
    Window = Toplevel()
    canvas = Canvas(Window, height=200, width=800)
    label4 = Label(canvas, text="Put a random Wikipedia site to seed (whole address) (seed will not part of the draw)\nPut a number of how deep (how many links) you want the draw to go from the seed (more bigger number = longer processing time and more random result) (recommended depth = 100-1000)\nResult will be printed to the terminal and also the path to the result from the seed")
    label4.pack() 
    canvas.pack()
 
#UI stuff
root = Tk()
root.geometry('500x500')
root.title('Random Wikipedia site')

info_B = Button(text ="Info", command = New_Window)
info_B.pack()
seed_L = Label( root, text="seed:")
seed_L.pack()

seed_Input = Entry(root)
seed_Input.pack()
seed_Input.focus_set()

label2 = Label( root, text="Wikipedia layers from seed:")
label2.pack() 

depth_Input = Entry(root)
depth_Input.pack()
depth_Input.focus_set()

label3 = Label( root, text="Choose Wikipedia language:")
label3.pack() 

english_B = Button(text ="English Wikipedia (default)", command = english)
english_B.pack()

finnish_B = Button(text ="Finnish Wikipedia", command = finnish)
finnish_B.pack()

randomize_B = Button(text ="Get random Wikipedia site", command = lambda: [f() for f in [set_depth, start]])
randomize_B.pack()


root.mainloop()
   
