import streamlit as st
import pandas as pd
import json


def load_library():
    try:
        with open('library.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
            return []
        
def save_library(library):
    with open('library.json', 'w') as file:
        json.dump(library, file, indent=4)
        
library = load_library()
st.title("Personal Library Manager")
st.write("Manage your personal library of books.")
st.sidebar.title("Library Management")

menu = st.sidebar.radio("Select an option", ("View Library", "Add Book", "Remove Book", "Search Book", "Save and Exit"))
if menu == "View Library":
    st.sidebar.title("Your Library")
    if library:
        st.table(library)
    else:
        st.write("No books in the library yet, add some books!")
        
elif menu == "Add Book":
    st.sidebar.title("Add a new book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=2022, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as read")
    
    if st.button("Add Book"):
        library.append({
            "Title": title,
            "Author": author,
            "Year": year,
            "Genre": genre,
            "Read": read_status
        })
        save_library(library)
        st.success(f"Book '{title}' added to the library!")
        st.rerun()
        
elif menu == "Remove Book":
    st.sidebar.header("Remove a book")
    book_titles = st.selectbox("Select a book to remove", [book['Title'] for book in library])
    
    if book_titles:
        selected_book = st.selectbox("Select a book to remove", book_titles, key="remove_book_selectbox")
        if st.button("Remove Book"):
            library = [book for book in library if book["Title"] != selected_book]
            save_library(library)
            st.success(f"Book '{selected_book}' removed from the library!")
            st.rerun()
            
            
elif menu == "Search Book":
    st.sidebar.title("Search for a book")
    search_term = st.text_input("Enter title or author to search")
    
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book["Title"].lower() or search_term.lower() in book["Author"].lower()]
        if results:
            st.table(results)
        else:
            st.warning("No books found matching your search.")
            
elif menu == "Save and Exit":
    st.sidebar.markdown("Save and Exit")
    save_library(library)
    st.success("Library saved successfully!")
    st.stop()