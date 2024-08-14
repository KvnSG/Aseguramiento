from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from fpdf import FPDF

# Configura las opciones del navegador
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Configura el path del chromedriver
chrome_driver_path = r"C:/Users/danip/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# Ruta de la carpeta para las capturas de pantalla y el archivo PDF
screenshots_folder = r"C:/Users/danip/OneDrive/Imágenes/test_failed2/screenshot_evidence"
pdf_path = r"C:/Users/danip/OneDrive/Imágenes/test_failed2/test_evidence.pdf"

# Asegúrate de que la carpeta de capturas de pantalla exista
if not os.path.exists(screenshots_folder):
    os.makedirs(screenshots_folder)

def add_screenshot_to_pdf(driver, step_name):
    screenshot_path = os.path.join(screenshots_folder, f"{step_name}.png")
    driver.save_screenshot(screenshot_path)

def create_pdf_with_screenshots(screenshots_folder, pdf_path, result):
    pdf = FPDF()
    for screenshot_name in sorted(os.listdir(screenshots_folder)):
        if screenshot_name.endswith('.png'):
            screenshot_path = os.path.join(screenshots_folder, screenshot_name)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Paso: {screenshot_name.replace('.png', '')}", ln=True, align="L")
            pdf.image(screenshot_path, x=10, y=20, w=180)
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=f"Resultado del Test: {'Passed' if result else 'Failed'}", ln=True, align="C")
    pdf.output(pdf_path)

@given('I am on the WhatsApp Web login page')
def step_given_i_am_on_the_whatsapp_web_login_page(context):
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.driver.get('https://web.whatsapp.com')
    WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
    )  # Espera hasta que el campo de búsqueda esté presente
    time.sleep(5)  # Pausa para observar el proceso
    add_screenshot_to_pdf(context.driver, 'login_page')

@when('I scan the QR code to log in')
def step_when_i_scan_the_qr_code_to_log_in(context):
    time.sleep(15)  # Pausa para permitir al usuario escanear el código QR
    add_screenshot_to_pdf(context.driver, 'QR_Code_Scanned')

@when('I search for the chat with PharmaBot')
def step_when_i_search_for_the_chat_with_pharmabot(context):
    search_box = WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))
    )
    search_box.click()
    search_box.send_keys("PharmaBot")
    time.sleep(5)  # Pausa para ver la búsqueda
    WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='PharmaBot']"))
    )  # Espera hasta que el chat esté visible
    add_screenshot_to_pdf(context.driver, 'search_chat')

@when('I open the chat with PharmaBot')
def step_when_i_open_the_chat_with_pharmabot(context):
    chat = WebDriverWait(context.driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@title='PharmaBot']"))
    )
    context.driver.execute_script("arguments[0].click();", chat)
    time.sleep(5)  # Pausa para observar la apertura del chat
    add_screenshot_to_pdf(context.driver, 'open_chat')

@when('I type "1+1" into the message box')
def step_when_i_type_into_the_message_box(context):
    message_box = WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
    )
    message_box.click()
    time.sleep(2)  # Pausa breve para asegurarse de que el campo de texto está activo
    message_box.send_keys("1+1")
    time.sleep(2)  # Pausa para observar el texto ingresado
    add_screenshot_to_pdf(context.driver, 'type_message')

@when('I send the message')
def step_when_i_send_the_message(context):
    message_box = WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
    )
    message_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Pausa para observar el envío del mensaje
    add_screenshot_to_pdf(context.driver, 'send_message')

@then('I should not receive a response from PharmaBot')
def step_then_i_should_not_receive_a_response_from_pharmabot(context):
    time.sleep(15)  # Pausa para dar tiempo a la posible respuesta
    messages = context.driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")
    result = True
    if messages:
        result = False
        raise AssertionError("Received a response from PharmaBot")
    add_screenshot_to_pdf(context.driver, 'no_response')
    context.driver.quit()

    # Crear el PDF final después de todas las pruebas
    create_pdf_with_screenshots(screenshots_folder, pdf_path, result)
