-- Creating user and DB
CREATE USER synergy_way WITH PASSWORD 'root';

CREATE DATABASE users
   WITH OWNER synergy_way
   TEMPLATE template0
   ENCODING 'SQL_ASCII'
   TABLESPACE  pg_default
   LC_COLLATE  'C'
   LC_CTYPE  'C'
   CONNECTION LIMIT  -1;

GRANT ALL PRIVILEGES ON DATABASE users TO synergy_way;

-- Connect to created DB
\c users synergy_way;

-- Creating DB schema
CREATE TABLE "course" (
  "course_id" serial NOT NULL PRIMARY KEY,
  "name" varchar(80) NOT NULL,
  "code" varchar(20) NOT NULL
);

CREATE TABLE "user" (
  "user_id" serial NOT NULL PRIMARY KEY,
  "name" varchar(100) NOT NULL,
  "email" varchar(254) NOT NULL,
  "mobile" varchar(20) NULL,
  "phone" varchar(20) NULL,
  "status" boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE "user_courses" (
  "id" serial NOT NULL PRIMARY KEY,
  "user_id" integer NOT NULL,
  "course_id" integer NOT NULL,
  UNIQUE ("user_id", "course_id")
);
