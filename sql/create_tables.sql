CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    date DATE,
    ticker TEXT,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT
);