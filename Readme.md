# Film Search (Sakila)

Этот проект представляет собой графическое приложение для поиска фильмов в базе данных Sakila. В нем используется библиотека `tkinter` для создания пользовательского интерфейса, а также база данных MySQL для хранения информации о фильмах и сохранения поисковых запросов пользователей.

## Функциональность
- Поиск фильмов по ключевым словам (название, описание).
- Фильтрация фильмов по жанру и году выпуска.
- Просмотр истории последних поисковых запросов.
- Подключение и работа с базой данных MySQL для хранения информации.

## Требования
Для работы проекта требуется установка следующих зависимостей:

```bash
pip install -r requirements.txt
```

Файл `requirements.txt` включает:
- cffi==1.17.1 — для взаимодействия Python с кодом на C и низкоуровневого доступа к C-библиотекам.
- cryptography==44.0.1 — для выполнения криптографических операций, таких как шифрование, создание хешей и управление сертификатами.
- pycparser==2.22 — для парсинга и анализа исходного кода на языке C, создания абстрактного синтаксического дерева.
- PyMySQL==1.1.1 — для работы с базой данных MySQL, выполнения SQL-запросов и управления базами данных.
- python-dotenv==1.0.1 — для загрузки переменных окружения из файла .env, что помогает безопасно управлять конфиденциальными данными.

## Настройка
### 1. Конфигурация базы данных
Перед запуском создайте файл `.env` в корневой директории проекта и укажите параметры подключения:

```env
DBCONFIG_SAKILA = "{
                    'host': '<ваш_хост>',
                    'user': '<ваш_пользователь>',
                    'password': '<ваш_пароль>',
                    'database': 'sakila',
                    'charset': 'utf8mb4'
                   }"

DBCONFIG_ICH_EDIT = "{
    'host': '<ваш_хост>',
    'user': '<ваш_пользователь>',
    'password': '<ваш_пароль>',
    'database': '160924_panas_search_film',
    'charset': 'utf8mb4'
}"
```

### 2. Запуск приложения
Запустите `main.py`:

```bash
python main.py
```

## Структура проекта
```
.
├── main.py                   	# Главный файл запуска
├── package db
│   ├── db_connection.py      	# Установление соединений с БД
│   ├── db_configs_manager.py 	# Формирование конфигурации подключения к БД из .env
│   ├── db_queries_manager.py 	# Работа с MySQL, обработчик команд SQL
│   └── sql_queries.py        	# SQL запросы к БД
├── package controls
│   ├── CustomButton.py       	# Компонент с кнопками
│   └── MultiSelectCombobox.py 	# Компонент с CB и мультивыбором
├── requirements.txt          	# Зависимости проекта
├── file_manager.py           	# Работа с файлами (создание и выгрузка)
├── .gitignore                	# Игнорируемые файлы
└── .env                      	# Конфигурация базы данных (не хранить в репозитории)

```


## Основные файлы
### `main.py`
Запускает приложениz, созданное с использованием `tkinter`.

### `db_queries_manager.py`
- Связывает интерфейс с базой данных.
- Выполняет поиск фильмов по разным параметрам.
- Обрабатывает последние запросы.

### `db_handler.py`
- Выполняет SQL-запросы к MySQL (поиск по названию, жанру, году и т. д.).
- Сохраняет поисковые запросы в MongoDB.

### `db_connection.py`
- Устанавливает соединение с MySQL.
- Загружает параметры из `db_configs_manager.py`.

### `db_configs_manager.py`
- Загружает параметры окружения из `.env`.
- Определяет конфигурацию MySQL.

## Дополнительная информация
- База данных Sakila должна быть предварительно загружена в MySQL.
- База данных для хранения истории запросов и последних поисков 160924_panas_search_film должна быть предварительно создана:
```
CREATE database 160924_panas_search_film;

-- Таблица для Популярных запросов пользователей по фильму
CREATE TABLE 160924_panas_search_film.search_criteria_film (
    id INT PRIMARY KEY AUTO_INCREMENT comment "Уникальный идентификатор",
	name_category VARCHAR(250) comment "Имя жанра(категории)",
    release_year numeric comment "Год релиза",
    category_by_words text comment "Критерий по словам",
    pquery text not null comment "Запрос", 
    cdate datetime not null default now() comment "Дата вставки"
) comment = "Таблица для популярных запросов пользователей по фильму";
```

## Автор
### Anatoli Panas [GitHub](https://github.com/AnatoliPanas/Python_project_search_films.git)

Проект разработан в образовательных целях.

