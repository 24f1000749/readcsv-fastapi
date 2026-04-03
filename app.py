from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
import re

app = FastAPI()

# Change this to your real email
EMAIL = "24f1000749@ds.study.iitm.ac.in"

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()

    # Try different encodings because the CSV can be messy
    text = None
    for encoding in ["utf-8", "latin1", "cp1252"]:
        try:
            text = content.decode(encoding)
            break
        except:
            continue

    # If file could not be decoded
    if text is None:
        return {
            "answer": 0,
            "email": EMAIL,
            "exam": "tds-2025-05-roe"
        }

    # Detect separator automatically
    try:
        dialect = csv.Sniffer().sniff(text[:1000])
        separator = dialect.delimiter
    except:
        separator = ","

    reader = csv.DictReader(io.StringIO(text), delimiter=separator)

    total = 0.0

    for row in reader:
        cleaned_row = {}

        # Clean all column names and values
        for key, value in row.items():
            if key is None:
                continue

            clean_key = str(key).strip().lower()
            clean_value = str(value).strip()

            cleaned_row[clean_key] = clean_value

        category_value = ""
        amount_value = ""

        # Find the category and amount columns automatically
        for key, value in cleaned_row.items():
            if (
                "category" in key
                or "type" in key
                or "expense" in key
            ):
                category_value = value

            if (
                "amount" in key
                or "price" in key
                or "cost" in key
                or "spent" in key
                or "value" in key
                or "total" in key
            ):
                amount_value = value

        # Normalize the category text
        category_value = " ".join(category_value.lower().split())

        # Count only Food rows
        if category_value == "food":
            # Remove commas, spaces, currency symbols, etc.
            amount_value = re.sub(r"[^0-9.\-]", "", amount_value)

            try:
                total += float(amount_value)
            except:
                pass

    # Return int if it is a whole number
    if total.is_integer():
        total = int(total)

    return {
        "answer": total,
        "email": EMAIL,
        "exam": "tds-2025-05-roe"
    }
