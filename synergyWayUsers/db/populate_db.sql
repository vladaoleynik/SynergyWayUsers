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

INSERT INTO "course" (
  name, code
) VALUES
    ('Python', 'C0001'),
    ('Databases', 'C0002'),
    ('FrontEnd', 'C0003'),
    ('Python/Django', 'C0004'),
    ('Java', 'C0005'),
    ('JavaScript', 'C0006');


CREATE TABLE "user" (
  "user_id" SERIAL NOT NULL PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL,
  "email" VARCHAR(80) NOT NULL,
  "mobile" VARCHAR(20) NULL,
  "phone" VARCHAR(20) NULL,
  "status" BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO "user" (
  name, email, mobile, phone, status
) VALUES
    ('Stephen King', 'king@email.com', '380960248369', NULL, FALSE),
    ('Edgar Poe', 'poe@email.com', NULL, NULL, TRUE),
    ('John Tolkien', 'tolkien@email.com', NULL, NULL, FALSE),
    ('George Martin', 'martin@email.com', NULL, NULL, FALSE),
    ('Isaac Azimov', 'azimov@email.com', NULL, NULL, TRUE),
    ('Charles Dickens', 'dickens@email.com', NULL, NULL, FALSE),
    ('Howard Lovecraft', 'lovecraft@email.com', NULL, NULL, FALSE),
    ('Leo Tolstoy', 'tolstoy@email.com', NULL, NULL, FALSE),
    ('August Derlet', 'derlet@email.com', NULL, NULL, FALSE),
    ('Clark Smith', 'smith@email.com', NULL, NULL, TRUE),
    ('Francis Fitzgerald', 'fitzgerald@email.com', NULL, NULL, TRUE),
    ('Erich Remarque', 'remarque@email.com', NULL, NULL, FALSE),
    ('Quentin Tarantino', 'tarantino@email.com', NULL, NULL, FALSE),
    ('Tim Burton', 'burton@email.com', NULL, NULL, TRUE),
    ('Deep Purple', 'purple@email.com', NULL, NULL, TRUE),
    ('Def Leppard', 'leppard@email.com', NULL, NULL, FALSE),
    ('Udo Dirkschneider', 'dirkschneider@email.com', NULL, NULL, FALSE),
    ('ZZ Top', 'zz_top@email.com', NULL, NULL, TRUE),
    ('AC/DC', 'ac_dc@email.com', NULL, NULL, TRUE),
    ('Scorpions', 'scorpions@email.com', NULL, NULL, FALSE);


CREATE TABLE "user_courses" (
  "id" SERIAL NOT NULL PRIMARY KEY,
  "user_id" INTEGER REFERENCES "user"(user_id)
                    ON DELETE CASCADE,
  "course_id" INTEGER REFERENCES course(course_id)
                      ON DELETE CASCADE,
  UNIQUE ("user_id", "course_id")
);

INSERT INTO "user_courses" (
  user_id, course_id
) VALUES
    (1, 1),
    (1, 2),
    (1, 5),
    (5, 3),
    (6, 4),
    (6, 1);


-- Creating procedures
CREATE OR REPLACE FUNCTION fn_GetUserData (
  _page_size INTEGER = NULL,
  _page_number INTEGER = NULL,
  _search_str VARCHAR(20) = '.'
)
RETURNS TABLE (
  "id" INTEGER,
  "name" VARCHAR,
  "email" VARCHAR,
  "mobile" VARCHAR,
  "phone" VARCHAR,
  "status" BOOLEAN,
  "full_count" BIGINT
) AS
$$
DECLARE page_number BIGINT;

BEGIN
 -- Construct paging parameter
  IF (_page_size IS NOT NULL AND _page_number IS NOT NULL) THEN
    page_number := (_page_size * (_page_number - 1));
  END IF;

  IF (_search_str IS NULL) THEN
    _search_str := '.';
  END IF;

  RETURN QUERY
  SELECT
    "user".user_id,
    "user".name,
    "user".email,
    "user".mobile,
    "user".phone,
    "user".status,
    COUNT(*) OVER() AS full_count
  FROM public.user
  WHERE "user".name ~* _search_str
  ORDER BY "user".name
  LIMIT _page_size
  OFFSET page_number;
EXCEPTION WHEN OTHERS THEN
  ROLLBACK;
END;
$$
LANGUAGE 'plpgsql';


CREATE OR REPLACE FUNCTION fn_getUserById (
  _user_id BIGINT
)
RETURNS TABLE (
  "id" INTEGER,
  "name" VARCHAR,
  "email" VARCHAR,
  "mobile" VARCHAR,
  "phone" VARCHAR,
  "status" BOOLEAN,
  "course_id" INTEGER,
  "course_name" VARCHAR,
  "course_code" VARCHAR
) AS
$$
  BEGIN
    RETURN QUERY SELECT
      "user".*,
      "course".course_id course_id,
      "course".name course_name,
      "course".code course_code
    FROM public."user"
    LEFT JOIN "user_courses" ON ("user".user_id = "user_courses".user_id)
    LEFT JOIN "course" ON ("user_courses".course_id = "course".course_id)
    WHERE "user".user_id = _user_id;
  EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
  END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_getCourseData (

)
RETURNS SETOF "course" AS
$$
  BEGIN
    RETURN QUERY SELECT
      *
    FROM public."course";
  EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
  END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_createUpdateUserCourseData (
  _user_id BIGINT,
  _course_ids INTEGER[],
  _update_flag BOOLEAN DEFAULT TRUE
) RETURNS VOID AS
$$
BEGIN
  IF _update_flag THEN
    PERFORM true FROM "user" WHERE "user".user_id = _user_id FOR UPDATE;

    IF (EXISTS (SELECT * FROM user_courses WHERE "user_courses".user_id = _user_id))
      THEN
        DELETE FROM user_courses
          WHERE "user_courses".user_id = _user_id;
    END IF;
  END IF;

  INSERT INTO user_courses (user_id, course_id)
  SELECT _user_id, _course_ids[gs.ser]
  FROM generate_series(1, array_upper(_course_ids, 1))
    AS gs(ser);
END;
$$
LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION fn_updateUser(
  _user_id INTEGER,
  _name VARCHAR(100),
  _email VARCHAR(80),
  _mobile VARCHAR(20),
  _phone VARCHAR(20),
  _status BOOLEAN,
  _course_ids INTEGER[]
)
RETURNS BOOLEAN SECURITY DEFINER AS
$$
-- Returns true if the user was updated, and false if not.
BEGIN
  PERFORM true FROM "user" WHERE "user".user_id = _user_id FOR UPDATE;

  UPDATE "user"
    SET name = COALESCE(_name, "user".name),
      email = COALESCE(_email, "user".email),
      mobile = COALESCE(_mobile, "user".mobile),
      phone = COALESCE(_phone, "user".phone),
      status = COALESCE(_status, "user".status)
  WHERE "user".user_id = _user_id;

  PERFORM fn_createUpdateUserCourseData(_user_id, _course_ids);

  RETURN FOUND;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_deleteUser (
  _user_id INTEGER
) RETURNS INTEGER AS
$$
DECLARE
  affected_rows NUMERIC DEFAULT 0;

BEGIN
  DELETE FROM "user"
    WHERE "user".user_id = _user_id;
  GET DIAGNOSTICS affected_rows = ROW_COUNT;
  RETURN affected_rows;
EXCEPTION WHEN OTHERS THEN
  ROLLBACK;
  RETURN affected_rows;
END;
$$
LANGUAGE plpgsql SECURITY DEFINER;


CREATE OR REPLACE FUNCTION fn_createUser(
  _name VARCHAR(100),
  _email VARCHAR(80),
  _mobile VARCHAR(20),
  _phone VARCHAR(20),
  _status BOOLEAN,
  _course_ids INTEGER[]
)
RETURNS BOOLEAN AS
$$
DECLARE created_id BIGINT;

BEGIN
  INSERT INTO "user" (
    name, email, mobile, phone, status
  )
  VALUES (
    _name, _email, _mobile, _phone, _status
  ) RETURNING user_id INTO created_id;
  PERFORM fn_createUpdateUserCourseData(created_id, _course_ids, FALSE );
  RETURN FOUND;
END;
$$
LANGUAGE plpgsql SECURITY DEFINER;

