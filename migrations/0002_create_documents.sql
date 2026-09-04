-- Documents transmis par les candidats, stockés dans R2.
-- La table ne garde que la référence : le fichier vit dans le bucket.
CREATE TABLE IF NOT EXISTS documents (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  email       TEXT NOT NULL,
  r2_key      TEXT NOT NULL UNIQUE,
  filename    TEXT NOT NULL,
  mime_type   TEXT,
  size_bytes  INTEGER
);

CREATE INDEX IF NOT EXISTS idx_documents_email ON documents(email);
