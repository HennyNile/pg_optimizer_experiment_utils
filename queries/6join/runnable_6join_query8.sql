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
      t.production_year=2011 AND
      mc.id>612789 AND
      ci.role_id=4 AND
      mi.id<2550795 AND
      mk.id<2310057 AND
      ml.linked_movie_id<83265;