# Scraping Sunat

Este proyecto puede ser útil para obtener información de los RUC ubicados en la pagina de la SUNAT


## Requisitos

Asegúrate de tener Python instalado en tu sistema. 
Asegúrate de tener el navegador web compatible con el WebDriver de Selenium.

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/erixcel/scraping-sunat-api.git
```
2. Navega al directorio del proyecto:
```bash
cd scraping-sunat-api
```
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el script de scraping con:
```bash
python main.py
```

## Docker

Si prefieres usar Docker, puedes construir y ejecutar el contenedor con los siguientes comandos:

1. Construye la imagen Docker:
```bash
docker build -t scraping-sunat-api .
```
2. Ejecuta el contenedor:
```bash
docker run -p 5000:5000 scraping-sunat-api
```


## Estructura del Proyecto

- `main.py`: Script principal que realiza el scraping.
- `requirements.txt`: Lista de dependencias necesarias.
- `Dockerfile`: Archivo de configuración para construir la imagen Docker.




