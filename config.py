# Конфигурация системы классификации телепрограмм

# Файлы
EXCEL_FILE = 'filtered_data.xlsx'
CACHE_FILE = 'classification_cache.json'
LOG_FILE = 'tv_classification.log'

# Параметры обработки
MAX_ITEMS = 50  # Максимальное количество программ для обработки
SAVE_INTERVAL = 10  # Интервал сохранения (каждые N элементов)
MIN_FREQUENCY = 2  # Минимальная частота для популярных программ
REQUEST_DELAY = 1  # Пауза между запросами в секундах

# Настройки OpenAI
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_MAX_TOKENS = 500
OPENAI_TEMPERATURE = 0.3

# Столбцы для результатов классификации
RESULT_COLUMNS = [
    'EBU_Category',
    'EBU_Subcategory', 
    'Program_Type',
    'Language',
    'Original_Title',
    'Slug',
    'Genre',
    'Description',
    'Country_Origin',
    'Accessibility',
    'Classification_Confidence'
]

# Категории EBU
EBU_CATEGORIES = [
    'News and Current Affairs',
    'Education',
    'Arts and Culture',
    'Religion',
    'Fiction/Entertainment',
    'Sports',
    'Children and Youth',
    'Documentary',
    'Music',
    'Service',
    'Other'
]

# Языки программ
LANGUAGES = [
    'kz', 'ru', 'tr', 'en', 'fr', 'de', 'it', 'es', 'other'
]

# Типы программ
PROGRAM_TYPES = [
    'series',
    'movie', 
    'documentary',
    'news',
    'entertainment',
    'sports',
    'children',
    'educational',
    'musical',
    'informational',
    'service',
    'other'
]

# Уровни уверенности
CONFIDENCE_LEVELS = ['high', 'medium', 'low']

# Настройки логирования
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO' 