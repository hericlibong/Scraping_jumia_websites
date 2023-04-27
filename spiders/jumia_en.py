import scrapy


class JumiaEnSpider(scrapy.Spider):
    name = "jumia_en"
    allowed_domains = ['jumia.co.ke','jumia.com.ng']
    start_urls = ['https://www.jumia.co.ke/','https://www.jumia.com.ng/']
    
    cats_ken = ['groceries', 'health-beauty', 'home-office', 'home-office-appliances', 
                'phones-tablets', 'computing', 'electronics', 
                 'category-fashion-by-jumia', 'video-games', 'baby-products', 
                 'sporting-goods']
    cats_ng = ['groceries', 'health-beauty', 'home-office', 'phones-tablets', 'computing', 'electronics', 
               'category-fashion-by-jumia', 
               'baby-products', 'video-games', 'sporting-goods', 'automobile']
    
    
    
    
    def start_requests(self):
        for url in self.start_urls:
            if 'jumia.co.ke' in url:
                for cat in self.cats_ken:
                    yield scrapy.Request(url=url+cat, callback=self.parse_listing_page)
                    
            elif 'jumia.com.ng' in url:
                for cat in self.cats_ng:
                    yield scrapy.Request(url=url+cat, callback=self.parse_listing_page)
                
                                                                                                                         

    def parse_listing_page(self, response):
        product_urls = response.xpath("//div[contains(@class, '-pax')]//a[@class='core']//@href")
        for product_url in product_urls.extract():
            if product_url:
                yield scrapy.Request(response.urljoin(product_url), callback=self.parse_data)


        #pagination
        next_page_link = response.xpath("//a[@aria-label='Next Page']/@href")
        if next_page_link:
        # If there is a link to the next page, follow it and call this function recursively
            yield scrapy.Request(response.urljoin(next_page_link.extract_first()), callback=self.parse_listing_page)
    
    
    
    #### Kenya Section #######
            
    #convert kenya currentprice to float
    def parse_price_kenya(self, price):
        if price :
            if 'KSh'in price :
                price = float(price.replace('KSh', '').replace(',', ''))               
        return price
    
    
    #convert kenya rawprice to float
    def parse_former_price_kenya(self, former_price):
        if former_price:
            if 'KSh' in former_price:
                former_price = float(former_price.replace('KSh ', '').replace(',', ''))                         
        return former_price
   
    
    
    ##### Nigeria Section ######
    
    # convert nigeria currentprice to float
    def parse_price_nigeria(self, price):
        if price :
            if '₦'in price :
                price = float(price.replace('₦', '').replace(',', ''))               
        return price
    
   
    
    # convert nigeria rawprice to float
    def parse_former_price_nigeria(self, former_price):
        if former_price:
            if '₦' in former_price:
                former_price = float(former_price.replace('₦ ', '').replace(',', ''))
        return former_price 
                 
    
    def parse_remove_price(self, price):
        if'-' in price:
            price = price.split('-')
            price = price[0].strip()
        return price
    
    def parse_remove_former_price(self, former_price):
        if '-' in former_price:
            former_price = former_price.split('-')
            former_price = former_price[0].strip()
        return former_price   
            
                       
      #### Get data #####      
    
    def parse_data(self, response):
        site_name = response.xpath('//meta[@property="og:site_name"]/@content').get()# Country of the Jumia Website 
        title = response.xpath("//h1[@class='-fs20 -pts -pbxs']/text()").get(default='').strip() # Name of the product
        url = response.url # Url of the web page
        sku = response.xpath("//span[contains(text(), 'SKU')]/following-sibling::text()").get() # SKU id of the product
        brand = response.xpath("//div[contains(text(), 'Brand')]//following-sibling::a/text()").get() # Brand of te product
        try : 
            starsname = response.xpath("//div[@class='stars _s _al']/text()").get().replace('out of 5', '') # stars on the range from 0 to 5
            stars = float(starsname)
        except :
            stars = 'None'
        verified_advices = response.xpath("//a[@class='-plxs _more']/text()").get().replace("(", "").replace(")", "")
        refurbished = response.xpath("//img[contains(@alt, 'REFU')]")
        
        if refurbished:
            refurbished =True
        else :
            refurbished = False
        
        
        #### current price ######
        price = response.xpath("//span[@class='-b -ltr -tal -fs24']/text()").get()
        if '-' in price:
            price = self.parse_remove_price(price)
        if 'KSh' in price:
            price = self.parse_price_kenya(price)
        else:
            price = self.parse_price_nigeria(price)
            
      
    
        ##### raw price ######
        former_price = response.xpath("//span[contains(@class, '-fs16')][1]/text()").get()
        if '-' in former_price:
            former_price = self.parse_remove_former_price(former_price)
        if 'KSh' in former_price:
            former_price = self.parse_former_price_kenya(former_price)  
        else: 
            former_price = self.parse_former_price_nigeria(former_price)
                                                           
         ###### device & currency ####   
        device = response.xpath("//span[contains(@class, '-fs16')][1]/text()").get()
        if device :
            if 'KSh' in device:
                device = 'Kenyan Shilling'
            elif '₦' in device :
                device = 'Naira'
        currency = response.xpath("//span[contains(@class, '-fs16')][1]/text()").get()
        if currency:
            if 'KSh' in currency:
                currency = 'KSh'
            elif '₦' in currency:
                currency = '₦'
        
        #### discount ######
        discount = response.xpath("//span[contains(@class, 'bdg _dsct _dyn -mls')]")
        if discount:
            discount = True
        else:
            discount = False
        discount_rate = response.xpath("//span[contains(@class, 'bdg _dsct _dyn -mls')]/text()")
        if discount_rate:
            discount_rate = response.xpath("//span[contains(@class, 'bdg _dsct _dyn -mls')]/text()").get()
        else :
            discount_rate = '0%'
        
        #### FlashSales ###
        flashsales = response.xpath("//span[contains(text(), 'Flash Sales')]")
        if flashsales:
            flashsales = True
        else:
            flashsales = False
        flashsales_remain_time = response.xpath("//div[contains(text(), 'Time Left')]/time/text()")
        if flashsales_remain_time :
            flashsales_remain_time = response.xpath("//div[contains(text(), 'Time Left')]/time/text()").get()
        else :
            flashsales_remain_time = False
            
        items_remain = response.xpath("//span[contains(@class, '-fsh0 -prs -fs12')]")
        if items_remain:
            items_remain = response.xpath("//span[contains(@class, '-fsh0 -prs -fs12')]/text()").get()
        else :
            items_remain = 0
            
        #### Pictures ####
        picture = response.xpath("//div[@id='imgs']//a/@href").get()
        image_links = []
        image_divs = response.xpath('//div[@class="crs"]/div[@class="itm"]/label')
        for div in image_divs:
            image_url = div.xpath('./img/@data-src').get()
            image_links.append({'url': image_url})
        
        #### breadcrumbs ####
        breadcumbs = response.xpath("//div[@class='brcbs col16 -pts -pbm']/a/text()").extract()
        bread = breadcumbs[1::]
        
        #### sailoors #####
        try:
            seller = response.xpath("//div[@class='-hr -pas']/p/text()").get()
        except:
            seller = 'Not mentionned'
        seller_score = response.xpath("//bdo[@class='-m -prxs']/text()").get()
        try : 
            seller_followers = response.xpath("//p[@data-followers='true']/span/text()").get()
            seller_followers_int = int(seller_followers)
        except :
            seller_followers_int = 'No followers'
        seller_Order_Fulfillment_Rate = response.xpath("//p[contains(text(), 'Order Fulfillment')]/span/text()").get()
        seller_quality_score = response.xpath("//p[contains(text(), 'Quality Score')]/span/text()").get()
        seller_customer_rating = response.xpath("//p[contains(text(), 'Customer Rating')]/span/text()").get()

        
        yield{
            'siteName':site_name,
            'title':title,
            'url':url,
            'SKU':sku,
            'productBrand':brand,
            'currentPrice':{
                'value': price,
                'currency':currency,
                'device':device,
                 
            },
            'rawPrice':{
                'value':former_price,
                'currency':currency,
                'device':device,
                'isDiscount':discount,
                'discountRate': discount_rate,   
            },
            'stars': stars,
            'advicesNumber':verified_advices,
            
            'Refurbished': refurbished,
            'SalesFalsh':{
                    'flashSales': flashsales,
                    'flashRemainingTime': flashsales_remain_time,
                    'flashItemsRemains': items_remain
                },
            'sellerInfos':{
                'Name': seller,
                'Score': seller_score,
                'Followers': seller_followers_int,
                'orderFulfillmentRate':seller_Order_Fulfillment_Rate,
                'qualityScore': seller_quality_score,
                'customerRating': seller_customer_rating
            },
            'breadcumbs':bread, 
            'imageItems':{
                'picture':picture,
                'thumbnnailLinks': image_links
            },
            
           
            
        }
        