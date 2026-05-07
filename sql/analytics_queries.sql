-- Average closing price per stock
SELECT ticker, AVG(close) AS avg_close
FROM stock_prices
GROUP BY ticker;

-- Highest price per stock
SELECT ticker, MAX(high) AS max_price
FROM stock_prices
GROUP BY ticker;

-- Total volume traded
SELECT ticker, SUM(volume) AS total_volume
FROM stock_prices
GROUP BY ticker;