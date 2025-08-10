<div align="center">
    <a href="https://www.youtube.com/@avencores/" target="_blank">
      <img src="https://github.com/user-attachments/assets/338bcd74-e3c3-4700-87ab-7985058bd17e" alt="YouTube" height="40">
    </a>
    <a href="https://t.me/avencoresyt" target="_blank">
      <img src="https://github.com/user-attachments/assets/939f8beb-a49a-48cf-89b9-d610ee5c4b26" alt="Telegram" height="40">
    </a>
    <a href="https://vk.com/avencoresvk" target="_blank">
      <img src="https://github.com/user-attachments/assets/dc109dda-9045-4a06-95a5-3399f0e21dc4" alt="VK" height="40">
    </a>
    <a href="https://dzen.ru/avencores" target="_blank">
      <img src="https://github.com/user-attachments/assets/bd55f5cf-963c-4eb8-9029-7b80c8c11411" alt="Dzen" height="40">
    </a>
</div>

# 📖 Описание проекта

Автоматически обновляемая коллекция публичных VPN-конфигов (V2Ray / VLESS / Trojan / VMess / Reality / Shadowsocks) для быстрого обхода блокировок.
  
Каждый конфиг — это TXT-подписка, которую можно импортировать практически в любой современный клиент (v2rayNG, NekoRay, Throne, v2rayN, V2Box, v2RayTun, Hiddify и др.).

Конфиги обновляются каждые **9 минут** с помощью GitHub Actions, поэтому ссылки из раздела «📋 Общий список всех вечно актуальных конфигов» всегда актуальны.

---

