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
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.deals = slickScraper()
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
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.deals = redditScraper()
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
            self.price = Label(self, text = '${}'.format(deal[1]))
            self.price.grid(row=num+2, column=6, columnspan=4)

    def openLink(self, link):
        webbrowser.open_new(link)

    def make_lambda(self, link):
        return lambda event: self.openLink(link)

class Main(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        slickpage = slickPage(self)
        redditpage = redditPage(self)

        buttonFrame = Frame(self)
        container = Frame(self)
        buttonFrame.pack(side='top', fill='x', expand=False)
        container.pack(side='top', fill='both', expand=True)

        slickpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        redditpage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        slickButton = Button(buttonFrame, text='Slick Deals',
                             command=slickpage.lift)
        slickButton.grid(row=0, sticky=W+E)
        redditButton = Button(buttonFrame, text='Build a PC',
                              command=redditpage.lift)
        redditButton.grid(row=0, column=1, sticky=W+E)

        slickpage.show()


def slickScraper():
    deals = []
    res = requests.get('http://slickdeals.net')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all(class_='itemTitle')
    for item in items:
        deal = item.get('title').split('$', 1)
        if len(deal) == 1:
            deal.append('No price')
        link = item.get('href')
        deal.append(link)
        deals.append(deal)
    return deals


def redditScraper():
    deals = []
    temp = []
    links = []
    while True:
        try:
            res = requests.get('https://www.reddit.com/r/buildapcsales')
            res.raise_for_status()
            break
        except requests.exceptions.HTTPError:
            continue
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    for item in soup.find_all(class_='title may-blank '):
        links.append(item.get('href'))
        temp.append(str(item))
    findname = re.compile('\>(.+)\<')
    findprice = re.compile('\$(\d+[\.\d{2}]*)')
    for num, item in enumerate(temp):
        price = re.findall(findprice, item)
        if len(price) >= 1:
            price = price[0]
        else:
            price = 'No price'
        deal = re.findall(findname, item) + [price] + [links[num]]
        deals.append(deal)
    return deals


if __name__ == "__main__":
    print('Scraping today\'s deals...')
    root = Tk()
    main = Main(root)
    main.pack(side='top', fill='both', expand=True)
    root.title('Deal Scraper')
    root.wm_geometry('800x500')
    root.mainloop()
