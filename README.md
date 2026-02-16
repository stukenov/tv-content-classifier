# TV Content Classifier

An AI-powered system for automatically classifying television programs according to EBU (European Broadcasting Union) standards using GPT-4. Specialized for Kazakhstan TV content with support for Kazakh language programs.

## Features

- **EBU Standard Classification**: Automatically categorizes TV programs using European Broadcasting Union standards
- **AI-Powered Analysis**: Uses GPT-4o-mini for accurate and cost-effective classification
- **Multi-language Support**: Handles Kazakh, Russian, English, and Turkish content
- **Smart Caching**: Avoids duplicate API calls with intelligent result caching
- **Excel Integration**: Reads from and writes to Excel files with detailed classification data
- **Kazakh Language Support**: Properly handles Kazakh characters (ә, ғ, қ, ң, ө, ұ, ү, һ, і)
- **Automatic Slug Generation**: Creates URL-friendly slugs for program names
- **Batch Processing**: Process multiple programs with automatic saving intervals
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## Classification Output

The system adds the following columns to your Excel file:

| Column | Description | Example |
|--------|-------------|---------|
| `EBU_Category` | Main EBU category | News and Current Affairs |
| `EBU_Subcategory` | EBU subcategory | Morning show |
| `Program_Type` | Program type | entertainment |
| `Language` | Program language | kz |
| `Original_Title` | Title with correct characters | Таңшолпан |
| `Slug` | Latin URL-friendly version | tansholpan |
| `Genre` | Program genre | Morning program |
| `Description` | Brief description (English) | Morning informational program |
| `Country_Origin` | Production country | Kazakhstan |
| `Accessibility` | Accessibility features | sign_language |
| `Classification_Confidence` | Confidence level | high |

## EBU Categories

- **News and Current Affairs** - News and current events
- **Education** - Educational programs
- **Arts and Culture** - Arts and cultural programs
- **Religion** - Religious content
- **Fiction/Entertainment** - Entertainment programs
- **Sports** - Sports content
- **Children and Youth** - Children's and youth programs
- **Documentary** - Documentary programs
- **Music** - Music programs
- **Service** - Service programs (logos, anthem, technical)
- **Other** - Uncategorized content

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Install Dependencies

1. Clone the repository:
```bash
git clone https://github.com/stukenov/tv-content-classifier.git
cd tv-content-classifier
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Quick Start (Demo Mode)

Run the demo without an API key to see how it works:
```bash
python demo_classifier.py
```

### Real Classification

```bash
python zero-shot-class.py
```

The script will:
1. Load your Excel file (`filtered_data.xlsx`)
2. Extract unique program names
3. Check cache for previously classified programs
4. Send remaining programs to GPT-4o-mini for classification
5. Save results every 10 programs (configurable)
6. Add classification columns to your Excel file

### Configuration Options

Edit the script to configure:
```python
classifier.process_classifications(
    max_items=50,      # Number of programs to process
    save_interval=10   # Save every N items
)
```

## Cost Estimation

**Using GPT-4o-mini (optimized model):**
- ~$0.0003 per program (10x cheaper than GPT-4o)
- For 50 programs: ~$0.015
- For all 212 programs: ~$0.064

## Kazakhstan TV Specifics

The system is adapted for:
- ✅ Kazakh programs with correct letters `ә, ғ, қ, ң, ө, ұ, ү, һ, і`
- ✅ Russian subtitles `рус/тит` → `subtitles`
- ✅ Sign language `сурдоперевод` → `sign_language`
- ✅ TV series `т/сериал` → `series`
- ✅ Turkish content
- ✅ Service programs (anthem, logos, weather)

## Example Results

**Inter-program fillers:**
- Category: `Service`
- Type: `service`
- Slug: `mezhprogrammnye_zastavki`
- Description: `Technical fillers between programs`

**Таңшолпан (Tansholpan):**
- Category: `News and Current Affairs`
- Type: `entertainment`
- Slug: `tansholpan`
- Description: `Morning informational and entertainment program`

**Ауа райы (Weather):**
- Category: `Service`
- Type: `informational`
- Slug: `aua_raiy`
- Description: `Weather forecast program in Kazakh language`

## Project Structure

```
tv-content-classifier/
├── demo_classifier.py       # Demo version (no API key required)
├── zero-shot-class.py      # Main classification script
├── gen.py                  # Synthetic data generator
├── prepare_dataset.py      # Dataset preparation
├── test_data_structure.py  # Data structure analyzer
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── filtered_data.xlsx      # Input data file
└── filtered_data_demo.xlsx # Demo data file
```

## Troubleshooting

### API Key Error
```
ERROR - OPENAI_API_KEY not found in environment variables
```
**Solution:** Set the environment variable with your API key

### Rate Limit Exceeded
```
ERROR - Rate limit exceeded
```
**Solution:** Increase delays between requests in the code

### Duplicate Programs
The system automatically normalizes titles and eliminates duplicates

## Algorithm

1. **Load data** from Excel file
2. **Normalize titles** to eliminate duplicates
3. **Select unique programs** for classification
4. **Check cache** to avoid repeat API calls
5. **Send request** to GPT-4o API for classification
6. **Parse JSON response** in English
7. **Add SLUG** and other fields
8. **Auto-save** every 10 items

## License

MIT License - see [LICENSE](LICENSE) file for details

Copyright (c) 2025 Saken Tukenov

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- OpenAI GPT-4 for intelligent classification
- EBU (European Broadcasting Union) for classification standards
