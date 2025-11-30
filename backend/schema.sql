-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Table to track the raw upload/scan event
CREATE TABLE scan_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_url TEXT NOT NULL,
    scan_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(50) CHECK (status IN ('PENDING', 'PROCESSED', 'FAILED')),
    raw_llm_response JSONB,
    confidence_score FLOAT,
    metadata_info JSONB
);

-- 2. Table for individual inventory items extracted from scans
CREATE TABLE inventory_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scan_id UUID REFERENCES scan_events(id) ON DELETE CASCADE,
    item_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    quantity NUMERIC(10, 2) NOT NULL DEFAULT 1.0,
    unit VARCHAR(50) DEFAULT 'pcs',
    unit_price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_inventory_item_name ON inventory_items(item_name);
CREATE INDEX idx_scan_event_status ON scan_events(status);
