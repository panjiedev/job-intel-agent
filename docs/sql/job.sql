CREATE TABLE IF NOT EXISTS job (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_name TEXT NOT NULL,
  salary_desc TEXT,
  post_description TEXT,
  work_address TEXT,
  show_skills TEXT,
  experience_name TEXT,
  degree_name TEXT,
  position_name TEXT
);