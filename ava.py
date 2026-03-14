from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# === CONFIGURAÇÕES ===
usuario = "AQUI VAI O SEU LOGIN"
senha = "AQUI VAI A SUA SENHA"
url_login = "https://ead.unieuro.edu.br/login/index.php"
nome_disciplina = "24 | GPSINN | PROJETO INTEGRADOR DE SISTEMAS COMPUTACIONAIS"
nome_arquivo = "globo.pdf"
pasta_download = os.path.join(os.getcwd(), "downloads")  # cria pasta "downloads" no projeto

if not os.path.exists(pasta_download):
    os.makedirs(pasta_download)

# Caminho do chromedriver baixado (ajuste se necessário)
caminho_chromedriver = r"C:\chromedriver\chromedriver-win64\chromedriver.exe"

# Configuração do Chrome para salvar PDF automaticamente
options = Options()
prefs = {
    "download.default_directory": pasta_download,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)

# Iniciar navegador
service = Service(caminho_chromedriver)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    # 1. Acessar página de login
    driver.get(url_login)

    # 2. Fazer login
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(senha)
    driver.find_element(By.ID, "loginbtn").click()

    # 3. Entrar na disciplina
    disciplina_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, nome_disciplina))
    )
    disciplina_link.click()

    # 4. Baixar o PDF
    pdf_link = wait.until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, nome_arquivo))
    )
    pdf_link.click()

    # Esperar o download terminar
    time.sleep(10)

finally:
    driver.quit()

print(f"✅ Arquivo '{nome_arquivo}' salvo em: {pasta_download}")
