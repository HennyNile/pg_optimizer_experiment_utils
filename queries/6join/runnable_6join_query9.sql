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
      t.production_year=1984 AND
      mc.id<1894986 AND
      ci.role_id=5 AND
      mi.id<2510347 AND
      mi_idx.id>13742 AND
      ml.linked_movie_id>596167;