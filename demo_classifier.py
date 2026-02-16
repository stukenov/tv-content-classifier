import pandas as pd
import json
import logging
import os
import time
from datetime import datetime
from collections import Counter
import hashlib
from typing import Dict, List, Optional
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tv_classification_demo.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DemoTVProgramClassifier:
    """Демонстрационная версия классификатора без реального API"""
    
    def __init__(self, excel_file: str = 'filtered_data.xlsx'):
        self.excel_file = excel_file
        self.cache_file = 'classification_cache_demo.json'
        self.cache = self.load_cache()
        self.results_added = 0
        
        # Демонстрационные результаты классификации
        self.demo_responses = {
            "ауа райы": {
                "original_title": "Ауа райы",
                "slug": "aua_raiy",
                "language": "kz",
                "category": "Service",
                "subcategory": "Weather forecast",
                "genre": "Informational",
                "type": "informational",
                "description": "Weather forecast program in Kazakh language",
                "country_origin": "Kazakhstan",
                "accessibility": "regular",
                "confidence": "high"
            },
            "гимн": {
                "original_title": "Гимн Республики Казахстан",
                "slug": "gimn_respubliki_qazaqstan",
                "language": "kz",
                "category": "Service",
                "subcategory": "National symbols",
                "genre": "Official",
                "type": "musical",
                "description": "National anthem of the Republic of Kazakhstan",
                "country_origin": "Kazakhstan",
                "accessibility": "regular",
                "confidence": "high"
            },
            "межпрограммные заставки": {
                "original_title": "Межпрограммные заставки",
                "slug": "mezhprogrammnye_zastavki",
                "language": "other",
                "category": "Service",
                "subcategory": "Technical content",
                "genre": "Technical",
                "type": "service",
                "description": "Technical fillers between programs",
                "country_origin": "Kazakhstan",
                "accessibility": "regular",
                "confidence": "high"
            },
            "qazaqstan. aqparat": {
                "original_title": "Qazaqstan. Aqparat",
                "slug": "qazaqstan_aqparat",
                "language": "kz",
                "category": "News and Current Affairs",
                "subcategory": "News",
                "genre": "News",
                "type": "news",
                "description": "Kazakhstani news program in Kazakh language with sign language interpretation",
                "country_origin": "Kazakhstan",
                "accessibility": "sign_language",
                "confidence": "high"
            },
            "кызым": {
                "original_title": "Кyzym",
                "slug": "kyzym",
                "language": "tr",
                "category": "Fiction/Entertainment",
                "subcategory": "Drama series",
                "genre": "Drama",
                "type": "series",
                "description": "Turkish drama series with Russian subtitles",
                "country_origin": "Turkey",
                "accessibility": "subtitles",
                "confidence": "high"
            },
            "tansholpan": {
                "original_title": "Таңшолпан",
                "slug": "tansholpan",
                "language": "kz",
                "category": "News and Current Affairs",
                "subcategory": "Morning show",
                "genre": "Morning program",
                "type": "entertainment",
                "description": "Morning informational and entertainment program in Kazakh language",
                "country_origin": "Kazakhstan",
                "accessibility": "regular",
                "confidence": "high"
            }
        }
        
        logger.info("Инициализация DemoTVProgramClassifier завершена")
    
    def load_cache(self) -> Dict:
        """Загрузка кэша классификаций"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                logger.info(f"Загружен демо-кэш с {len(cache)} записями")
                return cache
            except Exception as e:
                logger.error(f"Ошибка загрузки кэша: {e}")
        return {}
    
    def save_cache(self):
        """Сохранение кэша классификаций"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            logger.info(f"Демо-кэш сохранен ({len(self.cache)} записей)")
        except Exception as e:
            logger.error(f"Ошибка сохранения кэша: {e}")
    
    def get_title_hash(self, title: str) -> str:
        """Создание хэша для названия программы"""
        return hashlib.md5(title.lower().strip().encode('utf-8')).hexdigest()
    
    def parse_json_response(self, response_text: str) -> Optional[Dict]:
        """
        Парсинг JSON ответа, который может быть обернут в markdown блоки
        
        Args:
            response_text: Текст ответа от ChatGPT
            
        Returns:
            Словарь с результатами или None при ошибке
        """
        import re
        
        # Удаление markdown блоков если они есть
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1).strip()
        else:
            json_text = response_text.strip()
        
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.error(f"Демо: Ошибка парсинга JSON: {e}")
            return None
    
    def normalize_title(self, title: str) -> str:
        """Нормализация названия для избежания дублирования"""
        if pd.isna(title):
            return ""
        
        # Приведение к нижнему регистру и удаление лишних пробелов
        normalized = str(title).lower().strip()
        
        # Удаление множественных пробелов
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Удаление специальных символов в начале и конце
        normalized = re.sub(r'^[^\w\u0400-\u04FF]+|[^\w\u0400-\u04FF]+$', '', normalized)
        
        return normalized
    
    def load_data(self) -> pd.DataFrame:
        """Загрузка данных из Excel файла"""
        try:
            df = pd.read_excel(self.excel_file)
            logger.info(f"Загружено {len(df)} записей из {self.excel_file}")
            logger.info(f"Столбцы в файле: {list(df.columns)}")
            return df
        except Exception as e:
            logger.error(f"Ошибка загрузки файла {self.excel_file}: {e}")
            raise
    
    def analyze_titles(self, df: pd.DataFrame, top_unique: int = 10, min_frequency: int = 2) -> List[str]:
        """Анализ и выбор названий для демонстрации"""
        if 'Title' not in df.columns:
            logger.error("Столбец 'Title' не найден в данных")
            raise ValueError("Столбец 'Title' не найден")
        
        # Создание нормализованного столбца для группировки
        df['Title_Normalized'] = df['Title'].apply(self.normalize_title)
        
        # Подсчет частоты нормализованных названий
        title_counts = Counter(df['Title_Normalized'].dropna())
        logger.info(f"Найдено {len(title_counts)} уникальных названий программ (после нормализации)")
        
        # Создание словаря: нормализованное название -> оригинальное название
        title_mapping = {}
        for _, row in df.iterrows():
            normalized = row['Title_Normalized']
            original = row['Title']
            if pd.notna(normalized) and pd.notna(original):
                if normalized not in title_mapping:
                    title_mapping[normalized] = original
        
        # Выбираем программы для демонстрации на основе нормализованных названий
        demo_titles = []
        for norm_title in title_mapping:
            for demo_key in self.demo_responses.keys():
                if demo_key in norm_title:
                    demo_titles.append(title_mapping[norm_title])
                    break
        
        # Ограничиваем количество для демонстрации
        selected_titles = demo_titles[:top_unique]
        
        logger.info(f"Выбрано {len(selected_titles)} названий для демонстрации:")
        for title in selected_titles:
            logger.info(f"  - {title}")
        
        return selected_titles
    
    def classify_with_demo(self, title: str) -> Optional[Dict]:
        """Демонстрационная классификация программы"""
        title_hash = self.get_title_hash(title)
        
        # Проверка кэша
        if title_hash in self.cache:
            logger.info(f"Найдено в кэше: {title}")
            return self.cache[title_hash]
        
        logger.info(f"🔍 ДЕМО: Анализ программы '{title}'")
        
        # Поиск подходящего демо-ответа
        title_lower = title.lower().strip()
        demo_result = None
        
        for demo_key, demo_response in self.demo_responses.items():
            if demo_key in title_lower:
                demo_result = demo_response.copy()
                break
        
        if not demo_result:
            # Общий демо-ответ для неизвестных программ
            demo_result = {
                "original_title": title,
                "language": "kz",
                "category": "Other",
                "subcategory": "Unknown",
                "genre": "Неопределенный",
                "type": "другой",
                "description": "Программа требует дополнительного анализа",
                "country_origin": "Казахстан",
                "accessibility": "обычный показ",
                "confidence": "low"
            }
        
        # Имитация задержки API
        time.sleep(0.5)
        
        # Добавление метаданных
        demo_result['title'] = title
        demo_result['timestamp'] = datetime.now().isoformat()
        demo_result['demo_mode'] = True
        
        # Сохранение в кэш
        self.cache[title_hash] = demo_result
        
        logger.info(f"✅ ДЕМО: Классификация завершена для '{title}'")
        logger.info(f"   Категория: {demo_result['category']}")
        logger.info(f"   Тип: {demo_result['type']}")
        logger.info(f"   Язык: {demo_result['language']}")
        logger.info(f"   Страна: {demo_result['country_origin']}")
        logger.info(f"   Доступность: {demo_result['accessibility']}")
        
        return demo_result
    
    def add_results_to_excel(self, df: pd.DataFrame, classifications: List[Dict]) -> pd.DataFrame:
        """Добавление результатов в DataFrame"""
        class_dict = {cls['title']: cls for cls in classifications if cls is not None}
        
        new_columns = ['EBU_Category', 'EBU_Subcategory', 'Program_Type', 'Language', 
                      'Original_Title', 'Slug', 'Genre', 'Description', 'Country_Origin', 
                      'Accessibility', 'Classification_Confidence', 'Demo_Mode']
        
        for col in new_columns:
            if col not in df.columns:
                df[col] = ''
        
        for idx, row in df.iterrows():
            title = row['Title']
            if pd.notna(title) and title in class_dict:
                classification = class_dict[title]
                df.at[idx, 'EBU_Category'] = classification.get('category', '')
                df.at[idx, 'EBU_Subcategory'] = classification.get('subcategory', '')
                df.at[idx, 'Program_Type'] = classification.get('type', '')
                df.at[idx, 'Language'] = classification.get('language', '')
                df.at[idx, 'Original_Title'] = classification.get('original_title', '')
                df.at[idx, 'Slug'] = classification.get('slug', '')
                df.at[idx, 'Genre'] = classification.get('genre', '')
                df.at[idx, 'Description'] = classification.get('description', '')
                df.at[idx, 'Country_Origin'] = classification.get('country_origin', '')
                df.at[idx, 'Accessibility'] = classification.get('accessibility', '')
                df.at[idx, 'Classification_Confidence'] = classification.get('confidence', '')
                df.at[idx, 'Demo_Mode'] = 'True' if classification.get('demo_mode') else 'False'
        
        return df
    
    def save_excel(self, df: pd.DataFrame, demo_suffix: str = "_demo"):
        """Сохранение DataFrame в демо-файл"""
        try:
            demo_filename = self.excel_file.replace('.xlsx', f'{demo_suffix}.xlsx')
            df.to_excel(demo_filename, index=False)
            logger.info(f"🎯 ДЕМО: Результаты сохранены в {demo_filename}")
            return demo_filename
        except Exception as e:
            logger.error(f"Ошибка сохранения демо-файла: {e}")
    
    def process_demo_classifications(self, max_items: int = 10):
        """Демонстрационный процесс классификации"""
        logger.info("🚀 ДЕМО: Начало демонстрационной классификации")
        logger.info("=" * 60)
        
        # Загрузка данных
        df = self.load_data()
        
        # Анализ и выбор названий
        selected_titles = self.analyze_titles(df, top_unique=max_items)
        
        if not selected_titles:
            logger.warning("Не найдено программ для демонстрации")
            return
        
        # Классификация программ
        classifications = []
        
        for i, title in enumerate(selected_titles, 1):
            logger.info(f"\n📺 Обработка {i}/{len(selected_titles)}: {title}")
            logger.info("-" * 50)
            
            classification = self.classify_with_demo(title)
            if classification:
                classifications.append(classification)
                self.results_added += 1
        
        # Сохранение результатов
        logger.info(f"\n💾 ДЕМО: Сохранение результатов")
        df_final = self.add_results_to_excel(df, classifications)
        demo_file = self.save_excel(df_final)
        self.save_cache()
        
        # Статистика
        logger.info(f"\n📊 ДЕМО: Статистика завершения")
        logger.info("=" * 60)
        logger.info(f"✅ Обработано программ: {len(classifications)}")
        logger.info(f"📁 Результаты сохранены в: {demo_file}")
        logger.info(f"💾 Кэш сохранен в: {self.cache_file}")
        
        # Показать примеры результатов
        if classifications:
            logger.info(f"\n🎯 ПРИМЕРЫ КЛАССИФИКАЦИИ:")
            for cls in classifications[:3]:
                logger.info(f"  📺 {cls['title']}")
                logger.info(f"      Категория: {cls['category']}")
                logger.info(f"      Тип: {cls['type']}")
                logger.info(f"      Язык: {cls['language']}")
                logger.info(f"      Описание: {cls['description']}")
                logger.info("")

def main():
    """Демонстрационная функция"""
    print("🎭 ДЕМОНСТРАЦИОННЫЙ РЕЖИМ - TV Program Classifier")
    print("=" * 60)
    print("Это демонстрация работы системы классификации без реального API ключа OpenAI")
    print("Система проанализирует несколько популярных программ и покажет результаты")
    print("=" * 60)
    
    try:
        # Создание демо-классификатора
        classifier = DemoTVProgramClassifier()
        
        # Запуск демонстрации
        classifier.process_demo_classifications(max_items=6)
        
        print("\n🎉 Демонстрация завершена!")
        print("📁 Проверьте файл filtered_data_demo.xlsx с результатами")
        print("📄 Логи сохранены в tv_classification_demo.log")
        
    except Exception as e:
        logger.error(f"Ошибка в демонстрации: {e}")

if __name__ == "__main__":
    main() 