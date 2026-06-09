# Local Data Analyzer MCP Server

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple)](https://modelcontextprotocol.io)

A lightweight, production-ready **Model Context Protocol (MCP) server** that exposes a powerful tool for analyzing local CSV and Excel files through Claude Desktop. Built with FastMCP and pandas, it enables Claude to safely read, profile, and generate insights from your local data files in real-time.

---

## Features

✨ **Safe File Analysis**
- Secure local file reading with comprehensive error handling
- Support for CSV (`.csv`) and Excel (`.xlsx`, `.xls`) formats
- Validates file existence, permissions, and format before processing

📊 **Comprehensive Data Profiling**
- Dataset metadata (total rows, columns, file size)
- Column-by-column analysis (data types, missing values, percentages)
- Statistical summaries for numerical columns (mean, std, min, max, quartiles)
- Preview of first 3 rows in readable format

🎯 **Production-Ready**
- Robust error handling for missing files, invalid paths, and parsing errors
- Detailed logging for debugging and monitoring
- Type hints throughout for code clarity
- Professional formatted output (emoji-enhanced, human-readable)

🔌 **Seamless Integration**
- Runs on stdio transport for zero-configuration integration with Claude Desktop
- Single, intuitive tool: `analyze_local_file(file_path: str)`
- Returns clean text-based reports (no JSON parsing needed)

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Claude Desktop app installed

### Installation

1. **Clone or download the repository:**
   ```bash
   git clone https://github.com/yourusername/local-data-analyzer-mcp.git
   cd local-data-analyzer-mcp
   ```

2. **Create and activate a virtual environment:**
   
   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Register with Claude Desktop:**

   **Windows:**
   - Open: `C:\Users\[YOUR_USERNAME]\AppData\Local\Claude\claude_desktop_config.json`
   
   **macOS:**
   - Open: `~/Library/Application Support/Claude/claude_desktop_config.json`

   Add the following configuration:
   ```json
   {
     "mcpServers": {
       "local-data-analyzer": {
         "command": "/path/to/your/venv/bin/python",
         "args": ["/path/to/local-data-analyzer-mcp/server.py"],
         "disabled": false
       }
     }
   }
   ```

   Replace `/path/to/` with your actual installation path.

5. **Restart Claude Desktop** to load the configuration.

---

## Usage

Once registered, Claude Desktop will have access to the `analyze_local_file` tool. Simply ask Claude to analyze any local data file:

### Example 1: Analyze CSV File
```
Claude, please analyze the file at C:\Users\YourName\Documents\sales_data.csv
```

**Sample Output:**
```
======================================================================
📊 DATA ANALYSIS REPORT
======================================================================
File: sales_data.csv
Path: C:\Users\YourName\Documents\sales_data.csv
Size: 45,632 bytes

📈 DATASET METADATA
----------------------------------------------------------------------
Total Rows: 1,256
Total Columns: 8

📋 COLUMN INFORMATION
----------------------------------------------------------------------
Column Name                    Data Type       Missing   
----------------------------------------------------------------------
Order_ID                       int64           0 (0.0%)
Product                        str             0 (0.0%)
Region                         str             0 (0.0%)
Sales                          float64         0 (0.0%)
Quantity                       int64           2 (0.2%)
Date                           str             0 (0.0%)

👁️  DATA PREVIEW (First 3 Rows)
----------------------------------------------------------------------
  Order_ID       Product Region   Sales  Quantity        Date
0     1001  Widget Pro    East  2500.0        50  2024-01-15
1     1002  Gadget Max    West  1850.0        35  2024-01-16
2     1003  Gizmo Plus   North  3200.0        60  2024-01-17

📊 STATISTICAL SUMMARY (Numerical Columns)
----------------------------------------------------------------------
                Sales     Quantity
count    1256.000000   1254.000000
mean     2847.650000     45.320000
std       856.324000     18.540000
min       100.000000      1.000000
25%      2100.000000     28.000000
50%      2850.000000     45.000000
75%      3600.000000     62.000000
max      5000.000000    100.000000

======================================================================
✅ Analysis completed successfully
======================================================================
```

### Example 2: Analyze Excel File
```
Please analyze C:\Users\YourName\Desktop\employee_records.xlsx and tell me about the data structure
```

### Example 3: Check for Data Quality Issues
```
I want to understand data quality. Can you analyze employee_data.csv and highlight any missing values or anomalies?
```

---

## API Reference

### `analyze_local_file(file_path: str) -> str`

**Description:**
Analyzes a local CSV or Excel file and returns a comprehensive profile including metadata, column information, data preview, and statistical summaries.

**Parameters:**
- `file_path` (str): Absolute or relative path to the CSV or Excel file

**Returns:**
- str: Formatted text report with complete data analysis

**Supported Formats:**
- `.csv` - Comma-separated values
- `.xlsx` - Microsoft Excel (2010+)
- `.xls` - Microsoft Excel (97-2003)

**Error Handling:**
- Returns descriptive error messages for missing files
- Handles permission errors gracefully
- Validates file format before processing
- Provides feedback on invalid or corrupt files

**Example:**
```python
from server import analyze_local_file

report = analyze_local_file("./data/sales.csv")
print(report)
```

---

## Project Structure

```
local-data-analyzer-mcp/
├── server.py                      # Main FastMCP server implementation
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── LICENSE                        # MIT License
├── venv/                          # Virtual environment (created during setup)
└── sample_data.csv               # Example CSV for testing
```

---

## Technical Details

### Architecture

The server is built on three core components:

1. **FastMCP Framework**: Provides the MCP server backbone and tool registration
2. **Pandas Library**: Handles CSV and Excel file parsing with robust error management
3. **Stdio Transport**: Enables real-time bidirectional communication with Claude Desktop

### Error Handling

The server implements layered error handling:
- **File Validation**: Checks existence, type, and accessibility
- **Format Validation**: Ensures file extension is supported
- **Parse Error Recovery**: Provides meaningful feedback if file is corrupted
- **Permission Checks**: Detects and reports access restrictions

### Performance

- **Lightweight**: Minimal memory footprint for typical datasets (< 100MB)
- **Fast Profiling**: Analyzes files in milliseconds
- **Streaming Support**: Handles large CSV files efficiently using pandas chunking

---

## Configuration Examples

### Windows (Full Path Example)
```json
{
  "mcpServers": {
    "local-data-analyzer": {
      "command": "C:\\Users\\YourName\\Projects\\local-data-analyzer\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\Projects\\local-data-analyzer\\server.py"],
      "disabled": false
    }
  }
}
```

### macOS/Linux (Full Path Example)
```json
{
  "mcpServers": {
    "local-data-analyzer": {
      "command": "/Users/yourname/projects/local-data-analyzer/venv/bin/python",
      "args": ["/Users/yourname/projects/local-data-analyzer/server.py"],
      "disabled": false
    }
  }
}
```

---

## Troubleshooting

### Server Not Appearing in Claude Desktop

1. **Verify configuration file exists:**
   - Windows: `C:\Users\[USERNAME]\AppData\Local\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Check Python path is correct:**
   ```powershell
   # Windows: Verify venv Python executable exists
   Test-Path "C:\path\to\venv\Scripts\python.exe"
   
   # macOS/Linux: Verify venv Python executable exists
   ls -la /path/to/venv/bin/python
   ```

3. **Restart Claude Desktop completely** (including system tray)

4. **Check Claude Desktop logs** for startup errors (if available)

### File Analysis Fails

1. **Verify file path is correct:**
   ```python
   from pathlib import Path
   Path("your/file/path").resolve()  # Check absolute path
   ```

2. **Ensure file is readable:**
   ```powershell
   # Windows
   Test-Path "your_file.csv"  # Should return True
   ```

3. **Check file format:**
   - CSV files should be comma-separated
   - Excel files should have `.xlsx` or `.xls` extension

---

## Development & Contributing

### Running Tests

To test the server locally without Claude Desktop:

```python
from server import analyze_local_file

# Test with a CSV file
result = analyze_local_file("sample_data.csv")
print(result)
```

### Starting the Server Manually

```bash
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
python server.py
```

### Code Quality

- **Type Hints**: Full type annotations for IDE support
- **Logging**: Built-in logging at INFO level for debugging
- **Error Messages**: User-friendly, descriptive error reporting

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [Anthropic's Model Context Protocol](https://modelcontextprotocol.io)
- Data analysis powered by [Pandas](https://pandas.pydata.org/)
- FastMCP framework documentation: https://github.com/modelcontextprotocol/python-sdk

---

## Support & Questions

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above

---

## Roadmap

Future enhancements planned:
- 🎯 Support for JSON and Parquet files
- 🎯 Advanced statistical analysis (correlation, regression)
- 🎯 Data visualization generation
- 🎯 Performance profiling for large datasets
- 🎯 Data validation and quality scoring

---

**Made with ❤️ for data enthusiasts and developers**
