import pandas as pd
import logging
from collections import Counter

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_excel_structure(excel_file='filtered_data.xlsx'):
    """Анализ структуры Excel файла"""
    try:
        # Загрузка данных
        df = pd.read_excel(excel_file)
        
        print(f"\n{'='*60}")
        print(f"АНАЛИЗ ФАЙЛА: {excel_file}")
        print(f"{'='*60}")
        
        # Основная информация
        print(f"\n📊 ОСНОВНАЯ ИНФОРМАЦИЯ:")
        print(f"   Количество строк: {len(df)}")
        print(f"   Количество столбцов: {len(df.columns)}")
        
        # Список столбцов
        print(f"\n📋 СТОЛБЦЫ В ФАЙЛЕ:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        # Проверка наличия столбца Title
        if 'Title' in df.columns:
            print(f"\n✅ Столбец 'Title' найден!")
            
            # Анализ столбца Title
            title_series = df['Title'].dropna()
            print(f"   Всего названий (без пустых): {len(title_series)}")
            print(f"   Уникальных названий: {title_series.nunique()}")
            
            # Частота названий
            title_counts = Counter(title_series)
            
            print(f"\n📈 ТОП-10 САМЫХ ПОПУЛЯРНЫХ НАЗВАНИЙ:")
            for title, count in title_counts.most_common(10):
                print(f"   {count:4d}x - {title}")
            
            print(f"\n📝 ПРИМЕРЫ УНИКАЛЬНЫХ НАЗВАНИЙ:")
            unique_titles = [title for title, count in title_counts.items() if count == 1]
            for i, title in enumerate(unique_titles[:10], 1):
                print(f"   {i:2d}. {title}")
            
            # Статистика по частоте
            frequency_stats = Counter(title_counts.values())
            print(f"\n📊 СТАТИСТИКА ПО ЧАСТОТЕ:")
            print(f"   Программы с 1 показом: {frequency_stats[1]}")
            print(f"   Программы с 2-5 показами: {sum(frequency_stats[i] for i in range(2, 6) if i in frequency_stats)}")
            print(f"   Программы с 6+ показами: {sum(frequency_stats[i] for i in frequency_stats if i >= 6)}")
            
        else:
            print(f"\n❌ Столбец 'Title' НЕ найден!")
            print(f"   Доступные столбцы: {list(df.columns)}")
        
        # Первые несколько строк
        print(f"\n🔍 ПЕРВЫЕ 5 СТРОК ДАННЫХ:")
        print(df.head().to_string())
        
        # Информация о типах данных
        print(f"\n📋 ТИПЫ ДАННЫХ:")
        for col in df.columns:
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            print(f"   {col:20s} | {str(dtype):15s} | Пустых: {null_count}")
        
        return df
        
    except FileNotFoundError:
        print(f"\n❌ ОШИБКА: Файл '{excel_file}' не найден!")
        print(f"   Убедитесь, что файл находится в текущей директории.")
        return None
    except Exception as e:
        print(f"\n❌ ОШИБКА при загрузке файла: {e}")
        return None

if __name__ == "__main__":
    df = analyze_excel_structure()
    
    if df is not None:
        print(f"\n✅ Анализ завершен успешно!")
        print(f"   Файл готов для обработки системой классификации.")
    else:
        print(f"\n❌ Не удалось проанализировать файл.")
        print(f"   Проверьте наличие и формат файла 'filtered_data.xlsx'.") 