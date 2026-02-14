name: Daily NSE Swing Scanner

on:
  schedule:
    - cron: '0 13 * * 1-5'
  workflow_dispatch:

jobs:
  run-scanner:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          pip install pandas openpyxl

      - name: Run Scanner
        run: |
          python scanner.py

      - name: Upload Output File
        uses: actions/upload-artifact@v3
        with:
          name: swing-output
          path: swing_output.xlsx
