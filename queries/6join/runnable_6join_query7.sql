SELECT
       COUNT(*)
FROM
     title t,
     movie_companies mc,
     cast_info ci,
     movie_info mi,
     movie_info_idx mi_idx,
     movie_keyword mk,
     keyword k
WHERE
      t.id=mc.movie_id AND
      t.id=ci.movie_id AND
      t.id=mi.movie_id AND
      t.id=mi_idx.movie_id AND
      t.id=mk.movie_id AND
      mk.keyword_id=k.id AND
      t.production_year>1893 AND
      mc.id<1222723 AND
      ci.role_id=6 AND
      mi.id<5073257 AND
      mi_idx.id>650731 AND
      mk.id=3900105;