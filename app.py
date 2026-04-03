from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import csv
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

EMAIL = "24f1000749@ds.study.iitm.ac.in"

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()

    # try different encodings
    text = None
    for enc in ["utf-8", "latin1", "cp1252"]:
        try:
            text = content.decode(enc)
            break
        except:
            pass

    if text is None:
        return {
            "answer": 0,
            "email": EMAIL,
            "exam": "tds-2025-05-roe"
        }

    # detect separator
    sep = ","
    if text.count(";") > text.count(","):
        sep = ";"

    reader = csv.DictReader(io.StringIO(text), delimiter=sep)

    total = 0.0

    for row in reader:
        clean_row = {}

        # clean column names and values
        for k, v in row.items():
            if k is None:
                continue
            clean_row[k.strip().lower()] = (v or "").strip()

        category = ""
        amount = ""

        for key, value in clean_row.items():
            if "category" in key:
                category = value.strip().lower()

            if any(word in key for word in ["amount", "cost", "price", "spent", "value"]):
                amount = value

        if category == "food":
            amount = re.sub(r"[^0-9.-]", "", amount)

            try:
                total += float(amount)
            except:
                pass

    if total.is_integer():
        total = int(total)

    return {
        "answer": total,
        "email": EMAIL,
        "exam": "tds-2025-05-roe"
    }