## 📑 Содержание
- [📖 Описание проекта](#-описание-проекта)
  - [📑 Содержание](#-содержание)
  - [🚀 Быстрый старт](#-быстрый-старт)
  - [⚙️ Как это работает](#️-как-это-работает)
  - [🗂 Структура репозитория](#-структура-репозитория)
  - [🔧 Локальный запуск генератора](#-локальный-запуск-генератора)
- [🎦 Видео гайд по установке и решению проблем](#-видео-гайд-по-установке-и-решению-проблем)
- [🗂️ Общее меню гайдов репозитория](#️-общее-меню-гайдов-репозитория)
- [📜 Лицензия](#-лицензия)
- [💰 Поддержать автора](#-поддержать-автора)

---

## 🚀 Быстрый старт
1. Скопируйте нужную ссылку из раздела «📋 Общий список всех вечно актуальных конфигов».  
2. Импортируйте её в ваш VPN-клиент (см. инструкции ниже).  
3. Выберите сервер с минимальным пингом и подключайтесь.

---

## ⚙️ Как это работает
- Скрипт [`source/main.py`](source/main.py) скачивает публичные подписки из различных источников.
- Workflow [`frequent_update.yml`](.github/workflows/frequent_update.yml) запускает скрипт по cron `*/9 * * * *`.
- Результаты сохраняются в каталог `githubmirror/` и сразу пушатся в этот репозиторий.

Каждый запуск создаёт коммит вида:
> 🚀 Обновление конфига по часовому поясу Европа/Москва: HH:MM | DD.MM.YYYY

---

## 🗂 Структура репозитория
```text
githubmirror/        — сгенерированные .txt конфиги (23 файла)
qr-codes/            — PNG-версии конфигов для импорта по QR
source/              — Python-скрипт и зависимости генератора
 ├─ main.py
 └─ requirements.txt
.github/workflows/   — CI/CD (авто-обновление каждые 9 мин)
README.md            — этот файл
```

---

## 🔧 Локальный запуск генератора
```bash
git clone https://github.com/AvenCores/goida-vpn-configs
cd goida-vpn-configs/source
python -m pip install -r requirements.txt
export MY_TOKEN=<GITHUB_TOKEN>   # токен с правом repo, чтобы пушить изменения
python main.py                  # конфиги появятся в ../githubmirror
```

> **Важно!** В файле `source/main.py` вручную задайте `REPO_NAME = "<username>/<repository>"`, если запускаете скрипт из форка.

---

# 🎦 Видео гайд по установке и решению проблем

![maxresdefault](https://github.com/user-attachments/assets/e36e2351-3b1a-4b90-87f7-cafbc74f238c)

<div align="center">

> ⚠️ **Внимание!** Для iOS и iPadOS актуален только текстовый гайд ниже. Видео гайд актуален только для Android, Android TV, Windows, Linux, MacOS.

[**Смотреть на YouTube**](https://youtu.be/sagz2YluM70)  

[**Смотреть на Dzen**](https://dzen.ru/video/watch/680d58f28c6d3504e953bd6d)  

[**Смотреть на VK Video**](https://vk.com/video-200297343_456239303)

[**Смотреть в Telegram**](https://t.me/avencoreschat/56595)

</div>

---

# 🗂️ Общее меню гайдов репозитория

<details>

<summary>👩‍💻 Исходный код для генерации вечно актуальных конфигов</summary>

Ссылка на исходный код - [Ссылка](https://github.com/AvenCores/goida-vpn-configs/tree/main/source)

</details>


---
<details>

<summary>📋 Общий список всех вечно актуальных конфигов</summary>

> Рекомендованные списки: [6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt), [22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt), [23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt), [24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt) и [25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt).

1) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt`
2) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/2.txt`
3) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/3.txt`
4) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/4.txt`
5) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/5.txt`
6) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt`
7) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/7.txt`
8) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/8.txt`
9) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/9.txt`
10) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/10.txt`
11) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/11.txt`
12) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/12.txt`
13) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/13.txt`
14) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/14.txt`
15) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/15.txt`
16) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/16.txt`
17) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/17.txt`
18) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/18.txt`
19) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/19.txt`
20) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/20.txt`
21) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/21.txt`
22) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt`
23) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt`
24) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt`
25) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt`

🔗 [Ссылка на QR-коды вечно актуальных конфигов](https://github.com/AvenCores/goida-vpn-configs/tree/main/qr-codes)
</details>


---
<details>

<summary>📱 Гайд для Android</summary>

**1.** Скачиваем **v2rayNG** - [Ссылка](https://github.com/2dust/v2rayNG/releases/download/1.10.11/v2rayNG_1.10.11_universal.apk)

**2.** Копируем в буфер обмена: 

 - [ ] **Вечно актуальные**

> Рекомендованные списки: [6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt), [22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt), [23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt), [24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt) и [25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt).

1) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt`
2) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/2.txt`
3) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/3.txt`
4) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/4.txt`
5) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/5.txt`
6) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt`
7) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/7.txt`
8) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/8.txt`
9) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/9.txt`
10) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/10.txt`
11) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/11.txt`
12) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/12.txt`
13) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/13.txt`
14) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/14.txt`
15) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/15.txt`
16) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/16.txt`
17) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/17.txt`
18) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/18.txt`
19) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/19.txt`
20) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/20.txt`
21) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/21.txt`
22) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt`
23) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt`
24) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt`
25) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt`

**3.** Заходим в приложение **v2rayNG** и в правом верхнем углу нажимаем на ➕, а затем выбираем **Импорт из буфера обмена**.
   
**4.** Нажимаем **справа сверху на три точки**, а затем **Проверка профилей группы**, после окончания проверки в этом же меню нажмите на **Сортировка по результатам теста**. 

**5.** Выбираем нужный вам сервер и затем нажимаем на кнопку ▶️ в правом нижнем углу.

</details>

<details>

<summary>📺 Гайд для Android TV</summary>

