# BTBox

BTBox is a simple to use event-driven backtesting tool written in Python. The goal of this project is to provide a simple interface for backtesting trading strategy.

# Install

```
pip install -e .
```

# Design

Chainn of object compositions as follows:
backtest -> job -> strategy -> broker -> market -> datasource
