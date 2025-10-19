# --- ADD THIS CODE RIGHT AFTER ALL YOUR IMPORTS ---
import sys
if 'http' in sys.modules:
    print(f"DEBUG: Found http module at: {sys.modules['http'].__file__}")
# --- REMOVE THIS CODE ONCE YOU FIX THE PROBLEM ---
