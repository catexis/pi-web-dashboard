# -*- utf-8 -*-
import requests
from time import sleep
from datetime import datetime
import socket
from subprocess import Popen, PIPE
import json
from statistics import mode

# For logging
import sys, os
import django
sys.path.append(os.path.join(sys.path[0], ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pi_web.settings")
django.setup()
from dashboard.models import LogBotPi

from bot_pi_token import key

# Telegram bot
URL = 'https://api.telegram.org/bot' + key + '/'


def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    d = json.loads(r.text)  # Create dictionary for the responce
    return d


def send_message(chat_id, text = 'Just one moment ...'):
    url = URL + 'sendmessage?chat_id={0}&text={1}'.format(chat_id, text)
    requests.get(url)


def first_read_list_update_id():
    data = get_updates()
    len_of_new_mes_list = len(data['result'])
    update_list = []
    for i in range(0, len_of_new_mes_list, 1):
        update_list.append(data['result'][i]['update_id'])
    return update_list


def log_message(text):
    if text:
        log_string = LogBotPi.objects.create(history = "(bot_pi) {0}".format(text))
        log_string.save()


# DNS update
def ext_ip():
    """
    Function check external ip on different services
    Return ip, if ok
    Return 0, if external ip not checked    
    """
    time_out = 5  # Time out in seconds
    ip = 0  # Zero if nothing to return
    ret_ip = []
    try:
        req = requests.get("http://ipinfo.io/ip", timeout = time_out)
        ip = req.text.strip()
        ret_ip.append(ip)
    except:
        pass
    try:
        req = requests.get("https://api.ipify.org?format=json", timeout = time_out).text
        ip = json.loads(req)["ip"].strip()
        ret_ip.append(ip)
    except:
        pass
    try:
        req = requests.get("http://httpbin.org/ip", timeout = time_out).text
        ip = json.loads(req)["origin"].strip()
        ret_ip.append(ip)
    except:
        pass
    try:
        req = requests.get("https://myexternalip.com/json", timeout = time_out).text
        ip = json.loads(req)["ip"].strip()
        ret_ip.append(ip)
    except:
        pass
    try:
        req = requests.get("http://ipecho.net/plain", timeout = time_out)
        ip = req.text.strip()
        ret_ip.append(ip)
    except:
        pass
    try:
        req = requests.get("http://icanhazip.com", timeout = time_out)
        ip = req.text.strip()
        ret_ip.append(ip)
    except:
        pass
    try:
        req = requests.get("http://ipv4bot.whatismyipaddress.com", timeout = time_out)
        ip = req.text.strip()
        ret_ip.append(ip)
    except:
        pass
    try:
        req = requests.get("https://ident.me/", timeout = time_out)
        ip = req.text.strip()
        ret_ip.append(ip)
    except:
        pass
    log_message("[ext_ip()] return ip: {0}".format(mode(ret_ip)))
    return mode(ret_ip)


def dns_update(ip):
    domain = "catexis.ddns.net"  # Для указанного домена
    username = "catexis"  # Для этого пользователя
    password = "nosredna"  # с этим паролем
    time_out = 5  # Time out for request
    ret = 0  # Возвращаемое значение
    update_url = "http://" + username + ":" + password + "@dynupdate.no-ip.com/nic/update?hostname=" + domain + "&myip=" + ip
    try:
        log_message("[update_ip({0})] Запускаю обновление DNS".format(ip))
        req = requests.get(update_url, timeout = time_out)
        if req.status_code == 200:
            ret = 1
            log_message("[update_ip({0})] Успешно!".format(ip))
        else:
            log_message("[update_ip({0})] Сервер вернул код {1}".format(ip, req.status_code))
    except:
        pass
    return ret


req = get_updates()
if req["result"][-1]["message"]["message_id"]:
    last_message_id = int(req["result"][-1]["message"]["message_id"])
else:
    last_message_id = 0
chat_id = 30596375
count = 0
commands = [
    "/update_ip",
    "/help",
    "/dns_record",
    "/ext_ip",
    "/ping",
    "/start"
    ]

if __name__ == "__main__":
    send_message(chat_id, text="Бот запущен")
    log_message("bot_pi_v2 started")
    while 1:
        # Part of telegram bot
        req = get_updates()
        if req["result"][-1]["message"]["message_id"]:
            message_id = int(req["result"][-1]["message"]["message_id"])
            res_chat_id = int(req["result"][-1]["message"]["from"]["id"])
        else:
            message_id = 0
        
        if message_id > last_message_id and res_chat_id == chat_id:
            txt = req["result"][-1]["message"]["text"]
            
            if txt == "/help":
                text = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(
                    "Доступные команды:",
                    "/start - приветствие"
                    "/help - вывод всех доступных команд",
                    "/update_ip - обновить запись DNS",
                    "/dns_record - текущее доменное имя",
                    "/ext_ip - текущий внешний IP",
                    "/ping - проверка работы бота"
                )
                send_message(chat_id, text=text)
                del text

            if txt == "/start":
                send_message(chat_id, text="Hi! Use /help")

            if txt == "/update_ip":
                log_message("(update_ip) command start")
                ip_check = socket.gethostbyname('catexis.ddns.net')
                ext_ip = ext_ip()
                log_message("(update_ip) ext_ip = {0}".format(ext_ip))
                if ip_check != ext_ip:
                    upd_status = dns_update(ext_ip)
                    if upd_status == 1:
                        send_message(chat_id, text="ok")
                    else:
                        send_message(chat_id, text="Что-то пошло не так...")
                else:
                    send_message(chat_id, text="DNS record is correct!")

            if txt == "/dns_record":
                ip_check = socket.gethostbyname('catexis.ddns.net')
                log_message("(dns_record) ip_check = {0}".format(ip_check))
                text = "{0}\n{1}".format(
                    "catexis.ddns.net",
                    ip_check
                )
                send_message(chat_id, text=text)
                del ip_check

            if txt == "/ext_ip":
                text = ext_ip()
                send_message(chat_id, text=text)
                del text

            if txt == "/ping":
                text = "pong"
                send_message(chat_id, text=text)
                del text

            if txt not in commands:
                send_message(chat_id, text="Для вывода всех доступных комманд введите /help")

            last_message_id = message_id
        
        del req
        del message_id

        # Part of check ip
        if count > 61:  # Внешний IP проверяется раз в 5 минут (примерно)
            ip_check = socket.gethostbyname('catexis.ddns.net')  # Чекнули какой ip у dns записи
            ext_ip = ext_ip()  # Взяли внешний ip
            if ip_check != ext_ip:
                send_message(chat_id, text="Выдан новый IP. Начинаю обновление.")
                log_message("(from update cycle) Выдан новый IP. Начинаю обновление.")
                upd_status = dns_update(ext_ip)
                if upd_status == 1:
                    send_message(chat_id, text="Команда на обновления успешно отправлена")
                    for i in range(0,600,1):  # В течении 10 минут чекаем DNS запись
                        ip_check = socket.gethostbyname('catexis.ddns.net')
                        if ip_check == ext_ip:
                            text = "{0}\n{1}{2}".format(
                                "Запись DNS обновлена",
                                "Новый ip: ",
                                ip_check
                            )
                            send_message(chat_id, text=text)
                            log_message("(from update cycle) Запись DNS обновлена на {0} скунде".format(i))
                            del text
                            break
                        sleep(1)
                else:
                    send_message(chat_id, text="Что-то пошло не так...")
                    log_message("(ip check cicle) IP в DNS не обновлён")
            count = 0
        count += 1

        sleep(5)