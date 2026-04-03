from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MY_EMAIL = "24f1000749@ds.study.iitm.ac.in"

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()

    # Try reading messy CSV
    df = pd.read_csv(
        io.BytesIO(content),
        dtype=str,
        encoding="utf-8",
        keep_default_na=False
    )

    # Clean column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Find category and amount columns automatically
    category_col = None
    amount_col = None

    for col in df.columns:
        c = col.lower()

        if category_col is None and "category" in c:
            category_col = col

        if amount_col is None and (
            "amount" in c or
            "price" in c or
            "cost" in c or
            "spent" in c
        ):
            amount_col = col

    if category_col is None or amount_col is None:
        return {
            "answer": 0,
            "email": MY_EMAIL,
            "exam": "tds-2025-05-roe"
        }

    total = 0.0

    for _, row in df.iterrows():
        category = str(row[category_col]).strip().lower()

        # remove extra spaces inside text
        category = " ".join(category.split())

        if category == "food":
            value = str(row[amount_col]).strip()

            # remove commas, ₹, $, spaces, etc
            value = re.sub(r"[^0-9.\-]", "", value)

            try:
                total += float(value)
            except:
                pass

    if total.is_integer():
        total = int(total)

    return {
        "answer": total,
        "email": MY_EMAIL,
        "exam": "tds-2025-05-roe"
    }
