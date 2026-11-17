#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
School 21 API client with a Tkinter GUI.

Run:
    python3 s21_api_app.py

Requires requests:
    pip install -r requirements.txt
"""

import json
import re
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk

import requests

API_URL = "https://platform.21-school.ru/services/21-school/api/v1"
AUTH_URL = "https://auth.21-school.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token"
CLIENT_ID = "s21-open-api"

MAX_CELL_WIDTH = 34
LIST_COLUMNS = 4

# ---------- color scheme (dark, modern) ----------
COLORS = {
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

# ---------- key translation (API keys -> Russian labels) ----------
KEY_TRANSLATIONS = {
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

# ---------- command descriptions ----------
COMMAND_DESCRIPTIONS = {
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

# descriptions for "ALL"-commands
for _n in ["ВСЕ участники кампуса", "ВСЕ участники проекта", "ВСЕ участники коалиции",
           "ВСЕ проекты участника", "ВСЕ курсы участника", "ВСЯ история опыта",
           "ВСЕ значки участника", "ВСЕ кампусы", "ВСЕ кластеры кампуса",
           "ВСЕ коалиции кампуса", "ВСЕ события"]:
    COMMAND_DESCRIPTIONS[_n] = "Автоматически листает все страницы (по 1000 записей) и показывает полный список."

# ---------- field hints ----------
FIELD_HINTS = {
    "campusId": "UUID кампуса (из «Список кампусов»)",
    "limit": "Макс. записей за запрос (до 1000)",
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

def translate_key(key):
    return KEY_TRANSLATIONS.get(key, key.replace("_", " "))

def clean_params(params):
    return {k: v for k, v in params.items() if v not in (None, "")}


# ---------- pretty formatting ----------

def format_date(value):
    """Convert ISO date to readable DD.MM.YYYY HH:MM."""
    if not isinstance(value, str):
        return value
    s = value.strip()
    if not s:
        return value
    if not ("T" in s or re.match(r"^\d{4}-\d{2}-\d{2}", s)):
        return value
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if "T" in s:
            return dt.strftime("%d.%m.%Y %H:%M")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return value


def truncate(text, width=MAX_CELL_WIDTH):
    text = str(text)
    if len(text) <= width:
        return text
    return text[: width - 1] + "…"


def brief(value):
    """Short representation of a complex value for a table cell."""
    if value is None:
        return "—"
    if isinstance(value, str):
        if value.strip() == "":
            return "—"
        return format_date(value)
    if isinstance(value, list):
        if not value:
            return "(пусто)"
        if all(isinstance(x, dict) for x in value):
            parts = []
            for x in value:
                parts.append(str(x.get("code") or x.get("name") or x.get("title") or x.get("id") or x))
            return ", ".join(parts)
        return ", ".join(str(x) for x in value)
    if isinstance(value, dict):
        for v in value.values():
            return brief(v)
        return str(value)
    return format_date(value)


def make_table(data_list):
    if not data_list or not all(isinstance(x, dict) for x in data_list):
        return None
    keys = []
    for item in data_list:
        for key in item.keys():
            if key not in keys:
                keys.append(key)
    if not keys:
        return None
    widths = {}
    for key in keys:
        limit = 40 if key == "id" else MAX_CELL_WIDTH
        width = len(translate_key(key))
        for item in data_list:
            width = max(width, len(str(brief(item.get(key, "")))))
        widths[key] = min(width, limit)

    def row_cells(values):
        cells = []
        for key in keys:
            raw = values.get(key, "") if isinstance(values, dict) else values[key]
            text = truncate(brief(raw), widths[key])
            cells.append(text.ljust(widths[key]))
        return " | ".join(cells)

    header = row_cells({k: translate_key(k) for k in keys})
    separator = "-+-".join("-" * widths[k] for k in keys)
    lines = [header, separator]
    for item in data_list:
        lines.append(row_cells(item))
    return "\n".join(lines)


def list_columns(data_list, columns=LIST_COLUMNS):
    if not data_list:
        return "(пусто)"
    width = max(len(str(x)) for x in data_list)
    width = min(width + 2, 24)
    lines = []
    for i in range(0, len(data_list), columns):
        chunk = data_list[i:i + columns]
        lines.append("  ".join(str(format_date(x)).ljust(width) for x in chunk))
    return "\n".join(lines)


def make_card(data_dict, indent=""):
    lines = []
    for key, value in data_dict.items():
        if isinstance(value, dict):
            lines.append(f"{indent}{translate_key(key)}:")
            lines.append(make_card(value, indent + "  "))
        elif isinstance(value, list):
            if not value:
                lines.append(f"{indent}{translate_key(key)}: (пусто)")
                continue
            if all(isinstance(x, dict) for x in value):
                table = make_table(value)
                if table:
                    lines.append(f"{indent}{translate_key(key)} ({len(value)}):")
                    for line in table.split("\n"):
                        lines.append(f"{indent}  {line}")
                    continue
                lines.append(f"{indent}{translate_key(key)} ({len(value)}):")
                for i, item in enumerate(value, 1):
                    lines.append(f"{indent}  [{i}]")
                    lines.append(make_card(item, indent + "    "))
            elif all(not isinstance(x, (dict, list)) for x in value):
                lines.append(f"{indent}{translate_key(key)} ({len(value)}):")
                for line in list_columns(value).split("\n"):
                    lines.append(f"{indent}  {line}")
            else:
                lines.append(f"{indent}{translate_key(key)} ({len(value)}):")
                for i, x in enumerate(value, 1):
                    lines.append(f"{indent}  [{i}]")
                    lines.append(format_pretty(x, indent + "    "))
        else:
            lines.append(f"{indent}{translate_key(key)}: {format_date(value)}")
    return "\n".join(lines)


def format_pretty(data, indent=""):
    if isinstance(data, list):
        if not data:
            return indent + "(пусто)"
        if all(isinstance(x, dict) for x in data):
            table = make_table(data)
            if table:
                return "\n".join(f"{indent}{line}" for line in table.split("\n"))
        if all(not isinstance(x, (dict, list)) for x in data):
            return f"{indent}Всего: {len(data)}\n" + "\n".join(
                f"{indent}{line}" for line in list_columns(data).split("\n")
            )
        lines = []
        for i, item in enumerate(data, 1):
            if isinstance(item, (dict, list)):
                lines.append(f"{indent}[{i}]")
                lines.append(format_pretty(item, indent + "  "))
            else:
                lines.append(f"{indent}{i}. {format_date(item)}")
        return "\n".join(lines)

    if isinstance(data, dict):
        if len(data) == 1:
            only_key = next(iter(data))
            value = data[only_key]
            if isinstance(value, list):
                if value and all(isinstance(x, dict) for x in value):
                    table = make_table(value)
                    if table:
                        return f"{indent}{translate_key(only_key)} ({len(value)}):\n" + "\n".join(
                            f"{indent}  {line}" for line in table.split("\n")
                        )
                if value and all(not isinstance(x, (dict, list)) for x in value):
                    return f"{indent}{translate_key(only_key)} ({len(value)}):\n" + "\n".join(
                        f"{indent}  {line}" for line in list_columns(value).split("\n")
                    )
                if not value:
                    return f"{indent}{translate_key(only_key)}: (пусто)"
        return make_card(data, indent)

    return f"{indent}{data}"


# ---------- API client ----------

class ApiClient:
    def __init__(self):
        self.token = None
        self.session = requests.Session()
        self.last_request = ""

    def _headers(self):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get_token(self, username, password):
        data = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "username": username,
            "password": password,
        }
        response = self.session.post(
            AUTH_URL,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        self.token = result.get("access_token")
        return result

    def request(self, method, path, params=None):
        url = API_URL + path
        cleaned = clean_params(params or {})
        if cleaned:
            qs = "&".join(f"{k}={v}" for k, v in cleaned.items())
            self.last_request = f"{method} {path}?{qs}"
        else:
            self.last_request = f"{method} {path}"
        response = self.session.request(
            method,
            url,
            headers=self._headers(),
            params=cleaned,
            timeout=30,
        )
        try:
            body = response.json()
        except Exception:
            body = response.text
        return response.status_code, body


def make_get_command(name, path, fields, api_params=None):
    if api_params is None:
        api_params = []

    def handler(api, values):
        ready_path = path.format(**values)
        params = {api_key: values.get(form_key, "") for api_key, form_key in api_params}
        return api.request("GET", ready_path, params)

    return {"name": name, "fields": fields, "handler": handler}


def make_all_pages_command(name, path, list_key, fields, extra_params=None):
    if extra_params is None:
        extra_params = []

    def handler(api, values):
        ready_path = path.format(**values)
        limit = 1000
        offset = 0
        all_items = []
        last_response = None
        while True:
            params = {"limit": limit, "offset": offset}
            for api_key, form_key in extra_params:
                params[api_key] = values.get(form_key, "")
            code, body = api.request("GET", ready_path, params)
            if code != 200:
                return code, body
            last_response = body
            if isinstance(body, dict):
                item_list = body.get(list_key, [])
            elif isinstance(body, list):
                item_list = body
            else:
                item_list = []
            if not isinstance(item_list, list):
                return code, body
            all_items.extend(item_list)
            if len(item_list) < limit:
                break
            offset += limit
        if isinstance(last_response, dict):
            result = dict(last_response)
            result[list_key] = all_items
            return 200, result
        return 200, all_items

    return {"name": name, "fields": fields, "handler": handler}


def auth_command():
    def handler(api, values):
        result = api.get_token(values["username"], values["password"])
        return 200, result

    return {
        "name": "Авторизация",
        "fields": [("Логин", "username", "", False), ("Пароль", "password", "", True)],
        "handler": handler,
    }


# ---------- client-side filtering wrappers ----------

def wrap_campus_participants(base):
    def handler(api, values):
        code, body = base["handler"](api, values)
        if code != 200 or not isinstance(body, dict):
            return code, body
        participants = body.get("participants", [])
        search = (values.get("search") or "").lower().strip()
        if search:
            participants = [x for x in participants if search in str(x).lower()]
        result = dict(body)
        result["participants"] = participants
        return code, result

    fields = list(base["fields"]) + [("Поиск по логину", "search", "", False)]
    return {"name": base["name"], "fields": fields, "handler": handler}


def wrap_participant_projects(base):
    def handler(api, values):
        code, body = base["handler"](api, values)
        if code != 200 or not isinstance(body, dict):
            return code, body
        projects = body.get("projects", [])
        project_type = (values.get("projectType") or "").strip()
        search = (values.get("search") or "").lower().strip()
        filtered = []
        for p in projects:
            if project_type and p.get("type") != project_type:
                continue
            if search and search not in (p.get("title") or "").lower():
                continue
            filtered.append(p)
        result = dict(body)
        result["projects"] = filtered
        return code, result

    fields = list(base["fields"]) + [
        ("Тип проекта", "projectType", "", False),
        ("Поиск по названию", "search", "", False),
    ]
    return {"name": base["name"], "fields": fields, "handler": handler}


def wrap_participant_courses(base):
    def handler(api, values):
        code, body = base["handler"](api, values)
        if code != 200 or not isinstance(body, dict):
            return code, body
        courses = body.get("courses", [])
        search = (values.get("search") or "").lower().strip()
        if search:
            courses = [x for x in courses if search in (x.get("title") or "").lower()]
        result = dict(body)
        result["courses"] = courses
        return code, result

    fields = list(base["fields"]) + [("Поиск по названию", "search", "", False)]
    return {"name": base["name"], "fields": fields, "handler": handler}


# ---------- command list ----------

COMMANDS = [
    auth_command(),
    make_get_command("Список кампусов", "/campuses", [], []),
    make_get_command("Участники кампуса", "/campuses/{campusId}/participants",
        [("Номер кампуса", "campusId", "", False),
         ("Лимит записей", "limit", "50", False)],
        [("limit", "limit")]),
    make_get_command("Коалиции кампуса", "/campuses/{campusId}/coalitions",
        [("Номер кампуса", "campusId", "", False)], []),
    make_get_command("Кластеры кампуса", "/campuses/{campusId}/clusters",
        [("Номер кампуса", "campusId", "", False)], []),
    make_get_command("Карта кластера", "/clusters/{clusterId}/map",
        [("Номер кластера", "clusterId", "", False),
         ("Лимит записей", "limit", "50", False),
         ("Только занятые места (true/false)", "occupied", "", False)],
        [("limit", "limit"), ("occupied", "occupied")]),
    make_get_command("Список событий", "/events",
        [("Начало периода", "from", "", False),
         ("Конец периода", "to", "", False),
         ("Тип события", "type", "", False),
         ("Лимит записей", "limit", "50", False)],
        [("from", "from"), ("to", "to"), ("type", "type"), ("limit", "limit")]),
    make_get_command("Текущие продажи", "/sales", [], []),
    make_get_command("Проект по номеру", "/projects/{projectId}",
        [("Номер проекта", "projectId", "", False)], []),
    make_get_command("Участники проекта", "/projects/{projectId}/participants",
        [("Номер проекта", "projectId", "", False),
         ("Лимит записей", "limit", "50", False),
         ("Статус", "status", "", False),
         ("Номер кампуса (фильтр)", "campusIdFilter", "", False)],
        [("limit", "limit"), ("status", "status"), ("campusId", "campusIdFilter")]),
    make_get_command("Участники коалиции", "/coalitions/{coalitionId}/participants",
        [("Номер коалиции", "coalitionId", "", False),
         ("Лимит записей", "limit", "50", False)],
        [("limit", "limit")]),
    make_get_command("Информация об участнике", "/participants/{login}",
        [("Логин участника", "login", "", False)], []),
    make_get_command("Рабочее место участника", "/participants/{login}/workstation",
        [("Логин участника", "login", "", False)], []),
    make_get_command("Навыки участника", "/participants/{login}/skills",
        [("Логин участника", "login", "", False)], []),
    make_get_command("Проекты участника", "/participants/{login}/projects",
        [("Логин участника", "login", "", False),
         ("Лимит записей", "limit", "10", False),
         ("Статус", "status", "", False)],
        [("limit", "limit"), ("status", "status")]),
    make_get_command("Проект участника по номеру", "/participants/{login}/projects/{projectId}",
        [("Логин участника", "login", "", False),
         ("Номер проекта", "projectId", "", False)], []),
    make_get_command("Баллы участника", "/participants/{login}/points",
        [("Логин участника", "login", "", False)], []),
    make_get_command("Время в системе участника", "/participants/{login}/logtime",
        [("Логин участника", "login", "", False),
         ("Дата (ГГГГ-ММ-ДД)", "date", "", False)],
        [("date", "date")]),
    make_get_command("Отзывы об участнике", "/participants/{login}/feedback",
        [("Логин участника", "login", "", False)], []),
    make_get_command("История опыта участника", "/participants/{login}/experience-history",
        [("Логин участника", "login", "", False),
         ("Лимит записей", "limit", "50", False)],
        [("limit", "limit")]),
    make_get_command("Курсы участника", "/participants/{login}/courses",
        [("Логин участника", "login", "", False),
         ("Лимит записей", "limit", "10", False),
         ("Статус", "status", "", False)],
        [("limit", "limit"), ("status", "status")]),
    make_get_command("Курс участника по номеру", "/participants/{login}/courses/{courseId}",
        [("Логин участника", "login", "", False),
         ("Номер курса", "courseId", "", False)], []),
    make_get_command("Коалиция участника", "/participants/{login}/coalition",
        [("Логин участника", "login", "", False)], []),
    make_get_command("Значки участника", "/participants/{login}/badges",
        [("Логин участника", "login", "", False)], []),
    make_get_command("Курс по номеру", "/courses/{courseId}",
        [("Номер курса", "courseId", "", False)], []),
    make_get_command("Карта проектов", "/graph", [], []),
    # ---------- client-side filtering wrappers ----------
]

# Apply wrappers
for _i, _c in enumerate(COMMANDS):
    if _c["name"] == "Участники кампуса":
        COMMANDS[_i] = wrap_campus_participants(_c)
    if _c["name"] == "Проекты участника":
        COMMANDS[_i] = wrap_participant_projects(_c)
    if _c["name"] == "Курсы участника":
        COMMANDS[_i] = wrap_participant_courses(_c)

# ---------- ALL-commands (auto-pagination) ----------
ALL_COMMANDS = [
    make_all_pages_command("ВСЕ участники кампуса", "/campuses/{campusId}/participants", "participants",
        [("Номер кампуса", "campusId", "", False)]),
    make_all_pages_command("ВСЕ участники проекта", "/projects/{projectId}/participants", "participants",
        [("Номер проекта", "projectId", "", False)]),
    make_all_pages_command("ВСЕ участники коалиции", "/coalitions/{coalitionId}/participants", "participants",
        [("Номер коалиции", "coalitionId", "", False)]),
    make_all_pages_command("ВСЕ проекты участника", "/participants/{login}/projects", "projects",
        [("Логин участника", "login", "", False)]),
    make_all_pages_command("ВСЕ курсы участника", "/participants/{login}/courses", "courses",
        [("Логин участника", "login", "", False)]),
    make_all_pages_command("ВСЯ история опыта", "/participants/{login}/experience-history", "expHistory",
        [("Логин участника", "login", "", False)]),
    make_all_pages_command("ВСЕ значки участника", "/participants/{login}/badges", "badges",
        [("Логин участника", "login", "", False)]),
    make_all_pages_command("ВСЕ кампусы", "/campuses", "campuses", []),
    make_all_pages_command("ВСЕ кластеры кампуса", "/campuses/{campusId}/clusters", "clusters",
        [("Номер кампуса", "campusId", "", False)]),
    make_all_pages_command("ВСЕ коалиции кампуса", "/campuses/{campusId}/coalitions", "coalitions",
        [("Номер кампуса", "campusId", "", False)]),
    make_all_pages_command("ВСЕ события", "/events", "events",
        [("Начало периода", "from", "", False),
         ("Конец периода", "to", "", False),
         ("Тип события", "type", "", False)],
        [("from", "from"), ("to", "to"), ("type", "type")]),
]
COMMANDS.extend(ALL_COMMANDS)


# ---------- sidebar order ----------
SIDEBAR_ORDER = [
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
] + [c["name"] for c in ALL_COMMANDS] + [
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


# ---------- GUI ----------

class App:
    def __init__(self, root):
        self.root = root
        self.api = ApiClient()
        self.current_command = None
        self.entries = {}
        self.last_response = None
        self.show_json = False
        self.all_commands = list(COMMANDS)
        self.states = {}

        root.title("School 21 API Client")
        root.geometry("1320x820")
        root.minsize(1000, 600)
        root.configure(bg=COLORS["bg"])

        self.setup_styles()
        self.build_main_ui()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(".", background=COLORS["bg"], foreground=COLORS["text"], font=("Segoe UI", 10))
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TEntry", fieldbackground=COLORS["panel2"], foreground=COLORS["text"],
                        insertcolor=COLORS["text"], bordercolor=COLORS["border"],
                        lightcolor=COLORS["border"], darkcolor=COLORS["border"])
        style.configure("TButton", background=COLORS["accent"], foreground="white",
                        font=("Segoe UI", 10, "bold"), borderwidth=0, focusthickness=0, padding=(14, 8))
        style.map("TButton", background=[("active", COLORS["accent_hover"]), ("pressed", COLORS["accent_hover"])],
                  foreground=[("disabled", COLORS["muted"])])
        style.configure("Secondary.TButton", background=COLORS["panel2"], foreground=COLORS["text"],
                        font=("Segoe UI", 10), padding=(12, 7))
        style.map("Secondary.TButton", background=[("active", COLORS["panel"]), ("pressed", COLORS["panel"])])
        style.configure("TCombobox", fieldbackground=COLORS["panel2"], foreground=COLORS["text"],
                        background=COLORS["panel2"], arrowcolor=COLORS["muted"], bordercolor=COLORS["border"],
                        lightcolor=COLORS["border"], darkcolor=COLORS["border"])
        style.map("TCombobox", fieldbackground=[("readonly", COLORS["panel2"]), ("active", COLORS["panel2"])],
                  foreground=[("readonly", COLORS["text"]), ("active", COLORS["text"])],
                  selectbackground=[("readonly", COLORS["accent"])], selectforeground=[("readonly", "white")])
        style.configure("Vertical.TScrollbar", width=10, background=COLORS["muted"],
                        troughcolor=COLORS["panel"], arrowcolor=COLORS["panel"],
                        bordercolor=COLORS["panel"], lightcolor=COLORS["panel"], darkcolor=COLORS["panel"])
        style.configure("Horizontal.TScrollbar", height=12, background=COLORS["accent"],
                        troughcolor=COLORS["panel2"], arrowcolor=COLORS["panel2"],
                        bordercolor=COLORS["panel2"], lightcolor=COLORS["accent"], darkcolor=COLORS["accent"])

    def build_main_ui(self):
        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True)

        # header
        header = tk.Frame(main, bg=COLORS["panel"], height=58)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="  School 21 API Client", bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 15, "bold")).pack(side=tk.LEFT, padx=8)
        self.token_status = tk.StringVar(value="● Токен не получен")
        tk.Label(header, textvariable=self.token_status, bg=COLORS["panel"], fg=COLORS["muted"],
                 font=("Segoe UI", 10)).pack(side=tk.RIGHT, padx=16)

        # body
        body = tk.Frame(main, bg=COLORS["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # sidebar
        sidebar = tk.Frame(body, bg=COLORS["panel"], width=300)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Команды", bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=12, pady=(12, 6))

        self.search_entry = ttk.Entry(sidebar)
        self.search_entry.pack(fill=tk.X, padx=12, pady=(0, 8))
        self.search_entry.insert(0, "Поиск...")
        self.search_entry.bind("<FocusIn>", lambda e: self.clear_search())
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_list())

        list_frame = tk.Frame(sidebar, bg=COLORS["panel"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(
            list_frame, font=("Segoe UI", 10), bg=COLORS["panel2"], fg=COLORS["text"],
            selectbackground=COLORS["accent"], selectforeground="white", borderwidth=0,
            highlightthickness=0, activestyle="none", yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        for name in self._list_order():
            self.listbox.insert(tk.END, name)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # content
        content = tk.Frame(body, bg=COLORS["bg"])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # params card
        params_card = tk.Frame(content, bg=COLORS["panel"], highlightbackground=COLORS["border"], highlightthickness=1)
        params_card.pack(fill=tk.X, pady=(0, 10))
        tk.Label(params_card, text="Параметры", bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=14, pady=(10, 4))
        self.form_frame = tk.Frame(params_card, bg=COLORS["panel"])
        self.form_frame.pack(fill=tk.X, padx=14, pady=(0, 10))
        self.empty_form()

        # buttons
        btn_row = tk.Frame(content, bg=COLORS["bg"])
        btn_row.pack(fill=tk.X, pady=(0, 8))
        self.run_button = ttk.Button(btn_row, text="▶  Выполнить", style="TButton", command=self.run, state=tk.DISABLED)
        self.run_button.pack(side=tk.LEFT)
        self.copy_button = ttk.Button(btn_row, text="Копировать", style="Secondary.TButton", command=self.copy_result)
        self.copy_button.pack(side=tk.LEFT, padx=8)
        self.view_button = ttk.Button(btn_row, text="Показать JSON", style="Secondary.TButton", command=self.toggle_view)
        self.view_button.pack(side=tk.LEFT, padx=6)
        self.restore_button = ttk.Button(btn_row, text="Восстановить результат", style="Secondary.TButton", command=self.restore_result)
        self.restore_button.pack(side=tk.LEFT, padx=6)

        # result card
        result_card = tk.Frame(content, bg=COLORS["panel"], highlightbackground=COLORS["border"], highlightthickness=1)
        result_card.pack(fill=tk.BOTH, expand=True)
        tk.Label(result_card, text="Результат", bg=COLORS["panel"], fg=COLORS["text"],
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, padx=14, pady=(10, 4))
        result_frame = tk.Frame(result_card, bg=COLORS["panel"])
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        vscroll = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        hscroll = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL, style="Horizontal.TScrollbar")
        hscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_text = tk.Text(
            result_frame, wrap=tk.NONE, font=("Consolas", 10), bg=COLORS["panel2"],
            fg=COLORS["text"], insertbackground=COLORS["text"], borderwidth=0,
            highlightthickness=0, yscrollcommand=vscroll.set, xscrollcommand=hscroll.set,
            padx=10, pady=8,
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscroll.config(command=self.result_text.yview)
        hscroll.config(command=self.result_text.xview)

        # status bar
        status_bar = tk.Frame(main, bg=COLORS["panel"], height=24)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        self.status_bar_var = tk.StringVar(value="Готово. Выберите команду слева.")
        tk.Label(status_bar, textvariable=self.status_bar_var, bg=COLORS["panel"], fg=COLORS["muted"],
                 font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=12)

        self.show_text("Готово. Выберите команду в списке слева.")

    def _list_order(self):
        order = []
        for name in SIDEBAR_ORDER:
            if name.startswith("───"):
                order.append(name)
                continue
            if any(c["name"] == name for c in COMMANDS):
                order.append(name)
        # add any missing commands
        for c in COMMANDS:
            if c["name"] not in order:
                order.append(c["name"])
        return order

    def clear_search(self):
        if self.search_entry.get() == "Поиск...":
            self.search_entry.delete(0, tk.END)

    def filter_list(self):
        query = self.search_entry.get().strip().lower()
        if query == "поиск...":
            query = ""
        self.listbox.delete(0, tk.END)
        for name in self._list_order():
            if name.startswith("───"):
                continue
            if query in name.lower():
                self.listbox.insert(tk.END, name)

    def show_text(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)

    def on_select(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return
        name = self.listbox.get(selection[0])
        if name.startswith("───"):
            self.listbox.selection_clear(0, tk.END)
            return
        if self.current_command is not None:
            self.save_state(self.current_command["name"])
        for cmd in COMMANDS:
            if cmd["name"] == name:
                self.current_command = cmd
                break
        if self.current_command:
            self.build_form(self.current_command)
            state = self.states.get(self.current_command["name"])
            if state:
                for key, val in state["values"].items():
                    if key in self.entries:
                        try:
                            self.entries[key].delete(0, tk.END)
                            self.entries[key].insert(0, val)
                        except Exception:
                            pass
            self.show_text("Готово. Нажмите «Выполнить» или «Восстановить результат».")

    def empty_form(self):
        for w in self.form_frame.winfo_children():
            w.destroy()
        tk.Label(self.form_frame, text="Выберите команду слева", bg=COLORS["panel"], fg=COLORS["muted"],
                 font=("Segoe UI", 10)).pack(anchor=tk.W)

    def build_form(self, command):
        for w in self.form_frame.winfo_children():
            w.destroy()
        self.entries = {}
        tk.Label(self.form_frame, text=command["name"], bg=COLORS["panel"], fg=COLORS["accent"],
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0, 2))
        desc = COMMAND_DESCRIPTIONS.get(command["name"])
        if desc:
            tk.Label(self.form_frame, text=desc, bg=COLORS["panel"], fg=COLORS["muted"],
                     font=("Segoe UI", 9), wraplength=820, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 6))
        fields = command.get("fields", [])
        if not fields:
            tk.Label(self.form_frame, text="Параметры не требуются.", bg=COLORS["panel"], fg=COLORS["muted"],
                     font=("Segoe UI", 10)).pack(anchor=tk.W, pady=4)
        else:
            for label, key, default, secret in fields:
                row = tk.Frame(self.form_frame, bg=COLORS["panel"])
                row.pack(fill=tk.X, pady=4)
                tk.Label(row, text=label, bg=COLORS["panel"], fg=COLORS["text"], width=26, anchor=tk.W,
                         font=("Segoe UI", 10)).pack(side=tk.LEFT)
                if key == "type":
                    field = ttk.Combobox(row, values=["", "ACTIVITY", "EXAM", "TEST"], state="readonly")
                    field.set(default)
                elif key == "projectType":
                    field = ttk.Combobox(row, values=["", "INDIVIDUAL", "GROUP"], state="readonly")
                    field.set(default)
                elif key == "status":
                    field = ttk.Combobox(row, values=["", "ASSIGNED", "REGISTERED", "IN_PROGRESS",
                                                      "IN_REVIEWS", "ACCEPTED", "FAILED"], state="readonly")
                    field.set(default)
                elif key == "occupied":
                    field = ttk.Combobox(row, values=["", "true", "false"], state="readonly")
                    field.set(default)
                else:
                    field = ttk.Entry(row)
                    if secret:
                        field.config(show="*")
                    field.insert(0, default)
                field.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.entries[key] = field
                hint = FIELD_HINTS.get(key)
                if hint:
                    tk.Label(self.form_frame, text=f"  ↳ {hint}", bg=COLORS["panel"], fg=COLORS["muted"],
                             font=("Segoe UI", 8)).pack(anchor=tk.W, pady=(0, 2))
        if any(k in self.entries for k in ("from", "to")):
            tk.Label(self.form_frame, text="Введите дату: 2024-01-23 или 23.01.2024 — время автоматически 00:00 UTC",
                     bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(6, 0))
        if "type" in self.entries:
            tk.Label(self.form_frame, text="Типы событий: ACTIVITY (мероприятие), EXAM (экзамен), TEST (тест). Пусто — все типы.",
                     bg=COLORS["panel"], fg=COLORS["muted"], font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(2, 0))
        self.run_button.config(state=tk.NORMAL)

    def collect_values(self):
        values = {}
        for key, field in self.entries.items():
            values[key] = field.get().strip()
        return values

    def run(self):
        if not self.current_command:
            return
        values = self.collect_values()
        self.run_button.config(state=tk.DISABLED)
        self.show_text("Выполняется...")
        self.status_bar_var.set("Выполняется запрос...")
        threading.Thread(target=self._run_worker, args=(self.current_command, values), daemon=True).start()

    def _run_worker(self, command, values):
        try:
            if "from" in values and not values.get("from"):
                raise ValueError("Укажите начало периода (поле «С»)")
            if "to" in values and not values.get("to"):
                raise ValueError("Укажите конец периода (поле «По»)")
            # date normalization
            from datetime import datetime
            for date_field in ("from", "to"):
                val = values.get(date_field)
                if val:
                    val = val.strip()
                    if "T" not in val:
                        normalized = None
                        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
                            try:
                                dt = datetime.strptime(val, fmt)
                                normalized = dt.strftime("%Y-%m-%dT00:00:00Z")
                                break
                            except ValueError:
                                continue
                        if normalized is None:
                            raise ValueError(f"Неверный формат даты в поле «{date_field}». Введите, например: 2024-01-23 или 23.01.2024")
                        values[date_field] = normalized
                    else:
                        try:
                            datetime.fromisoformat(val.replace("Z", "+00:00"))
                        except ValueError:
                            raise ValueError(f"Неверный формат даты в поле «{date_field}». Пример: 2024-01-23T00:00:00Z")
            code, body = command["handler"](self.api, values)
            self.last_response = (code, body)
            if self.show_json:
                text = json.dumps(body, ensure_ascii=False, indent=2) if isinstance(body, (dict, list)) else str(body)
            else:
                text = format_pretty(body) if isinstance(body, (dict, list)) else str(body)
            result = f"Запрос: {self.api.last_request}\nКод ответа: {code}\n\n{text}"
            if command["name"] == "Авторизация":
                self.token_status.set("● Токен получен" if self.api.token else "● Токен не получен")
                self.status_bar_var.set("Токен получен" if self.api.token else "Токен не получен")
            else:
                self.status_bar_var.set(f"Готово. Код ответа: {code}")
        except Exception as error:
            result = f"Ошибка: {error}"
            self.last_response = None
            self.status_bar_var.set(f"Ошибка: {error}")
        self.root.after(0, lambda: self._finish_run(result))

    def _finish_run(self, result):
        self.show_text(result)
        self.run_button.config(state=tk.NORMAL)
        if self.current_command is not None:
            self.save_state(self.current_command["name"])

    def toggle_view(self):
        self.show_json = not self.show_json
        self.view_button.config(text="Показать красиво" if self.show_json else "Показать JSON")
        if self.last_response is not None:
            code, body = self.last_response
            if self.show_json:
                text = json.dumps(body, ensure_ascii=False, indent=2) if isinstance(body, (dict, list)) else str(body)
            else:
                text = format_pretty(body) if isinstance(body, (dict, list)) else str(body)
            self.show_text(f"Запрос: {self.api.last_request}\nКод ответа: {code}\n\n{text}")

    def save_state(self, name):
        if self.current_command is None:
            return
        values = {}
        for key, field in self.entries.items():
            try:
                values[key] = field.get()
            except Exception:
                values[key] = ""
        self.states[name] = {
            "values": values,
            "result": self.result_text.get("1.0", tk.END),
            "last_response": self.last_response,
        }

    def restore_result(self):
        if self.current_command is None:
            return
        state = self.states.get(self.current_command["name"])
        if state and state.get("result"):
            self.show_text(state["result"].rstrip("\n"))
            self.last_response = state.get("last_response")
        else:
            self.show_text("Сохранённого результата нет. Нажмите «Выполнить».")

    def copy_result(self):
        text = self.result_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Копирование", "Результат скопирован в буфер обмена.")


def main():
    root = tk.Tk()
    try:
        root.call("tk", "scaling", 1.2)
    except Exception:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
