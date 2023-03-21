SELECT
       COUNT(*)
FROM
     title t,
     movie_companies mc,
     cast_info ci,
     movie_info mi,
     movie_info_idx mi_idx,
     movie_keyword mk,
     movie_link ml
WHERE
      t.id=mc.movie_id AND
      t.id=ci.movie_id AND
      t.id=mi.movie_id AND
      t.id=mi_idx.movie_id AND
      t.id=mk.movie_id AND
      t.id=ml.movie_id AND
      t.production_year<2014 AND
      mc.id<832942 AND
      ci.person_id>3486580 AND
      mi.info_type_id=108 AND
      mk.id<2469842 AND
      ml.linked_movie_id>2271661;