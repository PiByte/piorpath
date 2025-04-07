# Path Purifier Tool

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

A powerful Python script to clean and standardize file/directory names in bulk.

## 📦 Installation

### 1. Method one: Install from source
   ```bash
   git clone https://github.com/yourusername/filename-normalizer.git
   cd piorpath
   pip install .
   ```
   
### 2. Method two: Install in development mode
   ```bash
   git clone https://github.com/yourusername/piorpath.git
   cd piorpath
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   pip install -e .
   ```

### 3. Method three: Install directly via pip
   ```bash
   pip install git+https://github.com/yourusername/piorpath.git
   ```

### 4. Make the script executable:
   ```bash
   chmod +x piropath.py
   ```

### 5. Run the script with the template:
   ```bash
   ./piorpath.py [OPTIONS] -p [PATH]
   ```

## ⁉️ Examples

| Header 1            | Header 2 
|---------------------|----------
| ./piorpath.py -u|Removes '_' underscore char 
| ./piorpath.py -d|Removes '-' dash char
| ./piorpath.py -k|Keep white spaces in names (Not Recommended.)
| ./piorpath.py -i|Include hidden files into the process
| ./piorpath.py -p|Starts from current directory.
| ./piorpath.py -dr|Preview changes and Nothing will be applied
| ./piorpath.py -v|Show the full paths of changed items instead of trees
| ./piorpath.py -dr|Convert capital-case into small-case with preview changes (-dr = dry run)
| ./piorpath.py -s -c '!'|Replace special chars with specified char (here it is '!') 

## 🧪 Transformation Examples
| Original Name | Command | Result |
|----------|----------|----------|
| Photo 12@Home.jpg| -s | Photo12Home.jpg  |
| report-2023-final.pdf| -d |  report2023final.pdf |
| My Document.docx  | -l -dr | mydocument.docx (dry run)  |
| .config_file!  | -H -s -u | .configfile |

## ⚠️ Safety Features
- Dry-run mode (-d) shows changes before applying

- Conflict resolution automatically handles duplicate names

- Extension preservation keeps file extensions intact

- Color-coded output for easy review

- ⚠️ Do not use this tool in root directroy, it is risky


## 💡 Want to Improve This Project?
Feel free to fork, modify, and submit pull requests! Open an issue for:

- Bug reports 🐛

- Feature ideas 💡

- Questions ❓

Keep changes focused and tested. All constructive contributions are welcome!



