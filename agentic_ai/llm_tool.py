from groq import Groq
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_llm_output(raw_code: str) -> str:
    """
    Cleans the raw output from the LLM to ensure it's valid Python code.
    This function removes markdown fences and leading/trailing whitespace.
    """
    if raw_code.startswith("```python"):
        raw_code = raw_code.removeprefix("```python")
    if raw_code.endswith("```"):
        raw_code = raw_code.removesuffix("```")
    return raw_code.strip()

def generate_parser_code(bank: str, error: str = None) -> str:
    """
    Generates parser code using Groq with the final, most robust prompt that
    matches the specific requirements of the assignment PDF and data files.
    """
    # This is the final, "golden" prompt that combines all our learnings.
    prompt = f"""
You are an expert Python code generation tool. Your sole purpose is to write clean, runnable Python code that solves the user's specific problem.

TASK:
Write the complete Python code for a function that parses an '{bank}' bank statement PDF. The final output DataFrame MUST be structured to pass a `pd.testing.assert_frame_equal()` check against the provided ground-truth CSV.

# --- CRITICAL PARSING STRATEGY --- #
The PDF contains non-data rows (headers) and transaction data merged into single cells with newlines. The only reliable strategy is:
1.  Use `pdfplumber.open(pdf_path)` to open the PDF and iterate through every page (`for page in pdf.pages:`).
2.  On each page, use `page.extract_tables()` to get the table data.
3.  Initialize an empty list to store transaction dictionaries.
4.  Iterate through every `row` in the extracted table.
5.  **CRITICAL ROW FILTERING:** A row is only a valid transaction if its first cell contains a string that starts with a date in 'DD-MM-YYYY' format. You MUST use a regex check like `re.match(r'\\d{{2}}-\\d{{2}}-\\d{{4}}', str(row[0]))` to validate and filter out header/junk rows.
6.  For each valid row, you MUST wrap the processing in a `try-except` block to gracefully handle any malformed rows and `continue` to the next.
7.  Inside the `try` block, clean each cell's text by replacing any newline characters (`'\\n'`) with a space.
8.  **CRITICAL DATA CLEANING:** The 'Debit Amt' and 'Credit Amt' cells can be empty. If the cleaned string for these cells is empty, the value should be `None` (which pandas will treat as `NaN`). Otherwise, clean the string by removing commas and convert it to a `float`. **Do NOT default empty values to `0.0`**.
9.  The 'Balance' column must also be cleaned of commas and converted to `float`.

# --- SPECIFICATIONS --- #
- The function contract must be exactly: `def parse(pdf_path: str) -> pd.DataFrame`
- The final DataFrame must have exactly these columns in this order to match the `result.csv` file: `['Date', 'Description', 'Debit Amt', 'Credit Amt', 'Balance']`.

{f"- You must fix the following error from the previous attempt: {error}" if error else ""}

# --- OUTPUT REQUIREMENTS --- #
- Your entire response must be ONLY the raw Python code.
- DO NOT include markdown fences (like ```python) or any explanations.
- The response must start with `import pandas as pd`.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    raw_code = response.choices[0].message.content
    clean_code = clean_llm_output(raw_code)
    return clean_code

