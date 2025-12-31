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

#add algorithm descriptions and any additional options for certain algorithms
match algorithm:
    case "Sequential Search":
        st.write("The sequential search is the most straightforward searching algorithm there is. "
                 "It entails iterating through the entire array element by element until the correct value is found. "
                 "If the entire array is searched and the correct value is not found, then the value is not in the array. "
                 "For the purposes of this demonstration, the correct value will always be in the array at least once. "
                 "The runtime of a selection sort is always O(n).")
    case "Binary Search":
        st.write("The binary search works by continually cutting the array in half. "
                 "The algorithm presupposes that the array is in sorted order and compares the desired value to the value of the midpoint. "
                 "If the desired value is less than the midpoint, the algorithm searches the sub-array to the left of the midpoint and to the right of the previous midpoint (or the beginning of the array). "
                 "If the desired value is greater than the midpoint, the algorithm searches the sub-array to the right of the midpoint and to the left of the previous midpoint (or the end of the array). "
                 "If the interval of the search reduces to 0, then the value is not in the array. "
                 "For the purposes of this demonstration, the correct value will always be in the array at least once. "
                 "The runtime of a binary search is always O(log(n)).")

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