# pip install Flask
# pip install Werkzeug
# pip install selenium 
# pip install beautifulsoup4
# pip install webdriver-manager
# pip install lxml

import time
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from bs4.element import Tag
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

app = Flask(__name__)

def clean_text(text:str):
    text = ' '.join(text.replace("\n", " ").replace("\t", " ").split())
    return text


@app.route('/')
def hello_word():
    return jsonify(saludo='¡Hola Mundo!')

@app.route('/consultar/ruc', methods=['GET'])
def get_titles():
    
    chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'
    driver.get(url)
    
    ruc = request.args.get('number', default = 0, type = int)
    wait_10 = WebDriverWait(driver, 10)
    
    input_ruc = driver.find_element(By.ID, 'txtRuc')
    input_ruc.send_keys(ruc)
    
    boton_ruc = driver.find_element(By.ID, 'btnAceptar')
    boton_ruc.click()
    
    try:
        current_url = driver.current_url   
    except UnexpectedAlertPresentException as e: 
        current_url = "bloqued"
        print(f'ERROR_VALID=[[{e}]]')
    
    if current_url.rstrip('/') == url.rstrip('/'):
        print("PASO AQUI")
        button_before = wait_10.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.form-button')))
        button_before.click()
        boton_ruc = wait_10.until(EC.presence_of_element_located((By.ID, 'btnAceptar'))) 
        boton_ruc.click()
        button_return = wait_10.until(EC.presence_of_element_located((By.ID, 'aNuevaConsulta'))) # importante no quitar
    
    data = {
        "estado": False,
        'mensaje': 'No encontrado',
        "resultado": {}
    }
        
    if current_url != "bloqued":
        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            id = ruc
            estado_api = True
            mensaje = 'Encontrado'
            numero_ruc = clean_text(soup.find('h4', string='Número de RUC:').parent.find_next_sibling('div').find('h4').text)
            print("PASO 01 ===================")
            tipo_contribuyente = clean_text(soup.find('h4', string='Tipo Contribuyente:').parent.find_next_sibling('div').find('p').text)
            print("PASO 02 ===================")
            tipo_documento = clean_text(soup.find('h4', string='Tipo de Documento:').parent.find_next_sibling('div').find('p').text) if soup.find('h4', string='Tipo de Documento:') else None
            print("PASO 03 ===================")
            nombre_comercial = clean_text(soup.find('h4', string='Nombre Comercial:').parent.find_next_sibling('div').find('p').text)
            print("PASO 04 ===================")
            fecha_inscripcion = clean_text(soup.find('h4', string='Fecha de Inscripción:').parent.find_next_sibling('div').find('p').text)
            print("PASO 05 ===================")
            fecha_inicio_actividades = clean_text(soup.find('h4', string='Fecha de Inicio de Actividades:').parent.find_next_sibling('div').find('p').text)
            print("PASO 06 ===================")
            estado_contribuyente = clean_text(soup.find('h4', string='Estado del Contribuyente:').parent.find_next_sibling('div').find('p').text)
            print("PASO 07 ===================")
            condicion_contribuyente = clean_text(soup.find('h4', string='Condición del Contribuyente:').parent.find_next_sibling('div').find('p').text)
            print("PASO 08 ===================")
            domicilio_fiscal = clean_text(soup.find('h4', string='Domicilio Fiscal:').parent.find_next_sibling('div').find('p').text)
            print("PASO 09 ===================")
            sistema_emision_comprobante = clean_text(soup.find('h4', string='Sistema Emisión de Comprobante:').parent.find_next_sibling('div').find('p').text)
            print("PASO 10 ===================")
            actividad_comercio_exterior = clean_text(soup.find('h4', string='Actividad Comercio Exterior:').parent.find_next_sibling('div').find('p').text)
            print("PASO 11 ===================")
            sistema_contabilidad = clean_text(soup.find('h4', string='Sistema Contabilidad:').parent.find_next_sibling('div').find('p').text)
            print("PASO 12 ===================")
            
            actividades_economicas = []
            tabla_ae = soup.find('h4', string='Actividad(es) Económica(s):').parent.find_next_sibling('div').find('table')
            if tabla_ae != None:
                for i in tabla_ae.find_all('tr'):
                    if isinstance(i, Tag):
                        actividades_economicas.append(clean_text(i.find('td').text))
            print("PASO 13 ===================")
            comprobantes_pagos = []
            tabla_cp = soup.find('h4', string='Comprobantes de Pago c/aut. de impresión (F. 806 u 816):').parent.find_next_sibling('div').find('table')
            if tabla_cp != None:
                for i in tabla_cp.find_all('tr'):
                    if isinstance(i, Tag):
                        comprobantes_pagos.append(clean_text(i.find('td').text))
            print("PASO 14 ===================")
            sistema_emision_electronica = []
            tabla_see = soup.find('h4', string='Sistema de Emisión Electrónica:').parent.find_next_sibling('div').find('table')
            if tabla_see != None:
                for i in tabla_see.find_all('tr'):
                    if isinstance(i, Tag):
                        sistema_emision_electronica.append(clean_text(i.find('td').text))
            print("PASO 15 ===================")
            fecha_emision_electronica = clean_text(soup.find('h4', string='Sistema Contabilidad:').parent.find_next_sibling('div').find('p').text)
            print("PASO 16 ===================")
            comprobantes_electronicos = clean_text(soup.find('h4', string='Comprobantes Electrónicos:').parent.find_next_sibling('div').find('p').text)
            print("PASO 17 ===================")        
            fecha_afiliado_ple = clean_text(soup.find('h4', string='Afiliado al PLE desde:').parent.find_next_sibling('div').find('p').text)
            print("PASO 18 ===================")
            padrones = []
            tabla_p = soup.find('h4', string='Padrones:').parent.find_next_sibling('div').find('table')
            if tabla_p != None:
                for i in tabla_p.find_all('tr'):
                    if isinstance(i, Tag):
                        padrones.append(clean_text(i.find('td').text))
            print("PASO 19 ===================")
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
            print(f'ERROR_GET_DATA=[[{e}]]')
            
    driver.quit()

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
