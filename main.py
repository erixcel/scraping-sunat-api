# pip install Flask
# pip install Werkzeug
# pip install selenium 
# pip install beautifulsoup4
# pip install webdriver-manager
# pip install lxml

import threading
import requests
import time
from flask import Flask, jsonify, request
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from bs4.element import Tag
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)

def call_api():
    while True:
        try:
            response = requests.get('https://web-scraping-sunat.onrender.com/')
            response.raise_for_status()
            print(response.json())
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')
        time.sleep(10)

def clean_text(text:str):
    text = ' '.join(text.replace("\n", " ").replace("\t", " ").split())
    return text

def find_error_page(driver):
    try:
        button_before = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.form-button')))
        return 'error'
    except Exception:
        return None

def find_correct_page(driver):
    try:
        button_return = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'aNuevaConsulta')))
        return 'correct'
    except Exception:
        return None

@app.route('/', methods=['GET'])
def hello_word():
    return jsonify(message='Te saluda Erick Flores, creador de esta api de scraping de sunat, siente libre de usarla, la api suele demorar 5s en ejecutarse')

@app.route('/consultar/ruc', methods=['GET'])
def get_ruc():
    
    data = {
        "estado": False,
        'mensaje': 'No encontrado',
        "resultado": {}
    }
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    url = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'
    driver.get(url)
    
    ruc = request.args.get('number', default = 0, type = int)
    
    try:
        input_ruc = driver.find_element(By.ID, 'txtRuc')
        input_ruc.send_keys(ruc)
        boton_ruc = driver.find_element(By.ID, 'btnAceptar')
        boton_ruc.click()
        
        try:
            alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
            print("RUC NO ENCONTRADO")

        except Exception:
            with ThreadPoolExecutor(max_workers=2) as executor:
                done = True
                while done:
                    futures = {executor.submit(find_error_page, driver), executor.submit(find_correct_page, driver)}
                    for future in as_completed(futures):
                        result = future.result()
                        if result == 'error':
                    
                            button_before = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.form-button')))
                            print("LLEGO PAG ERROR ===================")
                            actions = ActionChains(driver)
                            actions.move_to_element(button_before).click(button_before).perform()
                            
                            boton_ruc = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'btnAceptar')))
                            print("REGRESO PAG INICIO ===================")
                            actions = ActionChains(driver)
                            actions.move_to_element(boton_ruc).click(boton_ruc).perform()
                            break
                        elif result == 'correct':
                            print("CARGO PAG DATA ===================")
                            done = False
                            break
                
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            id = ruc
            estado_api = True
            mensaje = 'Encontrado'
            numero_ruc = clean_text(soup.find('h4', string='Número de RUC:').parent.find_next_sibling('div').find('h4').text)
            # print("PASO 01 ===================")
            tipo_contribuyente = clean_text(soup.find('h4', string='Tipo Contribuyente:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 02 ===================")
            tipo_documento = clean_text(soup.find('h4', string='Tipo de Documento:').parent.find_next_sibling('div').find('p').text) if soup.find('h4', string='Tipo de Documento:') else None
            # print("PASO 03 ===================")
            nombre_comercial = clean_text(soup.find('h4', string='Nombre Comercial:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 04 ===================")
            fecha_inscripcion = clean_text(soup.find('h4', string='Fecha de Inscripción:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 05 ===================")
            fecha_inicio_actividades = clean_text(soup.find('h4', string='Fecha de Inicio de Actividades:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 06 ===================")
            estado_contribuyente = clean_text(soup.find('h4', string='Estado del Contribuyente:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 07 ===================")
            condicion_contribuyente = clean_text(soup.find('h4', string='Condición del Contribuyente:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 08 ===================")
            domicilio_fiscal = clean_text(soup.find('h4', string='Domicilio Fiscal:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 09 ===================")
            sistema_emision_comprobante = clean_text(soup.find('h4', string='Sistema Emisión de Comprobante:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 10 ===================")
            actividad_comercio_exterior = clean_text(soup.find('h4', string='Actividad Comercio Exterior:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 11 ===================")
            sistema_contabilidad = clean_text(soup.find('h4', string='Sistema Contabilidad:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 12 ===================")
            
            actividades_economicas = []
            tabla_ae = soup.find('h4', string='Actividad(es) Económica(s):').parent.find_next_sibling('div').find('table')
            if tabla_ae != None:
                for i in tabla_ae.find_all('tr'):
                    if isinstance(i, Tag):
                        actividades_economicas.append(clean_text(i.find('td').text))
            # print("PASO 13 ===================")
            comprobantes_pagos = []
            tabla_cp = soup.find('h4', string='Comprobantes de Pago c/aut. de impresión (F. 806 u 816):').parent.find_next_sibling('div').find('table')
            if tabla_cp != None:
                for i in tabla_cp.find_all('tr'):
                    if isinstance(i, Tag):
                        comprobantes_pagos.append(clean_text(i.find('td').text))
            # print("PASO 14 ===================")
            sistema_emision_electronica = []
            tabla_see = soup.find('h4', string='Sistema de Emisión Electrónica:').parent.find_next_sibling('div').find('table')
            if tabla_see != None:
                for i in tabla_see.find_all('tr'):
                    if isinstance(i, Tag):
                        sistema_emision_electronica.append(clean_text(i.find('td').text))
            # print("PASO 15 ===================")
            fecha_emision_electronica = clean_text(soup.find('h4', string='Sistema Contabilidad:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 16 ===================")
            comprobantes_electronicos = clean_text(soup.find('h4', string='Comprobantes Electrónicos:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 17 ===================")        
            fecha_afiliado_ple = clean_text(soup.find('h4', string='Afiliado al PLE desde:').parent.find_next_sibling('div').find('p').text)
            # print("PASO 18 ===================")
            padrones = []
            tabla_p = soup.find('h4', string='Padrones:').parent.find_next_sibling('div').find('table')
            if tabla_p != None:
                for i in tabla_p.find_all('tr'):
                    if isinstance(i, Tag):
                        padrones.append(clean_text(i.find('td').text))
            # print("PASO 19 ===================")
            data = {
                "id": id,
                "estado": estado_api,
                "mensaje": mensaje,
                "resultado": {
                    "numero_ruc": numero_ruc,
                    "tipo_contribuyente": tipo_contribuyente,
                    "tipo_documento": tipo_documento,
                    "nombre_comercial": nombre_comercial,
                    "fecha_inscripcion": fecha_inscripcion,
                    "fecha_inicio_actividades": fecha_inicio_actividades,
                    "estado_contribuyente": estado_contribuyente,
                    "condicion_contribuyente": condicion_contribuyente,
                    "domicilio_fiscal": domicilio_fiscal,
                    "sistema_emision_comprobante": sistema_emision_comprobante,
                    "actividad_comercio_exterior": actividad_comercio_exterior,
                    "sistema_contabilidad": sistema_contabilidad,
                    "actividades_economicas": actividades_economicas,
                    "comprobantes_pagos": comprobantes_pagos,
                    "sistema_emision_electronica": sistema_emision_electronica,
                    "fecha_emision_electronica": fecha_emision_electronica,
                    "comprobantes_electronicos": comprobantes_electronicos,
                    "fecha_afiliado_ple": fecha_afiliado_ple,
                    "padrones": padrones
                }
            }
            
    except Exception as e:
        print(f'ERROR_CONTROLED=[[{e}]]')
        pass
            
    driver.quit()

    return jsonify(data)

if __name__ == '__main__':
    # thread = threading.Thread(target=call_api)
    # thread.start()
    app.run(host='0.0.0.0')