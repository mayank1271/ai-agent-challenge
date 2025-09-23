import pandas as pd
import pdfplumber
import re

def parse(pdf_path: str) -> pd.DataFrame:
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if re.match(r'\d{2}-\d{2}-\d{4}', str(row[0])):
                        try:
                            cleaned_row = row.copy()
                            for i in range(1, len(row)):
                                cleaned_row[i] = str(row[i]).replace('\n', ' ').strip()
                                if i in [2, 3]:
                                    cleaned_row[i] = None if cleaned_row[i] == '' else float(cleaned_row[i].replace(',', ''))
                                elif i == 4:
                                    cleaned_row[i] = float(cleaned_row[i].replace(',', ''))
                            data.append(cleaned_row)
                        except Exception as e:
                            print(f"Error processing row: {row}, Error: {e}")
    columns = ['Date', 'Description', 'Debit Amt', 'Credit Amt', 'Balance']
    df = pd.DataFrame(data, columns=columns)
    return df