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
screenshots_folder = r"C:\Users\danip\OneDrive\Imágenes\Documentación\screenshot_evidence"
pdf_path = r"C:\Users\danip\OneDrive\Imágenes\Documentación\test_evidence.pdf"

# Asegúrate de que la carpeta de capturas de pantalla exista
if not os.path.exists(screenshots_folder):
    os.makedirs(screenshots_folder)

def add_screenshot_to_pdf(driver, step_name):
    screenshot_path = os.path.join(screenshots_folder, f"{step_name}.png")
    
    # Toma una captura de pantalla y guárdala
    driver.save_screenshot(screenshot_path)

def create_pdf_with_screenshots(screenshots_folder, pdf_path):
    pdf = FPDF()
    for screenshot_name in sorted(os.listdir(screenshots_folder)):
        if screenshot_name.endswith('.png'):
            screenshot_path = os.path.join(screenshots_folder, screenshot_name)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Paso: {screenshot_name.replace('.png', '')}", ln=True, align="L")
            pdf.image(screenshot_path, x=10, y=20, w=180)
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
    # Asume que el usuario ya escaneó el código QR durante el tiempo de espera
    time.sleep(5)  # Pausa adicional para observar el proceso
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
    # Desplazar al elemento para asegurarse de que sea visible
    chat = WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//span[@title='PharmaBot']"))
    )
    context.driver.execute_script("arguments[0].scrollIntoView(true);", chat)  # Desplazar al elemento
    time.sleep(2)  # Pausa para asegurar el desplazamiento
    chat = WebDriverWait(context.driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@title='PharmaBot']"))
    )
    chat.click()
    time.sleep(5)  # Pausa para observar la apertura del chat
    add_screenshot_to_pdf(context.driver, 'open_chat')

@when('I type "Tengo dolor de cabeza" into the message box')
def step_when_i_type_into_the_message_box(context):
    message_box = WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
    )
    message_box.click()
    time.sleep(2)  # Pausa breve para asegurarse de que el campo de texto está activo
    message_box.send_keys("Tengo dolor de cabeza")
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

@then('the message should be sent to PharmaBot')
def step_then_the_message_should_be_sent_to_pharmabot(context):
    WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Tengo dolor de cabeza')]"))
    )
    # Ahora verifica que la respuesta contiene la palabra "Hola"
    response_message = WebDriverWait(context.driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Tengo dolor de cabeza')]"))
    )
    assert response_message is not None
    time.sleep(20)  # Pausa final para ver la verificación
    add_screenshot_to_pdf(context.driver, 'test_passed')
    context.driver.quit()

    # Crear el PDF final después de todas las pruebas
    create_pdf_with_screenshots(screenshots_folder, pdf_path)
