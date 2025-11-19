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

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/AvenCores/goida-vpn-configs)
[![GPL-3.0 License](https://img.shields.io/badge/License-GPL--3.0-blue?style=for-the-badge)](./LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/AvenCores/goida-vpn-configs?style=for-the-badge)](https://github.com/AvenCores/goida-vpn-configs/stargazers)
![GitHub forks](https://img.shields.io/github/forks/AvenCores/goida-vpn-configs?style=for-the-badge)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/AvenCores/goida-vpn-configs?style=for-the-badge)](https://github.com/AvenCores/goida-vpn-configs/pulls)
[![GitHub issues](https://img.shields.io/github/issues/AvenCores/goida-vpn-configs?style=for-the-badge)](https://github.com/AvenCores/goida-vpn-configs/issues)

Автоматически обновляемая коллекция публичных VPN-конфигов (`V2Ray` / `VLESS` / `Trojan` / `VMess` / `Reality` / `Shadowsocks`) для быстрого обхода блокировок.
  
Каждый конфиг — это TXT-подписка, которую можно импортировать практически в любой современный клиент (`v2rayNG`, `NekoRay`, `Throne`, `v2rayN`, `V2Box`, `v2RayTun`, `Hiddify` и др.).

Конфиги обновляются каждые **9 минут** с помощью GitHub Actions, поэтому ссылки из раздела **«📋 Общий список всех вечно актуальных конфигов»** всегда актуальны.

## 📑 Содержание
- [📖 Описание проекта](#-описание-проекта)
  - [📑 Содержание](#-содержание)
  - [🚀 Быстрый старт](#-быстрый-старт)
  - [📊 Статус конфигов](#-статус-конфигов)
  - [⚙️ Как это работает](#️-как-это-работает)
  - [🗂 Структура репозитория](#-структура-репозитория)
  - [🔧 Локальный запуск генератора](#-локальный-запуск-генератора)
- [🎦 Видео гайд по установке и решению проблем](#-видео-гайд-по-установке-и-решению-проблем)
- [🗂️ Общее меню гайдов репозитория](#️-общее-меню-гайдов-репозитория)
- [📜 Лицензия](#-лицензия)
- [💰 Поддержать автора](#-поддержать-автора)

---

## 🚀 Быстрый старт
1. Скопируйте нужную ссылку из раздела **«📋 Общий список всех вечно актуальных конфигов»**.  
2. Импортируйте её в ваш **VPN-клиент** (см. инструкции ниже).  
3. Выберите сервер с минимальным пингом и подключайтесь.

---

## 📊 Статус конфигов

> **⚠️ Внимание!** Эта таблица показывает только **источники** и статус обновления конфигов. **Не копируйте ссылки отсюда!**  
> Для использования копируйте ссылки из раздела **«📋 Общий список всех вечно актуальных конфигов»** ниже.

| № | Файл | Источник | Время | Дата |
|--|--|--|--|--|
| 1 | [`1.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt) | [sakha1370/OpenRay](https://github.com/sakha1370/OpenRay/raw/refs/heads/main/output/all_valid_proxies.txt) | 09:47 | 19.11.2025 |
| 2 | [`2.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/2.txt) | [sevcator/5ubscrpt10n](https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt) | 10:17 | 19.11.2025 |
| 3 | [`3.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/3.txt) | [yitong2333/proxy-minging](https://raw.githubusercontent.com/yitong2333/proxy-minging/refs/heads/main/v2ray.txt) | 10:17 | 19.11.2025 |
| 4 | [`4.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/4.txt) | [acymz/AutoVPN](https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt) | 09:47 | 19.11.2025 |
| 5 | [`5.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/5.txt) | [miladtahanian/V2RayCFGDumper](https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/config.txt) | 10:17 | 19.11.2025 |
| 6 | [`6.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt) | [roosterkid/openproxylist](https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt) | 10:17 | 19.11.2025 |
| 7 | [`7.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/7.txt) | [Epodonios/v2ray-configs](https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt) | 08:56 | 19.11.2025 |
| 8 | [`8.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/8.txt) | [YasserDivaR/pr0xy](https://raw.githubusercontent.com/YasserDivaR/pr0xy/refs/heads/main/ShadowSocks2021.txt) | 18:26 | 12.11.2025 |
| 9 | [`9.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/9.txt) | [mohamadfg-dev/telegram-v2ray-configs-collector](https://raw.githubusercontent.com/mohamadfg-dev/telegram-v2ray-configs-collector/refs/heads/main/category/vless.txt) | 10:17 | 19.11.2025 |
| 10 | [`10.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/10.txt) | [mheidari98/.proxy](https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/vless) | 10:17 | 19.11.2025 |
| 11 | [`11.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/11.txt) | [youfoundamin/V2rayCollector](https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt) | 08:20 | 19.11.2025 |
| 12 | [`12.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/12.txt) | [mheidari98/.proxy](https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/all) | 10:17 | 19.11.2025 |
| 13 | [`13.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/13.txt) | [Kwinshadow/TelegramV2rayCollector](https://github.com/Kwinshadow/TelegramV2rayCollector/raw/refs/heads/main/sublinks/mix.txt) | 21:46 | 11.11.2025 |
| 14 | [`14.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/14.txt) | [LalatinaHub/Mineral](https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes) | 10:17 | 19.11.2025 |
| 15 | [`15.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/15.txt) | [miladtahanian/multi-proxy-config-fetcher](https://raw.githubusercontent.com/miladtahanian/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt) | 05:46 | 19.11.2025 |
| 16 | [`16.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/16.txt) | [Pawdroid/Free-servers](https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub) | 10:17 | 19.11.2025 |
| 17 | [`17.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/17.txt) | [MhdiTaheri/V2rayCollector_Py](https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt) | 09:47 | 19.11.2025 |
| 18 | [`18.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/18.txt) | [Epodonios/v2ray-configs](https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt) | 10:17 | 19.11.2025 |
| 19 | [`19.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/19.txt) | [MhdiTaheri/V2rayCollector](https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix) | 10:17 | 19.11.2025 |
| 20 | [`20.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/20.txt) | [Argh94/Proxy-List](https://github.com/Argh94/Proxy-List/raw/refs/heads/main/All_Config.txt) | 09:20 | 19.11.2025 |
| 21 | [`21.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/21.txt) | [shabane/kamaji](https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt) | 10:17 | 19.11.2025 |
| 22 | [`22.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt) | [wuqb2i4f/xray-config-toolkit](https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri) | 07:42 | 19.11.2025 |
| 23 | [`23.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt) | [AzadNetCH/Clash](https://raw.githubusercontent.com/AzadNetCH/Clash/refs/heads/main/AzadNet.txt) | 08:45 | 22.10.2025 |
| 24 | [`24.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt) | [STR97/STRUGOV](https://raw.githubusercontent.com/STR97/STRUGOV/refs/heads/main/STR.BYPASS#STR.BYPASS%F0%9F%91%BE) | 17:40 | 18.11.2025 |
| 25 | [`25.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt) | [V2RayRoot/V2RayConfig](https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/refs/heads/main/Config/vless.txt) | 09:58 | 19.11.2025 |
| 26 | [`26.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt) | [Обход SNI белых списков](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt) | 09:47 | 19.11.2025 |

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

Ссылка на исходный код — [Ссылка](https://github.com/AvenCores/goida-vpn-configs/tree/main/source)

</details>


---
<details>

<summary>📋 Общий список всех вечно актуальных конфигов</summary>

> Рекомендованные списки: **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)**.

 - [ ] **Вечно актуальные**

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
26) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt`

🔗 [Ссылка на QR-коды вечно актуальных конфигов](https://github.com/AvenCores/goida-vpn-configs/tree/main/qr-codes)
</details>


---
<details>

<summary>📱 Гайд для Android</summary>

**1.** Скачиваем **«v2rayNG»** — [Ссылка](https://github.com/2dust/v2rayNG/releases/download/1.10.26/v2rayNG_1.10.26_universal.apk)

**2.** Копируем в буфер обмена: 

> Рекомендованные списки: **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)**.

 - [ ] **Вечно актуальные**

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
26) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt`

**3.** Заходим в приложение **«v2rayNG»** и в правом верхнем углу нажимаем на ➕, а затем выбираем **«Импорт из буфера обмена»**.
   
**4.** Нажимаем **«справа сверху на три точки»**, а затем **«Проверка профилей группы»**, после окончания проверки в этом же меню нажмите на **«Сортировка по результатам теста»**. 

**5.** Выбираем нужный вам сервер и затем нажимаем на кнопку ▶️ в правом нижнем углу.

</details>

<details>

<summary>📺 Гайд для Android TV</summary>

**1.** Скачиваем **«v2rayNG»** — [Ссылка](https://github.com/2dust/v2rayNG/releases/download/1.10.26/v2rayNG_1.10.26_universal.apk)

> Рекомендованные **«QR-коды»**: **[6](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/6.png)**, **[22](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/22.png)**, **[23](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/23.png)**, **[24](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/24.png)** и **[25](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/25.png)**.

> Обход SNI белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/26.png)**.

**2.** Скачиваем **«QR-коды»** вечно актуальных конфигов — [Ссылка](https://github.com/AvenCores/goida-vpn-configs/tree/main/qr-codes)

**3**. Заходим в приложение **«v2rayNG»** и в правом верхнем углу нажимаем на ➕, а затем выбираем **«Импорт из QR-кода»**, выбираем картинку нажав на иконку фото в правом верхнем углу.

**4.** Нажимаем **«справа сверху на три точки»**, а затем **«Проверка профилей группы»**, после окончания проверки в этом же меню нажмите на **«Сортировка по результатам теста»**. 

**5.** Выбираем нужный вам сервер и затем нажимаем на кнопку ▶️ в правом нижнем углу.

</details>

<details>

<summary>⚠ Если нету интернета при подключении к VPN в v2rayNG</summary>

Ссылка на видео с демонстрацией фикса — [Ссылка](https://t.me/avencoreschat/25254)

</details>

<details>

<summary>⚠ Если не появились конфиги при добавлении VPN в v2rayNG</summary>

**1.** Нажмите на **«три полоски»** в **«левом верхнем углу»**.

**2.** Нажимаем на кнопку **«Группы»**.

**3.** Нажимаем на **«иконку кружка со стрелкой»** в **«верхнем правом углу»** и дожидаемся окончания обновления.

</details>

<details>

<summary>⚠ Фикс ошибки "Cбой проверки интернет-соединения: net/http: 12X handshake timeout"</summary>

**1.** На рабочем столе зажимаем на иконке **«v2rayNG»** и нажимаем на пункт **«О приложении»**.

**2.** Нажимаем на кнопку **«Остановить»** и заново запускаем **«v2rayNG»**.

</details>

<details>

<summary>⚠ Фикс ошибки "Fail to detect internet connection: io: read/write closed pipe"</summary>

**1.** На рабочем столе зажимаем на иконке **«v2rayNG»** и нажимаем на пункт **«О приложении»**.

**2.** Нажимаем на кнопку **«Остановить»** и заново запускаем **«v2rayNG»**.

**3.** Нажимаем **«справа сверху на три точки»**, а затем **«Проверка профилей группы»**, после окончания проверки в этом же меню нажмите на **«Сортировка по результатам теста»**. 

**4.** Выбираем нужный вам сервер и затем нажимаем на кнопку ▶️ в правом нижнем углу.

</details>

<details>

<summary>🔄 Обновление конфигов в v2rayNG</summary>

**1.** Нажимаем на **«иконку трех полосок»** в **«левом верхнем углу»**.

**2.** Выбираем вкладку **«Группы»**.

**3.** Нажимаем на **«иконку кружка со стрелкой»** в **«правом верхнем углу»**.

</details>


---
<details>

<summary>🖥 Гайд для Windows, Linux</summary>

**1.** Скачиваем **«Throne»** — [Windows 10/11](https://github.com/throneproj/Throne/releases/download/1.0.8/Throne-1.0.8-windows64.zip) / [Windows 7/8/8.1](https://github.com/throneproj/Throne/releases/download/1.0.8/Throne-1.0.8-windowslegacy64.zip) / [Linux](https://github.com/throneproj/Throne/releases/download/1.0.8/Throne-1.0.8-linux-amd64.zip)

**2.** Копируем в буфер обмена: 

> Рекомендованные списки: **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)**.

 - [ ] **Вечно актуальные**

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
26) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt`

**3.** Нажимаем на **«Профили»**, а затем **«Добавить профиль из буфера обмена»**.

**4.** Выделяем все конфиги комбинацией клавиш **«Ctrl + A»**, нажимаем **«Профили»** в верхнем меню, а затем **«Тест задержки (пинга) выбранного профиля»** и дожидаемся окончания теста (во вкладке **«Логи»** появится надпись **«Тест задержек (пинга) завершён!»**)

**5.** Наживаем на кнопку колонки **«Задержка (пинг)»**.

**6.** В верхней части окна программы активируйте опцию **«Режим TUN»**, установив галочку.

**7.** Выбираем один из конфигов с наименьшим **«Задержка (пинг)»**, а затем нажимаем **«ЛКМ»** и **«Запустить»**.

</details>

<details>

<summary>⚠ Исправляем ошибку MSVCP и VCRUNTIME на Windows 10/11</summary>

**1.** Нажимаем **«Win+R»** и пишем **«control»**.

**2.** Выбираем **«Программы и компоненты»**.

**3.** В поиск (справа сверху) пишем слово **«Visual»** и удалям все что касается **«Microsoft Visual»**.

**4.** Скачиваем архив и распаковываем — [Ссылка](https://cf.comss.org/download/Visual-C-Runtimes-All-in-One-Jul-2025.zip)

**5.** Запускаем от *имени Администратора* **«install_bat.all»** и ждем пока все установиться.

</details>

<details>

<summary>🔄 Обновление конфигов в NekoRay</summary>

**1.** Нажимаем на кнопку **«Настройки»**.

**2.** Выбираем **«Группы»**.

**3.** Нажимаем на кнопку **«Обновить все подписки»**.

</details>


---
<details>

<summary>☎ Гайд для iOS, iPadOS</summary>

**1.** Скачиваем **«V2Box - V2ray Client»** — [Ссылка](https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690)

**2.** Копируем в буфер обмена:

> Рекомендованные списки: **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)**.

 - [ ] **Вечно актуальные**

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
26) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt`

**3.** Заходим в приложение **«V2Box - V2ray Client»** и переходим во вкладку **«Config»**, нажимаем на плюсик в правом верхнем углу, затем — **«Добавить подписку»**, вводим любое **«Название»** и вставляем ссылку на конфиг в поле **«URL»**.

**4.** После добавления конфига дожидаемся окончания проверки и выбираем нужный, просто нажав на его название.

**5.** В нижней панели программы нажимаем кнопку **«Подключиться»**.

</details>

<details>

<summary>🔄 Обновление конфигов в V2Box - V2ray Client</summary>

**1.** Переходим во вкладку **«Config»**.

**2.** Нажимаем на иконку обновления слева от названия группы подписки.

</details>


---
<details>

<summary>💻 Гайд для MacOS</summary>

**1.** Скачиваем **«Hiddify»** — [Ссылка](https://github.com/hiddify/hiddify-app/releases/latest/download/Hiddify-MacOS.dmg)

**2.** Нажимаем **«Новый профиль»**.

**3.** Копируем в буфер обмена:

> Рекомендованные списки: **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)**.

 - [ ] **Вечно актуальные**

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
26) `https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt`

**4.** Нажимаем на кнопку **«Добавить из буфера обмена»**.
   
**5.** Перейдите в **«Настройки»**, измените **«Вариант маршрутизации»** на **«Индонезия»**.

**6.** Нажмите в левом верхнем меню на иконку настроек и выберите **«VPN сервис»**.

**7.** Включаем **«VPN»** нажав на иконку по середине. 

**8.** Для смены сервера включите **«VPN»** и перейдите во вкладку **«Прокси»**.

</details>

<details>

<summary>🔄 Обновление конфигов в Hiddify</summary>

**1.** Заходим в приложение **«Hiddify»** и выбираем нужный вам профиль.

**2.** Нажимаем **«слева от названия профиля на иконку обновления»**.

</details>

---

# 📜 Лицензия

Проект распространяется под лицензией GPL-3.0. Полный текст лицензии содержится в файле [`LICENSE`](LICENSE).

---
# 💰 Поддержать автора
+ **SBER**: `2202 2050 7215 4401`
