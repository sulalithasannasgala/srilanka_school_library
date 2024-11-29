import streamlit as st
import pandas as pd
import numpy as np

# Function to save data to CSV
def save_data(df, filename):
    df.to_csv(filename, index=False)

# Function to load data from CSV
def load_data(filename, default_data):
    try:
        return pd.read_csv(filename, encoding='utf-8')
    except FileNotFoundError:
        st.warning(f"File {filename} not found. Creating a new one.")
        return pd.DataFrame(default_data)
    except pd.errors.ParserError:
        st.error(f"Error parsing {filename}. Please check the file format.")
        return pd.DataFrame(default_data)

# Function to handle member details page
def member_details_page(page_name, filename):
    st.title("Library Database App")
    st.subheader(page_name)

    member_data = {'name': [], 'address': [], 'contact': []}
    member_df = load_data(filename, member_data)

    name = st.text_input("Name", key=f"{page_name}_name")
    address = st.text_input("Address", key=f"{page_name}_address")
    contact = st.text_input("Contact", key=f"{page_name}_contact")

    if st.button("Submit", key=f"{page_name}_submit"):
        if name and address and contact:
            new_member = pd.DataFrame({'name': [name], 'address': [address], 'contact': [contact]})
            member_df = pd.concat([member_df, new_member], ignore_index=True)
            save_data(member_df, filename)
            st.success("Member added successfully!")
        else:
            st.error("Please enter name, address, and contact.")

    if st.button("Delete", key=f"{page_name}_delete"):
        if name:
            member_df = member_df[member_df['name'] != name]
            save_data(member_df, filename)
            st.success("Member deleted successfully!")
        else:
            st.error("Please enter the name of the member to delete.")

    if st.button("Search", key=f"{page_name}_search"):
        if name:
            result = member_df[member_df['name'] == name]
            st.write(result)
        else:
            st.error("Please enter the name of the member to search.")

# Navigation
st.sidebar.title("Library Database App")
pages = ["Home", "Book Details", "Inventory Details", "Misuse Book Details"] + [f"Member Details {i}" for i in range(1, 15)] + ["Teachers Details", "Non-Academic Details", "Other Member Details"]
page = st.sidebar.radio("Go to", pages, key="navigation")

# Home Page
if page == "Home":
    st.title("Library Database App")
    st.subheader("Home Page")
    st.write("Welcome to the Library Database App. Use the sidebar to navigate to different sections.")

# Book Details Page
elif page == "Book Details":
    st.title("Library Database App")
    st.subheader("Book Details")

    book_data = {'title': [], 'author': []}
    book_df = load_data('books.csv', book_data)

    title = st.text_input("Title", key="book_title")
    author = st.text_input("Author", key="book_author")

    if st.button("Submit", key="book_submit"):
        if title and author:
            new_book = pd.DataFrame({'title': [title], 'author': [author]})
            book_df = pd.concat([book_df, new_book], ignore_index=True)
            save_data(book_df, 'books.csv')
            st.success("Book added successfully!")
        else:
            st.error("Please enter both title and author.")

    if st.button("Delete", key="book_delete"):
        if title:
            book_df = book_df[book_df['title'] != title]
            save_data(book_df, 'books.csv')
            st.success("Book deleted successfully!")
        else:
            st.error("Please enter the title of the book to delete.")

    if st.button("Search", key="book_search"):
        if title:
            result = book_df[book_df['title'] == title]
            st.write(result)
        else:
            st.error("Please enter the title of the book to search.")

# Inventory Details Page
elif page == "Inventory Details":
    st.title("Library Database App")
    st.subheader("Inventory Details")

    inventory_data = {'item': [], 'quantity': []}
    inventory_df = load_data('inventory.csv', inventory_data)

    item = st.text_input("Item", key="inventory_item")
    quantity = st.number_input("Quantity", min_value=0, key="inventory_quantity")

    if st.button("Submit", key="inventory_submit"):
        if item and quantity:
            new_inventory = pd.DataFrame({'item': [item], 'quantity': [quantity]})
            inventory_df = pd.concat([inventory_df, new_inventory], ignore_index=True)
            save_data(inventory_df, 'inventory.csv')
            st.success("Inventory item added successfully!")
        else:
            st.error("Please enter both item and quantity.")

    if st.button("Delete", key="inventory_delete"):
        if item:
            inventory_df = inventory_df[inventory_df['item'] != item]
            save_data(inventory_df, 'inventory.csv')
            st.success("Inventory item deleted successfully!")
        else:
            st.error("Please enter the item to delete.")

    if st.button("Search", key="inventory_search"):
        if item:
            result = inventory_df[inventory_df['item'] == item]
            st.write(result)
        else:
            st.error("Please enter the item to search.")

# Misuse Book Details Page
elif page == "Misuse Book Details":
    st.title("Library Database App")
    st.subheader("Misuse Book Details")

    misuse_data = {'book': [], 'member_name': []}
    misuse_df = load_data('masuse_books.csv', misuse_data)

    book = st.text_input("Book", key="misuse_book")
    member_name = st.text_input("Member Name", key="misuse_member_name")

    if st.button("Submit", key="misuse_submit"):
        if book and member_name:
            new_misuse = pd.DataFrame({'book': [book], 'member_name': [member_name]})
            misuse_df = pd.concat([misuse_df, new_misuse], ignore_index=True)
            save_data(misuse_df, 'masuse_books.csv')
            st.success("Misuse book entry added successfully!")
        else:
            st.error("Please enter both book and member name.")

    if st.button("Delete", key="misuse_delete"):
        if book:
            misuse_df = misuse_df[misuse_df['book'] != book]
            save_data(misuse_df, 'masuse_books.csv')
            st.success("Misuse book entry deleted successfully!")
        else:
            st.error("Please enter the book to delete.")

    if st.button("Search", key="misuse_search"):
        if book:
            result = misuse_df[misuse_df['book'] == book]
            st.write(result)
        else:
            st.error("Please enter the book to search.")

# Member Details Pages
for i in range(1, 15):
    if page == f"Member Details {i}":
        member_details_page(f"Member Details {i}", f'members_{i}.csv')

# Teachers Details Page
if page == "Teachers Details":
    member_details_page("Teachers Details", 'teachers.csv')

# Non-Academic Details Page
if page == "Non-Academic Details":
    member_details_page("Non-Academic Details", 'non_academic.csv')

# Other Member Details Page
if page == "Other Member Details":
    member_details_page("Other Member Details", 'other_members.csv')
