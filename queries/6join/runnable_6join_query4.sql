SELECT
    COUNT(*)
FROM
    title t,
    movie_companies mc,
    movie_info mi,
    movie_info_idx mi_idx,
    movie_keyword mk,
    keyword k,
    movie_link ml 
WHERE
    t.id=mc.movie_id AND
      t.id=mi.movie_id AND
      t.id=mi_idx.movie_id AND
      t.id=mk.movie_id AND
      mk.keyword_id=k.id AND
      t.id=ml.movie_id AND
      t.production_year<1998 AND
      mc.id<732952 AND
      mi.info_type_id=6 AND
      mi_idx.id<868476 AND
      mk.id<3048561 AND
      ml.linked_movie_id<1185038;