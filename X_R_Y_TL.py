import requests
from colorama import Fore, Style, init
import socket
import os

init()

TELEGRAM_API_URL = ''

def display_title():
    title = "X_R-Y_TOOL"
    red_part = Fore.RED + title[:len(title)//2] + Style.RESET_ALL
    blue_part = Fore.BLUE + title[len(title)//2:] + Style.RESET_ALL
    centered_title = f"{red_part}{blue_part}".center(50)
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    print("\n" + centered_title + "\n")

def get_port_info(url):
    parsed_url = url.split('//')[-1]
    hostname = parsed_url.split('/')[0]
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((hostname, 80))
            return 80
    except (socket.error, socket.timeout):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((hostname, 443))
                return 443
        except (socket.error, socket.timeout):
            return None

def send_telegram_message(message, TELEGRAM_CHAT_ID):
    try:
        response = requests.post(TELEGRAM_API_URL, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
        response.raise_for_status()
    except requests.RequestException as e:
        print(Fore.RED + f"Failed to send message to Telegram: {e}" + Style.RESET_ALL)

def log_to_file(message):
    with open('results.txt', 'a') as f:
        f.write(message + '\n')

def check_website(url, option, TELEGRAM_CHAT_ID):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            port = get_port_info(url)
            port_info = f"Port: {port if port else 'Unknown'}"
            message = f"{url} is up\nServer: {response.headers.get('Server', 'Unknown')}\n{port_info}"
            print(Fore.GREEN + message + Style.RESET_ALL)
            if option == '1':
                send_telegram_message(message, TELEGRAM_CHAT_ID)
            elif option == '3':
                log_to_file(message)
        else:
            print(Fore.RED + f"{url} is down (status code: {response.status_code})" + Style.RESET_ALL)
    except requests.RequestException:
        print(Fore.RED + f"{url} is unreachable" + Style.RESET_ALL)

def main():
    display_title()
    print("Choose your response option:")
    print("1. Send response via Telegram bot")
    print("2. Normal response (display only)")
    print("3. Save response to a text file")
    print("4. Exit")

    option = input("Enter your choice (1-4): ")
    
    if option not in ['1', '2', '3', '4']:
        print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
        return

    if option == '4':
        print("Exiting...")
        return

    TELEGRAM_CHAT_ID = None

    if option == '1':
        TELEGRAM_TOKEN = input("Enter your Telegram bot token: ")
        TELEGRAM_CHAT_ID = input("Enter your chat ID: ")
        global TELEGRAM_API_URL
        TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

    print("Enter websites to check their status (type 'done' to finish):")
    
    while True:
        url = input("Enter website (e.g., example.com): ")
        if url.lower() == 'done':
            break
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        check_website(url, option, TELEGRAM_CHAT_ID)

if __name__ == "__main__":
    main()
