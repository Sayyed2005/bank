import pdfplumber
import re

def extract_transactions(file_path):

    text_data = ""

    try:
        with pdfplumber.open(file_path, password="9167641708") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_data += text + "\n"

    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

    pattern = r'(\d{2}-\d{2}-\d{4})\s+(.*?)\s+(\d+\.\d{2})\s+(\d+\.\d{2})'

    matches = re.findall(pattern, text_data)

    transactions = []

    for m in matches:

        description = m[1]

        # ✅ UTR extraction logic (ONLY ADDITION)
        utr = None
        utr_match = re.search(r'TRTR/(\d+)', description)
        if utr_match:
            utr = utr_match.group(1)

        transactions.append({
            "date": m[0],
            "description": description,
            "amount": m[2],
            "balance": m[3],
            "utr": utr   # ✅ added field
        })

    return transactions
