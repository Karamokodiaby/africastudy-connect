-- Demandes d'étude de profil envoyées depuis le formulaire du site.
CREATE TABLE IF NOT EXISTS leads (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
  name         TEXT NOT NULL,
  email        TEXT NOT NULL,
  phone        TEXT,
  country      TEXT NOT NULL,
  destination  TEXT NOT NULL,
  level        TEXT NOT NULL,
  formula      TEXT NOT NULL,
  postbac      INTEGER DEFAULT 0,
  message      TEXT,
  status       TEXT DEFAULT 'new',
  source       TEXT DEFAULT 'website'
);

CREATE INDEX IF NOT EXISTS idx_leads_status  ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at);
CREATE INDEX IF NOT EXISTS idx_leads_email   ON leads(email);
