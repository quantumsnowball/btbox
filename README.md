# BTBox

BTBox is a simple to use event-driven backtesting tool written in Python. The goal of this project is to provide a simple interface for backtesting trading strategy.

# Design

Chainn of object compositions as follows:
backtest -> strategy -> broker -> market -> datasource
