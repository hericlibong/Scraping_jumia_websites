from requests_html import HTMLSession, HTML



session = HTMLSession()

#response = session.get('https://www.jumia.sn')
url = 'https://www.jumia.com.ng/fashion-mid-sole-denim-athletic-sneakers-black-162096074.html/'

response = session.get(url)
liste_keys = response.html.xpath("//div[@class='flyout']/a")

liste_keys_strip = [i.attrs['href'].split('/')[-2] for i in liste_keys if i.attrs.get('href')]

#print(liste_keys_strip)


# cat = response.html.xpath("//span[contains(text(), 'SKU')]")
# print(cat)



# keys = ['telephone-tablette', 'electronique', 'maison-bureau-electromenager', 
#         'beaute-hygiene-sante', 'ordinateurs-accessoires-informatique', 'fashion-mode', 
#         'maison-cuisine-jardin', 'bebe-puericulture', 'sports-loisirs', 'jeux-videos-consoles']

list_price = response.html.xpath("//span[@class='-b -ltr -tal -fs24']/text()")
print(list_price)