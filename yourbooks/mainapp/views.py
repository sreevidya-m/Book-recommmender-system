import errno
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def home(request):
    return render(request, 'home.html')


new_df = pd.read_csv(
    "C:\\Users\\poona\\yourbooks\\mainapp\\cleaned_goodreads_data.csv", low_memory=False)


@login_required(login_url='../accounts/login')
def searchbooks(request, new_df=new_df):

    if request.method == "GET":
        query = request.GET.get('query', False)
        print("query:", query)

    # Function for recommending books based on Book title. It takes book title as input

    def recommend(title):    
        global rec
        title = title.lower()
        title = re.sub(r'[^\w\s]', '', title)
        # Getting genre of that title
        genre = new_df.loc[new_df['lower_title'] == title]['genre']
        genre = genre.iloc[0]
        # Matching the genre with the dataset and reset the index
        data = new_df.loc[new_df['genre'] == genre]  
        data.drop_duplicates(inplace=True)
        data.reset_index(level = 0, inplace = True) 
        # print(data)
    
        # Convert the index into series
        indices = pd.Series(data.index, index = data['lower_title'])
        
        #Converting the book description into vectors and used bigram
        tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df = 1, stop_words='english')
        tfidf_matrix = tf.fit_transform(data['cleaned_desc'].values.astype('U'))
        
        # Calculating the similarity measures based on Cosine Similarity
        sg = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Get the index corresponding to original_title
        
        idx = indices[title]# Get the pairwsie similarity scores 
        sig = list(enumerate(sg[idx]))# Sort the books
        # print(sig) 
        sig = sorted(sig, key=lambda x: x[1], reverse=True)# Scores of the 5 most similar books 
        sig = sig[0:6]# Book indicies
        movie_indices = [i[0] for i in sig]
    
        # Top 5 book recommendation
        rec = data.iloc[movie_indices]
        cols = ["index", "author",	"bookformat",	"desc",	"genre", "img",	"isbn",	"isbn13",	"link",	"pages",	"rating",	"reviews",	"title",	"totalratings"]
        return rec[cols]

    randomBooks = {}
    
    if query != False and query != "":
        try:
            randomBooks = recommend(query)
            randomBooks = randomBooks.T.to_dict()
            error = ""
        except Exception as e:
            error = "Please make sure you type the full book title."
    else:
        f = new_df.sample(8)
        randomBooks = f.T.to_dict()
        error = ""

    return render(request, 'searchbooks.html', {"randomBooks": randomBooks, "query": query, "error":error})


def bookdetails(request):
    return render(request, 'bookdetails.html')
