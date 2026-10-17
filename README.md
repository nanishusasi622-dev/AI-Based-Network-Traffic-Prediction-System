# AI-Based Network Traffic Prediction System

A student-friendly Flask web application that accepts recent network-traffic values, forecasts the next six periods using a simple linear-trend regression baseline, visualizes history and predictions, and estimates load relative to a user-entered network capacity.

## Features
- Enter traffic values separated by commas.
- Forecast six future periods.
- View a line chart of history and forecast.
- Estimate projected load percentage.
- Show Normal, Moderate, or High load status.
- Responsive dashboard UI.

## Requirements
- Python 3.9 or newer
- Internet connection for loading Chart.js and Google Fonts from CDN (the prediction itself works locally).

## Run on Windows
1. Extract the ZIP file.
2. Open Command Prompt in the extracted project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application:
   ```bash
   python app.py
   ```
5. Open the local address shown in the terminal, usually `http://127.0.0.1:5000`.

## Example input
- Traffic values: `35, 42, 38, 50, 57, 54, 63, 68`
- Network capacity: `100`

## Important note
This is an educational demo using a basic linear regression trend, not a trained AI model and not a live network monitor. Results are illustrative and should not be used for real network operations.
