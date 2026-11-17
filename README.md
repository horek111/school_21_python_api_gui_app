# School 21 API Client (Tkinter GUI)

Python-приложение с графическим интерфейсом для работы с API School 21.
Покрывает все эндпоинты из документации School 21 OpenAPI Specification.

![Скриншот приложения](screenshots/app.png)

## Возможности

- **37 команд** — от авторизации до графа проектов, включая команды с автоматической пагинацией («ВСЕ …»).
- **Тёмный современный интерфейс** с поиском по командам и категориями в боковой панели.
- **Выпадающие списки** (Combobox) для полей со фиксированными значениями: `status`, `type`, `occupied`, `projectType`.
- **Клиентская фильтрация** — поиск по логину/названию в списках участников, проектов, курсов.
- **Читаемые даты** — ISO-формат автоматически преобразуется в `ДД.ММ.ГГГГ ЧЧ:ММ`.
- **Красивый вывод** — таблицы с выравниванием, карточки, пустые поля показываются как «—».
- **Сохранение состояния** — при переключении команд параметры и результат сохраняются.
- **Подсказки** — описание каждой команды и формат каждого поля.
- **Горизонтальная прокрутка** — таскаемый фиолетовый ползунок для широких таблиц.

## Требования

- Python 3.8 или новее
- pip (менеджер пакетов Python)
- Библиотека `requests` (устанавливается автоматически)
- `tkinter` (входит в стандартную библиотеку Python на большинстве систем)

---

## Установка на Linux

### Шаг 1. Проверить Python

Откройте терминал и выполните:

```bash
python3 --version
```

Должно быть `Python 3.8.x` или выше. Если Python не установлен:

**Ubuntu / Debian / Linux Mint:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

**Arch Linux / Manjaro:**
```bash
sudo pacman -S python python-pip tk
```

**openSUSE:**
```bash
sudo zypper install python3 python3-pip python3-tk
```

### Шаг 2. Скачать проект

**Вариант А — через git:**
```bash
git clone https://github.com/horek111/school_21_python_api_gui_app.git
cd school_21_python_api_gui_app
```

**Вариант Б — скачать ZIP:**
1. Откройте https://github.com/horek111/school_21_python_api_gui_app
2. Нажмите зелёную кнопку **Code** → **Download ZIP**
3. Распакуйте архив в удобную папку
4. Откройте терминал в этой папке

### Шаг 3. Установить зависимости

```bash
pip3 install -r requirements.txt
```

Если pip3 не найден — попробуйте:
```bash
python3 -m pip install -r requirements.txt
```

### Шаг 4. Запустить

```bash
python3 s21_api_app.py
```

Если команда не найдена, попробуйте:
```bash
python s21_api_app.py
```

### Возможные проблемы на Linux

**Ошибка: `ModuleNotFoundError: No module named 'tkinter'`**
```bash
# Ubuntu/Debian:
sudo apt install python3-tk
# Fedora:
sudo dnf install python3-tkinter
# Arch:
sudo pacman -S tk
```

