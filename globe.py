import httplib2, os, oauth2client, base64, requests, gspread, globe
from lxml import html, etree
from urllib.parse import urlparse

globe.present = {}

def main():
    page = requests.get('http://conjugator.reverso.net/conjugation-german-verb-konnen.html')
    tree = html.fromstring(page.content)
    present = tree.xpath('//div[1]/div[2]/div[2]/div/fieldset/div[1]/font/i/text()')
    i = 0
    j = 1
    for form in range(0, 6):
        conj = present[i]
        vers = present[j]
        globe.present[conj] = vers
        # print(present[i],"-",present[j])
        i += 2
        j += 2
    #mod()
    for i in globe.present:
        print (i, globe.present[i])
        print (i, globe.present[i])

    #print(globe.present['ich'])
    #get = requests.get("http://www.linguee.de/deutsch-englisch/search?query=k%C3%B6nnen&source=auto").content
    #tree = html.fromstring(get)
    #etag = tree.xpath('//span[@class="tag_e"]')
    #stag = tree.xpath('//span[@class="tag_e"]/text()')
    #//div[@class="tag_e"]/text()

def mod():
    get = requests.get('http://www.linguee.de/deutsch-englisch/search?query=k%C3%B6nnen&source=auto')
    tree = html.fromstring(get.content)
    #    etag = tree.xpath('//span[@class="tag_e"]')
    #    stag = tree.xpath('//span[@class="tag_e"]/p')
    prices = tree.xpath('//div[2]/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[*]/span/text()')
    # for tag in etag:
    # print (etag)
    # print (stag)
    print(prices)


#<div class="responsive-sub responsive-sub-25">

if __name__ == '__main__':
        main()
        #mod()