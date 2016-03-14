\c synergy_way_users synergy_way;

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
DECLARE _page_number BIGINT;

BEGIN
 -- Construct paging parameter
 IF (_page_size IS NOT NULL AND _page_number IS NOT NULL) THEN
  _page_number := (_page_size * (_page_number - 1));
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
 ORDER BY user_id
 LIMIT _page_size
 OFFSET _page_number;

 EXCEPTION WHEN OTHERS THEN
 RAISE;
END;
$BODY$
LANGUAGE 'plpgsql';