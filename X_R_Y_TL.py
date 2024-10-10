import requests
from colorama import Fore, Style, init
import socket
import os

init()

TELEGRAM_API_URL = ''
CURRENT_VERSION = "0.1.1"  # الإصدار الحالي للأداة

def display_title():
    title = "X_R-Y_TOOL"
    version = f"Version {CURRENT_VERSION}"  # عرض الإصدار الحالي
    red_part = Fore.RED + title[:len(title)//2] + Style.RESET_ALL
    blue_part = Fore.BLUE + title[len(title)//2:] + Style.RESET_ALL
    centered_title = f"{red_part}{blue_part}".center(50)
    centered_version = version.center(50)  # تنسيق الإصدار ليكون في الوسط
    os.system('cls' if os.name == 'nt' else 'clear')  # مسح الشاشة
    print("\n" + centered_title + "\n" + centered_version + "\n")

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

def check_for_update():
    try:
        # الرابط الخاص بالأداة المحدثة
        url = 'https://raw.githubusercontent.com/xrida01/X_R-Y_TOOL/main/X_R_Y_TL.py'
        response = requests.get(url)
        
        if response.status_code == 200:
            remote_code = response.text
            # استخراج الإصدار من الكود البعيد
            remote_version = None
            for line in remote_code.splitlines():
                if "CURRENT_VERSION" in line:
                    remote_version = line.split("=")[-1].strip().strip('"')
                    break

            if remote_version and remote_version != CURRENT_VERSION:
                print(Fore.YELLOW + f"New version available: {remote_version}. Updating..." + Style.RESET_ALL)
                # حفظ الملف الجديد
                with open('X_R_Y_TL_updated.py', 'w') as f:
                    f.write(remote_code)
                print(Fore.GREEN + "Update downloaded. Running the new version..." + Style.RESET_ALL)
                os.system('python X_R_Y_TL_updated.py')  # تشغيل الإصدار الجديد
                exit()  # إنهاء العملية الحالية
            else:
                print(Fore.GREEN + "You are using the latest version." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Failed to check for updates. Please try again later." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"Error while checking for updates: {e}" + Style.RESET_ALL)

def main():
    display_title()
    print("Choose your response option:")
    print("1. Send response via Telegram bot")
    print("2. Normal response (display only)")
    print("3. Save response to a text file")
    print("4. Check for updates")
    print("5. Exit")

    option = input("Enter your choice (1-5): ")
    
    if option not in ['1', '2', '3', '4', '5']:
        print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
        return

    if option == '5':
        print("Exiting...")
        return

    if option == '4':
        check_for_update()
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
