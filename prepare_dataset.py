import pandas as pd

# 1. Загрузка и фильтрация сразу по TVCompany
xlsx_file = "ttv01122023-18052025.xlsx"
df = pd.read_excel(xlsx_file)

# 2. Фильтрация только для телеканала QAZAQSTAN
df = df[df["TVCompany"] == "QAZAQSTAN"]

import pandas as pd
from datetime import timedelta

def normalize_start_time(val):
    # Преобразуем timedelta в строку
    val = str(val)
    # Удаляем "1 day, " или другие префиксы вида "X day(s), "
    val = val.replace("1 day, ", "").replace("2 days, ", "").strip()
    return val

# Применим ко всей колонке Start time
df["Start time cleaned"] = df["Start time"].apply(normalize_start_time)

# Теперь создаём datetime с учётом теледня
def parse_datetime(row):
    base_date = pd.to_datetime(row["Date"])
    try:
        hours, minutes, seconds = map(int, row["Start time cleaned"].split(":"))
        dt = base_date + timedelta(hours=hours, minutes=minutes, seconds=seconds)
        if hours < 5:  # если раньше 05:00, значит это следующий календарный день
            dt += timedelta(days=1)
        return dt
    except:
        return pd.NaT

df["start_dt"] = df.apply(parse_datetime, axis=1)


import re

def detect_program_type(df, column_name):
    rules = {
        'serial': [
            r'\bт[\s\-/.]*с(ериал)?\b'
        ],
        'movie': [
            r'\bх[\s\-/.]*ф\b',
            r'\bхудожественный фильм\b'
        ],
        'documentary': [
            r'\bд[\s\-/.]*ф\b',
            r'\bдок[\s\-/.]*с(ериал)?\b',
            r'\bдокументальный\b'
        ],
        'cartoon': [
            r'\bм[\s\-/.]*ф\b',
            r'\bм[\s\-/.]*с(ериал)?\b',
            r'\bмультфильм\b'
        ],
        'shortfilm': [
            r'\bк[\s\-/.]*ф\b',
            r'\bкороткометраж\w*\b'
        ],
        'concert': [
            r'\bконцерт\b',
            r'\bмузыкальная программа\b'
        ],
        'news': [
            r'\bақпарат\b',
            r'\bqazaqstan\.?\s*aqparat\b',
            r'\bновости\b',
            r'\bжаңалықтар\b'
        ],
        'other': [
            r'\bгимн\b'
        ]
    }

    def classify(text):
        lowered = text.lower()
        for label, patterns in rules.items():
            for pattern in patterns:
                if re.search(pattern, lowered, flags=re.IGNORECASE):
                    return label
        return 'program'

    df['program_type'] = df[column_name].astype(str).apply(classify)
    return df

df = detect_program_type(df, 'Title')

def extract_country_code(df, column_name='Title'):
    import re

    # Словарь: название страны → код
    country_map = {
        'россия': 'RU',
        'рф': 'RU',
        'сша': 'US',
        'казахстан': 'KZ',
        'турция': 'TR',
    }

    # Функция обработки строки — только определяет
    def detect_country(text):
        lowered = text.lower()
        found = [code for name, code in country_map.items() if name in lowered]
        return found[-1] if found else 'KZ'  # По умолчанию KZ

    # Применяем
    df['country'] = df[column_name].astype(str).apply(detect_country)
    return df

df = extract_country_code(df)


df = df[["start_dt", "Title", "program_type", "country", "Rtg(000)" ]]

import pandas as pd

def round_time_to_10_minutes(df, column_name='start_dt'):
    def round_to_10_minutes(dt):
        # Округляем к ближайшим 10 минутам
        discard = pd.Timedelta(minutes=dt.minute % 10, seconds=dt.second)
        rounded = dt - discard
        if discard >= pd.Timedelta(minutes=5):
            rounded += pd.Timedelta(minutes=10)
        return rounded.replace(second=0, microsecond=0)

    df[column_name + '_rounded'] = df[column_name].apply(round_to_10_minutes)
    return df
df['start_dt'] = pd.to_datetime(df['start_dt'])  # если ещё не datetime
df = round_time_to_10_minutes(df)


def remove_duplicates_by_time(df, time_column='start_dt'):
    # Округляем до ближайших 10 минут
    def round_to_10_minutes(dt):
        discard = pd.Timedelta(minutes=dt.minute % 10, seconds=dt.second)
        rounded = dt - discard
        if discard >= pd.Timedelta(minutes=5):
            rounded += pd.Timedelta(minutes=10)
        return rounded.replace(second=0, microsecond=0)

    # Добавляем вспомогательный столбец с округлением
    df['_rounded_time'] = df[time_column].apply(round_to_10_minutes)

    # Удаляем дубликаты по округлённому времени, оставляя первый
    df = df.drop_duplicates(subset='_rounded_time', keep='first')

    # Удаляем вспомогательный столбец
    df = df.drop(columns=['_rounded_time'])

    return df
df = df.drop_duplicates(subset='start_dt_rounded', keep='first')


import pandas as pd

# ⏱️ Приведение даты к datetime (если ещё не сделано)
df["start_dt"] = pd.to_datetime(df["start_dt"])

# 🧼 Удаление слишком коротких передач (<5 минут), если ещё не сделано
# df["duration_min"] = (df["end_dt"] - df["start_dt"]).dt.total_seconds() / 60
# df = df[df["duration_min"] > 5].copy()
# Убедись, что колонка уже datetime и округлена
df["start_dt_rounded"] = pd.to_datetime(df["start_dt_rounded"])

# Уникальные значения отсортированы
sorted_times = sorted(df["start_dt_rounded"].unique())

# Сопоставим каждой дате её порядковый номер (индекс)
time_map = {ts: i for i, ts in enumerate(sorted_times)}

# Применим это сопоставление
df["time_idx"] = df["start_dt_rounded"].map(time_map).astype(int)

# 🕒 Временные признаки
df["hour"]       = df["start_dt"].dt.hour.astype("int8")
df["weekday"]    = df["start_dt"].dt.weekday.astype("int8")
df["is_weekend"] = (df["weekday"] >= 5).astype("int8")
df["is_prime"]   = df["hour"].between(19, 23).astype("int8")  # прайм-тайм 19–23

# 🏷️ Категориальные признаки → категориальные коды
df["country_id"]      = df["country"].astype("category")
df["program_type_id"] = df["program_type"].astype("category")

# 🧪 Целевая переменная
TARGET = "Rtg(000)"

# 🔧 Группировка (убрали TVCompany — заменили на фиктивную группу)
df["series_id"] = 0  # фиксированная группа
GROUPS = ["series_id"]


df.to_excel("filtered_data.xlsx", index=False)