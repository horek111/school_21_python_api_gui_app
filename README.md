# School 21 API Client (Tkinter GUI)

Python-приложение с графическим интерфейсом, покрывающее все эндпоинты из документации School 21 OpenAPI Specification.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python3 s21_api_app.py
```

## Использование

1. Выберите команду в списке слева.
2. Заполните параметры (если требуются).
3. Нажмите **«Выполнить»**.
4. Результат (JSON) отобразится в правой панели. Кнопка **«Копировать результат»** копирует его в буфер обмена.

Сначала выполните **Auth: получить токен**, введя логин и пароль. После успешной авторизации статус в правом верхнем углу изменится на «Токен: получен», и все остальные команды будут отправлять `Authorization: Bearer <token>`.

## Покрытые эндпоинты

- Auth (Keycloak token)
- Campuses: список, участники, коалиции, кластеры
- Clusters: карта
- Events: список
- Sales: текущие продажи
- Projects: по ID, участники
- Coalitions: участники
- Participants: базовая инфо, workstation, skills, проекты, points, logtime, feedback, XP history, courses, coalition, badges
- Courses: по ID
- Graph: карта проектов
