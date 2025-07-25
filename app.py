import streamlit as st
import pandas as pd 
import numpy as np
import pickle as pkl 

st.set_page_config(layout="wide")

st.header("Book Recommender System")

st.markdown('''
            #### we recommend top 50 books 
            ''')

# import our models 
# rb stands for read(binary)   --> reading binary files

popular = pkl.load(open("popular.pkl","rb"))
books = pkl.load(open("books.pkl","rb"))
pt = pkl.load(open("pt.pkl","rb"))
similarity_scores = pkl.load(open("similarity_scores.pkl","rb"))

# to 50 books 



st.sidebar.title("Top 50 Books")

if st.sidebar.button("show"):
    cols_per_row = 5 
    num_rows = 10 
    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row):
            book_idx = row * cols_per_row + col 
            if book_idx < len(popular):
                with cols[col]:
                    st.image(popular.iloc[book_idx]['Image-URL-M']) # Displays the image
                    st.text(popular.iloc[book_idx]['Book-Title']) # Displays the Book Title
                    st.text(popular.iloc[book_idx]['Book-Author'])

# function to recommed books

def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x : x[1], reverse=True)[1:6]
    # Lets create empty list and in that lies i want ot populate with the book information 
    # Book author book-title image url 
    # Empty list 
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item) 
    return data                    

# this is giving the names list of books
book_list = pt.index.values    

st.sidebar.title("similar Book suggestions")
# drop down to select the books 
selected_book = st.sidebar.selectbox("slelect a book from the dropdown",book_list)


if st.sidebar.button("Recommend me "): 
    book_recommend = recommend(selected_book)
    cols = st.columns(5)
    for col_idx in range(5):
        with cols[col_idx]:
            if col_idx < len(book_recommend):
                st.image(book_recommend[col_idx][2])
                st.text(book_recommend[col_idx][0])
                st.text(book_recommend[col_idx][1]) 


#import data

#import data

books = pd.read_csv("Data/Books.csv")
users = pd.read_csv("Data/Users.csv")
ratings = pd.read_csv("Data/Ratings.csv")

st.sidebar.title("Data Used")

if st.sidebar.button("SHOW"):
    st.subheader("this is the books data we used in our model")
    st.dataframe(books)
    st.subheader("this is the users rating data we used in our model")
    st.dataframe(ratings)
    st.subheader("this is the user data we used in our model")
    st.dataframe(users)


                
                  








                       