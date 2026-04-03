from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import re

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "your-email@example.com"

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()

    # Try different encodings because the CSV may be messy
    try:
        df = pd.read_csv(
            io.BytesIO(content),
            dtype=str,
            keep_default_na=False
        )
    except:
        df = pd.read_csv(
            io.BytesIO(content),
            dtype=str,
            keep_default_na=False,
            encoding="latin1"
        )

    # Clean column names
    df.columns = [str(col).strip().lower() for col in df.columns]

    category_col = None
    amount_col = None

    # Automatically find the category and amount columns
    for col in df.columns:
        clean = col.lower().strip()

        if category_col is None and "category" in clean:
            category_col = col

        if amount_col is None and (
            "amount" in clean
            or "price" in clean
            or "cost" in clean
            or "spent" in clean
            or "value" in clean
        ):
            amount_col = col

    # If columns not found, return 0 instead of crashing
    if category_col is None or amount_col is None:
        return {
            "answer": 0,
            "email": EMAIL,
            "exam": "tds-2025-05-roe"
        }

    total = 0.0

    for _, row in df.iterrows():
        try:
            category = str(row[category_col]).strip().lower()

            # remove extra spaces inside the category
            category = " ".join(category.split())

            if category == "food":
                amount = str(row[amount_col]).strip()

                # Remove commas, currency symbols, spaces, etc.
                amount = re.sub(r"[^0-9.\-]", "", amount)

                if amount != "":
                    total += float(amount)
        except:
            continue

    if total.is_integer():
        total = int(total)

    return {
        "answer": total,
        "email": EMAIL,
        "exam": "tds-2025-05-roe"
    }
