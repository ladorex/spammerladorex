import requests
import os
import time
import sys
import random
from pystyle import Colors, Colorate
from datetime import datetime
import uuid


def load_user_agents():
    """Agent.txt dosyasından User-Agent'ları yükler"""
    if not os.path.exists("data/Agent.txt"):  # Burada dosyanın data klasöründe olmasına dikkat et
        print(Colorate.Color(Colors.red, "[!] Hata: data/Agent.txt dosyası bulunamadı!"))
        sys.exit(1)

    with open("data/agent.txt", "r", encoding="utf-8") as file:
        agents = [line.strip() for line in file.readlines() if line.strip()]
    
    if not agents:
        print(Colorate.Color(Colors.red, "[!] Hata: data/Agent.txt dosyası boş!"))
        sys.exit(1)
    
    return agents

blacklist = ["ladorex.inc"]
user_agents = load_user_agents()

def gradient_text(text):
    colors = [
        "\033[91m", "\033[93m", "\033[92m", 
        "\033[96m", "\033[94m", "\033[95m"
    ]
    reset = "\033[0m"
    
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        sys.stdout.write(f"{color}{char}{reset}")
        sys.stdout.flush()
        time.sleep(0.002)  
    print()

ascii_text = """
 ██████ ▓█████  ▄▄▄▄   ▓█████  ██▓███    ██████  ██▓▒███████▒
▒██    ▒ ▓█   ▀ ▓█████▄ ▓█   ▀ ▓██░  ██▒▒██    ▒ ▓██▒▒ ▒ ▒ ▄▀░
░ ▓██▄   ▒███   ▒██▒ ▄██▒███   ▓██░ ██▓▒░ ▓██▄   ▒██▒░ ▒ ▄▀▒░ 
  ▒   ██▒▒▓█  ▄ ▒██░█▀  ▒▓█  ▄ ▒██▄█▓▒ ▒  ▒   ██▒░██░  ▄▀▒   ░
▒██████▒▒░▒████▒░▓█  ▀█▓░▒████▒▒██▒ ░  ░▒██████▒▒░██░▒███████▒
▒ ▒▓▒ ▒ ░░░ ▒░ ░░▒▓███▀▒░░ ▒░ ░▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░░▓  ░▒▒ ▓░▒░▒
░ ░▒  ░ ░ ░ ░  ░▒░▒   ░  ░ ░  ░░▒ ░     ░ ░▒  ░ ░ ▒ ░░░▒ ▒ ░ ▒
░  ░  ░     ░    ░    ░    ░   ░░       ░  ░  ░   ▒ ░░ ░ ░ ░ ░
      ░     ░  ░ ░         ░  ░               ░   ░    ░ ░    
                      ░                              ░        
"""

def spam_ngl():
    os.system('clear')

    gradient_text(ascii_text)  

    nglusername = input(Colorate.Color(Colors.orange,"[+] Kullanıcı Adı: ")).strip()

    # 🛑 Kara liste kontrolü
    if nglusername.lower() in blacklist:
        print(Colorate.Color(Colors.red, f"[!] Hata: '{nglusername}' kullanıcısına spam atamazsınız!"))
        time.sleep(3)
        sys.exit(0)

    message = input(Colorate.Color(Colors.orange,"[+] Mesaj: "))

    try:
        count = int(input(Colorate.Color(Colors.orange, "[+] Kaç mesaj gönderilecek: ")))
    except ValueError:
        print(Colorate.Color(Colors.red, "[-] Hata: Sayı girmeniz gerekiyor!"))
        time.sleep(3)
        sys.exit(0)

    print(Colorate.Color(Colors.green,"\n[!] Spam başlıyor... (Durdurmak için Ctrl + C)\n"))

    success = 0
    error = 0

    for i in range(count):
        useragent = random.choice(user_agents)  

        headers = {
            'Host': 'ngl.link',
            'user-agent': useragent,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://ngl.link',
            'referer': f'https://ngl.link/{nglusername}',
        }

        data = {
            'username': nglusername,
            'question': message,
            'deviceId': str(uuid.uuid4()),  # Her istekte farklı cihaz ID
            'gameSlug': '',
            'referrer': '',
        }

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=data)

            now = datetime.now().strftime("%H:%M:%S")

            if response.status_code == 200:
                success += 1
                print(Colorate.Color(Colors.green, f"[{now}] [+] Başarılı => {success}"))
            else:
                error += 1
                print(Colorate.Color(Colors.red, f"[{now}] [-] Hata! Kod => {response.status_code}"))

            time.sleep(random.uniform(1, 2))  # Rastgele bekleme süresi

        except requests.exceptions.RequestException:
            print(Colorate.Color(Colors.red, "[!] Bağlantı hatası! İnternet bağlantınızı kontrol edin."))

    print(Colorate.Color(Colors.orange, "\n<========== İŞLEM TAMAMLANDI ==========>"))
    print(Colorate.Color(Colors.green, f"Başarılı => {success}"))
    print(Colorate.Color(Colors.red, f"Hatalı => {error}"))
    print(Colorate.Color(Colors.orange, "<====================================>\n"))

spam_ngl()
