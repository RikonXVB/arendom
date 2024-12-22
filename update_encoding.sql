UPDATE pg_database SET encoding = pg_char_to_encoding('UTF8')
WHERE datname = 'arendom';

ALTER DATABASE arendom SET client_encoding TO 'UTF8'; 