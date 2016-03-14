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
$BODY$
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
$BODY$
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
$BODY$
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
$BODY$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_getCourseData (

)
RETURNS SETOF "course" AS
$BODY$
  BEGIN
    RETURN QUERY SELECT
      *
    FROM public."course";
  END;
$BODY$
LANGUAGE plpgsql;
