class CategoryQueries:
    GET_ALL_CATEGORYS = "select c.name name_categorys from category c order by c.name"

class FilmQueries:
    GET_ALL_YEAR = "select distinct release_year release_year from film order by release_year desc"
    GET_FILM_BY_CATEGORYS = """SELECT 
                                f.title,
                                f.description,
                                c.name name_category,
                                f.release_year,
                                f.length,
                                concat( f.title,f.description) td
                            FROM
                                film f
                                JOIN film_category fc ON fc.film_id = f.film_id
                                JOIN category c ON c.category_id = fc.category_id                               
                                --where
                                --SET_PARAM_CATEGORYS  
                                --SET_PARAM_YEARS
                                --SET_PARAM_TEXT                                
                                """
    SET_PARAM_CATEGORYS = " c.name IN (%s) and "
    SET_PARAM_YEARS = " f.release_year in (%s) and "
    SET_PARAM_TEXT = " concat(f.title, f.description) like '%%%%{}%%%%' and "
