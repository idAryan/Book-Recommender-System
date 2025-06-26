import streamlit as st
import pickle
import numpy as np

# Load artifacts
model = pickle.load(open("artifacts/model.pkl", "rb"))
book_names = pickle.load(open("artifacts/book_names.pkl", "rb"))
final_rating = pickle.load(open("artifacts/final_rating.pkl", "rb"))
book_pivot = pickle.load(open("artifacts/book_pivot.pkl", "rb"))

st.set_page_config(page_title="Book Recommender", layout="wide")

st.title("Book Recommendation System")
st.markdown("Get Book Recommendation")

selected_book = st.selectbox("Type / select book", book_names)

if st.button("Recommend"):
    try:
        book_id = np.where(book_pivot.index == selected_book)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id].values.reshape(1, -1), n_neighbors=6)

        st.success(f"You searched for: **{selected_book}**")
        st.markdown("### 🧠 Recommended Books:")

        for i in range(1, len(suggestion[0])):
            recommended_title = book_pivot.index[suggestion[0][i]]
            idx = np.where(final_rating['title'] == recommended_title)[0][0]
            image_url = final_rating.iloc[idx]['image_url']

            st.markdown(f"**{recommended_title}**")
            st.image(image_url, width=120)
            st.markdown("---")

    except Exception as e:
        st.error("Something went wrong. Please try again.")





