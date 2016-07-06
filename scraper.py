import requests
import bs4
import webbrowser
from tkinter import *


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class slickPage(Page):
    def __init__(self,  deals, *args, **kwargs): ##Take param deals for different pages
        Page.__init__(self, *args, **kwargs)
        self.deals = deals
        self.createLabels()
        self.createList()

    def createLabels(self):
        self.dealLabel = Label(self, text='Deal', foreground='red')
        self.priceLabel = Label(self, text='Price', foreground='red')
        self.dealLabel.grid(row=1, column=0, sticky=NW)
        self.priceLabel.grid(row=1, column=6, columnspan=4)

    def createList(self):
        for num, deal in enumerate(self.deals):
            self.deal = Label(self, text=deal[0])
            self.deal.bind('<Button-1>', self.make_lambda(deal[2]))
            self.deal.grid(row=num+2, column=0, columnspan=6, sticky=W)
            self.price = Label(self, text='${}'.format(deal[1]))
            self.price.grid(row=num+2, column=6, columnspan=4)

    def openLink(self, link):
        webbrowser.open_new(r'http://www.slickdeals.com' + link)

    def make_lambda(self, link):
        return lambda event: self.openLink(link)


class redditPage(Page):
    '''Creates frame for Build a PC Sales subreddit. Displays all the
       deals and their prices'''
    def __init__(self, deals, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.deals = deals
        self.createLabels()
        self.createList()

    def createLabels(self):
        self.dealLabel = Label(self, text='Deal', foreground='red')
        self.priceLabel = Label(self, text='Price', foreground='red')
        self.dealLabel.grid(row=1, column=0, sticky=NW)
        self.priceLabel.grid(row=1, column=6, columnspan=4)

    def createList(self):
        for num, deal in enumerate(self.deals):
            self.deal = Label(self, text=deal[0])
            self.deal.grid(row=num+2, column=0, columnspan=6, sticky=W)
            self.deal.bind('<Button-1>', self.make_lambda(deal[2]))
            self.price = Label(self, text='${}'.format(deal[1]))
            self.price.grid(row=num+2, column=6, columnspan=4)

    def openLink(self, link):
        webbrowser.open_new(link)

    def make_lambda(self, link):
        return lambda event: self.openLink(link)


class Main(Frame):
    '''Initializes the main frame and button frame.  Creates
       all frames and places them in the main frame.'''
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        # Frame for taskbar
        taskbar = Frame(self)
        # Container, or main frame
        self.container = Frame(self)

        # Create all pages for scrapers
        slickPages = self.createPages(slickScraper(), slickPage)
        redditPages = self.createPages(redditScraper(), redditPage)

        taskbar.pack(side='top', fill='x', expand=False)
        self.container.pack(side='top', fill='both', expand=True)

        # Creates buttons for taskbar
        slickButton = Button(taskbar, text='Slick Deals',
                             command=slickPages[0].lift)
        slickButton.grid(row=0, sticky=W+E)

        redditButton = Button(taskbar, text='Build a PC',
                              command=redditPages[0].lift)
        redditButton.grid(row=0, column=1, sticky=W+E)

        # Show the first slickdeals page. Homepage
        slickPages[0].show()

    def createPages(self, deals, pageType):
        pages = {}
        # Create page frame and place in main frame
        for page in deals:
            pages[page] = pageType(master=self, deals=deals[page])
            pages[page].place(in_=self.container, x=0,
                              y=0, relwidth=1, relheight=1)
        # Create forward and backward buttons depending on what page number
        for page in pages:
            if page == 0 and len(pages) > 1:
                forwardButton = Button(pages[page], text='Next',
                                       command=pages[page+1].lift)
                forwardButton.grid(row=22, column=10)
            elif page == len(pages) - 1 and len(pages) > 1:
                backButton = Button(pages[page], text='Back',
                                    command=pages[page-1].lift)
                backButton.grid(row=22, column=9)
            elif len(pages) == 1:
                break
            else:
                forwardButton = Button(pages[page], text='Next',
                                       command=pages[page+1].lift)
                forwardButton.grid(row=22, column=10)
                backButton = Button(pages[page], text='Back',
                                    command=pages[page-1].lift)
                backButton.grid(row=22, column=9)
        return pages

def slickScraper():
    '''Scrapes all the front page deals from slickdeals.net. Breaks
       up the HTML doc into deals and their respective prices in a
       list. Puts all deals in a dict, with the page number as the key.
       Returns: Pages, which is a dictionary'''
    deals = []
    # Gets html text
    res = requests.get('http://slickdeals.net')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # Finds all deals and their links
    items = soup.find_all(class_='itemTitle')
    # # Break up html doc into deal(string) and price, puts into list with link
    for item in items:
        deal = item.get('title').split('$', 1)
        if len(deal) == 1:
            deal.append('No price')
        link = item.get('href')
        deal.append(link)
        deals.append(deal)
    pages = {}
    i = 0
    # Breaks up deals into pages of 20 items and places into page[deal] dict
    for page in range(int(len(deals)/20)):
        if i + 20 < len(deals):
            pages[page] = deals[i:i+20]
            i += 20
        else:
            pages[page] = deals[i:]
    return pages


def redditScraper():
    '''Scrapes all the front page deals from the Build a pc sales
       subreddit. Breaks up the HTML doc into deals and their
       respective prices in alist. Puts all deals in a dict,
       with the page number as the key.
       Returns: Pages, which is a dictionary'''
    deals = []
    temp = []
    links = []
    # Gets html text
    while True:
        try:
            res = requests.get('https://www.reddit.com/r/buildapcsales')
            res.raise_for_status()
            break
        except requests.exceptions.HTTPError:
            continue
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # Finds all deals and their links
    for item in soup.find_all(class_='title may-blank '):
        links.append(item.get('href'))
        temp.append(str(item))
    for item in soup.find_all(class_='title may-blank affiliate'):
        links.append(item.get('href'))
        temp.append(str(item))
    findname = re.compile('\>(.+)\<')
    findprice = re.compile('\$(\d+[\.\d{2}]*)')
    # Break up html doc into deal(string) and price, puts into list with link
    for num, item in enumerate(temp):
        price = re.findall(findprice, item)
        if len(price) >= 1:
            price = price[0]
        else:
            price = 'No price'
        deal = re.findall(findname, item) + [price] + [links[num]]
        deals.append(deal)
    pages = {}
    numPages = int(len(deals)/20)
    if numPages == 0:
        numPages = 1
    i = 0
    # Breaks up deals into pages of 20 items and places into page[deal] dict
    for page in range(numPages):
        if i + 20 < len(deals):
            pages[page] = deals[i:i+20]
            i += 20
        else:
            pages[page] = deals[i:]
    return pages


if __name__ == "__main__":
    print('Scraping today\'s deals...')
    root = Tk()
    main = Main(root)
    main.pack(side='top', fill='both', expand=True)
    root.title('Deal Scraper')
    root.wm_geometry('800x500')
    root.mainloop()
