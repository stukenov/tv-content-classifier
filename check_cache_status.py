import pandas as pd
import json
import os
import hashlib
from collections import Counter

def get_title_hash(title: str) -> str:
    """Создание хэша для названия программы"""
    return hashlib.md5(title.lower().strip().encode('utf-8')).hexdigest()

def normalize_title(title: str) -> str:
    """Нормализация названия для избежания дублирования"""
    if pd.isna(title):
        return ""
    
    import re
    
    # Приведение к нижнему регистру и удаление лишних пробелов
    normalized = str(title).lower().strip()
    
    # Удаление множественных пробелов
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Удаление специальных символов в начале и конце
    normalized = re.sub(r'^[^\w\u0400-\u04FF]+|[^\w\u0400-\u04FF]+$', '', normalized)
    
    return normalized

def main():
    print("🔍 ПРОВЕРКА СТАТУСА КЭША")
    print("=" * 50)
    
    # Загрузка кэша
    cache_file = 'classification_cache.json'
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        print(f"📁 Загружен кэш: {len(cache)} записей")
    else:
        print("❌ Файл кэша не найден")
        return
    
    # Загрузка Excel данных
    excel_file = 'filtered_data.xlsx'
    try:
        df = pd.read_excel(excel_file)
        print(f"📊 Загружен Excel: {len(df)} записей")
    except Exception as e:
        print(f"❌ Ошибка загрузки Excel: {e}")
        return
    
    # Анализ уникальных названий
    df['Title_Normalized'] = df['Title'].apply(normalize_title)
    title_counts = Counter(df['Title_Normalized'].dropna())
    
    # Создание словаря: нормализованное название -> оригинальное название
    title_mapping = {}
    for _, row in df.iterrows():
        normalized = row['Title_Normalized']
        original = row['Title']
        if pd.notna(normalized) and pd.notna(original):
            if normalized not in title_mapping:
                title_mapping[normalized] = original
    
    print(f"🎯 Уникальных программ (после нормализации): {len(title_mapping)}")
    
    # Проверка кэша для каждого названия
    cached_titles = []
    uncached_titles = []
    
    for norm_title, original_title in title_mapping.items():
        title_hash = get_title_hash(original_title)
        count = title_counts[norm_title]
        if title_hash in cache:
            cached_titles.append((norm_title, original_title, count))
        else:
            uncached_titles.append((norm_title, original_title, count))
    
    print(f"\n📈 СТАТИСТИКА:")
    print(f"✅ В кэше: {len(cached_titles)} программ")
    print(f"❌ НЕ в кэше: {len(uncached_titles)} программ")
    
    if cached_titles:
        print(f"\n✅ ТОП КЭШИРОВАННЫХ ПРОГРАММ:")
        cached_titles.sort(key=lambda x: x[2], reverse=True)
        for i, (norm_title, orig_title, count) in enumerate(cached_titles[:10], 1):
            print(f"  {i}. {orig_title} ({count} показов)")
    
    if uncached_titles:
        print(f"\n❌ ТОП НЕКЭШИРОВАННЫХ ПРОГРАММ:")
        uncached_titles.sort(key=lambda x: x[2], reverse=True)
        for i, (norm_title, orig_title, count) in enumerate(uncached_titles[:20], 1):
            print(f"  {i}. {orig_title} ({count} показов)")
        
        if len(uncached_titles) > 20:
            print(f"  ... и еще {len(uncached_titles) - 20} программ")
    
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    if not uncached_titles:
        print("⚠️  Все программы уже в кэше!")
        print("   Для повторной обработки удалите файл кэша:")
        print(f"   del {cache_file}")
    else:
        print(f"✅ Можно обработать {len(uncached_titles)} новых программ")
        print("   Запустите: python zero-shot-class.py")

if __name__ == "__main__":
    main() 