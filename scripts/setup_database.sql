-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Table for medical cases
CREATE TABLE IF NOT EXISTS medical_cases (
    id serial PRIMARY KEY,
    case_id varchar(255) UNIQUE NOT NULL,
    age varchar(50),
    gender varchar(50),
    modality varchar(50) NOT NULL,
    body_part varchar(100) NOT NULL,
    diagnosis text NOT NULL,
    findings text,
    clinical_notes text,
    image_path text NOT NULL,
    image_url text,
    image_embedding vector(512) NOT NULL,
    text_embedding vector(512),
    source varchar(100) DEFAULT 'custom',
    metadata jsonb,
    created_at timestamptz DEFAULT NOW(),
    updated_at timestamptz DEFAULT NOW()
);

-- Create an HNSW index for fast approximate nearest neighbors
CREATE INDEX IF NOT EXISTS idx_medical_cases_image_embedding ON medical_cases USING ivfflat (image_embedding vector_cosine_ops) WITH (lists = 100);

-- Example helper function for similarity search (simple)
-- Note: adjust for performance tuning and HNSW parameters as needed
CREATE OR REPLACE FUNCTION search_similar_cases(query_embedding vector(512), limit_count int DEFAULT 10)
RETURNS SETOF medical_cases AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM medical_cases
    ORDER BY image_embedding <=> query_embedding
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Comments: To create a true HNSW index with pgvector later, follow pgvector docs and tune lists/m parameters.
