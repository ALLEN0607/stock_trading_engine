import threading
import random
import time

# Define the maximum number of tickers (stocks)
MAX_TICKERS = 1024

# Initialize order books:
# Each ticker (index 0 to 1023) has its own list for buy orders and sell orders.
buy_orders = [[] for _ in range(MAX_TICKERS)]
sell_orders = [[] for _ in range(MAX_TICKERS)]

def addOrder(order_type, ticker, quantity, price):
    """
    Add an order to the order book.
    
    Parameters:
    - order_type: "Buy" or "Sell"
    - ticker: an integer (0 to 1023) representing the stock ticker
    - quantity: the order quantity
    - price: the order price
    """
    order = (quantity, price)
    if order_type == "Buy":
        buy_orders[ticker].append(order)
    elif order_type == "Sell":
        sell_orders[ticker].append(order)
    else:
        print("Invalid order type:", order_type)

def random_order_generator():
    """
    Randomly generate order parameters.
    
    Returns:
    A tuple (order_type, ticker, quantity, price)
    """
    order_type = random.choice(["Buy", "Sell"])
    ticker = random.randint(0, MAX_TICKERS - 1)
    quantity = random.randint(1, 100)
    price = random.randint(10, 200)
    return order_type, ticker, quantity, price

def worker(num_orders):
    """
    Worker function for each thread to generate and add random orders.
    
    Parameters:
    - num_orders: number of orders to generate.
    """
    for _ in range(num_orders):
        order = random_order_generator()
        addOrder(*order)

def matchOrder(ticker):
    """
    For a given ticker, match buy and sell orders.
    
    Matching criteria:
    - Find the sell order with the lowest price.
    - Find the first buy order with a price >= that lowest sell price.
    - Execute a trade for the quantity equal to the smaller of the two orders.
    - Update the order books by reducing quantities or removing fully matched orders.
    
    Parameters:
    - ticker: stock ticker number (integer)
    """
    buys = buy_orders[ticker]
    sells = sell_orders[ticker]
    
    if not buys or not sells:
        return

    while sells and buys:
        # Find the sell order with the lowest price
        min_sell_index = 0
        min_sell_price = sells[0][1]
        for i in range(1, len(sells)):
            if sells[i][1] < min_sell_price:
                min_sell_index = i
                min_sell_price = sells[i][1]
        
        matched = False
        # Look for the first buy order that meets the condition: price >= min_sell_price
        for j in range(len(buys)):
            if buys[j][1] >= min_sell_price:
                matched = True
                trade_qty = min(buys[j][0], sells[min_sell_index][0])
                print(f"Match Order: Ticker {ticker} traded at price {min_sell_price} for quantity {trade_qty}")
                
                new_buy_qty = buys[j][0] - trade_qty
                new_sell_qty = sells[min_sell_index][0] - trade_qty
                
                # Update the buy order: remove it if fully executed, or update the remaining quantity.
                if new_buy_qty == 0:
                    buys.pop(j)
                else:
                    buys[j] = (new_buy_qty, buys[j][1])
                
                # Update the sell order similarly.
                if new_sell_qty == 0:
                    sells.pop(min_sell_index)
                else:
                    sells[min_sell_index] = (new_sell_qty, sells[min_sell_index][1])
                
                # Break out after one successful match and then re-check if further matches are possible.
                break
        
        if not matched:
            break

def match_all_orders():
    """
    Continuously scan all tickers and attempt to match orders.
    This function simulates a real-time matching engine.
    """
    while True:
        for ticker in range(MAX_TICKERS):
            matchOrder(ticker)
        time.sleep(1)  # Pause for 1 second between full scans

def run_tests():
    """
    Run enriched test cases to demonstrate the functionality of the order system.
    """
    # Test Case 1: Manual orders for a specific ticker
    test_ticker = 50
    # Clear the order book for the test ticker
    buy_orders[test_ticker] = []
    sell_orders[test_ticker] = []
    
    # Add manual test orders:
    # Buy order: 20 shares at price 100
    addOrder("Buy", test_ticker, 20, 100)
    # Sell orders: 15 shares at price 90 and 10 shares at price 95
    addOrder("Sell", test_ticker, 15, 90)
    addOrder("Sell", test_ticker, 10, 95)
    
    print("\n--- Test Case 1: Manual Orders ---")
    print("Before matching:")
    print("Buy orders:", buy_orders[test_ticker])
    print("Sell orders:", sell_orders[test_ticker])
    
    # Execute matching for the test ticker
    matchOrder(test_ticker)
    
    print("After matching:")
    print("Buy orders:", buy_orders[test_ticker])
    print("Sell orders:", sell_orders[test_ticker])
    
    # Test Case 2: Multi-threaded order generation with real-time matching
    print("\n--- Test Case 2: Multi-threaded Order Generation ---")
    
    # Start the matching engine thread as a daemon so it stops when the main thread exits.
    matching_thread = threading.Thread(target=match_all_orders, daemon=True)
    matching_thread.start()
    
    # Create multiple threads to generate random orders.
    threads = []
    num_threads = 5
    orders_per_thread = 20
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(orders_per_thread,))
        threads.append(t)
        t.start()
    
    # Wait for all order generation threads to finish.
    for t in threads:
        t.join()
    
    # Allow the matching engine to process orders for a few seconds.
    time.sleep(5)
    print("Real-time matching simulation completed.")

if __name__ == "__main__":
    run_tests()
