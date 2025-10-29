import streamlit as st

from algorithms.sorting import visual_merge
from visuals import sorting_vis
from algorithms import sorting

st.title("Sorting Algorithms")

algorithm = st.selectbox("Choose an algorithm", ["Selection Sort",
                                                 "Bubble Sort",
                                                 "Insertion Sort",
                                                 "Shell Sort",
                                                 "Merging",
                                                 "Merge Sort",
                                                 "Heap Sort",
                                                 "Quick Sort"])
size = st.slider("Array size", 5, 30, 10)
speed = st.selectbox("Animation speed", [1, 2, 3, 4, 5, "Instant"])
array = sorting_vis.generate_array(size)

#add any additional options for certain algorithms
match algorithm:
    case "Heap Sort":
        heap_display = st.radio(
            "How do you want to view the heap?",
            ["Array :computer:", "Tree :deciduous_tree:"],
            captions=[
                "Shows a heap programmed as an array (more efficient)",
                "Easily understood visually",
            ],
        )

if st.button("Run"):

    match algorithm:
        case "Selection Sort":
            sorting_vis.render_array(array, speed= speed)
            sorting.selection_sort(array, speed)
            sorting_vis.render_array(array, speed= speed)
        case "Bubble Sort":
            sorting_vis.render_array(array, speed= speed)
            sorting.bubble_sort(array, speed)
            sorting_vis.render_array(array, speed= speed)
        case "Insertion Sort":
            sorting_vis.render_array(array, speed= speed)
            sorting.insertion_sort(array, speed)
            sorting_vis.render_array(array, speed= speed)
        case "Shell Sort":
            sorting_vis.render_array(array, speed= speed)
            sorting.shell_sort(array, speed)
            sorting_vis.render_array(array, speed= speed)
        case "Merging":
            array1 = array
            array2 = sorting_vis.generate_array(size)

            #Merging requires sorted arrays
            array1.sort()
            array2.sort()

            sorting_vis.render_array(array1, speed= speed, label= "Array 1")
            sorting_vis.render_array(array2, speed= speed, label= "Array 2")
            visual_merge(array1, array2, speed= speed)
            sorting_vis.render_array(array, speed= speed, label= "Merged Array")
        case "Merge Sort":
            list_length = len(array) - 1
            sorting_vis.render_merge_step(array[:list_length//2], array[list_length//2:], separate= False, speed= speed)
            array = sorting.merge_sort(array, speed) #merge sort is not in-place so have to have "array =" so that final result displayed is sorted rather than original
        case "Heap Sort":
            sorting_vis.render_array(array, speed= speed)

            if heap_display == "Array :computer:":
                sorting.heap_sort(array, speed)
            else:
                sorting.heap_sort_tree(array, speed)

            sorting_vis.render_array(array, speed= speed)
        case "Quick Sort":
            sorting_vis.render_array(array, speed= speed)
            sorting.quick_sort_rand_pivot(array, speed)
            sorting_vis.render_array(array, speed= speed)
        case _:
            st.write("Please Select An Algorithm To Run")