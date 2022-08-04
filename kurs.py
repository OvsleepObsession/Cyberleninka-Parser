# -*- coding: utf-8 -*-
"""
Парсер
Написано : Чернецкий Андрей, БИВ174
"""
import urllib.request
from urllib.parse   import quote
from bs4 import BeautifulSoup

def pars(mywindow_, enter):
    html_doc = urllib.request.urlopen("https://cyberleninka.ru/search?q=" + quote(enter))
    soup = BeautifulSoup(html_doc, 'html.parser')
    if soup.find('ul', {'class' : 'list'}).find('li') == None:
        mywindow_.ui.tableWidget.setHorizontalHeaderLabels(
            (' ', 'Link', 'Article name', 'Authors', 'Description')
        )        
        return
    if (type(soup.find('ul', {'class' : 'paginator'})) != type(None)):
        li_pag = soup.find('ul', {'class' : 'paginator'}).find('a', {'class' : 'icon'})  
        i = -1
        while li_pag.get('href')[i] != '=':
            i -= 1
        digit = li_pag.get('href')[i+1:-1] + li_pag.get('href')[-1]
        page_cnt = int(digit)
    else:
        page_cnt = 1

    for i in range(page_cnt):
        html_doc = urllib.request.urlopen("https://cyberleninka.ru/search?q=" + quote(enter) + '&page=' + str(i + 1))
        soup = BeautifulSoup(html_doc, 'html.parser')
        list = soup.find('ul', {'class' : 'list'})
        mywindow_.ui.tableWidget.setEnabled(False)
        mywindow_.ui.pushButton.setEnabled(False)
        mywindow_.ui.pushButton_2.setEnabled(False)
        for meta in list.find_all('li'):
            for h in meta.find_all('h2'):
                for linq in h.find_all('a'):
                    linq_txt = 'https://cyberleninka.ru' + linq.get('href')
                    authors_txt = meta.find('span', {'class' : ''}).string
                    html_curr = urllib.request.urlopen(linq_txt)
                    soup_curr = BeautifulSoup(html_curr, 'html.parser')
                    head = soup_curr.find('head')
                    og_title = head.find('meta', {'property' : 'og:title'}).get('content')
                    og_description = head.find('meta', {'property' : 'og:description'}).get('content')
                    mywindow_.ui.progress.setValue(mywindow_.ui.tableWidget.rowCount()*100/(page_cnt*20))
                    mywindow_.addcolumn(linq_txt, og_title, authors_txt, og_description)
    
    mywindow_.ui.tableWidget.setEnabled(True)
    mywindow_.ui.pushButton.setEnabled(True)
    mywindow_.ui.pushButton_2.setEnabled(True)
                   
