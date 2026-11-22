
import re
import json
import logging

# ==========================================
# 1. CONTEXT ENGINEERING
# ==========================================

SYSTEM_PROMPT = """
You are an invoice processing AI assistant.

Extract:
- Vendor Name
- GSTIN
- Invoice Number
- Invoice Amount

Rules:
- Never guess missing information.
- Return null for missing fields.
- Extract only information available in the invoice.
"""

vendor_master = {
    "ABC Technologies": "27ABCDE1234F1Z5"
}

print("\n1. CONTEXT ENGINEERING")
print("Instructions:", SYSTEM_PROMPT)


# ==========================================
# 2. GUARDRAILS ENGINEERING
# ==========================================

def validate_gstin(gstin):

    if not gstin:
        return False

    pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"

    return bool(re.match(pattern, gstin))


def validate_invoice(data):

    if not data.get("Vendor Name"):
        return False

    if not data.get("Invoice Number"):
        return False

    if not validate_gstin(data.get("GSTIN")):
        return False

    if not isinstance(data.get("Invoice Amount"), (int, float)):
        return False

    if data["Invoice Amount"] <= 0:
        return False

    return True


# ==========================================
# 3. LOOP ENGINEERING
# ==========================================

def extract_invoice():

    # Simulating Gemini responses for learning

    responses = [
        {
            "Vendor Name": "ABC Technologies",
            "GSTIN": None,
            "Invoice Number": "INV101",
            "Invoice Amount": 25000
        },
        {
            "Vendor Name": "ABC Technologies",
            "GSTIN": "27ABCDE1234F1Z5",
            "Invoice Number": "INV101",
            "Invoice Amount": 25000
        }
    ]

    max_attempts = 3

    for attempt in range(max_attempts):

        print(f"\nExtraction attempt: {attempt + 1}")

        data = responses[min(attempt, len(responses) - 1)]

        if validate_invoice(data):
            print("Extraction successful!")
            return data

        print("Validation failed. Retrying...")

    raise ValueError("Invoice extraction failed after maximum attempts")


# ==========================================
# 4. HARNESS ENGINEERING
# ==========================================

logging.basicConfig(
    filename="invoice.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    try:

        print("\nInvoice processing started")

        logging.info("Invoice processing started")

        # Execute AI extraction and retry loop
        invoice_data = extract_invoice()

        # Final business rule check
        if invoice_data["GSTIN"] != vendor_master.get(
            invoice_data["Vendor Name"]
        ):
            raise ValueError("Vendor GSTIN does not match master")

        # Save output
        with open("invoice_output.json", "w") as file:
            json.dump(invoice_data, file, indent=4)

        logging.info("Invoice processed successfully")

        print("\nFinal Invoice Data:")
        print(json.dumps(invoice_data, indent=4))

        print("\nProcess completed successfully")

    except Exception as error:

        logging.exception("Invoice processing failed")

        print("Error:", error)


# ==========================================
# START EXECUTION
# ==========================================

if __name__ == "__main__":
    main()
