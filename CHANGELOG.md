# 📝 Changelog - TV Program Classification System

## Version 2.1 (2025-05-23)

### 🔧 **Technical Improvements**

#### 🚀 **Switched to GPT-4o-mini Model**
- Changed from GPT-4o to GPT-4o-mini for better cost efficiency
- Maintains high quality while reducing costs by 10x
- Updated configuration and documentation

#### 🛠️ **Enhanced JSON Parser**
- Added smart JSON parsing that handles markdown code blocks
- Fixes issue where ChatGPT returns JSON wrapped in ```json blocks
- More robust error handling and logging
- Works with both clean JSON and markdown-wrapped responses

#### 💰 **Updated Pricing**
- **v2.0 (GPT-4o)**: ~$0.64 for 212 programs
- **v2.1 (GPT-4o-mini)**: ~$0.064 for 212 programs (90% cost reduction!)
- Perfect balance of quality and affordability

### 🐛 **Bugs Fixed**
- **JSON Parsing Error**: Fixed "Expecting value: line 1 column 1" error
- **Markdown Blocks**: System now properly handles ```json code blocks
- **Response Processing**: More reliable parsing of ChatGPT responses

### 📁 **Files Updated**
- `zero-shot-class.py` - Added `parse_json_response()` method
- `demo_classifier.py` - Added JSON parsing consistency
- `config.py` - Updated to GPT-4o-mini model
- `README.md`, `SETUP_GUIDE.md`, `QUICK_START.md` - Updated pricing and features

---

## Version 2.0 (2025-05-23)

### ✨ Major Improvements

#### 🚀 **Upgraded to GPT-4o Model**
- Switched from GPT-3.5-turbo to GPT-4o for better accuracy
- Improved understanding of Kazakh TV program context
- Better handling of mixed-language content

#### 🌐 **All Responses in English**
- Updated prompts to request English-only responses
- Standardized field values (e.g., `сурдоперевод` → `sign_language`)
- Improved international compatibility

#### 🔗 **Added SLUG Field**
- New `Slug` column with Latin URL-friendly versions of titles
- Examples: `Таңшолпан` → `tansholpan`, `Ауа райы` → `aua_raiy`
- Perfect for web applications and URL generation

#### 🎯 **Eliminated Duplicates**
- Implemented smart title normalization
- Programs like `"Tansholpan (каз)"` and `"Tansholpan"` now treated as one
- Removes extra spaces, punctuation, and formatting differences
- Shows unique count after normalization in logs

#### 📝 **Proper Kazakh Letters**
- Enhanced prompt to use correct Kazakh alphabet: `ә, ғ, қ, ң, ө, ұ, ү, һ, і`
- Better representation of Kazakh program titles
- Improved cultural accuracy

### 🔧 Technical Improvements

#### **Enhanced Data Processing**
- Added `normalize_title()` method for consistent title handling
- Improved `analyze_titles()` to work with normalized data
- Better mapping between normalized and original titles

#### **Updated Configuration**
- Updated `config.py` with new GPT-4o settings
- Added SLUG to result columns
- Updated program types to English terms

#### **Improved Demo System**
- Updated demo responses to match new English format
- Added SLUG examples in demo data
- Better demonstration of capabilities

### 📊 **Updated Results Structure**

| Field | v1.0 | v2.0 |
|-------|------|------|
| Description | Russian | English |
| Genre | Russian | English |
| Type | `развлекательный` | `entertainment` |
| Accessibility | `сурдоперевод` | `sign_language` |
| **NEW** Slug | N/A | `tansholpan` |
| Country | `Казахстан` | `Kazakhstan` |

### 💰 **Cost Updates**
- **v1.0**: ~$0.106 for 212 programs (GPT-3.5-turbo)
- **v2.0**: ~$0.64 for 212 programs (GPT-4o)
- **Trade-off**: 6x cost increase for significantly better accuracy

### 🎯 **Demo Results Comparison**

#### v1.0 Demo Output:
```json
{
  "description": "Утренняя информационно-развлекательная программа",
  "type": "развлекательный",
  "accessibility": "обычный показ"
}
```

#### v2.0 Demo Output:
```json
{
  "description": "Morning informational and entertainment program",
  "slug": "tansholpan",
  "type": "entertainment", 
  "accessibility": "regular"
}
```

### 🐛 **Bugs Fixed**
- **Duplicate Processing**: No more processing same programs multiple times
- **Inconsistent Naming**: Normalized handling of title variations
- **Language Mixing**: All responses now consistently in English
- **Missing URLs**: SLUG field enables URL generation

### 📁 **Files Updated**
- `zero-shot-class.py` - Main classifier with all improvements
- `demo_classifier.py` - Updated demo with new format
- `config.py` - Updated configuration for v2.0
- `README.md` - Updated documentation with new features
- `SETUP_GUIDE.md` - Updated setup guide with v2.0 info

### 🚀 **Migration Guide**

#### From v1.0 to v2.0:
1. Clear old cache files to see new English responses
2. Update API key for GPT-4o access
3. Run demo to see new format: `python demo_classifier.py`
4. Check new SLUG field in Excel output
5. Verify normalized title processing in logs

---

## Version 1.0 (2025-05-23)

### 🎯 **Initial Release**
- Basic TV program classification using GPT-3.5-turbo
- Russian language responses
- EBU standard classification
- Caching system
- Incremental saving
- Demo system
- Excel integration

### ✅ **Features**
- Classification of Kazakhstani TV programs
- EBU category mapping
- Cache to avoid duplicate API calls
- Automatic backup creation
- Detailed logging
- Demo mode for testing

---

**📈 Next planned improvements:**
- [ ] Batch processing for better performance
- [ ] Web interface for easier use
- [ ] Advanced filtering options
- [ ] Export to multiple formats
- [ ] API endpoint for real-time classification 