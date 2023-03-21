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
      t.production_year=1944 AND
      mc.id>2160890 AND
      ci.role_id=7 AND
      mi.info_type_id=8 AND
      mi_idx.id>727802 AND
      mk.id>2930801;