import streamlit as st
import json
import os
import pandas as pd
import datetime
import pytz
from PIL import Image
import io

LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Get Karachi Time (Pakistan Standard Time)
karachi_tz = pytz.timezone("Asia/Karachi")
current_time = datetime.datetime.now(karachi_tz).strftime("%d-%m-%Y %H:%M:%S")

# Set page config
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# ✅ **Header Section**
st.markdown(
    f"""
    <h1 style="text-align: center;">📚 Personal Library Manager</h1>
    <h3 style="text-align: center;">Developed by uzma farhan</h3>
    <h3 style="text-align: center; color: red;">🕒 Current Time (Karachi):<br>{current_time}</h3>
    """,
    unsafe_allow_html=True
)

# Sidebar menu
menu = st.sidebar.radio("📌 Menu", ["📖 Add Book", "🗑️ Remove Book", "🔍 Search Book", 
                                    "📚 Display Books", "📊 Statistics", "📥 Import/Export", "🚪 Exit"])

# ✅ **Add a Book with Cover Upload**
if menu == "📖 Add Book":
    st.subheader("➕ Add a New Book")
    
    # Card-style form for adding a book
    with st.container():
        st.markdown("""
        <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h3 style="color: #2c3e50; text-align: center;">Add Book</h3>
        </div>
        """, unsafe_allow_html=True)

    title = st.text_input("📘 Book Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, step=1)
    genre = st.text_input("📂 Genre")
    read_status = st.checkbox("✔️ Read")
    cover = st.file_uploader("🖼️ Upload Book Cover (optional)", type=["png", "jpg", "jpeg"])

    if st.button("✅ Add Book"):
        if title.strip() == "" or author.strip() == "" or genre.strip() == "":
            st.error("⚠️ Please fill in all fields (Title, Author, and Genre are required).")
        else:
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status, "cover": ""}
            if cover:
                covers_dir = "covers"
                if not os.path.exists(covers_dir):
                    os.makedirs(covers_dir)
                cover_path = os.path.join(covers_dir, f"{title.replace(' ', '_')}.jpg")
                with open(cover_path, "wb") as f:
                    f.write(cover.getbuffer())
                book["cover"] = cover_path
            st.session_state.library.append(book)
            save_library(st.session_state.library)
            st.success(f'📖 Book "{title}" added successfully!')

