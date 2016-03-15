-- Creating user and DB
CREATE USER synergy_way WITH PASSWORD 'root';

DROP DATABASE IF EXISTS users;
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
  "course_id" SERIAL NOT NULL PRIMARY KEY,
  "name" VARCHAR(80) NOT NULL,
  "code" VARCHAR(20) NOT NULL
);

CREATE TABLE "user" (
  "user_id" SERIAL NOT NULL PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL,
  "email" VARCHAR(80) NOT NULL,
  "mobile" VARCHAR(20) NULL,
  "phone" VARCHAR(20) NULL,
  "status" BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE "user_courses" (
  "id" SERIAL NOT NULL PRIMARY KEY,
  "user_id" INTEGER REFERENCES "user"(user_id)
                    ON DELETE CASCADE,
  "course_id" INTEGER REFERENCES course(course_id)
                      ON DELETE CASCADE,
  UNIQUE ("user_id", "course_id")
);
