<div align="center">
    <a href="https://www.youtube.com/@avencores/" target="_blank">
      <img src="https://github.com/user-attachments/assets/338bcd74-e3c3-4700-87ab-7985058bd17e" alt="YouTube" height="40">
    </a>
    <a href="https://t.me/avencoresyt" target="_blank">
      <img src="https://github.com/user-attachments/assets/939f8beb-a49a-48cf-89b9-d610ee5c4b26" alt="Telegram" height="40">
    </a>
    <a href="https://vk.ru/avencoresreuploads" target="_blank">
      <img src="https://github.com/user-attachments/assets/dc109dda-9045-4a06-95a5-3399f0e21dc4" alt="VK" height="40">
    </a>
    <a href="https://dzen.ru/avencores" target="_blank">
      <img src="https://github.com/user-attachments/assets/bd55f5cf-963c-4eb8-9029-7b80c8c11411" alt="Dzen" height="40">
    </a>
</div>

# 📖 Описание проекта

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/AvenCores/goida-vpn-configs)
[![GPL-3.0 License](https://img.shields.io/badge/License-GPL--3.0-blue?style=for-the-badge)](./LICENSE)
[![Website](https://img.shields.io/badge/Website-Goida%20VPN-207e5c?style=for-the-badge&logo=firefox)](https://avencores.github.io/goida-vpn-site/)
[![GitHub stars](https://img.shields.io/github/stars/AvenCores/goida-vpn-configs?style=for-the-badge)](https://github.com/AvenCores/goida-vpn-configs/stargazers)
![GitHub forks](https://img.shields.io/github/forks/AvenCores/goida-vpn-configs?style=for-the-badge)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/AvenCores/goida-vpn-configs?style=for-the-badge)](https://github.com/AvenCores/goida-vpn-configs/pulls)
[![GitHub issues](https://img.shields.io/github/issues/AvenCores/goida-vpn-configs?style=for-the-badge)](https://github.com/AvenCores/goida-vpn-configs/issues)

Автоматически обновляемая коллекция публичных VPN-конфигов (`V2Ray` / `VLESS` / `Hysteria` / `Trojan` / `VMess` / `Reality` / `Shadowsocks`) для быстрого обхода блокировок.
  
Каждый конфиг — это TXT-подписка, которую можно импортировать практически в любой современный клиент (`v2rayNG`, `NekoRay`, `Throne`, `v2rayN`, `V2Box`, `v2RayTun`, `Hiddify` и др.).

Конфиги обновляются каждые **9 минут** с помощью GitHub Actions, поэтому ссылки из раздела **«📋 Общий список всех вечно актуальных конфигов»** всегда актуальны.

<a href="https://avencores.github.io/goida-vpn-site/">
  <img alt="1" src="https://github.com/user-attachments/assets/80f69696-5eb5-44fa-94bf-1fe50303f683" />
</a>

## 📑 Содержание
- [📖 Описание проекта](#-описание-проекта)
  - [📑 Содержание](#-содержание)
  - [🚀 Быстрый старт](#-быстрый-старт)
  - [📊 Статус конфигов](#-статус-конфигов)
  - [📊 Статистика репозитория](#-статистика-репозитория)
  - [⚙️ Как это работает](#️-как-это-работает)
  - [🗂 Структура репозитория](#-структура-репозитория)
  - [🔧 Локальный запуск генератора](#-локальный-запуск-генератора)
- [🎦 Видео гайд по установке и решению проблем](#-видео-гайд-по-установке-и-решению-проблем)
- [🔓 Видео гайд по обходу SNI/CIDR белых списков](#-видео-гайд-по-обходу-snicidr-белых-списков)
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
| 1 | [`1.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt) | [sakha1370/OpenRay](https://github.com/sakha1370/OpenRay/raw/refs/heads/main/output/all_valid_proxies.txt) | 01:37 (МСК) | 05.07.2026 |
| 2 | [`2.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/2.txt) | [sevcator/5ubscrpt10n](https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt) | 01:37 (МСК) | 05.07.2026 |
| 3 | [`3.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/3.txt) | [yitong2333/proxy-minging](https://raw.githubusercontent.com/yitong2333/proxy-minging/refs/heads/main/v2ray.txt) | 01:37 (МСК) | 05.07.2026 |
| 4 | [`4.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/4.txt) | [acymz/AutoVPN](https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt) | 00:37 (МСК) | 05.07.2026 |
| 5 | [`5.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/5.txt) | [miladtahanian/V2RayCFGDumper](https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/sub.txt) | 01:37 (МСК) | 05.07.2026 |
| 6 | [`6.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt) | [roosterkid/openproxylist](https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt) | 01:37 (МСК) | 05.07.2026 |
| 7 | [`7.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/7.txt) | [Epodonios/v2ray-configs](https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt) | 22:47 (МСК) | 04.07.2026 |
| 8 | [`8.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/8.txt) | [ShatakVPN/ConfigForge-V2Ray](https://github.com/ShatakVPN/ConfigForge-V2Ray/raw/refs/heads/main/configs/vless.txt) | 01:37 (МСК) | 05.07.2026 |
| 9 | [`9.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/9.txt) | [mohamadfg-dev/telegram-v2ray-configs-collector](https://raw.githubusercontent.com/mohamadfg-dev/telegram-v2ray-configs-collector/refs/heads/main/category/vless.txt) | 23:38 (МСК) | 04.07.2026 |
| 10 | [`10.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/10.txt) | [mheidari98/.proxy](https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/vless) | 01:37 (МСК) | 05.07.2026 |
| 11 | [`11.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/11.txt) | [youfoundamin/V2rayCollector](https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt) | 00:37 (МСК) | 05.07.2026 |
| 12 | [`12.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/12.txt) | [VOID-Anonymity/V.O.I.D-VPN_Bypass](https://github.com/VOID-Anonymity/V.O.I.D-VPN_Bypass/raw/refs/heads/main/url_work.txt) | 01:37 (МСК) | 05.07.2026 |
| 13 | [`13.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/13.txt) | [MahsaNetConfigTopic/config](https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt) | 12:39 (МСК) | 04.07.2026 |
| 14 | [`14.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/14.txt) | [LalatinaHub/Mineral](https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes) | 01:37 (МСК) | 05.07.2026 |
| 15 | [`15.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/15.txt) | [miladtahanian/Config-Collector](https://raw.githubusercontent.com/miladtahanian/Config-Collector/refs/heads/main/mixed_iran.txt) | 01:37 (МСК) | 05.07.2026 |
| 16 | [`16.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/16.txt) | [Pawdroid/Free-servers](https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub) | 01:37 (МСК) | 05.07.2026 |
| 17 | [`17.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/17.txt) | [MhdiTaheri/V2rayCollector_Py](https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt) | 01:37 (МСК) | 05.07.2026 |
| 18 | [`18.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/18.txt) | [free18/v2ray](https://raw.githubusercontent.com/free18/v2ray/refs/heads/main/v.txt) | 10:32 (МСК) | 04.07.2026 |
| 19 | [`19.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/19.txt) | [MhdiTaheri/V2rayCollector](https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix) | 01:37 (МСК) | 05.07.2026 |
| 20 | [`20.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/20.txt) | [Argh94/Proxy-List](https://github.com/Argh94/Proxy-List/raw/refs/heads/main/All_Config.txt) | 19:16 (МСК) | 04.07.2026 |
| 21 | [`21.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/21.txt) | [shabane/kamaji](https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt) | 09:24 (МСК) | 29.06.2026 |
| 22 | [`22.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt) | [wuqb2i4f/xray-config-toolkit](https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri) | 23:38 (МСК) | 04.07.2026 |
| 23 | [`23.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt) | [igareck/vpn-configs-for-russia](https://github.com/igareck/vpn-configs-for-russia/raw/refs/heads/main/BLACK_VLESS_RUS.txt) | 01:37 (МСК) | 05.07.2026 |
| 24 | [`24.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt) | [Mr-Meshky/vify](https://github.com/Mr-Meshky/vify/raw/refs/heads/main/configs/vless.txt) | 01:37 (МСК) | 05.07.2026 |
| 25 | [`25.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt) | [V2RayRoot/V2RayConfig](https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/refs/heads/main/Config/vless.txt) | 01:37 (МСК) | 05.07.2026 |
| 26 | [`26.txt`](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt) | [Обход SNI/CIDR белых списков](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt) | 01:37 (МСК) | 05.07.2026 |

## 📊 Статистика репозитория
| Показатель | Значение |
|--|--|
| Просмотры (14Д) | 65,911 |
| Клоны (14Д) | 7,989 |
| Уникальные клоны (14Д) | 1,303 |
| Уникальные посетители (14Д) | 25,124 |

## 🗂 Структура репозитория
```text
.github/workflows/   — CI/CD (авто-обновление каждые 9 мин)
githubmirror/        — сгенерированные .txt конфиги (26 файлов)
qr-codes/            — PNG-версии конфигов для импорта по QR (26 файлов)
source/              — исходный код и конфигурации генератора
 ├─ main.py          — основной скрипт генерации
 ├─ requirements.txt — зависимости Python
 ├─ urls.json        — список источников для конфигов 1-25
 ├─ 26_urls.json     — источники для конфига №26 (обход SNI)
 └─ sni_domains.json — список доменов для подмены SNI
LICENSE              — лицензия GPL-3.0
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

[**Смотреть на VK Video**](https://vk.com/video-200297343_456239303)

[**Смотреть в Telegram**](https://t.me/avencoreschat/56595)

</div>

---

# 🔓 Видео гайд по обходу SNI/CIDR белых списков

![maxresdefault](https://github.com/user-attachments/assets/63397f2f-4aca-44c3-bd2e-ed9d629388c6)

<div align="center">

[**Смотреть на YouTube**](https://youtu.be/uz6JmOO7sGU)

[**Смотреть на VK Video**](https://vk.ru/video-234234162_456239052)

[**Смотреть в Telegram**](https://t.me/avencoreschat/346024)

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

> Рекомендованные списки: **[1](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt)**, **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI/CIDR белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)** | **[Видео гайд по установке](https://youtu.be/uz6JmOO7sGU)**.

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

**1.** Скачиваем **«v2rayNG»** — [Ссылка](https://github.com/2dust/v2rayNG/releases/download/2.2.5/v2rayNG_2.2.5_universal.apk)

**2.** Копируем в буфер обмена: 

> Рекомендованные списки: **[1](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt)**, **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI/CIDR белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)** | **[Видео гайд по установке](https://youtu.be/uz6JmOO7sGU)**.

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
   
**4.** Нажимаем **«справа сверху на три точки»**, а затем **«Проверить задержку профилей»**, после окончания проверки в этом же меню нажмите на **«Сортировать по результатам теста»**. 

**5.** Выбираем нужный вам сервер и затем нажимаем на кнопку ▶️ в правом нижнем углу.

</details>

<details>

<summary>📺 Гайд для Android TV</summary>

**1.** Скачиваем **«v2rayNG»** — [Ссылка](https://github.com/2dust/v2rayNG/releases/download/2.2.5/v2rayNG_2.2.5_universal.apk)

> Рекомендованные **«QR-коды»**: **[1](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/1.png)**, **[6](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/6.png)**, **[22](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/22.png)**, **[23](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/23.png)**, **[24](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/24.png)** и **[25](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/25.png)**.

> Обход SNI/CIDR белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/blob/main/qr-codes/26.png)** | **[Видео гайд по установке](https://youtu.be/uz6JmOO7sGU)**.

**2.** Скачиваем **«QR-коды»** вечно актуальных конфигов — [Ссылка](https://github.com/AvenCores/goida-vpn-configs/tree/main/qr-codes)

**3**. Заходим в приложение **«v2rayNG»** и в правом верхнем углу нажимаем на ➕, а затем выбираем **«Импорт из QR-кода»**, выбираем картинку нажав на иконку фото в правом верхнем углу.

**4.** Нажимаем **«справа сверху на три точки»**, а затем **«Проверить задержку профилей»**, после окончания проверки в этом же меню нажмите на **«Сортировать по результатам теста»**. 

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

**3.** Нажимаем **«справа сверху на три точки»**, а затем **«Проверить задержку профилей»**, после окончания проверки в этом же меню нажмите на **«Сортировать по результатам теста»**. 

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

**1.** Скачиваем **«Throne»** — [Windows 10/11](https://github.com/throneproj/Throne/releases/download/1.1.6/Throne-1.1.6-windows64.zip) / [Windows 7/8/8.1](https://github.com/throneproj/Throne/releases/download/1.1.6/Throne-1.1.6-windowslegacy64.zip) / [Linux](https://github.com/throneproj/Throne/releases/download/1.1.6/Throne-1.1.6-linux-amd64.zip)

**2.** Копируем в буфер обмена: 

> Рекомендованные списки: **[1](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt)**, **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI/CIDR белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)** | **[Видео гайд по установке](https://youtu.be/uz6JmOO7sGU)**.

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

**5.** Нажимаем на кнопку колонки **«Задержка (пинг)»**.

**6.** В верхней части окна программы активируйте опцию **«Режим TUN»**, установив галочку.

**7.** Выбираем один из конфигов с наименьшим **«Задержка (пинг)»**, а затем нажимаем **«ЛКМ»** и **«Запустить»**.

</details>

<details>

<summary>⚠ Исправляем ошибку MSVCP и VCRUNTIME на Windows 10/11</summary>

**1.** Нажимаем **«Win+R»** и пишем **«control»**.

**2.** Выбираем **«Программы и компоненты»**.

**3.** В поиск (справа сверху) пишем слово **«Visual»** и удалям все что касается **«Microsoft Visual»**.

**4.** Скачиваем архив и распаковываем — [Ссылка](https://dl.comss.org/download/Visual-C-Runtimes-All-in-One-Jun-2026.zip)

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

> Рекомендованные списки: **[1](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt)**, **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI/CIDR белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)** | **[Видео гайд по установке](https://youtu.be/uz6JmOO7sGU)**.

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

> Рекомендованные списки: **[1](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt)**, **[6](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt)**, **[22](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt)**, **[23](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt)**, **[24](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/24.txt)** и **[25](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/25.txt)**.

> Обход SNI/CIDR белых списков: **[26](https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt)** | **[Видео гайд по установке](https://youtu.be/uz6JmOO7sGU)**.

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
+ **SBER**: `2202 2050 1464 4675`
