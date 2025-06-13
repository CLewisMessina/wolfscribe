# 🐺 Wolfstitch - AI Training Dataset Creator

**Transform Your Document Library into Production-Ready AI Training Datasets**  
*Scalable batch processing for LLM fine-tuning and training data preparation*

## 🎉 Recent Updates

### **v2.5.0 - Code Intelligence Update** (Current)
- ✅ **Complete Code Support**: Added extraction for 30+ programming languages
- ✅ **PowerPoint Integration**: Full .pptx/.ppt support with speaker notes
- ✅ **Smart Quality Control**: Auto-skip minified and auto-generated files  
- ✅ **Encoding Detection**: Automatic handling of international character sets
- ✅ **40+ Total Formats**: Most comprehensive format support available

---

## 🚀 Overview

Wolfstitch (formerly Wolfscribe) is a professional-grade desktop application that transforms document collections into optimized AI training datasets. Built for AI developers, researchers, and enterprises who need scalable, accurate dataset creation with complete cost transparency.

## ✨ Key Features

- **🎯 Batch Processing Pipeline**: Process hundreds of files simultaneously with intelligent queue management
- **📚 Comprehensive Format Support**: 40+ file formats including documents, presentations, spreadsheets, and source code
- **💻 Code Intelligence**: Automatic detection of minified/auto-generated files with quality control
- **🌍 International Support**: Automatic character encoding detection for global codebases
- **🧠 Smart Token-Aware Chunking**: Configurable token limits (1024-2048) with exact tokenization
- **💰 Advanced Cost Analysis**: 15+ training approaches with real-time pricing and ROI calculations
- **📊 LLM-Ready Output**: Export to JSONL with metadata, optimized for fine-tuning pipelines
- **🛡️ Error Isolation**: Individual file failures don't stop batch processing

---

## 📋 Supported File Formats

### **✅ Business Documents**
| Format | Status | Description | Key Features |
|--------|--------|-------------|--------------|
| **PDF** | ✅ Complete | Adobe PDF documents | Text extraction, multi-page support |
| **Word (.docx)** | ✅ Complete | Microsoft Word documents | Tables, formatting preservation |
| **Excel (.xlsx)** | ✅ Complete | Spreadsheets & data | Multi-sheet intelligent extraction |
| **PowerPoint (.pptx)** | ✅ Complete | Presentations | Slide text, speaker notes, tables |
| **Web/HTML** | ✅ Complete | Web pages & documentation | Content isolation, clean extraction |
| **Markdown** | ✅ Complete | Technical documentation | Syntax removal, clean formatting |
| **EPUB** | ✅ Complete | E-books | Chapter extraction, metadata |
| **Plain Text** | ✅ Complete | TXT files | Encoding detection, multi-format |

### **✅ Source Code & Configuration Files**
| Format | Status | Description | Key Features |
|--------|--------|-------------|--------------|
| **Python (.py)** | ✅ Complete | Python source code | Auto-encoding detection, minification check |
| **JavaScript (.js/.jsx)** | ✅ Complete | JS/React code | TypeScript support, quality control |
| **Java (.java)** | ✅ Complete | Java source code | Comment preservation, structure detection |
| **C/C++ (.c/.cpp/.h)** | ✅ Complete | C/C++ source & headers | Multiple extensions support |
| **Go (.go)** | ✅ Complete | Go source code | UTF-8 handling, import detection |
| **Rust (.rs)** | ✅ Complete | Rust source code | Cargo file support ready |
| **Config Files** | ✅ Complete | YAML, TOML | Structure preservation, comment handling |
| **30+ Languages** | ✅ Complete | Swift, Kotlin, Ruby, PHP, etc. | Comprehensive language support |

---

## 🎯 Use Cases

### **1. Business Document Fine-Tuning**
Transform your organization's knowledge base into training data:
- Company policies and procedures
- Technical documentation and manuals
- Training presentations and materials
- Annual reports and business documents

### **2. Codebase Training**
Prepare code repositories for AI model training:
- **Full Language Support**: 30+ programming languages with intelligent extraction
- **Quality Control**: Automatic detection and skipping of minified/auto-generated files
- **Encoding Handling**: Automatic character encoding detection for international codebases
- **Structure Preservation**: Maintains indentation and code structure
- **Smart Filtering**: Configurable file size limits and quality thresholds

### **3. Research & Academic**
Process large document collections for research:
- Academic papers and publications
- Research datasets and corpora
- Multi-format document libraries
- Batch processing with metadata

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- 8GB RAM recommended for large batch processing
- Windows, macOS, or Linux

### Quick Start
```bash
# Clone the repository
git clone https://github.com/CLewisMessina/wolfstitch.git
cd wolfstitch

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Note: If you see an error about chardet, install it separately:
pip install chardet>=5.0.0

# Launch application
python main.py
```

---

## 💡 Usage Guide

### Single File Processing
1. Click "Select File" or drag & drop a supported file
2. Choose splitting method (paragraph, sentence, or custom)
3. Configure token limits if needed
4. Click "Process Text" to chunk the document
5. Preview chunks and export to desired format

### Batch Processing (Coming Soon)
1. Click "Select Folder" or use multi-file selection
2. Configure batch processing settings
3. Monitor progress with real-time updates
4. Review error log for any failed files
5. Export complete dataset in JSONL format

---

## 🎯 Roadmap

### **Phase A: Batch Processing Foundation** (Current)
- [x] PowerPoint (.pptx) format support ✅
- [x] Source code file support (.py, .js, .java, etc.) ✅
- [ ] Context-aware cleaning system (Day 2)
- [ ] Multi-file selection UI
- [ ] Batch processing architecture

### **Phase B: Smart Chunking & Quality**
- [ ] Token-aware intelligent chunking
- [ ] Content deduplication
- [ ] Metadata tracking and tagging
- [ ] Quality scoring system

### **Phase C: Enhanced Output & Integration**
- [ ] JSONL export with metadata
- [ ] Batch analytics dashboard
- [ ] API integration options
- [ ] Cloud storage support

---

## 🤝 Contributing

Wolfstitch is open source and welcomes contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built on the foundation of Wolfscribe
- Part of the Wolflow ecosystem
- Special thanks to all contributors

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/CLewisMessina/wolfstitch/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CLewisMessina/wolfstitch/discussions)
- **Email**: support@wolflow.ai

---

**Built with ❤️ by the Wolflow Team**