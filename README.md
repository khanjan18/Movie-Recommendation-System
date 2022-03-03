# Movie-Recommendation-System

This Movie Recommendation System takes a movie name as an input and recommends you some movies like the input movie based on similarity between them. It also shows you information about input movie and the details of cast who have acted in it. These recommendation system consists of only Hollywood movies. 

The details of movie such as (title, genres, poster, status, runtime, release date, IMDB Rating etc) have been fetched from TMDB API  https://www.themoviedb.org/documentation/api.

`CountVectorizer` and `PorterStemmer` are used to stem the words and create the tags column values into vectors.

To create the recommendation system, `cosine_similarity` method is used which compares vectors with other vectors and gives similarity between 0 and 1.

To get the final data after preprocessing and model file from Jupyter Notebook to app.py, `pickle` is used.


## TMDB API Key
Create an account in https://www.themoviedb.org/, click on the `API` link from the left hand sidebar in your account settings and fill all the details to apply for API key. If you are asked for the website URL, just give "NA" if you don't have one. You will see the API key in your API sidebar once your request is approved.

## Cosine Similarity
Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.

## Sources Of Datasets

- [TMDB 5000 Movies](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset)
- [The Movies Datset](https://www.kaggle.com/rounakbanik/the-movies-dataset)
- [2018 Movies](https://en.wikipedia.org/wiki/List_of_American_films_of_2018)
- [2019 Movies](https://en.wikipedia.org/wiki/List_of_American_films_of_2019)
- [2020 Movies](https://en.wikipedia.org/wiki/List_of_American_films_of_2020)
- [2021 Movies](https://en.wikipedia.org/wiki/List_of_American_films_of_2021)
