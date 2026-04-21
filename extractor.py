import pdfplumber
import re

def extract_transactions(file_path, password=password):

    text_data = ""

    # Open PDF (with or without password)
    with pdfplumber.open(file_path, password=9167641708) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Normalize spaces
                text = re.sub(r'\s+', ' ', text)
                text_data += text + "\n"

    # Improved pattern:
    # - Handles negative amounts
    # - Cleaner separation of fields
    pattern = r'(\d{2}[-/]\d{2}[-/]\d{4})\s+(.*?)\s+(-?\d+\.\d{2})\s+(\d+\.\d{2})'

    matches = re.findall(pattern, text_data)

    transactions = []

    for m in matches:

        date = m[0]
        description = m[1].strip()
        amount = float(m[2])
        balance = float(m[3])

        # ✅ UTR Extraction (robust)
        utr = None
        utr_match = re.search(r'(TRTR|UPI|IMPS)/(\d+)', description)
        if utr_match:
            utr = utr_match.group(2)

        transactions.append({
            "date": date,
            "description": description,
            "amount": amount,
            "balance": balance,
            "utr": utr   # ✅ now included
        })

    return transactions
