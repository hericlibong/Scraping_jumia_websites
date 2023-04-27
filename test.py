import scrapy
import re

class MonSpider(scrapy.Spider):
    name = 'mon_spider'
    start_urls = ['https://www.jumia.com.ng/fashion-mid-sole-denim-athletic-sneakers-black-162096074.html']

    def parse(self, response):
        # Extraire la chaîne de caractères contenant les prix
        # list_price = response.xpath("//span[@class='-b -ltr -tal -fs24']/text()").get()
        
        # # Vérifier si la chaîne contient un tiret
        # if '-' in list_price:
        #     # Séparer la chaîne en fonction du tiret
        #     price_range = list_price.split('-')
            
        #     # Extraire les valeurs numériques à partir de chaque partie de la chaîne
        #     p1 = float(price_range[0].replace('₦', '').replace(',', '').strip()) if '₦' in price_range[0] else None
        #     p2 = float(price_range[1].replace('₦', '').replace(',', '').strip()) if '₦' in price_range[1] else None
        #     p3 = float(price_range[0].replace('KSh', '').replace(',', '').strip()) if 'KSh' in price_range[0] else None
        #     p4 = float(price_range[1].replace('KSh', '').replace(',', '').strip()) if 'KSh' in price_range[1] else None

        #     # Afficher les valeurs numériques
        #     return {"Prix 1": p1, "Prix 2": p2}
        
    
        bread = response.xpath("//div[@class='brcbs col16 -pts -pbm']/a/text()").extract()
        bread = bread[1::]
        print(bread)

            
       

                
                
                #['₦ 3,790 - ₦ 3,990']


            
        

