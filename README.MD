# Knitting Pi

A Python application for generating and visualizing circular knitting charts.

## Features

- Modular codebase for knitting chart logic
- Random chart generation
- Console output of knitting charts
- Easily extensible for new stitch types and rules

## Project Structure

```
knitting-pi/
├── src/
│   ├── app.py
│   ├── circular_chart.py
│   ├── row.py
│   ├── stitch.py
│   ├── rules.py
│   └── __init__.py
├── README.md
```

## Getting Started

1. **Install Python 3.8+**

2. **Clone the repository**
   ```bash
   git clone https://github.com/koehlepe/knitting-pi.git
   cd knitting-pi
   ```

3. **Run the application**
   ```bash
   python -m src.app
   ```

## Usage

The main entry point is `src/app.py`.  
You can modify `main()` to generate different charts or integrate with other modules.

## Extending

- Add new stitch types in `stitch.py`
- Add new rules in `rules.py`
- Extend chart logic in `circular_chart.py`
