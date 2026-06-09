#!/usr/bin/env python3
"""
Local Data Analyzer MCP Server

A production-ready Model Context Protocol server that exposes a tool for
analyzing local CSV and Excel (.xlsx) files using pandas. The server runs
on stdio transport for seamless integration with Claude Desktop.

Features:
- Safe file reading with comprehensive error handling
- Data profiling: rows, columns, data types, missing values
- Statistical summaries for numerical columns
- Preview of first 3 rows in readable format
- Support for CSV and Excel (.xlsx) files
"""

import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd
from mcp.server.fastmcp import FastMCP

# Configure logging for production-ready error tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server with stdio transport
server = FastMCP("local-data-analyzer")


@server.tool()
def analyze_local_file(file_path: str) -> str:
    """
    Analyze a local CSV or Excel file and return a comprehensive profile.
    
    This tool safely reads and analyzes local data files, returning:
    - File metadata (rows, columns, size)
    - Column data types and missing value counts
    - Statistical summary for numerical columns
    - Preview of first 3 rows
    
    Args:
        file_path: Absolute or relative path to the CSV or .xlsx file
        
    Returns:
        A formatted text report with complete file analysis
        
    Raises:
        ValueError: If file doesn't exist, has unsupported extension, or cannot be parsed
    """
    try:
        # Validate and resolve file path
        file_path_obj = Path(file_path).resolve()
        
        # Check if file exists
        if not file_path_obj.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}\n"
                f"Resolved path: {file_path_obj}"
            )
        
        # Verify it's a file, not a directory
        if not file_path_obj.is_file():
            raise IsADirectoryError(
                f"Path is a directory, not a file: {file_path_obj}"
            )
        
        # Get file extension
        file_ext = file_path_obj.suffix.lower()
        
        # Validate file extension
        supported_extensions = {'.csv', '.xlsx', '.xls'}
        if file_ext not in supported_extensions:
            raise ValueError(
                f"Unsupported file type: {file_ext}\n"
                f"Supported formats: {', '.join(supported_extensions)}"
            )
        
        # Attempt to read the file based on extension
        try:
            if file_ext == '.csv':
                df = pd.read_csv(file_path_obj)
            elif file_ext in {'.xlsx', '.xls'}:
                df = pd.read_excel(file_path_obj)
        except pd.errors.ParserError as e:
            raise ValueError(
                f"Error parsing file: {str(e)}\n"
                f"Please verify the file format is valid."
            )
        except PermissionError:
            raise PermissionError(
                f"Permission denied reading file: {file_path_obj}"
            )
        except Exception as e:
            raise ValueError(
                f"Error reading file: {type(e).__name__}: {str(e)}"
            )
        
        # Build comprehensive analysis report
        report = _generate_analysis_report(df, file_path_obj)
        logger.info(f"Successfully analyzed file: {file_path_obj}")
        return report
        
    except FileNotFoundError as e:
        error_msg = f"❌ File Error: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except IsADirectoryError as e:
        error_msg = f"❌ Invalid Input: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except ValueError as e:
        error_msg = f"❌ Invalid File: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except PermissionError as e:
        error_msg = f"❌ Permission Error: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Unexpected Error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        return error_msg


def _generate_analysis_report(df: pd.DataFrame, file_path: Path) -> str:
    """
    Generate a formatted, human-readable analysis report for a DataFrame.
    
    Args:
        df: Pandas DataFrame to analyze
        file_path: Path to the source file
        
    Returns:
        Formatted analysis report as a string
    """
    report_lines = []
    
    # Header
    report_lines.append("=" * 70)
    report_lines.append("📊 DATA ANALYSIS REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"File: {file_path.name}")
    report_lines.append(f"Path: {file_path}")
    report_lines.append(f"Size: {file_path.stat().st_size:,} bytes")
    report_lines.append("")
    
    # Basic metadata
    report_lines.append("📈 DATASET METADATA")
    report_lines.append("-" * 70)
    report_lines.append(f"Total Rows: {len(df):,}")
    report_lines.append(f"Total Columns: {len(df.columns)}")
    report_lines.append("")
    
    # Column information
    report_lines.append("📋 COLUMN INFORMATION")
    report_lines.append("-" * 70)
    report_lines.append(f"{'Column Name':<30} {'Data Type':<15} {'Missing':<10}")
    report_lines.append("-" * 70)
    
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        report_lines.append(
            f"{col:<30} {str(df[col].dtype):<15} {missing_count} ({missing_pct:.1f}%)"
        )
    report_lines.append("")
    
    # Data preview
    report_lines.append("👁️  DATA PREVIEW (First 3 Rows)")
    report_lines.append("-" * 70)
    preview = df.head(3).to_string()
    report_lines.append(preview)
    report_lines.append("")
    
    # Statistical summary for numerical columns
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numerical_cols:
        report_lines.append("📊 STATISTICAL SUMMARY (Numerical Columns)")
        report_lines.append("-" * 70)
        stats = df[numerical_cols].describe()
        report_lines.append(stats.to_string())
        report_lines.append("")
    
    # Missing values summary
    missing_total = df.isna().sum().sum()
    if missing_total > 0:
        report_lines.append("⚠️  MISSING VALUES SUMMARY")
        report_lines.append("-" * 70)
        missing_by_col = df.isna().sum()
        missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)
        for col, count in missing_by_col.items():
            pct = (count / len(df)) * 100
            report_lines.append(f"{col}: {count} ({pct:.1f}%)")
        report_lines.append("")
    
    # Footer
    report_lines.append("=" * 70)
    report_lines.append("✅ Analysis completed successfully")
    report_lines.append("=" * 70)
    
    return "\n".join(report_lines)


if __name__ == "__main__":
    """Run the FastMCP server on stdio transport."""
    logger.info("Starting Local Data Analyzer MCP Server...")
    server.run()
