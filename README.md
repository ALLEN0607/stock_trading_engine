# Stock Trading Engine (Python)

A simple, real-time stock trading simulation that matches buy and sell orders for up to 1024 tickers. This engine demonstrates how multiple threads can continuously generate orders while a separate matching thread scans and executes trades based on defined criteria.

## Overview
This project simulates a simplified version of a stock trading environment:
- **Order Generation**: Multiple threads generate random buy/sell orders.
- **Matching Engine**: A continuous process scans the order books, matching orders if the buy price is greater than or equal to the lowest sell price.
- **Data Structure Constraint**: Uses arrays/lists to store orders (no dictionaries or maps).
- **Time Complexity**: The matching algorithm is O(n) for each ticker’s order list.

It’s a great demonstration of concurrency, data structures, and basic matching logic.

## Features
1. **Support for 1024 Tickers**  
   Each ticker (0 to 1023) has its own buy and sell order list.

2. **Multi-threaded Order Generation**  
   Multiple worker threads generate random orders in parallel.

3. **Continuous Matching**  
   A separate thread continuously scans and matches orders in real-time.

4. **No Dictionaries or Maps**  
   Complies with the requirement to avoid advanced data structures; instead uses lists and manual indexing.

5. **Lock-Free Approach (within Python’s GIL)**  
   Demonstrates a basic concurrency approach without explicit locks, leveraging Python’s Global Interpreter Lock for thread safety in list appends.

## How It Works
1. **Order Creation**  
   - A `worker` thread calls `random_order_generator()` to produce orders with random parameters.  
   - Each order is appended to the buy or sell list (depending on order type).

2. **Matching Logic**  
   - The matching engine (`match_all_orders`) scans each ticker’s buy/sell lists.  
   - For each ticker, `matchOrder` finds the lowest sell price and tries to match it with a buy order whose price is >= that sell price.  
   - The quantity matched is the minimum of the two orders’ quantities, and both orders get updated accordingly.

3. **Multi-threading**  
   - Python’s `threading.Thread` is used to create separate threads for order generation and matching.  
   - A daemon thread continuously runs the matching engine every second, while other threads feed new orders.

## Installation
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/YourUsername/stock_trading_engine.git
   cd stock_trading_engine
