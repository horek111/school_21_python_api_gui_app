#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Клиент API School 21 с графическим интерфейсом.

Запуск:
    python3 s21_api_app.py

Требуется библиотека requests:
    pip install -r requirements.txt
"""

import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import requests

АДРЕС_API = "https://platform.21-school.ru/services/21-school/api/v1"
АДРЕС_АВТОРИЗАЦИИ = "https://auth.21-school.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token"
ИДЕНТИФИКАТОР_КЛИЕНТА = "s21-open-api"

МАКС_ШИРИНА_ЯЧЕЙКИ = 34
КОЛОНКИ_СПИСКА = 4

# ---------- словарь перевода ключей API на русский ----------
ПЕРЕВОД_КЛЮЧЕЙ = {
    "login": "Логин",
    "className": "Класс",
    "parallelName": "Параллель",
    "expValue": "Опыт (XP)",
    "level": "Уровень",
    "expToNextLevel": "До след. уровня",
    "campus": "Кампус",
    "id": "ID",
    "shortName": "Краткое имя",
    "fullName": "Полное имя",
    "status": "Статус",
    "participants": "Участники",
    "campuses": "Кампусы",
    "clusters": "Кластеры",
    "coalitions": "Коалиции",
    "clusterId": "ID кластера",
    "clusterName": "Кластер",
    "row": "Ряд",
    "number": "Номер",
    "limit": "Лимит",
    "offset": "Смещение",
    "occupied": "Занятые",
    "from": "С",
    "to": "По",
    "type": "Тип",
    "events": "События",
    "name": "Название",
    "description": "Описание",
    "location": "Место",
    "startDateTime": "Начало",
    "endDateTime": "Конец",
    "organizers": "Организаторы",
    "capacity": "Вместимость",
    "registerCount": "Зарегистрировано",
    "sales": "Продажи",
    "progressPercentage": "Прогресс %",
    "projectId": "ID проекта",
    "title": "Название",
    "durationHours": "Часов",
    "xp": "XP",
    "startConditions": "Условия старта",
    "courseId": "ID курса",
    "coalitionId": "ID коалиции",
    "workstation": "Рабочее место",
    "skills": "Навыки",
    "points": "Баллы",
    "projects": "Проекты",
    "finalPercentage": "Процент",
    "completionDateTime": "Завершено",
    "teamMembers": "Члены команды",
    "isTeamlead": "Тимлид",
    "peerReviewPoints": "Баллы пир-ревью",
    "codeReviewPoints": "Баллы код-ревью",
    "coins": "Монеты",
    "logtime": "Время в системе",
    "feedback": "Отзывы",
    "averageVerifierPunctuality": "Пунктуальность",
    "averageVerifierInterest": "Интерес",
    "averageVerifierThoroughness": "Тщательность",
    "averageVerifierFriendliness": "Дружелюбие",
    "expHistory": "История опыта",
    "experience-history": "История опыта",
    "expHistory": "История опыта",
    "accrualDateTime": "Дата начисления",
    "courses": "Курсы",
    "coalition": "Коалиция",
    "badges": "Значки",
    "receiptDateTime": "Получен",
    "iconUrl": "Иконка",
    "graph": "Граф",
    "nodes": "Узлы",
    "edges": "Рёбра",
    "label": "Метка",
    "items": "Элементы",
    "code": "Код",
    "handles": "Ручки",
    "entityType": "Тип сущности",
    "entityId": "ID сущности",
    "source": "Источник",
    "target": "Цель",
    "sourceHandle": "Ручка источника",
    "targetHandle": "Ручка цели",
    "clusterMap": "Карта кластера",
    "accessToken": "Токен доступа",
    "refreshToken": "Токен обновления",
    "tokenType": "Тип токена",
    "expiresIn": "Истекает через",
    "refreshExpiresIn": "Обновление истекает через",
    "scope": "Область",
    "logicalOperator": "Логический оператор",
    "rulesInGroup": "Правила в группе",
    "value": "Значение",
    "fieldId": "ID поля",
    "fieldName": "Поле",
    "subFieldKey": "Подполе (ключ)",
    "subFieldValue": "Подполе (значение)",
    "operator": "Оператор",
    "campusId": "ID кампуса",
    "clusterId": "ID кластера",
}


def перевести_ключ(ключ):
    return ПЕРЕВОД_КЛЮЧЕЙ.get(ключ, ключ.replace("_", " "))

# ---------- цветовая схема (тёмная, современная) ----------
ЦВЕТ = {
    "bg": "#1a1a2e",
    "panel": "#252540",
    "panel2": "#2f2f50",
    "accent": "#861be3",
    "accent_hover": "#9d3bf0",
    "text": "#e8e8f0",
    "muted": "#9a9ab0",
    "border": "#3a3a5c",
    "success": "#4ade80",
    "error": "#f87171",
}


# ---------- описания команд и подсказки полей ----------
ОПИСАНИЯ_КОМАНД = {
    "Авторизация": "Получить токен доступа (JWT) по логину и паролю School 21.",
    "Список кампусов": "Возвращает список всех кампусов Школы 21.",
    "Участники кампуса": "Список логинов участников выбранного кампуса (с пагинацией).",
    "Коалиции кампуса": "Список коалиций кампуса.",
    "Кластеры кампуса": "Список кластеров кампуса.",
    "Карта кластера": "Схема рабочих мест кластера (кто где сидит).",
    "Список событий": "События за период (мероприятия, экзамены, тесты).",
    "Текущие продажи": "Статусы текущих продаж в параллели.",
    "Проект по номеру": "Информация о проекте по его ID.",
    "Участники проекта": "Список участников проекта (с фильтрами).",
    "Участники коалиции": "Список участников коалиции.",
    "Информация об участнике": "Базовая информация об участнике по логину.",
    "Рабочее место участника": "Где сидит участник (кластер, ряд, место).",
    "Навыки участника": "Навыки и баллы участника.",
    "Проекты участника": "Проекты участника (с фильтром по статусу).",
    "Проект участника по номеру": "Информация об одном проекте участника.",
    "Баллы участника": "Баллы пир-ревью, код-ревью, монеты.",
    "Время в системе участника": "Среднее недельное время в системе.",
    "Отзывы об участнике": "Средние оценки от проверяющих.",
    "История опыта участника": "История начисления опыта (XP).",
    "Курсы участника": "Курсы участника (с фильтром по статусу).",
    "Курс участника по номеру": "Информация об одном курсе участника.",
    "Коалиция участника": "Коалиция и ранг участника.",
    "Значки участника": "Список значков участника.",
    "Курс по номеру": "Информация о курсе по ID.",
    "Карта проектов": "Граф проектов участника (узлы и связи).",
}

# описания для "ВСЕ"-команд
for _н in ["ВСЕ участники кампуса", "ВСЕ участники проекта", "ВСЕ участники коалиции",
           "ВСЕ проекты участника", "ВСЕ курсы участника", "ВСЯ история опыта",
           "ВСЕ значки участника", "ВСЕ кампусы", "ВСЕ кластеры кампуса",
           "ВСЕ коалиции кампуса", "ВСЕ события"]:
    ОПИСАНИЯ_КОМАНД[_н] = "Автоматически листает все страницы (по 1000 записей) и показывает полный список."

ПОДСКАЗКИ_ПОЛЕЙ = {
    "campusId": "UUID кампуса (из «Список кампусов»)",
    "limit": "Макс. записей за запрос (до 1000)",
    "offset": "Смещение для пагинации: 0, 1000, 2000...",
    "occupied": "true — занятые места, false — свободные, пусто — все",
    "from": "Дата начала (обычный формат: 2024-01-23)",
    "to": "Дата конца (обычный формат: 2024-01-23)",
    "type": "ACTIVITY, EXAM, TEST или пусто — все типы",
    "status": "ASSIGNED, REGISTERED, IN_PROGRESS, IN_REVIEWS, ACCEPTED, FAILED",
    "login": "Логин участника, например lavonnet",
    "date": "Дата ГГГГ-ММ-ДД, пусто — текущая неделя",
    "projectId": "ID проекта",
    "coalitionId": "ID коалиции",
    "clusterId": "ID кластера",
    "courseId": "ID курса",
    "username": "Ваш логин School 21",
    "password": "Ваш пароль School 21",
    "campusIdFilter": "UUID кампуса для фильтрации",
    "search": "Поиск по подстроке (логин/название)",
    "projectType": "INDIVIDUAL (индивидуальный) или GROUP (групповой)",
}

def очистить_параметры(параметры):
    return {ключ: значение for ключ, значение in параметры.items() if значение not in (None, "")}


# ---------- красивое форматирование вывода ----------

def _обрезать(текст, ширина=МАКС_ШИРИНА_ЯЧЕЙКИ):
    текст = str(текст)
    if len(текст) <= ширина:
        return текст
    return текст[: ширина - 1] + "…"


def _форматировать_дату(значение):
    """Преобразует ISO-дату в читаемый формат ДД.ММ.ГГГГ ЧЧ:ММ."""
    if not isinstance(значение, str):
        return значение
    s = значение.strip()
    if not s:
        return значение
    import re
    if not ("T" in s or re.match(r"^\d{4}-\d{2}-\d{2}", s)):
        return значение
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if "T" in s:
            return dt.strftime("%d.%m.%Y %H:%M")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return значение


def _кратко(значение):
    """Краткое представление сложного значения для ячейки таблицы."""
    if значение is None:
        return "—"
    if isinstance(значение, str) and значение.strip() == "":
        return "—"
    if isinstance(значение, list):
        if not значение:
            return "(пусто)"
        if all(isinstance(x, dict) for x in значение):
            части = []
            for x in значение:
                части.append(str(x.get("code") or x.get("name") or x.get("title") or x.get("id") or x))
            return ", ".join(части)
        return ", ".join(str(x) for x in значение)
    if isinstance(значение, dict):
        for v in значение.values():
            return _кратко(v)
        return str(значение)
    return _форматировать_дату(значение)


def _таблица(список):
    if not список or not all(isinstance(x, dict) for x in список):
        return None
    ключи = []
    for элемент in список:
        for ключ in элемент.keys():
            if ключ not in ключи:
                ключи.append(ключ)
    if not ключи:
        return None
    ширины = {}
    for ключ in ключи:
        лимит = 40 if ключ == "id" else МАКС_ШИРИНА_ЯЧЕЙКИ
        ширина = len(перевести_ключ(ключ))
        for элемент in список:
            ширина = max(ширина, len(str(_кратко(элемент.get(ключ, "")))))
        ширины[ключ] = min(ширина, лимит)

    def строка_ячеек(значения):
        ячейки = []
        for ключ in ключи:
            сырые = значения.get(ключ, "") if isinstance(значения, dict) else значения[ключ]
            текст = _обрезать(_кратко(сырые), ширины[ключ])
            ячейки.append(текст.ljust(ширины[ключ]))
        return " | ".join(ячейки)

    заголовок = строка_ячеек({к: перевести_ключ(к) for к in ключи})
    разделитель = "-+-".join("-" * ширины[к] for к in ключи)
    строки = [заголовок, разделитель]
    for элемент in список:
        строки.append(строка_ячеек(элемент))
    return "\n".join(строки)


def _список_колонками(список, колонок=КОЛОНКИ_СПИСКА):
    if not список:
        return "(пусто)"
    ширина = max(len(str(x)) for x in список)
    ширина = min(ширина + 2, 24)
    строки = []
    for i in range(0, len(список), колонок):
        кусок = список[i:i + колонок]
        строки.append("  ".join(str(_форматировать_дату(x)).ljust(ширина) for x in кусок))
    return "\n".join(строки)


def _карточка(словарь, отступ=""):
    строки = []
    for ключ, значение in словарь.items():
        if isinstance(значение, dict):
            строки.append(f"{отступ}{перевести_ключ(ключ)}:")
            строки.append(_карточка(значение, отступ + "  "))
        elif isinstance(значение, list):
            if not значение:
                строки.append(f"{отступ}{перевести_ключ(ключ)}: (пусто)")
                continue
            if all(isinstance(x, dict) for x in значение):
                табл = _таблица(значение)
                if табл:
                    строки.append(f"{отступ}{перевести_ключ(ключ)} ({len(значение)}):")
                    for строка in табл.split("\n"):
                        строки.append(f"{отступ}  {строка}")
                    continue
                # если таблицу построить нельзя — выводим каждый элемент карточкой
                строки.append(f"{отступ}{перевести_ключ(ключ)} ({len(значение)}):")
                for i, элемент in enumerate(значение, 1):
                    строки.append(f"{отступ}  [{i}]")
                    строки.append(_карточка(элемент, отступ + "    "))
                continue
            if all(not isinstance(x, (dict, list)) for x in значение):
                строки.append(f"{отступ}{перевести_ключ(ключ)} ({len(значение)}):")
                for строка in _список_колонками(значение).split("\n"):
                    строки.append(f"{отступ}  {строка}")
            else:
                строки.append(f"{отступ}{перевести_ключ(ключ)} ({len(значение)}):")
                for i, x in enumerate(значение, 1):
                    строки.append(f"{отступ}  [{i}]")
                    строки.append(_красиво_отформатировать(x, отступ + "    "))
        else:
            строки.append(f"{отступ}{перевести_ключ(ключ)}: {_форматировать_дату(значение)}")
    return "\n".join(строки)


def _красиво_отформатировать(данные, отступ=""):
    if isinstance(данные, list):
        if not данные:
            return отступ + "(пусто)"
        if all(isinstance(x, dict) for x in данные):
            табл = _таблица(данные)
            if табл:
                return "\n".join(f"{отступ}{строка}" for строка in табл.split("\n"))
        if all(not isinstance(x, (dict, list)) for x in данные):
            return f"{отступ}Всего: {len(данные)}\n" + "\n".join(
                f"{отступ}{строка}" for строка in _список_колонками(данные).split("\n")
            )
        строки = []
        for i, элемент in enumerate(данные, 1):
            if isinstance(элемент, (dict, list)):
                строки.append(f"{отступ}[{i}]")
                строки.append(_красиво_отформатировать(элемент, отступ + "  "))
            else:
                строки.append(f"{отступ}{i}. {элемент}")
        return "\n".join(строки)

    if isinstance(данные, dict):
        if len(данные) == 1:
            единственный_ключ = next(iter(данные))
            значение = данные[единственный_ключ]
            if isinstance(значение, list):
                if значение and all(isinstance(x, dict) for x in значение):
                    табл = _таблица(значение)
                    if табл:
                        return f"{отступ}{перевести_ключ(единственный_ключ)} ({len(значение)}):\n" + "\n".join(
                            f"{отступ}  {строка}" for строка in табл.split("\n")
                        )
                if значение and all(not isinstance(x, (dict, list)) for x in значение):
                    return f"{отступ}{перевести_ключ(единственный_ключ)} ({len(значение)}):\n" + "\n".join(
                        f"{отступ}  {строка}" for строка in _список_колонками(значение).split("\n")
                    )
                if not значение:
                    return f"{отступ}{перевести_ключ(единственный_ключ)}: (пусто)"
        return _карточка(данные, отступ)

    return f"{отступ}{данные}"


# ---------- клиент API ----------

class КлиентAPI:
    def __init__(self):
        self.токен = None
        self.сессия = requests.Session()
        self.последний_запрос = ""

    def _заголовки(self):
        заголовки = {"Accept": "application/json"}
        if self.токен:
            заголовки["Authorization"] = f"Bearer {self.токен}"
        return заголовки

    def получить_токен(self, логин, пароль):
        данные = {
            "grant_type": "password",
            "client_id": ИДЕНТИФИКАТОР_КЛИЕНТА,
            "username": логин,
            "password": пароль,
        }
        ответ = self.сессия.post(
            АДРЕС_АВТОРИЗАЦИИ,
            data=данные,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        ответ.raise_for_status()
        результат = ответ.json()
        self.токен = результат.get("access_token")
        return результат

    def запрос(self, метод, путь, параметры=None):
        адрес = АДРЕС_API + путь
        очищенные = очистить_параметры(параметры or {})
        # сохраняем строку запроса для отладки
        if очищенные:
            qs = "&".join(f"{k}={v}" for k, v in очищенные.items())
            self.последний_запрос = f"{метод} {путь}?{qs}"
        else:
            self.последний_запрос = f"{метод} {путь}"
        ответ = self.сессия.request(
            метод,
            адрес,
            headers=self._заголовки(),
            params=очищенные,
            timeout=30,
        )
        try:
            тело = ответ.json()
        except Exception:
            тело = ответ.text
        return ответ.status_code, тело


def сделать_get_команду(название, путь, поля, параметры_api=None):
    if параметры_api is None:
        параметры_api = []

    def обработчик(api, значения):
        готовый_путь = путь.format(**значения)
        параметры = {api_ключ: значения.get(ключ_формы, "") for api_ключ, ключ_формы in параметры_api}
        return api.запрос("GET", готовый_путь, параметры)

    return {"название": название, "поля": поля, "обработчик": обработчик}


def сделать_команду_все_страницы(название, путь, ключ_списка, поля, доп_параметры=None):
    if доп_параметры is None:
        доп_параметры = []

    def обработчик(api, значения):
        готовый_путь = путь.format(**значения)
        лимит = 1000
        смещение = 0
        все = []
        последний_ответ = None
        while True:
            параметры = {"limit": лимит, "offset": смещение}
            for api_ключ, ключ_формы in доп_параметры:
                параметры[api_ключ] = значения.get(ключ_формы, "")
            код, тело = api.запрос("GET", готовый_путь, параметры)
            if код != 200:
                return код, тело
            последний_ответ = тело
            if isinstance(тело, dict):
                список = тело.get(ключ_списка, [])
            elif isinstance(тело, list):
                список = тело
            else:
                список = []
            if not isinstance(список, list):
                return код, тело
            все.extend(список)
            if len(список) < лимит:
                break
            смещение += лимит
        if isinstance(последний_ответ, dict):
            результат = dict(последний_ответ)
            результат[ключ_списка] = все
            return 200, результат
        return 200, все

    return {"название": название, "поля": поля, "обработчик": обработчик}


def команда_авторизации():
    def обработчик(api, значения):
        результат = api.получить_токен(значения["username"], значения["password"])
        return 200, результат

    return {
        "название": "Авторизация",
        "поля": [("Логин", "username", "", False), ("Пароль", "password", "", True)],
        "обработчик": обработчик,
    }


КОМАНДЫ = [
    команда_авторизации(),
    сделать_get_команду("Список кампусов", "/campuses", [], []),
    сделать_get_команду("Участники кампуса", "/campuses/{campusId}/participants",
        [("Номер кампуса", "campusId", "", False), ("Лимит записей", "limit", "50", False), ],
        [("limit", "limit"), ]),
    сделать_get_команду("Коалиции кампуса", "/campuses/{campusId}/coalitions",
        [("Номер кампуса", "campusId", "", False)], []),
    сделать_get_команду("Кластеры кампуса", "/campuses/{campusId}/clusters",
        [("Номер кампуса", "campusId", "", False)], []),
    сделать_get_команду("Карта кластера", "/clusters/{clusterId}/map",
        [("Номер кластера", "clusterId", "", False), ("Лимит записей", "limit", "50", False), ("Только занятые места (true/false)", "occupied", "", False)],
        [("limit", "limit"), ("occupied", "occupied")]),
    сделать_get_команду("Список событий", "/events",
        [("Начало периода (ISO)", "from", "", False), ("Конец периода (ISO)", "to", "", False), ("Тип события", "type", "", False), ("Лимит записей", "limit", "50", False), ],
        [("from", "from"), ("to", "to"), ("type", "type"), ("limit", "limit"), ]),
    сделать_get_команду("Текущие продажи", "/sales", [], []),
    сделать_get_команду("Проект по номеру", "/projects/{projectId}",
        [("Номер проекта", "projectId", "", False)], []),
    сделать_get_команду("Участники проекта", "/projects/{projectId}/participants",
        [("Номер проекта", "projectId", "", False), ("Лимит записей", "limit", "50", False), ("Статус", "status", "", False), ("Номер кампуса (фильтр)", "campusIdFilter", "", False)],
        [("limit", "limit"), ("status", "status"), ("campusId", "campusIdFilter")]),
    сделать_get_команду("Участники коалиции", "/coalitions/{coalitionId}/participants",
        [("Номер коалиции", "coalitionId", "", False), ("Лимит записей", "limit", "50", False), ],
        [("limit", "limit"), ]),
    сделать_get_команду("Информация об участнике", "/participants/{login}",
        [("Логин участника", "login", "", False)], []),
    сделать_get_команду("Рабочее место участника", "/participants/{login}/workstation",
        [("Логин участника", "login", "", False)], []),
    сделать_get_команду("Навыки участника", "/participants/{login}/skills",
        [("Логин участника", "login", "", False)], []),
    сделать_get_команду("Проекты участника", "/participants/{login}/projects",
        [("Логин участника", "login", "", False), ("Лимит записей", "limit", "10", False), ("Статус", "status", "", False)],
        [("limit", "limit"), ("status", "status")]),
    сделать_get_команду("Проект участника по номеру", "/participants/{login}/projects/{projectId}",
        [("Логин участника", "login", "", False), ("Номер проекта", "projectId", "", False)], []),
    сделать_get_команду("Баллы участника", "/participants/{login}/points",
        [("Логин участника", "login", "", False)], []),
    сделать_get_команду("Время в системе участника", "/participants/{login}/logtime",
        [("Логин участника", "login", "", False), ("Дата (ГГГГ-ММ-ДД)", "date", "", False)],
        [("date", "date")]),
    сделать_get_команду("Отзывы об участнике", "/participants/{login}/feedback",
        [("Логин участника", "login", "", False)], []),
    сделать_get_команду("История опыта участника", "/participants/{login}/experience-history",
        [("Логин участника", "login", "", False), ("Лимит записей", "limit", "50", False), ],
        [("limit", "limit"), ]),
    сделать_get_команду("Курсы участника", "/participants/{login}/courses",
        [("Логин участника", "login", "", False), ("Лимит записей", "limit", "10", False), ("Статус", "status", "", False)],
        [("limit", "limit"), ("status", "status")]),
    сделать_get_команду("Курс участника по номеру", "/participants/{login}/courses/{courseId}",
        [("Логин участника", "login", "", False), ("Номер курса", "courseId", "", False)], []),
    сделать_get_команду("Коалиция участника", "/participants/{login}/coalition",
        [("Логин участника", "login", "", False)], []),
    сделать_get_команду("Значки участника", "/participants/{login}/badges",
        [("Логин участника", "login", "", False)], []),
    сделать_get_команду("Курс по номеру", "/courses/{courseId}",
        [("Номер курса", "courseId", "", False)], []),
    сделать_get_команду("Карта проектов", "/graph", [], []),
    # --- команды, которые автоматически загружают ВСЕ страницы ---
    сделать_команду_все_страницы("ВСЕ участники кампуса", "/campuses/{campusId}/participants", "participants",
        [("Номер кампуса", "campusId", "", False)]),
    сделать_команду_все_страницы("ВСЕ участники проекта", "/projects/{projectId}/participants", "participants",
        [("Номер проекта", "projectId", "", False)]),
    сделать_команду_все_страницы("ВСЕ участники коалиции", "/coalitions/{coalitionId}/participants", "participants",
        [("Номер коалиции", "coalitionId", "", False)]),
    сделать_команду_все_страницы("ВСЕ проекты участника", "/participants/{login}/projects", "projects",
        [("Логин участника", "login", "", False)]),
    сделать_команду_все_страницы("ВСЕ курсы участника", "/participants/{login}/courses", "courses",
        [("Логин участника", "login", "", False)]),
    сделать_команду_все_страницы("ВСЯ история опыта", "/participants/{login}/experience-history", "expHistory",
        [("Логин участника", "login", "", False)]),
    сделать_команду_все_страницы("ВСЕ значки участника", "/participants/{login}/badges", "badges",
        [("Логин участника", "login", "", False)]),
    сделать_команду_все_страницы("ВСЕ кампусы", "/campuses", "campuses", []),
    сделать_команду_все_страницы("ВСЕ кластеры кампуса", "/campuses/{campusId}/clusters", "clusters",
        [("Номер кампуса", "campusId", "", False)]),
    сделать_команду_все_страницы("ВСЕ коалиции кампуса", "/campuses/{campusId}/coalitions", "coalitions",
        [("Номер кампуса", "campusId", "", False)]),
    сделать_команду_все_страницы("ВСЕ события", "/events", "events",
        [("Начало периода (ISO)", "from", "", False), ("Конец периода (ISO)", "to", "", False), ("Тип события", "type", "", False)],
        [("from", "from"), ("to", "to"), ("type", "type")]),
]


# ---------- современный интерфейс ----------


# ---------- клиентская фильтрация для списков ----------
def _обернуть_участники_кампуса(базовая):
    def обработчик(api, значения):
        код, тело = базовая["обработчик"](api, значения)
        if код != 200 or not isinstance(тело, dict):
            return код, тело
        участники = тело.get("participants", [])
        поиск = (значения.get("search") or "").lower().strip()
        if поиск:
            участники = [x for x in участники if поиск in str(x).lower()]
        результат = dict(тело)
        результат["participants"] = участники
        return код, результат
    поля = list(базовая["поля"]) + [("Поиск по логину", "search", "", False)]
    return {"название": базовая["название"], "поля": поля, "обработчик": обработчик}


def _обернуть_проекты_участника(базовая):
    def обработчик(api, значения):
        код, тело = базовая["обработчик"](api, значения)
        if код != 200 or not isinstance(тело, dict):
            return код, тело
        проекты = тело.get("projects", [])
        тип = (значения.get("projectType") or "").strip()
        поиск = (значения.get("search") or "").lower().strip()
        отфильтрованные = []
        for p in проекты:
            if тип and p.get("type") != тип:
                continue
            if поиск and поиск not in (p.get("title") or "").lower():
                continue
            отфильтрованные.append(p)
        результат = dict(тело)
        результат["projects"] = отфильтрованные
        return код, результат
    поля = list(базовая["поля"]) + [
        ("Тип проекта", "projectType", "", False),
        ("Поиск по названию", "search", "", False),
    ]
    return {"название": базовая["название"], "поля": поля, "обработчик": обработчик}


# Применяем обёртки к соответствующим командам
for _i, _к in enumerate(КОМАНДЫ):
    if _к["название"] == "Участники кампуса":
        КОМАНДЫ[_i] = _обернуть_участники_кампуса(_к)
    if _к["название"] == "Проекты участника":
        КОМАНДЫ[_i] = _обернуть_проекты_участника(_к)


def _обернуть_курсы_участника(базовая):
    def обработчик(api, значения):
        код, тело = базовая["обработчик"](api, значения)
        if код != 200 or not isinstance(тело, dict):
            return код, тело
        курсы = тело.get("courses", [])
        поиск = (значения.get("search") or "").lower().strip()
        if поиск:
            курсы = [x for x in курсы if поиск in (x.get("title") or "").lower()]
        результат = dict(тело)
        результат["courses"] = курсы
        return код, результат
    поля = list(базовая["поля"]) + [("Поиск по названию", "search", "", False)]
    return {"название": базовая["название"], "поля": поля, "обработчик": обработчик}

for _i, _к in enumerate(КОМАНДЫ):
    if _к["название"] == "Курсы участника":
        КОМАНДЫ[_i] = _обернуть_курсы_участника(_к)

class Приложение:
    def __init__(self, корень):
        self.корень = корень
        self.api = КлиентAPI()
        self.текущая_команда = None
        self.поля_ввода = {}
        self.последний_ответ = None
        self.показывать_json = False
        self._все_команды = list(КОМАНДЫ)
        self._состояния = {}  # сохранённые параметры/результаты по командам

        корень.title("School 21 API Client")
        корень.geometry("1320x820")
        корень.minsize(1000, 600)
        корень.configure(bg=ЦВЕТ["bg"])

        self._настроить_стили()
        self._построить_основной_интерфейс()

    def _настроить_стили(self):
        стиль = ttk.Style()
        try:
            стиль.theme_use("clam")
        except Exception:
            pass
        стиль.configure(".", background=ЦВЕТ["bg"], foreground=ЦВЕТ["text"], font=("Segoe UI", 10))
        стиль.configure("TFrame", background=ЦВЕТ["bg"])
        стиль.configure("Card.TFrame", background=ЦВЕТ["panel"], relief="flat")
        стиль.configure("TLabel", background=ЦВЕТ["bg"], foreground=ЦВЕТ["text"])
        стиль.configure("Muted.TLabel", background=ЦВЕТ["bg"], foreground=ЦВЕТ["muted"], font=("Segoe UI", 9))
        стиль.configure("Title.TLabel", background=ЦВЕТ["bg"], foreground=ЦВЕТ["text"], font=("Segoe UI", 16, "bold"))
        стиль.configure("TEntry", fieldbackground=ЦВЕТ["panel2"], foreground=ЦВЕТ["text"], insertcolor=ЦВЕТ["text"], bordercolor=ЦВЕТ["border"], lightcolor=ЦВЕТ["border"], darkcolor=ЦВЕТ["border"])
        стиль.configure("TButton", background=ЦВЕТ["accent"], foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0, focusthickness=0, padding=(14, 8))
        стиль.map("TButton", background=[("active", ЦВЕТ["accent_hover"]), ("pressed", ЦВЕТ["accent_hover"])], foreground=[("disabled", ЦВЕТ["muted"])])
        стиль.configure("Secondary.TButton", background=ЦВЕТ["panel2"], foreground=ЦВЕТ["text"], font=("Segoe UI", 10), padding=(12, 7))
        стиль.map("Secondary.TButton", background=[("active", ЦВЕТ["panel"]), ("pressed", ЦВЕТ["panel"])])
        стиль.configure("TProgressbar", background=ЦВЕТ["accent"], troughcolor=ЦВЕТ["panel2"], bordercolor=ЦВЕТ["panel2"], lightcolor=ЦВЕТ["accent"], darkcolor=ЦВЕТ["accent"])
        стиль.configure("TCombobox", fieldbackground=ЦВЕТ["panel2"], foreground=ЦВЕТ["text"], background=ЦВЕТ["panel2"], arrowcolor=ЦВЕТ["muted"], bordercolor=ЦВЕТ["border"], lightcolor=ЦВЕТ["border"], darkcolor=ЦВЕТ["border"])
        стиль.map("TCombobox", fieldbackground=[("readonly", ЦВЕТ["panel2"]), ("active", ЦВЕТ["panel2"])], foreground=[("readonly", ЦВЕТ["text"]), ("active", ЦВЕТ["text"])], selectbackground=[("readonly", ЦВЕТ["accent"])], selectforeground=[("readonly", "white")])
        стиль.configure("Vertical.TScrollbar", width=10, background=ЦВЕТ["muted"], troughcolor=ЦВЕТ["panel"], arrowcolor=ЦВЕТ["panel"], bordercolor=ЦВЕТ["panel"], lightcolor=ЦВЕТ["panel"], darkcolor=ЦВЕТ["panel"])
        стиль.configure("Horizontal.TScrollbar", height=12, background=ЦВЕТ["accent"], troughcolor=ЦВЕТ["panel2"], arrowcolor=ЦВЕТ["panel2"], bordercolor=ЦВЕТ["panel2"], lightcolor=ЦВЕТ["accent"], darkcolor=ЦВЕТ["accent"])

    def _построить_основной_интерфейс(self):
        # корневой контейнер
        главный = tk.Frame(self.корень, bg=ЦВЕТ["bg"])
        главный.pack(fill=tk.BOTH, expand=True)

        # ---- шапка ----
        шапка = tk.Frame(главный, bg=ЦВЕТ["panel"], height=58)
        шапка.pack(fill=tk.X)
        шапка.pack_propagate(False)
        tk.Label(шапка, text="  School 21 API Client", bg=ЦВЕТ["panel"], fg=ЦВЕТ["text"], font=("Segoe UI", 15, "bold")).pack(side=tk.LEFT, padx=8)
        self.статус_токена = tk.StringVar(value="● Токен не получен")
        tk.Label(шапка, textvariable=self.статус_токена, bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=16)

        # ---- тело: sidebar + content ----
        тело = tk.Frame(главный, bg=ЦВЕТ["bg"])
        тело.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # sidebar
        sidebar = tk.Frame(тело, bg=ЦВЕТ["panel"], width=300)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Команды", bg=ЦВЕТ["panel"], fg=ЦВЕТ["text"], font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=12, pady=(12, 6))

        self.поиск = ttk.Entry(sidebar)
        self.поиск.pack(fill=tk.X, padx=12, pady=(0, 8))
        self.поиск.insert(0, "Поиск...")
        self.поиск.bind("<FocusIn>", lambda e: self._очистить_поиск())
        self.поиск.bind("<KeyRelease>", lambda e: self._фильтровать_список())

        рамка_списка = tk.Frame(sidebar, bg=ЦВЕТ["panel"])
        рамка_списка.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        скролл = ttk.Scrollbar(рамка_списка, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        скролл.pack(side=tk.RIGHT, fill=tk.Y)
        self.список = tk.Listbox(
            рамка_списка,
            font=("Segoe UI", 10),
            bg=ЦВЕТ["panel2"],
            fg=ЦВЕТ["text"],
            selectbackground=ЦВЕТ["accent"],
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",
            yscrollcommand=скролл.set,
        )
        self.список.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        скролл.config(command=self.список.yview)
        # порядок: самые частые вверху, затем по категориям
        self._порядок_списка = [
            "─── Частые ───",
            "Авторизация",
            "Информация об участнике",
            "История опыта участника",
            "Баллы участника",
            "Рабочее место участника",
            "Навыки участника",
            "Участники кампуса",
            "Список кампусов",
            "Список событий",
            "─── Загрузить всё ───",
        ] + [c["название"] for c in КОМАНДЫ if c["название"].startswith("ВСЕ") or c["название"].startswith("ВСЯ")] + [
            "─── Участник ───",
            "Проекты участника",
            "Курсы участника",
            "Время в системе участника",
            "Отзывы об участнике",
            "Коалиция участника",
            "Значки участника",
            "Проект участника по номеру",
            "Курс участника по номеру",
            "─── Кампусы и кластеры ───",
            "Коалиции кампуса",
            "Кластеры кампуса",
            "Карта кластера",
            "─── Проекты и курсы ───",
            "Проект по номеру",
            "Участники проекта",
            "Участники коалиции",
            "Курс по номеру",
            "─── События и продажи ───",
            "Текущие продажи",
            "─── Утилиты ───",
            "Карта проектов",
        ]
        for имя in self._порядок_списка:
            self.список.insert(tk.END, имя)
        self.список.bind("<<ListboxSelect>>", self.при_выборе)

        # content
        content = tk.Frame(тело, bg=ЦВЕТ["bg"])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # карточка параметров
        карточка_формы = tk.Frame(content, bg=ЦВЕТ["panel"], highlightbackground=ЦВЕТ["border"], highlightthickness=1)
        карточка_формы.pack(fill=tk.X, pady=(0, 10))
        tk.Label(карточка_формы, text="Параметры", bg=ЦВЕТ["panel"], fg=ЦВЕТ["text"], font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=14, pady=(10, 4))
        self.форма = tk.Frame(карточка_формы, bg=ЦВЕТ["panel"])
        self.форма.pack(fill=tk.X, padx=14, pady=(0, 10))
        self._пустая_форма()

        # кнопки
        строка_кнопок = tk.Frame(content, bg=ЦВЕТ["bg"])
        строка_кнопок.pack(fill=tk.X, pady=(0, 8))
        self.кнопка_выполнить = ttk.Button(строка_кнопок, text="▶  Выполнить", style="TButton", command=self.выполнить, state=tk.DISABLED)
        self.кнопка_выполнить.pack(side=tk.LEFT)
        self.кнопка_копировать = ttk.Button(строка_кнопок, text="Копировать", style="Secondary.TButton", command=self.копировать)
        self.кнопка_копировать.pack(side=tk.LEFT, padx=8)
        self.кнопка_вид = ttk.Button(строка_кнопок, text="Показать JSON", style="Secondary.TButton", command=self.переключить_вид)
        self.кнопка_вид.pack(side=tk.LEFT)
        self.кнопка_восстановить = ttk.Button(строка_кнопок, text="Восстановить результат", style="Secondary.TButton", command=self.восстановить_результат)
        self.кнопка_восстановить.pack(side=tk.LEFT, padx=6)

        # прогресс-бар
        self.прогресс = ttk.Progressbar(content, mode="indeterminate", style="TProgressbar")
        self.прогресс.pack(fill=tk.X, pady=(0, 8))

        # карточка результата
        карточка_результата = tk.Frame(content, bg=ЦВЕТ["panel"], highlightbackground=ЦВЕТ["border"], highlightthickness=1)
        карточка_результата.pack(fill=tk.BOTH, expand=True)
        tk.Label(карточка_результата, text="Результат", bg=ЦВЕТ["panel"], fg=ЦВЕТ["text"], font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=14, pady=(10, 4))
        рамка_результата = tk.Frame(карточка_результата, bg=ЦВЕТ["panel"])
        рамка_результата.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        скролл_рез = ttk.Scrollbar(рамка_результата, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        скролл_рез.pack(side=tk.RIGHT, fill=tk.Y)
        скролл_гориз = ttk.Scrollbar(рамка_результата, orient=tk.HORIZONTAL, style="Horizontal.TScrollbar")
        скролл_гориз.pack(side=tk.BOTTOM, fill=tk.X)
        self.результат = tk.Text(
            рамка_результата,
            wrap=tk.NONE,
            font=("Consolas", 10),
            bg=ЦВЕТ["panel2"],
            fg=ЦВЕТ["text"],
            insertbackground=ЦВЕТ["text"],
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=скролл_рез.set,
            xscrollcommand=скролл_гориз.set,
            padx=10,
            pady=8,
        )
        self.результат.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        скролл_рез.config(command=self.результат.yview)
        скролл_гориз.config(command=self.результат.xview)
        # горизонтальная прокрутка колесом мыши (Shift+колесо)
        def _прокрутка_горизонтальная(событие):
            if событие.num == 4 or событие.delta > 0:
                self.результат.xview_scroll(-1, "units")
            else:
                self.результат.xview_scroll(1, "units")
        self.результат.bind("<Shift-MouseWheel>", _прокрутка_горизонтальная)
        self.результат.bind("<Shift-Button-4>", _прокрутка_горизонтальная)
        self.результат.bind("<Shift-Button-5>", _прокрутка_горизонтальная)

        # статус-бар
        статус_бар = tk.Frame(главный, bg=ЦВЕТ["panel"], height=24)
        статус_бар.pack(fill=tk.X, side=tk.BOTTOM)
        статус_бар.pack_propagate(False)
        self.строка_статуса = tk.StringVar(value="Готово. Выберите команду слева.")
        tk.Label(статус_бар, textvariable=self.строка_статуса, bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=12)

        self.показать_текст("Готово. Выберите команду в списке слева.")

    def _очистить_поиск(self):
        if self.поиск.get() == "Поиск...":
            self.поиск.delete(0, tk.END)

    def _фильтровать_список(self):
        запрос = self.поиск.get().strip().lower()
        if запрос == "поиск...":
            запрос = ""
        self.список.delete(0, tk.END)
        for имя in self._порядок_списка:
            if имя.startswith("───"):
                continue
            if запрос in имя.lower():
                self.список.insert(tk.END, имя)

    def показать_текст(self, текст):
        self.результат.config(state=tk.NORMAL)
        self.результат.delete("1.0", tk.END)
        self.результат.insert(tk.END, текст)
        self.результат.config(state=tk.NORMAL)

    def при_выборе(self, событие=None):
        выделение = self.список.curselection()
        if not выделение:
            return
        имя = self.список.get(выделение[0])
        if имя.startswith("───"):
            # игнорируем заголовки-разделители
            self.список.selection_clear(0, tk.END)
            return
        # сохраняем состояние текущей команды (включая результат)
        if self.текущая_команда is not None:
            self._сохранить_состояние(self.текущая_команда["название"])
        for команда in КОМАНДЫ:
            if команда["название"] == имя:
                self.текущая_команда = команда
                break
        if self.текущая_команда:
            self.построить_форму(self.текущая_команда)
            # восстанавливаем только параметры, результат очищаем
            состояние = self._состояния.get(self.текущая_команда["название"])
            if состояние:
                for ключ, значение in состояние["значения"].items():
                    if ключ in self.поля_ввода:
                        try:
                            self.поля_ввода[ключ].delete(0, tk.END)
                            self.поля_ввода[ключ].insert(0, значение)
                        except Exception:
                            pass
            self.показать_текст("Готово. Нажмите «Выполнить» или «Восстановить результат».")

    def _пустая_форма(self):
        for виджет in self.форма.winfo_children():
            виджет.destroy()
        tk.Label(self.форма, text="Выберите команду слева", bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 10)).pack(anchor=tk.W)

    def построить_форму(self, команда):
        for виджет in self.форма.winfo_children():
            виджет.destroy()
        self.поля_ввода = {}
        # заголовок выбранной команды
        tk.Label(self.форма, text=команда["название"], bg=ЦВЕТ["panel"], fg=ЦВЕТ["accent"], font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0, 2))
        описание = ОПИСАНИЯ_КОМАНД.get(команда["название"])
        if описание:
            tk.Label(self.форма, text=описание, bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 9), wraplength=820, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 6))
        поля = команда.get("поля", [])
        if not поля:
            tk.Label(self.форма, text="Параметры не требуются.", bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 10)).pack(anchor=tk.W, pady=4)
        else:
            for метка, ключ, значение_по_умолчанию, секрет in поля:
                строка = tk.Frame(self.форма, bg=ЦВЕТ["panel"])
                строка.pack(fill=tk.X, pady=4)
                tk.Label(строка, text=метка, bg=ЦВЕТ["panel"], fg=ЦВЕТ["text"], width=26, anchor=tk.W, font=("Segoe UI", 10)).pack(side=tk.LEFT)
                if ключ == "type":
                    поле = ttk.Combobox(строка, values=["", "ACTIVITY", "EXAM", "TEST"], state="readonly")
                    поле.set(значение_по_умолчанию)
                elif ключ == "projectType":
                    поле = ttk.Combobox(строка, values=["", "INDIVIDUAL", "GROUP"], state="readonly")
                    поле.set(значение_по_умолчанию)
                elif ключ == "status":
                    поле = ttk.Combobox(строка, values=["", "ASSIGNED", "REGISTERED", "IN_PROGRESS", "IN_REVIEWS", "ACCEPTED", "FAILED"], state="readonly")
                    поле.set(значение_по_умолчанию)
                elif ключ == "occupied":
                    поле = ttk.Combobox(строка, values=["", "true", "false"], state="readonly")
                    поле.set(значение_по_умолчанию)
                else:
                    поле = ttk.Entry(строка)
                    if секрет:
                        поле.config(show="*")
                    поле.insert(0, значение_по_умолчанию)
                поле.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.поля_ввода[ключ] = поле
                подсказка = ПОДСКАЗКИ_ПОЛЕЙ.get(ключ)
                if подсказка:
                    tk.Label(self.форма, text=f"  ↳ {подсказка}", bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 8)).pack(anchor=tk.W, pady=(0, 2))
        # восстановление сохранённых значений
        состояние = self._состояния.get(команда["название"])
        if состояние:
            for ключ, значение in состояние["значения"].items():
                if ключ in self.поля_ввода:
                    try:
                        self.поля_ввода[ключ].delete(0, tk.END)
                        self.поля_ввода[ключ].insert(0, значение)
                    except Exception:
                        pass
        if any(k in self.поля_ввода for k in ("from", "to")):
            tk.Label(self.форма, text="Введите дату: 2024-01-23 или 23.01.2024 — время автоматически 00:00 UTC", bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(6, 0))
        if "type" in self.поля_ввода:
            tk.Label(self.форма, text="Типы событий: ACTIVITY (мероприятие), EXAM (экзамен), TEST (тест). Пусто — все типы.", bg=ЦВЕТ["panel"], fg=ЦВЕТ["muted"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(2, 0))
        self.кнопка_выполнить.config(state=tk.NORMAL)

    def _сохранить_состояние(self, имя):
        if self.текущая_команда is None:
            return
        значения = {}
        for ключ, поле in self.поля_ввода.items():
            try:
                значения[ключ] = поле.get()
            except Exception:
                значения[ключ] = ""
        self._состояния[имя] = {
            "значения": значения,
            "результат": self.результат.get("1.0", tk.END),
            "последний_ответ": self.последний_ответ,
        }

    def _восстановить_состояние(self, имя):
        состояние = self._состояния.get(имя)
        if not состояние:
            return
        for ключ, значение in состояние["значения"].items():
            if ключ in self.поля_ввода:
                try:
                    self.поля_ввода[ключ].delete(0, tk.END)
                    self.поля_ввода[ключ].insert(0, значение)
                except Exception:
                    pass
        self.последний_ответ = состояние.get("последний_ответ")

    def собрать_значения(self):
        значения = {}
        for ключ, поле in self.поля_ввода.items():
            значения[ключ] = поле.get().strip()
        return значения

    def выполнить(self):
        if not self.текущая_команда:
            return
        значения = self.собрать_значения()
        self.кнопка_выполнить.config(state=tk.DISABLED)
        self.показать_текст("Выполняется...")
        self.строка_статуса.set("Выполняется запрос...")
        self.прогресс.start(10)
        threading.Thread(target=self._выполнить_в_потоке, args=(self.текущая_команда, значения), daemon=True).start()

    def _выполнить_в_потоке(self, команда, значения):
        try:
            if "from" in значения and not значения.get("from"):
                raise ValueError("Укажите начало периода (поле «С»)")
            if "to" in значения and not значения.get("to"):
                raise ValueError("Укажите конец периода (поле «По»)")
            # проверка формата ISO-даты
            from datetime import datetime
            for поле_даты in ("from", "to"):
                значение = значения.get(поле_даты)
                if значение:
                    значение = значение.strip()
                    # нормализация: обычный формат -> ISO с 00:00:00Z
                    if "T" not in значение:
                        нормализовано = None
                        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
                            try:
                                dt = datetime.strptime(значение, fmt)
                                нормализовано = dt.strftime("%Y-%m-%dT00:00:00Z")
                                break
                            except ValueError:
                                continue
                        if нормализовано is None:
                            raise ValueError(f"Неверный формат даты в поле «{поле_даты}». Введите, например: 2024-01-23 или 23.01.2024")
                        значения[поле_даты] = нормализовано
                    else:
                        try:
                            datetime.fromisoformat(значение.replace("Z", "+00:00"))
                        except ValueError:
                            raise ValueError(f"Неверный формат даты в поле «{поле_даты}». Пример: 2024-01-23T00:00:00Z")
            код, тело = команда["обработчик"](self.api, значения)
            self.последний_ответ = (код, тело)
            if self.показывать_json:
                текст = json.dumps(тело, ensure_ascii=False, indent=2) if isinstance(тело, (dict, list)) else str(тело)
            else:
                текст = _красиво_отформатировать(тело) if isinstance(тело, (dict, list)) else str(тело)
            результат = f"Запрос: {self.api.последний_запрос}\nКод ответа: {код}\n\n{текст}"
            if команда["название"] == "Авторизация":
                self.статус_токена.set("● Токен получен" if self.api.токен else "● Токен не получен")
                self.строка_статуса.set("Токен получен" if self.api.токен else "Токен не получен")
            else:
                self.строка_статуса.set(f"Готово. Код ответа: {код}")
        except Exception as ошибка:
            результат = f"Ошибка: {ошибка}"
            self.последний_ответ = None
            self.строка_статуса.set(f"Ошибка: {ошибка}")
        self.корень.after(0, lambda: self._завершить(результат))

    def _завершить(self, результат):
        self.показать_текст(результат)
        self.кнопка_выполнить.config(state=tk.NORMAL)
        self.прогресс.stop()
        if self.текущая_команда is not None:
            self._сохранить_состояние(self.текущая_команда["название"])

    def переключить_вид(self):
        self.показывать_json = not self.показывать_json
        self.кнопка_вид.config(text="Показать красиво" if self.показывать_json else "Показать JSON")
        if self.последний_ответ is not None:
            код, тело = self.последний_ответ
            if self.показывать_json:
                текст = json.dumps(тело, ensure_ascii=False, indent=2) if isinstance(тело, (dict, list)) else str(тело)
            else:
                текст = _красиво_отформатировать(тело) if isinstance(тело, (dict, list)) else str(тело)
            self.показать_текст(f"Код ответа: {код}\n\n{текст}")

    def восстановить_результат(self):
        if self.текущая_команда is None:
            return
        состояние = self._состояния.get(self.текущая_команда["название"])
        if состояние and состояние.get("результат"):
            self.показать_текст(состояние["результат"].rstrip("\n"))
            self.последний_ответ = состояние.get("последний_ответ")
        else:
            self.показать_текст("Сохранённого результата нет. Нажмите «Выполнить».")

    def копировать(self):
        текст = self.результат.get("1.0", tk.END)
        self.корень.clipboard_clear()
        self.корень.clipboard_append(текст)
        messagebox.showinfo("Копирование", "Результат скопирован в буфер обмена.")


def main():
    корень = tk.Tk()
    # сглаживание шрифтов
    try:
        корень.call("tk", "scaling", 1.2)
    except Exception:
        pass
    Приложение(корень)
    корень.mainloop()


if __name__ == "__main__":
    main()
