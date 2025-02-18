class CategoryQueries:
    GET_ALL_CATEGORYS = "select group_concat(c.name) name_categorys from category c"

class FilmQueries:
    GET_ALL_YEAR = "select distinct release_year from film order by release_year"