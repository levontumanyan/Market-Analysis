import os
import sys

# Add the project root to the sys.path so tests can find analyze.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
