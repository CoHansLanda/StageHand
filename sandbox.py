import imdb
ia = imdb.IMDb()
items = ia.search_movie('Avengers')
for i in items:
    print(i)