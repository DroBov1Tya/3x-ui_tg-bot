import flet
import asyncio
import api
from config import http, fastapi_key
from flet import Page, Row, TextField, ElevatedButton, Column, Text

headers = {
    "X-API-Key": fastapi_key
}

async def main(page: Page):
    # Заголовок страницы
    page.title = "Импортирование серверов для 3X-UI"
    page.vertical_alignment = "center"

    # Отображение результата
    result_display = Column()

    # Поле для ввода
    input_field = TextField(
        hint_text="Введите серверы в формате 'hostname:passwd' (каждый сервер с новой строки)",
        expand=True,
        multiline=True,  # Многострочный ввод
        height=150  # Увеличиваем высоту поля ввода
    )

    # Функция для обработки нажатия на кнопку "Добавить"
    async def add_click(e):
    # Очищаем старый результат
        result_display.controls.clear()

        # Получаем введенный текст и разбиваем по строкам
        if input_field.value is None or not input_field.value.strip():
            result_display.controls.append(Text("Поле ввода не может быть пустым!"))
            page.update()
            return

        # Разбиваем ввод на строки
        lines = input_field.value.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Пропускаем пустые строки

            # Проверка правильности формата строки
            parts = line.split(":")
            if len(parts) != 2:
                result_display.controls.append(Text(f"Ошибка: неверный формат в строке '{line}'"))
                continue  # Пропускаем ошибочные строки и продолжаем обработку других строк

            hostname, passwd = parts[0].strip(), parts[1].strip()

            try:
                # Отправка данных на API
                r = await api.send_data(hostname, passwd)

                # Попытка парсинга JSON
                try:
                    response_json = r.json()

                    # Проверка успешного добавления
                    if response_json.get("Success") == True:
                        try:
                            await http(method="POST", url="http://api:8000/xui/init_server", json={"hostname": hostname}, headers=headers)
                            result_display.controls.append(Text(f"Сервер {hostname} успешно добавлен!"))
                        except Exception as e:
                            result_display.controls.append(Text(f"Ошибка при инициализации сервера {hostname}: {e}"))
                    else:
                        result_display.controls.append(Text(f"Ошибка: API не удалось добавить сервер {hostname}!"))

                except ValueError:
                    result_display.controls.append(Text(f"Ошибка: некорректный ответ от API для сервера {hostname} (не JSON)"))
                    print(f"Ошибка: API не вернул JSON для {hostname}: {r.text}")

            except Exception as ex:
                result_display.controls.append(Text(f"Ошибка при отправке данных для сервера {hostname}: {ex}"))
                print(f"Ошибка: {ex}")

            # Обновление страницы для каждой строки
            page.update()

        # Очищаем поле ввода и выводим итоговое сообщение
        result_display.controls.append(Text("Ввод завершён!"))
        input_field.value = ""
        page.update()

    # Добавляем элементы на страницу
    page.add(
        Column(
            [
                Text("Импортирование серверов для 3X-UI"),
                Row(
                    [
                        input_field,
                        ElevatedButton("Добавить", on_click=add_click)
                    ]
                ),
                result_display
            ]
        )
    )

# Запуск приложения на порту 80
flet.app(target=main, view=flet.AppView.WEB_BROWSER, port=80)
