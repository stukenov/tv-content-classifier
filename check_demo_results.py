import pandas as pd

# Загрузка демо результатов
try:
    df = pd.read_excel('filtered_data_demo.xlsx')
    
    print("📊 СТОЛБЦЫ В ДЕМО ФАЙЛЕ:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n📈 СТАТИСТИКА:")
    print(f"   Всего записей: {len(df)}")
    print(f"   Записей с классификацией: {df['EBU_Category'].notna().sum()}")
    
    # Проверка наличия SLUG поля
    if 'Slug' in df.columns:
        print(f"\n✅ SLUG поле найдено!")
        filled_slugs = df['Slug'].notna().sum()
        print(f"   Заполненных SLUG: {filled_slugs}")
        
        # Показать примеры SLUG
        slug_examples = df[df['Slug'].notna()][['Title', 'Original_Title', 'Slug']].head(3)
        print(f"\n📝 ПРИМЕРЫ SLUG:")
        for _, row in slug_examples.iterrows():
            print(f"   {row['Title']} → {row['Slug']}")
    else:
        print(f"\n❌ SLUG поле НЕ найдено!")
    
    # Показать пример классифицированной записи
    classified = df[df['EBU_Category'].notna()]
    if len(classified) > 0:
        print(f"\n🎯 ПРИМЕР ПОЛНОЙ КЛАССИФИКАЦИИ:")
        example = classified.iloc[0]
        print(f"   Title: {example['Title']}")
        if pd.notna(example.get('Original_Title')):
            print(f"   Original_Title: {example['Original_Title']}")
        if pd.notna(example.get('Slug')):
            print(f"   Slug: {example['Slug']}")
        if pd.notna(example.get('EBU_Category')):
            print(f"   Category: {example['EBU_Category']}")
        if pd.notna(example.get('Program_Type')):
            print(f"   Type: {example['Program_Type']}")
        if pd.notna(example.get('Language')):
            print(f"   Language: {example['Language']}")
        if pd.notna(example.get('Description')):
            print(f"   Description: {example['Description']}")
        if pd.notna(example.get('Accessibility')):
            print(f"   Accessibility: {example['Accessibility']}")
    
    print(f"\n🎉 Проверка завершена!")
    
except Exception as e:
    print(f"❌ Ошибка загрузки файла: {e}") 