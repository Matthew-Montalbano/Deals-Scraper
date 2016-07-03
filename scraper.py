import requests
import bs4
from tkinter import *
import webbrowser


class GUI(Frame):
    def __init__(self, master, deals):
        Frame.__init__(self, root)
        self.deals = deals
        self.frame = Frame(root)
        self.frame.grid()
        self.createToolbar()
        self.createLabels()
        self.createList()

    def createToolbar(self):
        slickButton = Button(self.frame, text='Slick Deals')
        slickButton.grid(row=0, sticky=NW)
        redditButton = Button(self.frame, text='Reddit')
        redditButton.grid(row=0, column=1)

    def createLabels(self):
        self.dealLabel = Label(self.frame, text='Deal', foreground = 'red')
        self.priceLabel = Label(self.frame, text='Price', foreground = 'red')
        self.dealLabel.grid(row=1, column=0, sticky = NW)
        self.priceLabel.grid(row=1, column=6, columnspan=4)

    def createList(self):
        for num, deal in enumerate(self.deals):
            self.deal = Label(self.frame, text=deal[0])
            self.deal.bind('<Button-1>', self.make_lambda(deal[2]))
            self.deal.grid(row=num+2, column=0, columnspan=6, sticky=W)
            self.price = Label(self.frame, text='${}'.format(deal[1]))
            self.price.grid(row=num+2, column=6, columnspan=4)

    def openLink(self, link):
        webbrowser.open_new(r'http://www.slickdeals.com' + link)

    def make_lambda(self, link):
        return lambda event: self.openLink(link)

print('Scraping today\'s deals...')
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


root = Tk()
root.title('Slick Deals')
root.geometry('800x500')
GUI(root, deals)
root.mainloop()
