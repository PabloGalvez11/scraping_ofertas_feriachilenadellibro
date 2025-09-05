CREATE DATABASE feriachilenadellibro_db;

CREATE USER feriachilenadellibro_user WITH ENCRYPTED PASSWORD 'feriachilenadellibro';

GRANT ALL ON DATABASE feriachilenadellibro_db TO feriachilenadellibro_user;