# ✅ **Remove a Book**
elif menu == "🗑️ Remove Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    title_to_remove = st.selectbox("🗂️ Select a book to remove", titles) if titles else None

    if title_to_remove and st.button("🚮 Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
        save_library(st.session_state.library)
        st.success(f'🚮 Book "{title_to_remove}" removed!')

# ✅ **Search for Books**
elif menu == "🔍 Search Book":
    st.subheader("🔍 Search for a Book")
    search_criteria = st.radio("🔎 Search by:", ["Title", "Author", "Year", "Genre", "Read/Unread"])

    query = st.text_input(f"Enter {search_criteria} to search") if search_criteria != "Read/Unread" else None
    if search_criteria == "Read/Unread":
        read_status = st.radio("✔️ Choose status:", ["Read", "Unread"])

    if st.button("🔎 Search"):
        if search_criteria == "Read/Unread":
            results = [book for book in st.session_state.library if (read_status == "Read" and book["read"]) or (read_status == "Unread" and not book["read"])]
        else:
            results = [book for book in st.session_state.library if query.lower() in str(book[search_criteria.lower()]).lower()]

        if results:
            for book in results:
                st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✔️ Read" if book["read"] else "📖 Unread"}')
        else:
            st.warning("❌ No books found.")

# ✅ **Display Books in Card Format or Table Format**
elif menu == "📚 Display Books":
    st.subheader("📚 All Books in Library")
    
    if not st.session_state.library:
        st.info("📭 No books available.")
    else:
        filter_genre = st.selectbox("📂 Filter by Genre", ["All"] + list(set(book["genre"] for book in st.session_state.library)))
        filter_read = st.radio("✔️ Filter by Read Status", ["All", "Read", "Unread"])
        sort_by = st.radio("🔽 Sort By", ["Title", "Author", "Year"])
        view_format = st.radio("📅 View Format", ["Card View", "Table View"])

        books = st.session_state.library
        if filter_genre != "All":
            books = [book for book in books if book["genre"] == filter_genre]
        if filter_read != "All":
            books = [book for book in books if book["read"] == (filter_read == "Read")]

        books.sort(key=lambda x: x[sort_by.lower()], reverse=(sort_by == "Year"))

        # Display in Card Format
        if view_format == "Card View":
            for book in books:
                with st.container():
                    col1, col2 = st.columns([0.3, 0.7])
                    with col1:
                        # Show image if it exists
                        if book["cover"]:
                            st.image(book["cover"], width=120, use_container_width=True)
                    with col2:
                        st.markdown(f"""
                        <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                            <h4 style="color: #2c3e50;">{book["title"]}</h4>
                            <p style="color: #34495e; font-size: 16px;">{book["author"]}</p>
                            <p style="color: #7f8c8d;">{book["year"]} | {book["genre"]}</p>
                            <p style="color: #16a085;">{"✔️ Read" if book["read"] else "📖 Unread"}</p>
                        </div>
                        """, unsafe_allow_html=True)

        # Display in Table Format
        elif view_format == "Table View":
            # Prepare data for table view
            table_data = []
            for book in books:
                table_data.append([book["title"], book["author"], book["year"], book["genre"], "✔️ Read" if book["read"] else "📖 Unread"])
            
            # Create a DataFrame for easy table display
            df = pd.DataFrame(table_data, columns=["Title", "Author", "Year", "Genre", "Status"])
            st.dataframe(df)

# ✅ **Library Statistics (Card Format)**
elif menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")

    # Calculate Statistics
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books

    most_common_genre = pd.Series([book["genre"] for book in st.session_state.library]).mode().get(0, "N/A")
    most_read_author = pd.Series([book["author"] for book in st.session_state.library]).mode().get(0, "N/A")

    with st.container():
        st.markdown(f"""
        <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
            <h4 style="color: #2c3e50;">✔️ Books Read</h4>
            <p style="color: #16a085; font-size: 24px; font-weight: bold;">{read_books} ({(read_books/total_books*100) if total_books > 0 else 0:.2f}%)</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h4 style="color: #2c3e50;">📖 Books Unread</h4>
                <p style="color: #e74c3c; font-size: 24px; font-weight: bold;">{unread_books}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h4 style="color: #2c3e50;">🎬 Most Common Genre</h4>
                <p style="color: #34495e; font-size: 20px;">{most_common_genre}</p>
            </div>
            """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h4 style="color: #2c3e50;">🌟 Most Read Author</h4>
                <p style="color: #34495e; font-size: 20px;">{most_read_author}</p>
            </div>
            """, unsafe_allow_html=True)

# ✅ **Import/Export Books**
elif menu == "📥 Import/Export":
    st.subheader("📥 Import/Export Library")

    # Import and Export options
    export_format = st.selectbox("📤 Export Format", ["CSV", "Excel", "JSON", "Text"])
    if export_format:
        if export_format == "CSV":
            csv_data = pd.DataFrame(st.session_state.library)
            csv_string = csv_data.to_csv(index=False)
            st.download_button("📤 Download CSV", csv_string, file_name="library.csv", mime="text/csv")
        
        elif export_format == "Excel":
            excel_data = pd.DataFrame(st.session_state.library)
            excel_file = io.BytesIO()
            with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
                excel_data.to_excel(writer, index=False, sheet_name="Library")
            st.download_button("📤 Download Excel", excel_file.getvalue(), file_name="library.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        elif export_format == "JSON":
            json_data = json.dumps(st.session_state.library, indent=4)
            st.download_button("📤 Download JSON", json_data, file_name="library.json", mime="application/json")
        
        elif export_format == "Text":
            text_data = "\n".join([f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']}" for book in st.session_state.library])
            st.download_button("📤 Download Text", text_data, file_name="library.txt", mime="text/plain")

    uploaded_file = st.file_uploader("📥 Upload Library File", type=["csv", "xlsx", "json", "txt"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.session_state.library = df.to_dict(orient="records")
            save_library(st.session_state.library)
            st.success("📚 Library successfully imported from CSV!")
        
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
            st.session_state.library = df.to_dict(orient="records")
            save_library(st.session_state.library)
            st.success("📚 Library successfully imported from Excel!")
        
        elif uploaded_file.name.endswith(".json"):
            library_data = json.load(uploaded_file)
            st.session_state.library.extend(library_data)
            save_library(st.session_state.library)
            st.success("📚 Library successfully imported from JSON!")
        
        elif uploaded_file.name.endswith(".txt"):
            text_data = uploaded_file.read().decode("utf-8")
            book_lines = text_data.split("\n")
            for line in book_lines:
                if line.strip():
                    title, author, year, genre = line.split(" - ")
                    book = {"title": title.strip(), "author": author.strip(), "year": int(year.strip()), "genre": genre.strip(), "read": False, "cover": ""}
                    st.session_state.library.append(book)
            save_library(st.session_state.library)
            st.success("📚 Library successfully imported from Text file!")
            
# ✅ **Exit**
elif menu == "🚪 Exit":
    st.warning("🚪 Exiting the application...")
    st.stop()

