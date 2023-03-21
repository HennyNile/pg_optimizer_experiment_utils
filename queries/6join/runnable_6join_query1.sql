SELECT
    COUNT(*)
FROM
    title t,
    movie_companies mc,
    cast_info ci,
    movie_info_idx mi_idx,
    movie_keyword mk,
    keyword k,
    movie_link ml 
WHERE
    t.id=mc.movie_id AND 
    t.id=ci.movie_id AND 
    t.id=mi_idx.movie_id AND 
    t.id=mk.movie_id AND 
    mk.keyword_id=k.id AND 
    t.id=ml.movie_id AND 
    t.production_year<1945 AND 
    mc.id>554774 AND 
    ci.role_id=3 AND 
    mi_idx.id<377872 AND 
    mk.id<3484459 AND 
    ml.linked_movie_id>1506524;