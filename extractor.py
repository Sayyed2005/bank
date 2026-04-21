import pdfplumber
import re

def extract_transactions(file_path):

    text_data = ""

    try:
        # Open PDF with fixed password
        with pdfplumber.open(file_path, password="9167641708") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Normalize spaces
                    text = re.sub(r'\s+', ' ', text)
                    text_data += text + "\n"

    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

    # If no text extracted → likely scanned PDF
    if not text_data.strip():
        raise Exception("No text extracted from PDF")

    # Regex pattern
    pattern = r'(\d{2}[-/]\d{2}[-/]\d{4})\s+(.*?)\s+(-?\d+\.\d{2})\s+(\d+\.\d{2})'

    matches = re.findall(pattern, text_data)

    transactions = []

    for m in matches:

        date = m[0]
        description = m[1].strip()
        amount = float(m[2])
        balance = float(m[3])

        # UTR extraction
        utr = None
        utr_match = re.search(r'(TRTR|UPI|IMPS)/(\d+)', description)
        if utr_match:
            utr = utr_match.group(2)

        transactions.append({
            "date": date,
            "description": description,
            "amount": amount,
            "balance": balance,
            "utr": utr
        })

    if not transactions:
        raise Exception("No transactions found. Check PDF format.")

    return transactions
