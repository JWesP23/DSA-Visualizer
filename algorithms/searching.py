import math
import random
import time
from typing import List, Any
from visuals import searching_vis
import streamlit as st
import math



#Sequential Search implementation
def sequential_search(list_to_search: List, value, speed= 1):
    for i in range(len(list_to_search)):
        searching_vis.render_array(list_to_search, highlight_indices= [i], speed= speed)
        if list_to_search[i] == value:
            searching_vis.render_array(list_to_search, selected_indices= [i], speed= speed)
            return i

    searching_vis.render_array(list_to_search, not_found= True, speed= speed)
    st.write(f"The value {value} is not in the array")
    return None     #value not in array


#Binary Search implementation
def binary_search(list_to_search: List, value, speed=1):
    low = 0
    high = len(list_to_search) - 1

    while low <= high:
        mid = (low + high) // 2

        # Optional visualization step
        searching_vis.render_array(list_to_search, highlight_indices=[mid], speed= speed)
        if list_to_search[mid] == value:
            searching_vis.render_array(list_to_search, selected_indices= [mid], speed= speed)
            st.write(f"The value {value} has been found")
            return mid
        elif list_to_search[mid] > value:
            high = mid - 1
            st.write(f"{value} is less than {list_to_search[mid]}, search the left half of the sub-array")
        else:
            low = mid + 1
            st.write(f"{value} is greater than {list_to_search[mid]}, search the right half of the sub-array")

    searching_vis.render_array(list_to_search, not_found= True, speed= speed)
    st.write(f"The value {value} is not in the array")
    return None