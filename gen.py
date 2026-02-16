import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)  # Для воспроизводимости

channels = [
    {"id": "31KZ", "name": "31 канал"},
    {"id": "KTK", "name": "KTK"},
    {"id": "Qazaqstan", "name": "Qazaqstan"},
    {"id": "NTK", "name": "NTK"}
]
audience = 'ALL4+'

program_schedule = [
    {"title": "Утро",        "start": "06:00", "end": "09:00", "base_rating": 2.1, "var": 0.4},
    {"title": "Детская",     "start": "09:00", "end": "12:00", "base_rating": 1.3, "var": 0.3},
    {"title": "Фильм",       "start": "12:00", "end": "14:00", "base_rating": 2.0, "var": 0.5},
    {"title": "Ток-шоу",     "start": "14:00", "end": "17:00", "base_rating": 2.3, "var": 0.5},
    {"title": "Сериал",      "start": "17:00", "end": "20:00", "base_rating": 3.0, "var": 0.7},
    {"title": "Новости",     "start": "20:00", "end": "20:30", "base_rating": 6.5, "var": 1.0},
    {"title": "Прайм-тайм",  "start": "20:30", "end": "23:00", "base_rating": 7.5, "var": 1.1},
    {"title": "Поздний фильм","start": "23:00", "end": "01:00", "base_rating": 2.4, "var": 0.8},
    {"title": "Ночной эфир", "start": "01:00", "end": "06:00", "base_rating": 0.7, "var": 0.2},
]

def time_to_minutes(t):
    h, m = map(int, t.split(':'))
    return h * 60 + m

def get_program_for_minute(minute):
    for prog in program_schedule:
        start = time_to_minutes(prog['start'])
        end = time_to_minutes(prog['end'])
        # обрабатываем ночь (01:00-06:00)
        if start > end:
            if minute >= start or minute < end:
                return prog
        else:
            if start <= minute < end:
                return prog
    return program_schedule[-1]  # ночной эфир

def generate_minute_data(date, channel_id):
    rows = []
    for minute in range(0, 24 * 60):
        prog = get_program_for_minute(minute)
        cur_time = (datetime.combine(date, datetime.min.time()) + timedelta(minutes=minute)).strftime('%Y-%m-%dT%H:%M:%S')
        base = prog['base_rating']
        fluct = np.random.normal(0, prog['var'])
        rating = max(0.15, round(base + fluct, 2))
        share = round(rating * np.random.uniform(1.8, 2.7), 1)
        rows.append([channel_id, cur_time, audience, rating, share])
    return pd.DataFrame(rows, columns=['channel_id', 'time', 'audience', 'rating', 'share'])

def generate_program_summary(minute_df, date, channel_id):
    result = []
    for prog in program_schedule:
        start_min = time_to_minutes(prog['start'])
        end_min = time_to_minutes(prog['end'])
        if start_min > end_min:
            mask = ((minute_df['minute'] >= start_min) | (minute_df['minute'] < end_min))
        else:
            mask = ((minute_df['minute'] >= start_min) & (minute_df['minute'] < end_min))
        segment = minute_df[mask]
        if not segment.empty:
            avg_rating = round(segment['rating'].mean(), 1)
            peak_rating = round(segment['rating'].max(), 1)
            result.append([channel_id, date.strftime('%Y-%m-%d'), prog['title'], avg_rating, peak_rating])
    return result

def generate_daily_summary(minute_df, date, channel_id):
    avg_rating = round(minute_df['rating'].mean(), 1)
    share = round(minute_df['share'].mean(), 1)
    # Всегда только ALL4+
    reach1 = int(np.clip(np.random.normal(400000 + avg_rating * 40000, 25000), 200000, 1200000))
    return [channel_id, date.strftime('%Y-%m-%d'), audience, avg_rating, share, reach1]

def main_generate_files():
    start_date = datetime(2025, 5, 8)
    n_days = 7

    program_rows = []
    daily_rows = []

    for channel in channels:
        channel_id = channel["id"]
        for i in range(n_days):
            date = start_date - timedelta(days=i)
            minute_df = generate_minute_data(date, channel_id)
            minute_df['minute'] = pd.to_datetime(minute_df['time']).dt.hour * 60 + pd.to_datetime(minute_df['time']).dt.minute
            filename = f"minute_{date.strftime('%Y%m%d')}_{channel_id}.csv"
            minute_df.drop(columns=['minute']).to_csv(filename, sep=';', index=False)
            program_rows.extend(generate_program_summary(minute_df, date, channel_id))
            daily_rows.append(generate_daily_summary(minute_df, date, channel_id))

    df_program = pd.DataFrame(program_rows, columns=['channel_id', 'date', 'program_title', 'avg_rating', 'peak_rating'])
    df_program.to_csv('program_last7days.csv', sep=';', index=False)

    df_daily = pd.DataFrame(daily_rows, columns=['channel_id', 'date', 'audience', 'avg_rating', 'share', 'reach1'])
    df_daily.to_csv('daily_last7days.csv', sep=';', index=False)

    print("Все файлы сгенерированы!")

# Запуск генератора
main_generate_files()