**1.** Скачиваем **v2rayNG** - [Ссылка](https://github.com/2dust/v2rayNG/releases/download/1.10.11/v2rayNG_1.10.11_universal.apk)

> Рекомендованные **QR-коды**: [6](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/6.png), [22](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/22.png), [23](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/23.png), [24](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/24.png) и [25](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/25.png).

**2.** Скачиваем **QR-коды** вечно актуальных конфигов - [Ссылка](https://github.com/AvenCores/goida-vpn-configs/tree/main/qr-codes)

**3**. Заходим в приложение **v2rayNG** и в правом верхнем углу нажимаем на ➕, а затем выбираем **Импорт из QR-кода**, выбираем картинку нажав на иконку фото в правом верхнем углу.

**4.** Нажимаем **справа сверху на три точки**, а затем **Проверка профилей группы**, после окончания проверки в этом же меню нажмите на **Сортировка по результатам теста**. 

**5.** Выбираем нужный вам сервер и затем нажимаем на кнопку ▶️ в правом нижнем углу.

</details>

<details>

<summary>⚠ Если нету интернета при подключении к VPN в v2rayNG</summary>

Ссылка на видео с демонстрацией фикса - [Ссылка](https://t.me/avencoreschat/25254)

</details>

<details>

<summary>⚠ Если не появились конфиги при добавлении VPN в v2rayNG</summary>

**1.** Нажмите на **три полоски** в **левом верхнем углу**.

**2.** Нажимаем на кнопку **Группы**.

**3.** Нажимаем на **иконку кружка со стрелкой** в **верхнем правом углу** и дожидаемся окончания обновления.

</details>

<details>

<summary>⚠ Фикс ошибки "Cбой проверки интернет-соединения: net/http: 12X handshake timeout"</summary>

**1.** На рабочем столе зажимаем на иконке **v2rayNG** и нажимаем на пункт **О приложении**.

**2.** Нажимаем на кнопку **Остановить** и заново запускаем **v2rayNG**.

</details>

<details>

<summary>⚠ Фикс ошибки "Fail to detect internet connection: io: read/write closed pipe"</summary>

**1.** На рабочем столе зажимаем на иконке **v2rayNG** и нажимаем на пункт **О приложении**.

**2.** Нажимаем на кнопку **Остановить** и заново запускаем **v2rayNG**.

**3.** Нажимаем **справа сверху на три точки**, а затем **Проверка профилей группы**, после окончания проверки в этом же меню нажмите на **Сортировка по результатам теста**. 

**4.** Выбираем нужный вам сервер и затем нажимаем на кнопку ▶️ в правом нижнем углу.

</details>

<details>

<summary>🔄 Обновление конфигов в v2rayNG</summary>

**1.** Нажимаем на **иконку трех полосок** в **левом верхнем углу**.

**2.** Выбираем вкладку **Группы**.

**3.** Нажимаем на **иконку кружка со стрелкой** в **правом верхнем углу**.

</details>


---
<details>

<summary>🖥 Гайд для Windows, Linux</summary>

**1.** Скачиваем **Throne** - [Windows 10/11](https://github.com/throneproj/Throne/releases/download/1.0.0/Throne-1.0.0-windows64.zip) / [Windows 7](https://github.com/throneproj/Throne/releases/download/1.0.0/Throne-1.0.0-windowslegacy64.zip) / [Linux](https://github.com/throneproj/Throne/releases/download/1.0.0/Throne-1.0.0-linux-amd64.zip)

**2.** Копируем в буфер обмена: 

 - [ ] **Вечно актуальные**

> Рекомендованные списки: [6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt), [22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt), [23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt), [24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt) и [25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt).

1) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt`
2) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/2.txt`
3) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/3.txt`
4) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/4.txt`
5) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/5.txt`
6) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt`
7) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/7.txt`
8) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/8.txt`
9) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/9.txt`
10) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/10.txt`
11) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/11.txt`
12) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/12.txt`
13) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/13.txt`
14) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/14.txt`
15) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/15.txt`
16) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/16.txt`
17) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/17.txt`
18) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/18.txt`
19) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/19.txt`
20) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/20.txt`
21) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/21.txt`
22) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt`
23) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt`
24) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt`
25) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt`

**3.** Нажимаем на **Профили**, а затем **Добавить профиль из буфера обмена**.

**4.** Выделяем все конфиги комбинацией клавиш **Ctrl + A**, нажимаем **Профили** в верхнем меню, а затем **Тест задержки (пинга) выбранного профиля** и дожидаемся окончания теста (во вкладке **Логи** появится надпись **Тест задержек (пинга) завершён!**)

**5.** Наживаем на кнопку колонки **Задержка (пинг)**.

**6.** В верхней части окна программы активируйте опцию **Режим TUN**, установив галочку.

**7.** Выбираем один из конфигов с наименьшим **Задержка (пинг)**, а затем нажимаем **ЛКМ** и **Запустить**.

</details>

<details>

<summary>⚠ Исправляем ошибку MSVCP и VCRUNTIME на Windows 10/11</summary>

**1.** Нажимаем **Win+R** и пишем **control**.

**2.** Выбираем **Программы и компоненты**.

**3.** В поиск (справа сверху) пишем слово **Visual** и удалям все что касается **Microsoft Visual**.

**4.** Скачиваем архив и распаковываем - [Ссылка](https://cf.comss.org/download/Visual-C-Runtimes-All-in-One-Jul-2025.zip)

**5.** Запускаем от *имени Администратора* **install_bat.all** и ждем пока все установиться.

</details>

<details>

<summary>🔄 Обновление конфигов в NekoRay</summary>

**1.** Нажимаем на кнопку **Настройки**.

**2.** Выбираем **Группы**.

**3.** Нажимаем на кнопку **Обновить все подписки**.

</details>


---
<details>

<summary>☎ Гайд для iOS, iPadOS</summary>

**1.** Скачиваем **V2Box - V2ray Client** - [Ссылка](https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690)

**2.** Копируем в буфер обмена:

 - [ ] **Вечно актуальные**

> Рекомендованные списки: [6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt), [22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt), [23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt), [24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt) и [25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt).

1) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt`
2) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/2.txt`
3) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/3.txt`
4) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/4.txt`
5) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/5.txt`
6) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt`
7) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/7.txt`
8) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/8.txt`
9) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/9.txt`
10) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/10.txt`
11) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/11.txt`
12) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/12.txt`
13) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/13.txt`
14) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/14.txt`
15) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/15.txt`
16) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/16.txt`
17) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/17.txt`
18) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/18.txt`
19) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/19.txt`
20) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/20.txt`
21) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/21.txt`
22) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt`
23) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt`
24) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt`
25) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt`

