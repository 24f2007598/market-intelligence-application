CREATE TABLE competitors (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    competitor_id INT REFERENCES competitors(id),
    url TEXT,
    page_type TEXT, -- pricing, product, landing
    snapshot_date TIMESTAMP
);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    page_id INT REFERENCES pages(id),
    raw_text TEXT,
    cleaned_text TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    source TEXT, -- Gartner
    company TEXT,
    review_text TEXT,
    rating FLOAT,
    date TIMESTAMP,
    sentiment_label TEXT,
    sentiment_score FLOAT,
    sentiment_updated_at TIMESTAMP
);

CREATE TABLE changes (
    id SERIAL PRIMARY KEY,
    url TEXT,
    snapshot_date TIMESTAMP,
    old_text TEXT,
    new_text TEXT,
    change_type TEXT,
    change_confidence FLOAT
);