**Ошибка: `externally-managed-environment` (Python 3.11+)**
Используйте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 s21_api_app.py
```

**Ошибка: `Permission denied` при установке пакетов**
Не используйте `sudo pip`. Вместо этого:
```bash
pip3 install --user -r requirements.txt
```

---

## Установка на Windows

### Шаг 1. Установить Python

1. Откройте https://www.python.org/downloads/
2. Нажмите **Download Python 3.x.x** (последняя версия)
3. Запустите установщик
4. **ВАЖНО:** поставьте галочку **«Add python.exe to PATH»** внизу окна установщика
5. Нажмите **Install Now**
6. После установки нажмите **Close**

Проверьте установку — откройте **Командную строку** (Win + R → `cmd` → Enter):
```cmd
python --version
```
Должно показать `Python 3.x.x`.

### Шаг 2. Скачать проект

**Вариант А — через git:**
1. Установите Git для Windows: https://git-scm.com/download/win
2. Откройте **Командную строку** или **PowerShell**
3. Выполните:
```cmd
git clone https://github.com/horek111/school_21_python_api_gui_app.git
cd school_21_python_api_gui_app
```

**Вариант Б — скачать ZIP:**
1. Откройте https://github.com/horek111/school_21_python_api_gui_app
2. Нажмите зелёную кнопку **Code** → **Download ZIP**
3. Распакуйте архив в удобную папку (например, `C:\school_21_api`)
4. Откройте **Командную строку** и перейдите в папку:
```cmd
cd C:\school_21_api
```

### Шаг 3. Установить зависимости

В Командной строке (в папке проекта):
```cmd
pip install -r requirements.txt
```

Если pip не найден:
```cmd
python -m pip install -r requirements.txt
```

### Шаг 4. Запустить

```cmd
python s21_api_app.py
```

Или дважды кликните на файл `s21_api_app.py` в Проводнике (если Python ассоциирован с .py файлами).

### Возможные проблемы на Windows

**Ошибка: `python` не является внутренней или внешней командой**
- Переустановите Python с галочкой **«Add python.exe to PATH»**
- Или добавьте путь вручную: Панель управления → Система → Дополнительные параметры → Переменные среды → Path → добавить `C:\Users\<имя>\AppData\Local\Programs\Python\Python3x\`

**Ошибка: `No module named 'tkinter'`**
- Переустановите Python, выбрав **Modify** → поставьте галочку **tcl/tk and IDLE** → Install

**Окно не открывается / мигает и закрывается**
- Запустите из Командной строки, чтобы увидеть ошибку:
```cmd
python s21_api_app.py
```

**Антивирус блокирует запуск**
- Добавьте папку проекта в исключения антивируса

---

## Использование

1. При запуске откроется основной интерфейс.
2. Выполните **«Авторизация»** — введите логин и пароль School 21. Токен сохранится автоматически.
3. Выберите команду в списке слева (поиск — в поле над списком).
4. Заполните параметры (под каждым полем есть подсказка).
5. Нажмите **«Выполнить»** — результат появится справа.
6. Кнопки:
   - **Копировать результат** — копирует вывод в буфер обмена.
   - **Показать JSON / Показать красиво** — переключает вид вывода.
   - **Восстановить результат** — показывает сохранённый результат выбранной команды.

## Формат дат

Можно вводить в обычном формате — время автоматически станет `00:00 UTC`:
- `2024-01-23`
- `23.01.2024`
- `23/01/2024`

Или полный ISO: `2024-01-23T00:00:00Z`.

## Типы событий

Поле «Тип события» — выпадающий список:
- `ACTIVITY` — мероприятие
- `EXAM` — экзамен
- `TEST` — тест
- пусто — все типы

## Статусы проектов/курсов

`ASSIGNED`, `REGISTERED`, `IN_PROGRESS`, `IN_REVIEWS`, `ACCEPTED`, `FAILED`.

## Команды с автозагрузкой всех страниц («ВСЕ …»)

Автоматически листают все страницы по 1000 записей и показывают полный список:
- ВСЕ участники кампуса / проекта / коалиции
- ВСЕ проекты / курсы / значки / история опыта участника
- ВСЕ кампусы / кластеры / коалиции
- ВСЕ события

## Покрытые эндпоинты

- Auth (Keycloak token)
- Campuses: список, участники, коалиции, кластеры
- Clusters: карта
- Events: список (с фильтром по типу и периоду)
- Sales: текущие продажи
- Projects: по ID, участники
- Coalitions: участники
- Participants: базовая инфо, workstation, skills, проекты, points, logtime, feedback, XP history, courses, coalition, badges
- Courses: по ID
- Graph: карта проектов

## Репозиторий

https://github.com/horek111/school_21_python_api_gui_app
