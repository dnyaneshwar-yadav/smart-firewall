import os

# ==============================
# Project Information
# ==============================
PROJECT_NAME = "Smart Firewall"

# ==============================
# Base Directory
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==============================
# Database
# ==============================
DATABASE_PATH = os.path.join(BASE_DIR, "database", "firewall.db")

# ==============================
# Logs
# ==============================
LOG_FOLDER = os.path.join(BASE_DIR, "logs")

# ==============================
# Flask
# ==============================
SECRET_KEY = "smart_firewall_secret"

# ==============================
# Network
# ==============================
DEFAULT_INTERFACE = "any"

# ==============================
# Debug
# ==============================
DEBUG = True


# ==========================
# Firewall Mode
# ==========================

SIMULATION_MODE = True
