\c users synergy_way;

CREATE OR REPLACE FUNCTION fn_GetUserData (
  _page_size INTEGER = NULL,
  _page_number INTEGER = NULL
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
 ORDER BY "user".name
 LIMIT _page_size
 OFFSET page_number;

 EXCEPTION WHEN OTHERS THEN
 RAISE;
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
  END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION fn_updateUserCourseData (
       _user_id INTEGER,
       _course_ids INTEGER[]
) RETURNS VOID AS
$$
BEGIN
  -- Lock the containing object tuple to prevernt inserts into the
  -- collection table.
  PERFORM true FROM "user" WHERE "user".user_id = _user_id FOR UPDATE;

  IF (EXISTS (SELECT * FROM user_courses WHERE "user_courses".user_id = _user_id))
    THEN
      DELETE FROM user_courses
        WHERE "user_courses".user_id = _user_id;
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
  _email VARCHAR(100),
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

  PERFORM public.fn_updateUserCourseData(_user_id, _course_ids);

  RETURN FOUND;
END;
$$
LANGUAGE plpgsql;
