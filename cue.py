from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import telegram
from dotenv import load_dotenv
import os
# https://cduser.com/como-automatizar-el-llenado-de-formularios-web-usando-selenium-en-python/

# Credentials
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PASSPORT_NUM = os.getenv("PASSPORT_NUM")
FULLNAME = os.getenv("FULLNAME")
PHONE_NUM = os.getenv("PHONE_NUM")
MAIL = os.getenv("MAIL")

bot = telegram.Bot(token=BOT_TOKEN)

driver_options = Options()
driver_options.add_argument('--headless')
driver_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver', options=driver_options)
driver.get('https://sede.administracionespublicas.gob.es/icpplus/index.html')

def slow_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(0.3)

def scroll():
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

def madrid():
    place = Select(driver.find_element_by_id('form'))
    place_selected = place.select_by_visible_text("Madrid")

def sb_aceptar():
    submit = driver.find_element_by_id('btnAceptar')
    submit.click()

def tramite():
    tramite = Select(driver.find_element_by_id('tramiteGrupo[0]'))
    tramite_selected = tramite.select_by_visible_text("POLICIA-CERTIFICADO DE REGISTRO DE CIUDADANO DE LA U.E.")

def sb_entrar():
    submit = driver.find_element_by_id('btnEntrar')
    submit.click()

def radio_pasaporte():
    radio = driver.find_element_by_id("rdbTipoDocPas")
    radio.click();

def pasaporte():
    ps = driver.find_element_by_id('txtIdCitado')
    slow_typing(ps,PASSPORT_NUM)

def fullname():
    fn = driver.find_element_by_id('txtDesCitado')
    slow_typing(fn,FULLNAME)

def sb_enviar():
    submit = driver.find_element_by_id('btnEnviar')
    submit.click()

def sb_solicitar_cita():
    submit = driver.find_element_by_id('btnEnviar')
    submit.click()



def screenshot():
    time.sleep(3)
    screenshot = driver.save_screenshot("screenshot.png")

def no_hay_cita():
    bodyText = driver.find_element_by_tag_name('body').text
    if "En este momento no hay citas disponibles." in bodyText:
        res = True
    else:
        res = False
    return res

def message():

    if not(no_hay_cita()):
        print("Puede ser que haya")
        bot.sendMessage(CHAT_ID=CHAT_ID, text='Puede ser que haya cita para el CUE \n link rapido comun: https://sede.administracionespublicas.gob.es/icpplus/index.html')
        bot.sendMessage(CHAT_ID=CHAT_ID, text='seguir tramite:' + driver.current_url)

        bot.sendPhoto(CHAT_ID=CHAT_ID, photo=open('screenshot.png', 'rb'))
    else:
        print('no hay citas')

while True:
    madrid()
    sb_aceptar()

    tramite()
    sb_aceptar()

    scroll()
    sb_entrar()

    radio_pasaporte()
    pasaporte()
    scroll()
    fullname()
    sb_enviar()

    sb_solicitar_cita()

    screenshot()
    message()
    driver.get('https://sede.administracionespublicas.gob.es/icpplus/index.html')

    time.sleep(20)