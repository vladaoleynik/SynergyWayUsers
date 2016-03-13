CREATE USER synergy_way WITH PASSWORD 'root';

CREATE DATABASE synergy_way_users
   WITH OWNER synergy_way
   TEMPLATE template0
   ENCODING 'SQL_ASCII'
   TABLESPACE  pg_default
   LC_COLLATE  'C'
   LC_CTYPE  'C'
   CONNECTION LIMIT  -1;

GRANT ALL PRIVILEGES ON DATABASE synergy_way_users TO synergy_way;