**3.** Заходим в приложение **V2Box - V2ray Client** и переходим во вкладку **Config**, нажимаем на плюсик в правом верхнем углу, затем - **Добавить подписку**, вводим любое **Название** и вставляем ссылку на конфиг в поле **URL**.

**4.** После добавления конфига дожидаемся окончания проверки и выбираем нужный, просто нажав на его название.

**5.** В нижней панели программы нажимаем кнопку **Подключиться**.

</details>

<details>

<summary>🔄 Обновление конфигов в V2Box - V2ray Client</summary>

**1.** Переходим во вкладку **Config**.

**2.** Нажимаем на иконку обновления слева от названия группы подписки.

</details>


---
<details>

<summary>💻 Гайд для MacOS</summary>

**1.** Скачиваем **Hiddify** - [Ссылка](https://github.com/hiddify/hiddify-app/releases/latest/download/Hiddify-MacOS.dmg)

**2.** Нажимаем **Новый профиль**.

**3.** Копируем в буфер обмена:

 - [ ] **Вечно актуальные**

> Рекомендованные списки: [6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt), [22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt), [23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt), [24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt) и [25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt).

1) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt`
2) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/2.txt`
3) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/3.txt`
4) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/4.txt`
5) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/5.txt`
6) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt`
7) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/7.txt`
8) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/8.txt`
9) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/9.txt`
10) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/10.txt`
11) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/11.txt`
12) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/12.txt`
13) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/13.txt`
14) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/14.txt`
15) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/15.txt`
16) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/16.txt`
17) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/17.txt`
18) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/18.txt`
19) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/19.txt`
20) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/20.txt`
21) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/21.txt`
22) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt`
23) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt`
24) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt`
25) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt`

**4.** Нажимаем на кнопку **Добавить из буфера обмена**.
   
**5.** Перейдите в **Настройки**, измените **Вариант маршрутизации** на **Индонезия**.

**6.** Нажмите в левом верхнем меню на иконку настроек и выберите **VPN сервис**.

**7.** Включаем **VPN** нажав на иконку по середине. 

**8.** Для смены сервера включите **VPN** и перейдите во вкладку **Прокси**.

</details>

<details>

<summary>🔄 Обновление конфигов в Hiddify</summary>

**1.** Заходим в приложение **Hiddify** и выбираем нужный вам профиль.

**2.** Нажимаем **слева от названия профиля на иконку обновления**.

</details>

---

# 📜 Лицензия

Проект распространяется под лицензией GPL-3.0. Полный текст лицензии содержится в файле [`LICENSE`](LICENSE).

---
# 💰 Поддержать автора
+ **SBER**: `2202 2050 7215 4401`
