from selenium import webdriver 
from webdriver_manager.firefox import GeckoDriverManager as FM
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
class Rentals:
    def __init__(self,locations_wanted_to_find,beds,baths,min_price,max_price,type_of_the_location,pets,availability,laundry,AC,dishW,garage_parking,target = '1'):
        '''
            *** all information has to be in str ***        
            
            choose filters you want. use numbers as your answers.
            your answer has to be in numbers. for example if you want filters 1,2 and 4 your answer has to be: 124 , order doesn't matter.
            the min price has to be atleast 0 and the max price has to be atmost 1,000,000.
            locations wanted to find has to be in range of 1 to 50.
            you can choose not to have any filters for each part by writing 'no'.
            
            filters:
            locations_wanted_to_find = how many locations do you want to get the average price from ? (atmost 50)
            beds = how many beds ? (0=Studio , 1=1bed , 2=2beds , 3=3beds , 4=+4beds)
            baths = how many baths ? (1=1bath , 2=2baths , 3=3baths , 4=4baths , 5=+5baths)
            min_price = what's the min price ? (atleast 0)
            max_price = what's the max price ? (atmost 10000)
            type_of_the_location = what type ? (1=Apartment , 2=Condo , 3=House , 4=Room , 5=Townhouse , 6=Other)
            pets = input("do you have pets ? (1=dog , 2=cat)
            availability = input("be available ? (1=only if it is available)
            laundry = laundry ? (1=In unit , 2=In building)
            AC = AC ? (1=only if it has AC)
            dishW = dish washer ? (1=only if it has dish washer)
            garage_parking = garage/parking ? (1=only if it has garage/parking)
            target = which city is your target ? (1=Toronto , 2=Vancouver , 3=Richmond hill)(default is Toronto)
            
        '''
        self.locations_wanted_to_find = int(locations_wanted_to_find)
        self.beds = beds
        self.baths = baths
        self.min_price = min_price
        self.max_price = max_price
        self.type_of_the_location = type_of_the_location
        self.pets = pets
        self.availability = availability
        self.laundry = laundry
        self.AC = AC
        self.dishW = dishW
        self.garage_parking = garage_parking
        if target == '2': 
            url = 'https://www.zumper.com/apartments-for-rent/vancouver-bc'
            self.target = 'Vancouver'
        elif target == '3':
            url = 'https://www.zumper.com/apartments-for-rent/richmond-hill-on'
            self.target = 'Richmond Hill'
        else:
            url = 'https://www.zumper.com/apartments-for-rent/toronto-on'
            self.target = 'Toronto'
        fm = FM().install()
        service = Service(executable_path = fm)
        self.driver = webdriver.Firefox(service = service)
        self.driver.get(url)
        sleep(3)
        self.driver.find_element(By.XPATH , "//div[@id='onetrust-close-btn-container']//button[1]").click()
        
        
    def is_equal_bed(self,input1,input2):
        if (input1 == 'Studio' or '0' in input1) and (input2 == 'Studio' or '0' in input2) :
            return True
        elif '1' in input1 and '1' in input2 :
            return True
        elif '2' in input1 and '2' in input2 :
            return True
        elif '3' in input1 and '3' in input2 :
            return True
        elif (('Studio' not in input1 and '1' not in input1 and '2' not in input1 and '3' not in input1) or '4' in input1) and (('Studio' not in input2 and '1' not in input2 and '2' not in input2 and '3' not in input2) or '4' in input2) :
            return True
        else:
            return False
        
        
    def is_equal_bath(self,input1,input2):
        if '1' in input1 and '1' in input2 :
            return True
        elif '2' in input1 and '2' in input2 :
            return True
        elif '3' in input1 and '3' in input2 :
            return True
        elif '4' in input1 and '4' in input2 :
            return True
        elif (('1' not in input1 and '2' not in input1 and '3' not in input1 and '4' not in input1) or '5' in input1) and (('1' not in input2 and '2' not in input2 and '3' not in input2 and '4' not in input2) or '5' in input2) :
            return True
        else:
            return False
        
        
    def rawNumberToFloatNumber(self,raw_price):
        string_price = ''
        for letter in raw_price:
            if letter == '0' or letter == '9' or letter == '8' or letter == '7' or letter == '6' or letter == '5' or letter == '4' or letter == '3' or letter == '2' or letter == '1':
                string_price += letter
        if string_price != '':
            final_price = float(string_price)
        else:
            return ''
        return final_price
    
    
    def scroll_until_it_finds_the_element(self,driver, scroll_element_xpath, specific_element_xpath, scroll_increment=50, wait_time=1):
        scroll_direction = 'down'  # Start with scrolling down
        specific_element = None
        scroll_element = driver.find_element(By.XPATH, scroll_element_xpath)
        while not specific_element:
            # Scroll the div
            if scroll_direction == 'down':
                driver.execute_script("var element = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; element.scrollTop += arguments[1];", scroll_element_xpath, scroll_increment)
            else:
                driver.execute_script("var element = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; element.scrollTop -= arguments[1];", scroll_element_xpath, scroll_increment)
            
            sleep(wait_time)  # Wait for a short time after each scroll
            
            # Check if the specific element is found
            specific_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, specific_element_xpath)))
            
            # Check if the scroll direction needs to be changed
            js_code = """
                var element = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
                    .singleNodeValue;
                var scrollTop = element.scrollTop;
                var scrollHeight = element.scrollHeight;
                return [scrollTop, scrollHeight];
            """

            # Executing the JavaScript code to get scroll top and scroll height
            current_scroll_top, current_scroll_height = driver.execute_script(js_code, scroll_element_xpath)
            if current_scroll_top == 0 and scroll_direction == 'up':
                # If the scroll top is 0 and direction is up, change direction to down
                scroll_direction = 'down'
            elif (current_scroll_top + scroll_element.size['height']) >= current_scroll_height and scroll_direction == 'down':
                # If the bottom of the div is reached and direction is down, change direction to up
                scroll_direction = 'up'

        # Click on the specific element
        return specific_element
    
    
    def beds_and_baths_function(self,beds,baths):
        if beds!='no' or baths!='no':
            self.driver.find_element(By.ID , "popover-trigger-Beds/Baths-filter-btn").click()
            if beds != 'no':
                if '0' in beds:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[1]//div[1]//div[1]//button[1]").click()
                if '1' in beds:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[1]//div[1]//div[1]//button[2]").click()
                if '2' in beds:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[1]//div[1]//div[1]//button[3]").click()
                if '3' in beds:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[1]//div[1]//div[1]//button[4]").click()
                if '4' in beds:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[1]//div[1]//div[1]//button[5]").click()        
            if baths != 'no':
                if '1' in baths:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[2]//div[1]//div[1]//button[1]").click()
                if '2' in baths:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[2]//div[1]//div[1]//button[2]").click()
                if '3' in baths:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[2]//div[1]//div[1]//button[3]").click()
                if '4' in baths:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[2]//div[1]//div[1]//button[4]").click()
                if '5' in baths:
                    self.driver.find_element(By.XPATH , "//div[@class='css-1wcmpjk']//div[2]//div[1]//div[1]//button[5]").click()
            self.driver.find_element(By.XPATH , "//div[@class='css-tuflmg']//button[2]").click()
            sleep(3)
            try:
                self.driver.find_element(By.XPATH , "//button[@class='chakra-modal__close-btn css-lw6vcm e1k4it830']").click()
            except:
                pass
            
            
    def min_price_and_max_price_function(self,min_price,max_price):  
        if min_price != 'no':
            min_price = int(min_price)
        else:
            min_price = 0
        if max_price != 'no':
            max_price = int(max_price)
        else:
            max_price = 1000000
        self.driver.find_element(By.ID , "popover-trigger-Price-filter-btn").click()
        self.driver.find_element(By.ID , "minPrice").send_keys(min_price)
        self.driver.find_element(By.ID , "maxPrice").send_keys(max_price)
        self.driver.find_element(By.XPATH , "//div[@class='css-13cmu35']").click()
        self.driver.find_element(By.XPATH , "//section[@id='popover-content-Price-filter-btn']//div[2]//button[2]").click()
        sleep(3)
        try:
            self.driver.find_element(By.XPATH , "//button[@class='chakra-modal__close-btn css-lw6vcm e1k4it830']").click()
        except:
            pass
        return min_price,max_price
        
        
    def type_of_the_location_funtion(self,type_of_the_location):
        if type_of_the_location != 'no':
            self.driver.find_element(By.ID , "popover-trigger-Type-filter-btn").click()
            main_types_page = self.driver.find_element(By.ID , "popover-content-Type-filter-btn")
            types = main_types_page.find_elements(By.XPATH, "//div[@class='css-raadhi']//label[1]")
            for index in range(0,6):
                if str(index+1) in type_of_the_location:
                    types[index].click()
            self.driver.find_element(By.XPATH , "//*[@id='popover-content-Type-filter-btn']//div[2]//button[2]").click()
            sleep(3)
            try:
                self.driver.find_element(By.XPATH , "//button[@class='chakra-modal__close-btn css-lw6vcm e1k4it830']").click()
            except:
                pass
            
            
    def pets_function(self,pets): 
        if pets != 'no':
            self.driver.find_element(By.ID , "popover-trigger-Pets-filter-btn").click()
            if '1' in pets:
                self.driver.find_element(By.XPATH , "//section[@id='popover-content-Pets-filter-btn']//div[1]//div[1]//label[1]").click()
            if '2' in pets:
                self.driver.find_element(By.XPATH , "//section[@id='popover-content-Pets-filter-btn']//div[1]//div[2]//label[1]").click()
            self.driver.find_element(By.XPATH , "//section[@id='popover-content-Pets-filter-btn']//div[2]//button[2]").click()
            sleep(3)
            try:
                self.driver.find_element(By.XPATH , "//button[@class='chakra-modal__close-btn css-lw6vcm e1k4it830']").click()
            except:
                pass
            
            
    def availability_function(self,availability):    
        if availability != 'no' and '1' in availability:
            self.driver.find_element(By.XPATH , "//div[@id='root']//div[1]//div[1]//div[2]//div[1]//div[1]//button[7]").click()
            sleep(3)
            try:
                self.driver.find_element(By.XPATH , "//button[@class='chakra-modal__close-btn css-lw6vcm e1k4it830']").click()
            except:
                pass
    
    
    def laundry_function(self,laundry):
        if laundry != 'no':
            if '1' in laundry:
                self.driver.find_element(By.XPATH, "//*[@class='chakra-modal__body css-d8ne84 e1k4it830']")
                child = self.scroll_until_it_finds_the_element(self.driver, "//*[@class='chakra-modal__body css-d8ne84 e1k4it830']", "//input[@value='In unit']")
                child.find_element(By.XPATH , "..").click()
            if '2' in laundry:
                child = self.scroll_until_it_finds_the_element(self.driver, "//*[@class='chakra-modal__body css-d8ne84 e1k4it830']", "//input[@value='In building']")
                child.find_element(By.XPATH , "..").click()
                
                
    def AC_function(self,AC):            
        if AC != 'no' and '1' in AC:
            child = self.scroll_until_it_finds_the_element(self.driver, "//*[@class='chakra-modal__body css-d8ne84 e1k4it830']", "//div[@class='css-1tl054d e1k4it830']//div[1]//div[1]//div[1]//div[1]//label//span[text()='Air conditioning']")
            child.find_element(By.XPATH , "..").click()
            
            
    def dish_washer_function(self,dishW):      
        if dishW != 'no' and '1' in dishW:
            child = self.scroll_until_it_finds_the_element(self.driver, "//*[@class='chakra-modal__body css-d8ne84 e1k4it830']", "//div[@class='css-1tl054d e1k4it830']//div[1]//div[1]//div[1]//div[1]//label//span[text()='Dishwasher']")
            child.find_element(By.XPATH , "..").click()
    
    
    def garage_parking_function(self,garage_parking):        
        if garage_parking != 'no' and '1' in garage_parking:
            child = self.scroll_until_it_finds_the_element(self.driver, "//*[@class='chakra-modal__body css-d8ne84 e1k4it830']", "//div[@class='css-1tl054d e1k4it830']//div[1]//div[1]//div[1]//div[1]//label//span[text()='Garage parking']")
            child.find_element(By.XPATH , "..").click()
    
    
    def find_locations_function(self):
        rentals_found = self.driver.find_element(By.XPATH , "//div[@class='css-19ybsap']//p[1]").text
        rentals_found_final = ''
        for letter in rentals_found:
            if letter == '0' or letter == '9' or letter == '8' or letter == '7' or letter == '6' or letter == '5' or letter == '4' or letter == '3' or letter == '2' or letter == '1':
                rentals_found_final += letter
        rentals_found_final = int(rentals_found_final)
        num_of_locations = self.locations_wanted_to_find if rentals_found_final >= self.locations_wanted_to_find else rentals_found_final
        for num in range(50):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        all_locations = self.driver.find_elements(By.CLASS_NAME , 'css-8a605h')
        locations = all_locations[:num_of_locations]
        return locations
    
    
    def open_tabs(self):
        for location in self.find_locations_function():
            while True:    
                before = len(self.driver.window_handles)
                location.click()
                try:
                    WebDriverWait(self.driver, 5).until(lambda driver: len(driver.window_handles) == before + 1)
                    break
                except:
                    pass
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
    
    
    def is_address_valid(self):
        addresses = self.driver.find_elements(By.TAG_NAME , "address")
        for address in addresses:
            try:
                if self.target in address.text:
                    return True
            except:
                pass
        return False
    
    
    def get_price_list(self):
        self.beds_and_baths_function(self.beds,self.baths)
        self.min_price , self.max_price = self.min_price_and_max_price_function(self.min_price,self.max_price)
        self.type_of_the_location_funtion(self.type_of_the_location)
        self.pets_function(self.pets)
        self.availability_function(self.availability)
        self.driver.find_element(By.XPATH , "//div[@id='root']//div[1]//div[1]//div[2]//div[1]//div[1]//button[8]").click()
        self.driver.find_element(By.XPATH , "//button[@class='chakra-button css-1oyrh39 e1k4it830']").click()
        self.laundry_function(self.laundry)
        self.AC_function(self.AC)
        self.dish_washer_function(self.dishW)
        self.garage_parking_function(self.garage_parking)
        self.driver.find_element(By.XPATH , "//div[@class='css-1r5azra e1k4it830']//button[2]").click()
        sleep(5)
        try:
            self.find_locations_function()
        except:
            return []
        self.open_tabs()
        locations_prices = []
        for window_index in range(len(self.driver.window_handles)):
            self.driver.switch_to.window(self.driver.window_handles[window_index])
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body")))
            WebDriverWait(self.driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            if not self.is_address_valid():
                continue
            self.driver.execute_script("window.scrollBy(0, 400);")
            price_list = []
            the_second_link = self.driver.find_element(By.XPATH , "//nav[@class='css-13pt18b']//ul[1]//li[2]//a[1]")
            if the_second_link.text == 'FLOOR PLANS':
                while True:
                    if price_list != []:
                        break
                    try:    
                        sleep(1)
                        the_second_link.click()
                        sleep(1) 
                        try:
                            self.driver.find_element(By.XPATH , '//button[@class="chakra-button css-mdv1fo e1k4it830"]').click()
                            sleep(1)
                            table_rows = self.driver.find_elements(By.XPATH , "//div[@class='chakra-modal__body css-414uhe e1k4it830']//div[1]//div[2]//div[1]//table[1]//tbody[1]//tr")
                        except:
                            table_rows = self.driver.find_element(By.ID , 'floor-plans').find_elements(By.XPATH , "//tr[@class='css-1nhlpk2 e1k4it830']")
                        for row in table_rows:
                            table_datas = row.find_elements(By.TAG_NAME , "td")
                            beds_website = table_datas[2].text
                            baths_website = table_datas[3].text
                            price_website = self.rawNumberToFloatNumber(table_datas[5].text)
                            if ((self.beds == 'no') or (self.is_equal_bed(beds_website,self.beds))) and ((self.baths == 'no') or (self.is_equal_bath(baths_website,self.baths))):
                                if price_website != '' and self.min_price<=price_website and price_website<=self.max_price:
                                    price_list.append(price_website)
                    except:
                        price_list = []
            elif the_second_link.text == 'UNITS':
                while True:
                    if price_list != []:
                        break
                    try:    
                        sleep(1)
                        the_second_link.click()
                        sleep(1)
                        table_rows = self.driver.find_element(By.ID , 'pa-units').find_elements(By.XPATH , "//div[@class='chakra-stack css-1mdlggf']")
                        if table_rows == []:
                            table_rows = self.driver.find_element(By.ID , "pa-units--tabpanel-0")
                            table_rows.find_elements(By.XPATH , "//div[@class='css-1q1y455']//div[1]//div[1]//div[1]//div[2]")
                            table_rows.find_elements(By.XPATH , "//div[@class='css-1kht2la']//div[1]//div[1]//div[1]//div[2]")
                            table_rows = table_rows.find_elements(By.XPATH , "//div[@class='css-1q1y455']//div[1]//div[1]//div[1]//div[2]") + table_rows.find_elements(By.XPATH , "//div[@class='css-1kht2la']//div[1]//div[1]//div[1]//div[2]")
                        for row in table_rows:
                            table_datas = row.find_elements(By.TAG_NAME , "p")
                            beds_website = table_datas[0].text
                            baths_website = table_datas[1].text
                            price_website = self.rawNumberToFloatNumber(table_datas[3].text)
                            if ((self.beds == 'no') or (self.is_equal_bed(beds_website,self.beds))) and ((self.baths == 'no') or (self.is_equal_bath(baths_website,self.baths))):
                                if price_website != '' and self.min_price<=price_website and price_website<=self.max_price:    
                                    price_list.append(price_website)
                    except:
                        price_list = []
            else:
                while True:
                    try:    
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        final_raw_price = self.driver.find_element(By.XPATH , "//table[@class='chakra-table css-wv10h e1k4it830']//tbody[1]//tr[1]//td[1]").text
                        break
                    except:
                        pass
            if price_list != []:
                total_price = 0
                for price in price_list:
                    total_price += price
                total_num_of_prices = len(price_list)
                average_price = total_price / total_num_of_prices
                locations_prices.append(average_price)
            else:
                final_string_price = ''
                for final_letter in final_raw_price:
                    if final_letter == '0' or final_letter == '9' or final_letter == '8' or final_letter == '7' or final_letter == '6' or final_letter == '5' or final_letter == '4' or final_letter == '3' or final_letter == '2' or final_letter == '1':
                        final_string_price += final_letter
                final_price = float(final_string_price)
                locations_prices.append(final_price)
        self.driver.quit()
        return locations_prices
    
    
    def get_average(self,the_list):
        final_numbers_of_items = len(the_list)
        final_total_price = 0
        for each_price in the_list:
            final_total_price += each_price
        if final_numbers_of_items != 0:
            final_average_price = final_total_price / final_numbers_of_items
        else:
            final_average_price = 'no result'
        return final_average_price