
This project provides an interactive application for visualizing stock data and financial indicators. 

## Key Features

- **Data Processing**: Utilizes `pandas` and `numpy` for efficient data manipulation, including financial indicator calculations like exponential moving averages, MACD, and RSI.
- **Interactive Plotting**: Integrates `matplotlib` plots within a `PyQt5` application to render stock charts that support user interactions like line-drawing and zooming.

## Structure

The project is organized into scripts that focus on specific functionalities:
- `indicators.py`: Contains the financial indicator calculation functions.
- `plotting.py`: Contains all plotting functions and utilities for visual representation.
- `app.py`: Contains the PyQt5 application interface, managing user interactions with the charts.
- `main.py`: Serves as the application's entry point, orchestrating data fetching, processing, and UI initialization.

## Getting Started

To run the application, clone the repository and set up your environment with the following commands:

```bash
git clone https://github.com/AnnaTz/stock-plotter-pyqt5.git
cd stock-plotter-pyqt
pip install -r requirements.txt
python main.py
```
