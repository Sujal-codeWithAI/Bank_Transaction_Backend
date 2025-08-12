
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path 
import os
from bank_logic import Account

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

accounts = {
    "1001": Account(pin=1234, balance=1000),
    "1002": Account(pin=1111, balance=2000)
}

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    # Bust browser cache when CSS file changes by appending last-modified timestamp
    css_path = BASE_DIR / "static" / "styles.css"
    static_version = int(os.path.getmtime(css_path)) if css_path.exists() else 1
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "static_version": static_version},
    )

@app.post("/login")
async def login(account_number: str = Form(...), password: str = Form(...)):
    account = accounts.get(account_number)
    if not account:
        return {"success": False, "message": "Account not found."}
    try:
        pin = int(password)
    except ValueError:
        return {"success": False, "message": "PIN must be numeric."}
    if account.check_pin(pin):
        return {"success": True, "message": "Login successful", "account_number": account_number}
    return {"success": False, "message": "Incorrect PIN."}

@app.post("/deposit")
async def deposit(account_number: str = Form(...), amount: int = Form(...)):
    account = accounts.get(account_number)
    if not account:
        return {"success": False, "message": "Account not found."}
    success, message = account.deposit(amount)
    return {
        "success": success,
        "message": message,
        "balance": account.get_balance() if success else None
    }

@app.post("/withdraw")
async def withdraw(account_number: str = Form(...), amount: int = Form(...)):
    account = accounts.get(account_number)
    if not account:
        return {"success": False, "message": "Account not found."}
    success, message = account.withdraw(amount)
    return {
        "success": success,
        "message": message,
        "balance": account.get_balance() if success else None
    }

@app.get("/balance")
async def get_balance(account_number: str):
    account = accounts.get(account_number)
    if not account:
        return {"success": False, "message": "Account not found."}
    return {"success": True, "balance": account.get_balance()}
