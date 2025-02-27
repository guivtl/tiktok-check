# importação das bibliotecas necessárias para o funcionamento do bot
import json
import os
import random
import time
import signal
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Back, Style, init
from tiktok_captcha_solver import SeleniumSolver
import requests

# inicialização do colorama para suporte a cores no terminal
init(autoreset=True)

# carregamento do arquivo de configuração com as credenciais
try:
    with open('config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print(f"{Fore.RED}Erro: Arquivo config.json não encontrado.")
    exit(1)
except json.JSONDecodeError:
    print(f"{Fore.RED}Erro: Arquivo config.json está mal formatado.")
    exit(1)

# classe principal responsável pela verificação de bloqueio no tiktok
class TikTokChecker:
    def __init__(self):
        # inicialização do contador de verificações
        self.verification_count = 0
        # inicialização das variáveis do selenium e captcha
        self.driver = None
        self.sadcaptcha = None

    def setup_driver(self):
        # configuração das opções do chrome para execução em modo headless
        chrome_options = Options()
        chrome_options.add_argument("--headless=New")  # execução sem interface gráfica
        chrome_options.add_argument("--no-sandbox")    # modo sandbox desativado
        chrome_options.add_argument("--disable-gpu")   # desativa aceleração gpu
        chrome_options.add_argument("--window-size=1366,768")  # dimensões da janela
        # configuração do user agent para simular dispositivo móvel
        chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1")
        chrome_options.add_argument("--disable-webrtc")  # desativa webrtc para privacidade

        # inicialização do webdriver do chrome
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        # inicialização do solucionador de captcha
        self.sadcaptcha = SeleniumSolver(self.driver, config.get('sadcaptcha_api_key'))

    def manual_login(self):
        # processo de login manual no tiktok
        self.setup_driver()
        print(f"{Fore.YELLOW}Abrindo página de login do TikTok...")
        self.driver.get('https://www.tiktok.com/login')
        
        # orientações para o usuário realizar o login
        print(f"{Fore.CYAN}Por favor, faça o login manualmente no navegador aberto.")
        print(f"{Fore.CYAN}Após fazer o login, navegue para a página principal do TikTok.")
        input(f"{Fore.CYAN}Quando estiver logado e na página principal, pressione Enter aqui...")

        try:
            # validação da permanência na página do tiktok
            if "tiktok.com" not in self.driver.current_url:
                print(f"{Fore.RED}Erro: Não estamos mais na página do TikTok. Por favor, tente novamente.")
                self.driver.quit()
                return

            # armazenamento dos cookies para uso posterior
            cookies = self.driver.get_cookies()
            with open('tiktok_cookies.json', 'w') as f:
                json.dump(cookies, f)
            print(f"{Fore.GREEN}Cookies salvos com sucesso!")

        except Exception as e:
            print(f"{Fore.RED}Erro ao salvar cookies: {str(e)}")
        finally:
            self.driver.quit()

    def load_cookies(self):
        self.driver.get('https://www.tiktok.com')
        with open('tiktok_cookies.json', 'r') as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def check_user_blocked(self, target_user):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(HEADER)
        self.verification_count += 1
        print(f"{Fore.GREEN}Verificação {self.verification_count}: Checando @{target_user}")
        self.driver.get(f"https://www.tiktok.com/@{target_user}")
        time.sleep(2)

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "swiper-wrapper")))
            swiper_wrapper = self.driver.find_element(By.CLASS_NAME, "swiper-wrapper")
            is_blocked = all(text in swiper_wrapper.text for text in [
                "Não é possível visualizar os vídeos devido às configurações de privacidade do usuário.",
                "Sem conteúdo"
            ])

            if is_blocked:
                print(f"{Fore.RED}Usuário {target_user} está bloqueado.")
                return True

            print(f"{Fore.GREEN}Usuário {target_user} está desbloqueado.")
            self.sadcaptcha.solve_captcha_if_present()
            time.sleep(1)
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"{target_user}_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            self.send_telegram_message(target_user, screenshot_path)

            return False
        except Exception as e:
            print(f"{Fore.RED}Erro ao verificar o usuário {target_user}: {str(e)}")
            return True

    def send_telegram_message(self, target_user, screenshot_path):
        current_time = datetime.now().strftime("%H:%M")
        message = f"@{target_user} te desbloqueou às: {current_time}"
        url = f"https://api.telegram.org/bot{config['telegram_bot_token']}/sendPhoto"
        
        with open(screenshot_path, "rb") as image_file:
            files = {"photo": image_file}
            data = {"chat_id": config['telegram_chat_id'], "caption": message}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print(f"{Fore.GREEN}Mensagem enviada com sucesso para o Telegram.")
        else:
            print(f"{Fore.RED}Erro ao enviar mensagem para o Telegram: {response.text}")

    def check_user(self, target_user):
        print(f"{Fore.CYAN}Iniciando verificação para o usuário @{target_user}")
        self.setup_driver()
        self.load_cookies()
        while True:
            is_blocked = self.check_user_blocked(target_user)
            if not is_blocked:
                break
            delay = random.randint(2, 11)
            print(f"{Fore.BLUE}Verificando novamente em {delay} segundos...")
            time.sleep(delay)
        self.driver.quit()

def signal_handler(sig, frame):
    print(f"\n{Fore.GREEN}Programa interrompido pelo usuário. Encerrando...")
    exit(0)

def main_login():
    checker = TikTokChecker()
    checker.print_header()
    print(f"{Fore.CYAN}Iniciando processo de login manual...")
    checker.manual_login()

def main_check():
    checker = TikTokChecker()
    checker.print_header()
    while True:
        target_user = input(f"{Fore.BLUE}Digite o @usuario que deseja verificar (ou 'sair' para encerrar): ")
        if target_user.lower() == 'sair':
            break
        checker.check_user(target_user)
        print(f"\n{Fore.MAGENTA}Pressione Enter para verificar outro usuário ou digite 'sair' para encerrar.")
        if input().lower() == 'sair':
            break
    print(f"{Fore.GREEN}Programa encerrado. Obrigado por usar!")

if __name__ == "__main__":
    HEADER = f"""{Fore.CYAN}
╔════════════════════════════════════════════════════════════════════════════╗
║                        TIKTOK BLOCK CHECKER v1.0                           ║
║                                                                           ║
║  ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗    ██████╗  ██████╗████████╗ ║
║  ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝    ██╔══██╗██╔═══██╚══██╔══╝ ║
║     ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝     ██████╔╝██║   ██║  ██║    ║
║     ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗     ██╔══██╗██║   ██║  ██║    ║
║     ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    ██████╔╝╚██████╔╝  ██║    ║
║     ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝   ╚═╝    ║
║                                                                           ║
╚════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""

    signal.signal(signal.SIGINT, signal_handler)
    print(HEADER)
    print(f"{Fore.YELLOW}Escolha uma opção:")
    print(f"{Fore.YELLOW}1 - Fazer login manual e salvar cookies")
    print(f"{Fore.YELLOW}2 - Verificar usuários (usando cookies salvos)")
    choice = input(f"{Fore.BLUE}Digite sua escolha (1 ou 2): ")
    if choice == '1':
        main_login()
    elif choice == '2':
        if not os.path.exists('tiktok_cookies.json'):
            print(f"{Fore.RED}Erro: Arquivo de cookies não encontrado. Por favor, faça o login manual primeiro.")
            time.sleep(5)
            print(f"{Fore.RED}Encerrando programa...")
            time.sleep(2)
            exit(0)
        else:
            main_check()
    else:
        print(f"{Fore.RED}Escolha inválida. Por favor, execute o programa novamente.")