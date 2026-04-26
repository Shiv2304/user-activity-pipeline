CREATE TABLE events_raw (
    event_id SERIAL PRIMARY KEY,
    user_id INT,
    event_type TEXT,
    event_timestamp TIMESTAMP,
    feature TEXT
);

CREATE INDEX idx_events_raw_user_id ON events_raw (user_id);
CREATE INDEX idx_events_raw_event_timestamp ON events_raw (event_timestamp);
