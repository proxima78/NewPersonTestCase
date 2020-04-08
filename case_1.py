import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from faker import Faker

# def cls():
#     os.system('cls' if os.name=='nt' else 'clear')
def out_default(text):
    print("\033[0m {}".format(text))
def out_red(text):
    print("\033[31m {}".format(text))
def out_green(text):
    print("\033[32m {}".format(text))
def out_yellow(text):
    print("\033[33m {}".format(text))
def out_blue(text):
    print("\033[34m {}".format(text))
def out_purple(text):
    print("\033[35m {}".format(text))
def out_turquoise(text):
    print("\033[36m {}".format(text))
def out_white(text):
    print("\033[37m {}".format(text))

class TestRunner:
    def __init__(self):
        env_var = os.getenv("ENVIRONMENT_ID")
        if env_var != None:
            if env_var.isnumeric():
                self.environment = int(env_var) # 0-Prod, 1-Test
            else:
                raise Exception("invalid env var")
        else:
            raise Exception("Please set env var ENVIRONMENT_ID")
        

        self.chromedriver_path = "" # FIXME Change path!
        self.electron_path = "" # FIXME Change path!

        self.my_factory = Faker('de_AT')
        self.data = {}
        self.data["user_name"] = self.my_factory.name()
        self.data["user_anrede"] = 'herr'
        self.data["user_land"] = 'AT'
        self.data["user_plz"] = '4030'
        self.data["user_ort"] = 'Linz'
        self.data["user_street"] = str(self.my_factory.street_address())
        self.data["tel_number"]=str(self.my_factory.phone_number())
        self.data["email_user"]=f'test{str(self.my_factory.random_number())}@test.tst'
        self.data["user_merkmale"]='hotelbesucher'
        self.data["user_job"] = str(self.my_factory.job())

        if self.environment == 0:
            print('Prod environment is used')
        elif self.environment == 1:
            print('Test environment is used')
        else:
            raise Exception("Invalid environment ID")

        self._init_driver()

    def _init_driver(self):
        opts = Options()
        opts.binary_location = self.electron_path
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=opts)

    def _get_auth_data(self):
        env_type = ""
        if self.environment == 0:
            env_type = "prod"
        elif self.environment == 1:
            env_type = "test"
        env_file = open(f'{env_type}_auth_data.env', 'r')
        lines = env_file.readlines()
        auth_data = []
        for e in lines:
            auth_data.append(e)
        return auth_data

    def _test_minimized(self):
        try:
            self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div/div[1]/button[1]").click()
            out_green ('Minimized - Test Passed')
        except:
            out_red ('Minimized - Test failed')

    def _test_maximized(self):
        try:
            self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div/div[1]/button[2]").click()
            out_green ('Maximized - Test Passed')
        except:
            out_red ('Maximized - Test failed')

    def _test_auth(self):
        auth_data = self._get_auth_data()
        el=self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div/div[2]/div/main/div/div[2]/form/main/div[1]/div[1]/div/input")
        el.send_keys(auth_data[0])
        el=self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div/div[2]/div/main/div/div[2]/form/main/div[1]/div[2]/div/input")
        el.send_keys(auth_data[1])
        self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div/div[2]/div/main/div/div[2]/form/main/div[2]/button").click()

    def _new_person(self):
        #Person dashboard
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div/header/nav/div[1]/button[1]").click()
        #time.sleep(1)
        #New Person
        self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div/div[2]/div/div/div[1]/div/div[1]/section[1]/button[1]").click()


        #time.sleep(1)
        #Anrede
        self.driver.find_element_by_xpath("//*[@id='enum-input--genInfo.salutation']/div/div[2]/div").click()
        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='react-select-2-input']")
        el1.send_keys(self.data["user_anrede"])
        el1.send_keys(Keys.ENTER)

        #time.sleep(1)
        #CheckBox='paar'
        #driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[3]/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/button").click()

        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[3]/div[2]/div[1]/div/div[1]/div/div[3]/div[2]/input")
        el1.send_keys(self.data["user_name"])
        #el1.send_keys(Keys.ENTER)
        #Beruf
        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[3]/div[2]/div[1]/div/div[1]/div/div[4]/div/input")
        el1.send_keys(self.data["user_job"])

        #PLZ
        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/div[1]/div/input")
        el1.send_keys(self.data["user_plz"])
        time.sleep(5)
        el1.send_keys(Keys.ENTER)
        #strasse
        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[3]/div[2]/div[1]/div/div[3]/div[3]/div/div/input")
        el1.send_keys(self.data["user_street"])
        el1.send_keys(Keys.TAB)

        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[4]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[1]/div[1]/div[2]/div/input")
        el1.send_keys(self.data["email_user"])

        #Email prufen

        self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[4]/div[1]/div[2]/div[1]/div/div[1]/div/div/div[1]/div[2]/button[1]").click()


        #Phone Number
        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[4]/div[1]/div[2]/div[1]/div/div[3]/div/div/div[1]/div[2]/div/input")
        #el1.send_keys(str(myFactory.phone_number()))
        el1.send_keys(str(self.data["tel_number"]))
        el1.send_keys(Keys.TAB)

        #WebSite
        #time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[4]/div[1]/div[2]/div[1]/div/div[5]/div/div/div[1]/div/input")
        el1.send_keys(str(self.my_factory.url()))
        el1.send_keys(Keys.TAB)

        #Maximize  Form New Person

        self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div[3]/div[1]/div/header/div[2]/div[2]/nav/button[2]").click()



        ###Sonstige Informationen###
        #Socialversicherungsnummer
        self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[5]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/input").send_keys(str(self.my_factory.ssn()))
        #Bankverbindung
        self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[5]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/input").send_keys(str(self.my_factory.bban()))
        #IBAN
        self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[5]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/input").send_keys(str(self.my_factory.iban()))
        #ExtNumber
        self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[5]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div/input").send_keys('qwerty3')
        #BLZ
        self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[5]/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/input").send_keys('61370086')

        self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[5]/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/input").send_keys(Keys.TAB)

        #Merkmale
        time.sleep(1)

        self.driver.find_element_by_xpath("//*[@id='enum-input--characteristics[0].id']/div/div[2]/div").click()
        el1=self.driver.find_element_by_xpath("//*[@id='react-select-8-input']")
        el1.send_keys(self.data["user_merkmale"])
        el1.send_keys(Keys.ENTER)

        #Notizen
        time.sleep(1)
        el1=self.driver.find_element_by_xpath("//*[@id='person-scroll']/div/main/div/div[6]/div[2]/div/div/div[2]/div[1]/div/div/div/div/textarea")
        el1.send_keys(self.my_factory.text())
        #Save
        self.driver.find_element_by_xpath("//*[@id='edi__modal-layer-root']/div[3]/div[1]/div/header/div[2]/div[1]/button").click()
        time.sleep(8)

    def _verify_new_person_creation(self):
        try:
            self.driver.find_element_by_xpath(f"//span[contains(text(), \"{self.data['user_name']}\")]")
            out_green ('Name user verification - pass')
        except:
            out_red ('User verification - failed')
        try:
            self.driver.find_element_by_xpath(f"//span[contains(text(), \"{self.data['user_street']}\")]")
            out_green ('Strasse verification - pass')
        except:
            out_red ('Strasse verification- failed')
        try:
            self.driver.find_element_by_xpath(f"//span/a[contains(text(), \"{self.data['email_user']}\")]")
            out_green ('Email verification - pass')
        except Exception as e:
            print(e)
            out_red ('Email verification- failed')
        try:
            self.driver.find_element_by_xpath(f"//span[contains(text(), \"{self.data['tel_number']}\")]")
            out_green ('Phone verification - pass')
        except:
            out_red ('Phone verification - failed')
        try:
            self.driver.find_element_by_xpath(f"//div[contains(text(), \"{self.data['user_merkmale']}\")]")
            out_green ('Merkmale verification - pass')
        except:
            out_red ('Merkmale verification - failed')

    def run(self):
        self.driver.implicitly_wait(15)
        time.sleep(1)

        self._test_auth()
        self._test_minimized()
        out_default('*')
        self._test_maximized()
        out_default('*')
        time.sleep(1)
        self._new_person()
        self._verify_new_person_creation()
        time.sleep(20)
        self.driver.quit()
        out_default('*')

if __name__ == "__main__":
    runner = TestRunner()
    runner.run()
