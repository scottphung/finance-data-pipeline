SELECT ticker, AVG(close)
FROM stock_prices
GROUP BY ticker;

SELECT ticker, MAX(high)
FROM stock_prices
GROUP BY ticker;