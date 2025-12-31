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

#add algorithm descriptions and any additional options for certain algorithms
match algorithm:
    case "Selection Sort":
        st.write("The selection sort is the simplest sorting algorithm there is, it's likely what you'd do if you had to sort an array by hand. "
                 "The selection sort iterates through the entire array searching for the smallest value, once it's found it, the algorithm swaps the lowest value with the value at index 0 "
                 "Then, the selection sort finds the next smallest value and swaps it with the value at index 1. "
                 "This process continues until the whole array is sorted. "
                 "The runtime of a selection sort is always O(n²).")
    case "Bubble Sort":
        st.write("The bubble sort works by having the largest values \"bubble up\" to the top. "
                 "The algorithm moves through the array, comparing pairs of values and making swaps if the value at index n is greater than the value at index n + 1. "
                 "After each loop, more and more of the values at the end of the array will be in their final sorted position. "
                 "This continues until the whole array has been sorted. "
                 "The average runtime of a bubble sort is O(n²).")
    case "Insertion Sort":
        st.write("The insertion sort works by iterating through the array and ensuring that every value it passes has been sorted within a smaller sub-array. "
                 "The algorithm can either copy each value it passes into a separate array (out-of-place), or it can maintain the sub-array within the original array itself (in-place). "
                 "By \"inserting\" each value into a sub-array and maintaining a sorted order within that sub-array, the insertion sort sorts a small sub-array that progressively grows to become a sorted version of the original array "
                 "The average runtime of an insertion sort is O(n²).")
    case "Shell Sort":
        st.write("The shell sort compares distant values across a \"gap\" rather than adjacent values. "
                 "It works similarly to an insertion sort in that it sorts a sub array so that sorting the full sized array (when the gap becomes 1) at the end becomes easy. "
                 "The runtime of a shell sort varies significantly depending on the sequence of gap sizes used but its worst-case runtime is O(n²) and its best-case runtime is O(nlog(n)).")
    case "Merging":
        st.write("Merging two arrays is the basis of the merge sort. "
                 "It entails iterating through two sorted arrays while continually placing the smallest value in either array into a new merged array. "
                 "The goal of merging is to produce a merged array which contains all the values of both arrays in sorted order. "
                 "The runtime of merging is always O(n).")
    case "Merge Sort":
        st.write("The merge sort works by repeatedly splitting the array into left and right halves. "
                 "The algorithm recursively does this until the sub-arrays have a length of 1 or 0. "
                 "The sub-arrays are then merged so that each merge ensures the sub-arrays are combined into a single sorted array. "
                 "This process continues until the merging produces a sorted version of the original array. "
                 "Essentially, the merge sort breaks the array down into smaller and smaller sub-arrays that are easier to sort and then merges them back together. "
                 "The average runtime of a merge sort is O(nlog(n)).")
    case "Heap Sort":
        st.write("The heap sort works by heapify-ing the array, relying on the heap's inherent properties to sort the array, and then popping each element off the heap and back into the array. "
                 "This version of the heap sort uses a max heap, so each value popped off the heap goes into the array from right to left (if we sort in ascending order). "
                 "We could've just as easily used a min heap and added the values back into the array from left to right. "
                 "In an array heap, the index of the left and right child nodes will be (2 * parent_index + 1) and (2 * parent_index + 2) respectively. "
                 "The average runtime of a heap sort is O(nlog(n)).")
        heap_display = st.radio(
            "How do you want to view the heap?",
            ["Array :computer:", "Tree :deciduous_tree:"],
            captions=[
                "Shows a heap programmed as an array (more efficient)",
                "Easily understood visually",
            ],
        )
    case "Quick Sort":
        st.write("The quick sort works by selecting a pivot element, moving it to the front of the array, and then iterating up and down the array while comparing values to the pivot. "
                 "The iterator moving up the array is looking for values greater than the pivot while the iterator moving down the array is looking for values less than the pivot. "
                 "Once each iterator has found a value, they swap values and continue searching until they have passed each other. "
                 "When the iterators have passed each other, the pivot is swapped with the iterator moving down the array, ensuring that the value at index 0 is less than the pivot. "
                 "After each loop, the pivot value is guaranteed to be in it's final sorted position and the arrays on either side of the pivot are then recursively sorted. "
                 "The average runtime for a quick sort is O(nlog(n)).")
        sort_type = st.radio(
            "How do you want to handle pivot selection?",
            ["Arbitrarily :point_up:", "Random :zany:", "Median of three :monocle:"],
            captions=[
                "Arbitrarily selects the first element as the pivot (inefficient if the array is semi-sorted)",
                "Randomly selects the pivot from the array (less likely to be inefficient for a semi-sorted array)",
                "Chooses the median between the first, middle, and last elements as the pivot (very unlikely to choose a bad pivot for unsorted or semi-sorted arrays)",
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
            array = visual_merge(array1, array2, speed= speed)
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

            if sort_type == "Arbitrarily :point_up:":
                array = sorting.quick_sort_arbitrary_pivot(array, speed)
            elif sort_type == "Random :zany:":
                array = sorting.quick_sort_rand_pivot(array, speed)
            else:
                array = sorting.quick_sort_smart_pivot(array, speed)

            sorting_vis.render_array(array, speed= speed)
        case _:
            st.write("Please Select An Algorithm To Run")