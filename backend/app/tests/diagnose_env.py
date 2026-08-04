"""Diagnostic script to inspect DB config and test connections (password-safe output)."""
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

lines = []


def log(msg):
    lines.append(str(msg))


user = os.getenv("DB_USER")
pw = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")

log("=== ENV VARIABLE PRESENCE ===")
log(f"DB_USER present: {user is not None}  repr={user!r}")
log(f"DB_PASSWORD present: {pw is not None}  length={len(pw) if pw else 0}")
log(f"DB_HOST present: {host is not None}  repr={host!r}")
log(f"DB_PORT present: {port is not None}  repr={port!r}")
log(f"DB_NAME present: {name is not None}  repr={name!r}")

if pw:
    log("\n=== PASSWORD ANALYSIS ===")
    log(f"Contains URL-special characters (needs encoding): {not pw.isalnum()}")
    log(f"Has leading/trailing whitespace: {pw != pw.strip()}")
    log(f"First char={pw[0]!r}  Last char={pw[-1]!r}  Printable alphabet: {pw.isprintable()}")

log("\n=== URL CONSTRUCTIONS (password masked) ===")
log(f"Current raw URL:  postgresql+psycopg2://{user}:***@{host}:{port}/{name}?sslmode=require")
if pw:
    enc_user = urllib.parse.quote_plus(user or "")
    enc_pw = urllib.parse.quote_plus(pw)
    log(f"URL-encoded URL:  postgresql+psycopg2://{enc_user}:***@{host}:{port}/{name}?sslmode=require")
    log(f"(encoded password would be length {len(enc_pw)})")

log("\n=== CONNECTION TESTS ===")
import psycopg2

# Test 1: raw password via keyword args (bypasses URL parsing entirely)
try:
    conn = psycopg2.connect(
        host=host, port=port, dbname=name,
        user=user, password=pw, sslmode="require",
        connect_timeout=10,
    )
    log("TEST 1 (raw password, kwarg connect): SUCCESS")
    conn.close()
except Exception as e:
    log(f"TEST 1 (raw password, kwarg connect): FAILED -> {type(e).__name__}: {e}")

# Test 2: URL-encoded password via SQLAlchemy engine
if pw:
    from sqlalchemy import create_engine
    enc_user = urllib.parse.quote_plus(user or "")
    enc_pw = urllib.parse.quote_plus(pw)
    encoded_url = (
        f"postgresql+psycopg2://{enc_user}:{enc_pw}@{host}:{port}/{name}?sslmode=require"
    )
    try:
        eng = create_engine(encoded_url, pool_pre_ping=True)
        with eng.connect():
            log("TEST 2 (URL-encoded password): SUCCESS")
    except Exception as e:
        log(f"TEST 2 (URL-encoded password): FAILED -> {type(e).__name__}: {str(e)[:300]}")

# Test 3: raw URL as currently built in database.py
if pw:
    from sqlalchemy import create_engine
    raw_url = (
        f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{name}?sslmode=require"
    )
    try:
        eng = create_engine(raw_url, pool_pre_ping=True)
        with eng.connect():
            log("TEST 3 (raw URL as in database.py): SUCCESS")
    except Exception as e:
        log(f"TEST 3 (raw URL as in database.py): FAILED -> {type(e).__name__}: {str(e)[:300]}")

with open("diagnose_output.txt", "w") as f:
    f.write("\n".join(lines))

print("Diagnostics written to diagnose_output.txt")

