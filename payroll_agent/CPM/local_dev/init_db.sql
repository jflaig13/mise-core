-- PostgreSQL schema for CPM payroll shifts
-- Mirrors BigQuery production schema exactly

CREATE TABLE IF NOT EXISTS shifts (
    -- Primary key for deduplication (filename-employee-date)
    row_id VARCHAR(255) PRIMARY KEY,

    -- Core shift data
    shift_date DATE NOT NULL,
    shift VARCHAR(10) NOT NULL,  -- AM or PM
    employee VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- server, busser, expo, utility, etc.
    category VARCHAR(50) DEFAULT 'foh',  -- foh or support

    -- Financial data
    amount_final DECIMAL(10, 2) NOT NULL,
    pool_hours DECIMAL(10, 2),
    food_sales DECIMAL(10, 2),

    -- Metadata
    filename VARCHAR(255),
    file_id VARCHAR(255),
    parsed_confidence VARCHAR(50),
    parser_version VARCHAR(50),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_shifts_date ON shifts(shift_date);
CREATE INDEX IF NOT EXISTS idx_shifts_employee ON shifts(employee);
CREATE INDEX IF NOT EXISTS idx_shifts_date_employee ON shifts(shift_date, employee);

-- View for human-readable queries
CREATE OR REPLACE VIEW shifts_summary AS
SELECT
    shift_date,
    shift,
    employee,
    role,
    amount_final,
    filename
FROM shifts
ORDER BY shift_date DESC, employee;

-- Grant permissions (for docker user)
GRANT ALL PRIVILEGES ON TABLE shifts TO payroll_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO payroll_user;
