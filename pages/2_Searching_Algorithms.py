import streamlit as st
from visuals import searching_vis
from algorithms import searching

st.title("Searching Algorithms")

algorithm = st.selectbox("Choose an algorithm", ["Sequential Search",
                                                 "Binary Search"])
size = st.slider("Array size", 5, 30, 10)
value = st.number_input("Value to search for", min_value= -100, max_value= 100, value= 0)
speed = st.selectbox("Animation speed", [1, 2, 3, 4, 5])
array = searching_vis.generate_array(size, value)

if st.button("Run"):

    match algorithm:
        case "Sequential Search":
            searching_vis.render_array(array)
            searching.sequential_search(array, value, speed)
        case "Binary Search":
            array.sort() #Binary search requires a sorted array
            searching_vis.render_array(array)
            searching.binary_search(array, value, speed)
        case _:
            st.write("Please Select An Algorithm To Run")