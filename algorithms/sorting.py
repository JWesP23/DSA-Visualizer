import math
import random
import time
from typing import List, Any
from visuals import sorting_vis
import streamlit as st


#Swaps to elements in an array given the array and the element indices
def swap(arr, a, b):
    c = arr[a]
    arr[a] = arr[b]
    arr[b] = c


#---------------------- Quadratic Sorts ----------------------#

#In-place Selection Sort implementation
def selection_sort(list_to_sort: List, speed= 1, ascending: bool = True) -> List:
    for i in range(len(list_to_sort) - 1):
        min_index = i
        sorting_vis.render_array(list_to_sort, [i], speed= speed)
        st.write(f"Searching for a value less than {list_to_sort[i]}")
        for j in range(i, len(list_to_sort)):
            sorting_vis.render_array(list_to_sort, [i, j], [min_index], speed= speed)
            if (list_to_sort[j] < list_to_sort[min_index] and ascending) or (list_to_sort[j] > list_to_sort[min_index] and not ascending):
                st.write(f"Value less than {list_to_sort[min_index]} found")
                min_index = j
                st.write(f"Searching for a value less than {list_to_sort[min_index]}")
                sorting_vis.render_array(list_to_sort, [i], [min_index], speed= speed)
        st.write(f"No value less than {list_to_sort[min_index]} found")

        st.write(f"Assigning {list_to_sort[min_index]} to first unsorted index")
        sorting_vis.render_array(list_to_sort, swap_indices= [i, min_index], speed= speed)
        swap(list_to_sort, i, min_index)
        sorting_vis.render_array(list_to_sort, swap_indices= [i, min_index], speed= speed)

    return list_to_sort


#In-place Bubble Sort implementation for 1D arrays
def bubble_sort(list_to_sort: List, speed= 1, ascending: bool = True) -> List:

    list_length = len(list_to_sort)

    for i in range(list_length - 1):
        swap_occurred = False
        for j in range(list_length - 1 - i): #minus i stops us from resorting the tail which will have already been sorted (after one loop, the last number is sorted. after two loops the last two numbers are sorted. etc.)
            sorting_vis.render_array(list_to_sort, [j], speed= speed)
            sorting_vis.render_array(list_to_sort, [j, j + 1], speed= speed)
            if (list_to_sort[j] > list_to_sort[j + 1] and ascending) or (list_to_sort[j] < list_to_sort[j + 1] and not ascending):
                swap_occurred = True
                sorting_vis.render_array(list_to_sort, swap_indices= [j, j + 1], speed= speed)
                swap(list_to_sort, j, j+1)
                sorting_vis.render_array(list_to_sort, swap_indices= [j, j + 1], speed= speed)
        if 0 < i < list_length - 2:
            st.write(f"The last {i + 1} values are in their final sorted positions")
        elif i == 0:
            st.write(f"The last value is in its final sorted position")
        else:
            st.write(f"All values are in their final sorted positions")
        if not swap_occurred: #exit loop if no swaps occur on a full pass through (list is sorted)
            st.write("No swap occurred in this loop so the array is sorted")
            break

    return list_to_sort


#Out-of-place Insertion sort implementation using 2 arrays
def two_array_insertion_sort(list_to_sort: List, speed= 1, ascending: bool = True) -> List:

    list_length = len(list_to_sort)

    sorting_array = [None] * list_length

    sorting_array[0] = list_to_sort[0]
    for i in range(1, list_length):
        value = list_to_sort[i]
        while i > 0 and (sorting_array[i - 1] is None or sorting_array[i - 1] > value):
            sorting_array[i] = sorting_array[i - 1]
            i -= 1
        sorting_array[i] = value

    if not ascending:
        sorting_array.reverse()

    return sorting_array


#In-place Insertion sort implementation using 1 array
def insertion_sort(list_to_sort: List, speed= 1, ascending: bool = True) -> List:

    list_length = len(list_to_sort)

    for i in range(1, list_length):
        value = list_to_sort[i]
        sorting_vis.render_array(list_to_sort, highlight_indices= [i], speed= speed)

        sorting_necessary = True #Only needed for animation

        if list_to_sort[i-1] <= value: #Triggers a highlight to denote a comparison occurred which would not show up inside the while loop (unnecessary for algorithm, just for animation)
            sorting_vis.render_array(list_to_sort, highlight_indices= [i, i - 1], speed= speed)
            st.write(f"{value} is already sorted within the sub-array (from index 0 to index {i})")
            sorting_necessary = False
        else:
            st.write(f"Swap {value} backward until the sub-array (from index 0 to index {i}) is sorted")

        while i > 0 and list_to_sort[i-1] > value:
            sorting_vis.render_array(list_to_sort, highlight_indices= [i, i - 1], speed= speed)
            sorting_vis.render_array(list_to_sort, swap_indices= [i, i - 1], speed= speed)
            list_to_sort[i] = list_to_sort[i - 1]
            sorting_vis.render_array(list_to_sort, swap_indices= [i, i - 1], speed= speed)
            i -= 1
            if list_to_sort[i-1] < value: #Triggers a highlight to denote a comparison occurred between the target value and the first element smaller than the target value in the sub-array (unnecessary for algorithm, just for animation)
                sorting_vis.render_array(list_to_sort, highlight_indices= [i, i - 1], speed= speed)

        if list_to_sort[i] != value: #if statement is unnecessary for algorithm but needed for animation
            st.write(f"Place {value} into its correct position in the sub-array")
            list_to_sort[i] = value
            sorting_vis.render_array(list_to_sort, swap_indices= [i], speed= speed)

        if sorting_necessary:
            st.write(f"{value} is now sorted within the sub-array")

    if not ascending:
        list_to_sort.reverse()

    return list_to_sort


#In-place Insertion sort implementation using 1 array
def shell_sort(list_to_sort: List, speed= 1, ascending: bool = True) -> List:

    list_length = len(list_to_sort)
    gap = list_length // 2
    st.write(f"Set initial gap to {gap} (list length // 2).")

    while gap > 0:
        for i in range(gap, list_length):
            value = list_to_sort[i]
            j = i

            if j >= gap and list_to_sort[j - gap] < value: #For animation purposes only
                sorting_vis.render_array(list_to_sort, highlight_indices=[j - gap, j], speed= speed)
                st.write(f"Sub-array (the highlighted indices) is already sorted")

            if j >= gap and list_to_sort[j - gap] > value: #For animation purposes only
                st.write(f"Swap {value} backward until the sub-array (the highlighted indices) is sorted")
            #Insertion sort on subarray
            while j >= gap and list_to_sort[j - gap] > value:
                sub_array_indices = list(range(i, -1, -gap))
                sorting_vis.render_array(list_to_sort, highlight_indices=sub_array_indices, speed= speed)
                sorting_vis.render_array(list_to_sort, highlight_indices=sub_array_indices, swap_indices=[j, j - gap], speed= speed)
                list_to_sort[j] = list_to_sort[j - gap]
                sorting_vis.render_array(list_to_sort, highlight_indices=sub_array_indices, swap_indices=[j, j - gap], speed= speed)

                j -= gap

            if list_to_sort[j] != value:
                sub_array_indices = list(range(i, -1, -gap))
                st.write(f"Place {value} into its correct position in the sub-array")
                list_to_sort[j] = value
                sorting_vis.render_array(list_to_sort, highlight_indices=sub_array_indices, swap_indices=[j], speed= speed)

        #Reduce the gap for the next pass
        if gap == 2:
            gap = 1
            st.write(f"Gap equals 2 so set gap to 1.")
        else:
            gap = math.floor(gap / 2.2)
            st.write(f"Set gap to {gap} (current gap // 2.2).")

    st.write(f"Gap equals 0 so algorithm has finished.")

    #Reverse if descending order requested
    if not ascending:
        list_to_sort.reverse()

    return list_to_sort


#Visual implementation of the concept of merging two sorted arrays
def visual_merge(arr1, arr2, speed= 1):
    return_arr = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        sorting_vis.render_array(arr1, highlight_indices= [i], speed= speed, label= "Array 1")
        sorting_vis.render_array(arr2, highlight_indices= [j], speed= speed, label= "Array 2")
        if arr1[i] < arr2[j]:
            sorting_vis.render_array(arr1, swap_indices= [i], speed= speed, label= "Array 1")
            sorting_vis.render_array(arr2, highlight_indices= [j], speed= speed, label= "Array 2")
            st.write(f"{arr1[i]} is less than {arr2[j]}, append {arr1[i]} to the merged array")
            return_arr.append(arr1[i])
            sorting_vis.render_array(return_arr, swap_indices= [len(return_arr) - 1], speed= speed, label= "Merged Array")
            i += 1
        else:
            sorting_vis.render_array(arr1, highlight_indices= [i], speed= speed, label= "Array 1")
            sorting_vis.render_array(arr2, swap_indices= [j], speed= speed, label= "Array 2")
            st.write(f"{arr2[i]} is less than {arr1[j]}, append {arr2[i]} to the merged array")
            return_arr.append(arr2[j])
            sorting_vis.render_array(return_arr, swap_indices= [len(return_arr) - 1], speed= speed, label= "Merged Array")
            j += 1

    #append the rest of the unprocessed list to the return list
    if i > len(arr1) - 1:
        st.write("Array 1 has been fully processed, append the rest of Array 2 to the merged array")
        sorting_vis.render_array(arr2, highlight_indices= range(j, len(arr2)), speed= speed, label= "Array 2")
        pre_append_length = len(return_arr)
        return_arr += arr2[j:]
        sorting_vis.render_array(return_arr, swap_indices= range(pre_append_length, len(return_arr)), speed= speed, label= "Merged Array")
    else:
        st.write("Array 2 has been fully processed, append the rest of Array 1 to the merged array")
        sorting_vis.render_array(arr1, highlight_indices= range(i, len(arr1)), speed= speed, label= "Array 1")
        pre_append_length = len(return_arr)
        return_arr += arr1[i:]
        sorting_vis.render_array(return_arr, swap_indices= range(pre_append_length, len(return_arr)), speed= speed, label= "Merged Array")
    return return_arr


#---------------------- Logarithmic-Linear Sorts ----------------------#

#Merge sort (out of place) implementation
def merge_sort(list_to_sort: List, speed= 1, ascending: bool = True) -> list[Any]:

    #compare elements from both arrays until one is fully processed
    def merge(arr1, arr2):
        return_arr = []
        i, j = 0, 0
        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                return_arr.append(arr1[i])
                i += 1
            else:
                return_arr.append(arr2[j])
                j += 1

        #append the rest of the unprocessed list to the return list
        if i > len(arr1) - 1:
            return_arr += arr2[j:]
        else:
            return_arr += arr1[i:]

        return return_arr


    list_length = len(list_to_sort)

    left_half = list_to_sort[:list_length//2]
    right_half = list_to_sort[list_length//2:]
    sorting_vis.render_merge_step(left_half, right_half, speed= speed)

    if list_length <= 1:  #base case
        st.write("Base case reached: list length <= 1 so stop splitting sub-array into left and right halves")
        return list_to_sort
    else:
        left_half = merge_sort(left_half)
        right_half = merge_sort(right_half)
        st.write("Merge Sorted Sub-Arrays")
        sorting_vis.render_merge_step(left_half, right_half, merge= True, speed= speed)
        sorted_sub_array = merge(left_half, right_half)
        sorting_vis.render_merge_step(sorted_sub_array[:list_length//2], sorted_sub_array[list_length//2:], separate= False, speed= speed)
        return sorted_sub_array


#Heap sort implementation using a max heap
#Displays as an array
def heap_sort(list_to_sort: List, speed= 1, ascending: bool = True) -> list[Any]:

    def add_to_heap(heap: List, value):
        heap.append(value)
        child_index = len(heap) - 1
        parent_index = math.floor((child_index-1)/2)
        sorting_vis.render_heap(a_heap, highlight_indices=[child_index], speed= speed)
        if parent_index >= 0 and value < heap[parent_index]: #Triggers a highlight to denote a comparison occurred which would not show up inside the while loop (unnecessary for algorithm, just for animation)
            sorting_vis.render_heap(a_heap, highlight_indices=[child_index, parent_index], speed= speed)
        while parent_index >= 0 and value > heap[parent_index]:
            sorting_vis.render_heap(a_heap, highlight_indices=[child_index, parent_index], speed= speed)
            sorting_vis.render_heap(a_heap, swap_indices= [child_index, parent_index], speed= speed)
            swap(heap, child_index, parent_index)
            sorting_vis.render_heap(a_heap, swap_indices= [child_index, parent_index], speed= speed)
            child_index = parent_index
            parent_index = math.floor((child_index-1)/2)
            if parent_index >= 0 and value < heap[parent_index]: #Triggers a highlight to denote a comparison occurred with a child and a parent of greater value (unnecessary for algorithm, just for animation)
                sorting_vis.render_heap(a_heap, highlight_indices=[child_index, parent_index], speed= speed)



    def remove_from_heap(heap: List) -> list[Any]:
        root = heap[0]

        sorting_vis.render_heap(a_heap, highlight_indices=[0], speed= speed)
        #adjust heap
        if len(heap) > 1:
            st.write("Readjust heap starting by moving item at bottom of heap to the root")
        sorting_vis.render_heap(a_heap, swap_indices=[0, len(heap) - 1], speed= speed)
        heap[0] = heap[len(heap) - 1]   #move last item in heap to top
        heap.pop(-1)              #shrink heap size by one by removing last item
        sorting_vis.render_heap(a_heap, swap_indices=[0], speed= speed)

        parent_index = 0
        l_child_index = 2 * parent_index + 1
        r_child_index = 2 * parent_index + 2

        #if left child exists consider swaps between children and parents
        while l_child_index < len(heap):
            sorting_vis.render_heap(a_heap, highlight_indices=[parent_index], speed= speed)
            largest_child_index = l_child_index
            #if right child exists and is greater than left child set right child as largest child
            if r_child_index < len(heap):
                st.write("Select largest child to be compared with parent")
                sorting_vis.render_heap(a_heap, highlight_indices=[l_child_index, r_child_index], speed= speed)
                if heap[l_child_index] < heap[r_child_index]:
                        largest_child_index = r_child_index
            #if largest child is greater than parent, swap parent and largest child
            sorting_vis.render_heap(a_heap, highlight_indices=[largest_child_index, parent_index], speed= speed)
            if heap[parent_index] < heap[largest_child_index]:
                sorting_vis.render_heap(a_heap, swap_indices=[largest_child_index, parent_index], speed= speed)
                swap(heap, parent_index, largest_child_index)
                sorting_vis.render_heap(a_heap, swap_indices=[largest_child_index, parent_index], speed= speed)
                parent_index = largest_child_index
            #if largest child is less than parent, heap order is correct
            else:
                break

            l_child_index = 2 * parent_index + 1
            r_child_index = 2 * parent_index + 2

        return root

    st.write("Heapify the array (add each item in the array into an empty heap)")
    sorting_vis.render_array(list_to_sort, highlight_indices=[0], speed= speed)
    a_heap = list_to_sort[0:1]  #begin a heap with the first item in the list
    sorting_vis.render_heap(a_heap, highlight_indices=[0], speed= speed)

    for i in range(1, len(list_to_sort)):
        sorting_vis.render_array(list_to_sort, highlight_indices=[i], speed= speed)
        add_to_heap(a_heap, list_to_sort[i])

    st.write("Pop each element from the heap and insert into the original array")

    for i in reversed(range(len(list_to_sort))):
        sorting_vis.render_array(list_to_sort, highlight_indices=[i], speed= speed)
        list_to_sort[i] = remove_from_heap(a_heap)
        sorting_vis.render_array(list_to_sort, swap_indices=[i], speed= speed)

    return list_to_sort


#Heap sort implementation using a max heap
#Displays as a tree
def heap_sort_tree(list_to_sort: List, speed= 1, ascending: bool = True) -> list[Any]:

    def add_to_heap(heap: List, value):
        heap.append(value)
        child_index = len(heap) - 1
        parent_index = math.floor((child_index-1)/2)
        sorting_vis.render_heap_tree(a_heap, highlight_indices=[child_index], speed= speed)
        if parent_index >= 0 and value < heap[parent_index]: #Triggers a highlight to denote a comparison occurred which would not show up inside the while loop (unnecessary for algorithm, just for animation)
            sorting_vis.render_heap_tree(a_heap, highlight_indices=[child_index, parent_index], speed= speed)
        while parent_index >= 0 and value > heap[parent_index]:
            sorting_vis.render_heap_tree(a_heap, highlight_indices=[child_index, parent_index], speed= speed)
            sorting_vis.render_heap_tree(a_heap, swap_indices= [child_index, parent_index], speed= speed)
            swap(heap, child_index, parent_index)
            sorting_vis.render_heap_tree(a_heap, swap_indices= [child_index, parent_index], speed= speed)
            child_index = parent_index
            parent_index = math.floor((child_index-1)/2)
            if parent_index >= 0 and value < heap[parent_index]: #Triggers a highlight to denote a comparison occurred with a child and a parent of greater value (unnecessary for algorithm, just for animation)
                sorting_vis.render_heap_tree(a_heap, highlight_indices=[child_index, parent_index], speed= speed)



    def remove_from_heap(heap: List) -> list[Any]:
        root = heap[0]

        sorting_vis.render_heap_tree(a_heap, highlight_indices=[0], speed= speed)

        #adjust heap
        if len(heap) > 1:
            st.write("Readjust heap starting by moving item at bottom of heap to the root")
        sorting_vis.render_heap_tree(a_heap, swap_indices=[0, len(heap) - 1], speed= speed)
        heap[0] = heap[len(heap) - 1]   #move last item in heap to top
        heap.pop(-1)              #shrink heap size by one by removing last item
        sorting_vis.render_heap_tree(a_heap, swap_indices=[0], speed= speed)

        parent_index = 0
        l_child_index = 2 * parent_index + 1
        r_child_index = 2 * parent_index + 2

        #if left child exists consider swaps between children and parents
        while l_child_index < len(heap):
            sorting_vis.render_heap_tree(a_heap, highlight_indices=[parent_index], speed= speed)
            largest_child_index = l_child_index
            #if right child exists and is greater than left child set right child as largest child
            if r_child_index < len(heap):
                st.write("Select largest child to be compared with parent")
                sorting_vis.render_heap_tree(a_heap, highlight_indices=[l_child_index, r_child_index], speed= speed)
                if heap[l_child_index] < heap[r_child_index]:
                    largest_child_index = r_child_index
            #if largest child is greater than parent, swap parent and largest child
            sorting_vis.render_heap_tree(a_heap, highlight_indices=[largest_child_index, parent_index], speed= speed)
            if heap[parent_index] < heap[largest_child_index]:
                sorting_vis.render_heap_tree(a_heap, swap_indices=[largest_child_index, parent_index], speed= speed)
                swap(heap, parent_index, largest_child_index)
                sorting_vis.render_heap_tree(a_heap, swap_indices=[largest_child_index, parent_index], speed= speed)
                parent_index = largest_child_index
            #if largest child is less than parent, heap order is correct
            else:
                break

            l_child_index = 2 * parent_index + 1
            r_child_index = 2 * parent_index + 2

        return root

    st.write("Heapify the array (add each item in the array into an empty heap)")
    sorting_vis.render_array(list_to_sort, highlight_indices=[0], speed= speed)
    a_heap = list_to_sort[0:1]  #begin a heap with the first item in the list
    sorting_vis.render_heap_tree(a_heap, highlight_indices=[0], speed= speed)

    for i in range(1, len(list_to_sort)):
        sorting_vis.render_array(list_to_sort, highlight_indices=[i], speed= speed)
        add_to_heap(a_heap, list_to_sort[i])

    st.write("Pop each element from the heap and insert into the original array")

    for i in reversed(range(len(list_to_sort))):
        sorting_vis.render_array(list_to_sort, highlight_indices=[i], speed= speed)
        list_to_sort[i] = remove_from_heap(a_heap)
        sorting_vis.render_array(list_to_sort, swap_indices=[i], speed= speed)

    return list_to_sort



#Quick Sort (in place) implementation arbitrarily using the first value as the pivot
def quick_sort_arbitrary_pivot(list_to_sort: List, speed= 1, ascending: bool = True) -> list[Any]:

    if len(list_to_sort) <= 1: #base case
        sorting_vis.render_array_with_pivot(list_to_sort, speed= speed)
        st.write("This array consists of one element or less so it's sorted")
        return list_to_sort

    #choose first element as pivot
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[0], speed= speed)
    pivot = list_to_sort[0]
    pivot_index = 0
    first = 1   #the index of values greater than the pivot starting at the front of the list
    last = len(list_to_sort) - 1 #the index of values less than the pivot starting at the end of the list
    st.write("Choose the first element to be the pivot")
    sorting_vis.render_array_with_pivot(list_to_sort, pivot_index=pivot_index, speed= speed)

    #when first and last markers pass each other swap the pivot with last since last will be less than the pivot (since first passed it)
    #and every value above last will be greater than the pivot (since last already passed them)
    while first <= last:

        #find the first element from the start of the list greater than the pivot
        st.write("Search from left to right for a value greater than or equal to the pivot")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[first, last], pivot_index=pivot_index, speed= speed)
        while first < len(list_to_sort) - 1 and list_to_sort[first] < pivot:
            first += 1
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[first, last], pivot_index=pivot_index, speed= speed)
        if list_to_sort[first] > pivot:
            #ensures up iterator's green highlight doesn't get covered by down iterator's yellow highlight (which gets precedence in sorting_vis.render_array_with_pivot())
            if last == first:
                sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[first], pivot_index=pivot_index, speed= speed)
            else:
                sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
            st.write("Value greater than pivot found")
        else:
            st.write("No value greater than pivot found or iterator moving up list has passed iterator moving down list")

        #find the last element from the back of the list less than the pivot
        st.write("Search from right to left for a value less than or equal to the pivot")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
        while last > 0 and list_to_sort[last] > pivot:
            last -= 1
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
        if list_to_sort[last] < pivot:
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
            st.write("Value less than pivot found")
        else:
            st.write("No value less than pivot found or iterator moving down list has passed iterator moving up list")

        #swap values at first and last so that values less than pivot are at the front of the list
        #and values greater than the pivot are at the end of the list
        if first < last:
            st.write("Swap values less than and greater than pivot")
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last, first], pivot_index=pivot_index, speed= speed)
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
            swap(list_to_sort, first, last)
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
        else:
            st.write("Iterator moving up and iterator moving down have passed each other")
            break

    #this swap ensures pivot is in the correct place in the array, with all smaller values to its left
    #and all larger values to its right
    st.write("Swap pivot with the last value less than the pivot")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last, pivot_index], speed= speed)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, pivot_index], speed= speed)
    swap(list_to_sort, pivot_index, last)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, pivot_index], speed= speed)
    pivot_index = last
    sorting_vis.render_array_with_pivot(list_to_sort, pivot_index=pivot_index, speed= speed)

    #recursively sort the left and right halves of the array (minus the pivot which is already in its sorted position)
    st.write("The pivot is now in its sorted position")
    st.write("Recursively sort the arrays to the left and right of the pivot")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[range(0, pivot_index)], pivot_index=pivot_index, speed= speed)
    left = quick_sort_arbitrary_pivot(list_to_sort[:pivot_index])
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[range(pivot_index + 1, len(list_to_sort))], pivot_index=pivot_index, speed= speed)
    right = quick_sort_arbitrary_pivot(list_to_sort[pivot_index + 1:])

    return left + [list_to_sort[pivot_index]] + right


#Quick Sort implementation using a random value as the pivot
def quick_sort_rand_pivot(list_to_sort: List, speed= 1, ascending: bool = True) -> list[Any]:

    if len(list_to_sort) <= 1: #base case
        sorting_vis.render_array_with_pivot(list_to_sort, speed= speed)
        st.write("This array consists of one element or less so it's sorted")
        return list_to_sort

    #choose random element as pivot
    st.write("Choose a random element as the pivot")
    pivot_index = random.randint(0, len(list_to_sort) - 1)
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[pivot_index], speed= speed)
    sorting_vis.render_array_with_pivot(list_to_sort, pivot_index=pivot_index, speed= speed)
    pivot = list_to_sort[pivot_index]
    st.write("Move pivot to index 0")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[0, pivot_index], speed= speed)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[0, pivot_index], speed= speed)
    swap(list_to_sort, 0, pivot_index)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[0, pivot_index], speed= speed)
    pivot_index = 0
    sorting_vis.render_array_with_pivot(list_to_sort, pivot_index=pivot_index, speed= speed)
    first = 1   #the index of values greater than the pivot starting at the front of the list
    last = len(list_to_sort) - 1 #the index of values less than the pivot starting at the end of the list

    #when first and last markers pass each other swap the pivot with last since last will be less than the pivot (since first passed it)
    #and every value above last will be greater than the pivot (since last already passed them)
    while first <= last:

        #find the first element from the start of the list greater than the pivot
        st.write("Search from left to right for a value greater than or equal to the pivot")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[first, last], pivot_index=pivot_index, speed= speed)
        while first < len(list_to_sort) - 1 and list_to_sort[first] < pivot:
            first += 1
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[first, last], pivot_index=pivot_index, speed= speed)
        if list_to_sort[first] > pivot:
            #ensures up iterator's green highlight doesn't get covered by down iterator's yellow highlight (which gets precedence in sorting_vis.render_array_with_pivot())
            if last == first:
                sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[first], pivot_index=pivot_index, speed= speed)
            else:
                sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
            st.write("Value greater than pivot found")
        else:
            st.write("No value greater than pivot found or iterator moving up list has passed iterator moving down list")

        #find the last element from the back of the list less than the pivot
        st.write("Search from right to left for a value less than or equal to the pivot")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
        while last > 0 and list_to_sort[last] > pivot:
            last -= 1
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
        if list_to_sort[last] < pivot:
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
            st.write("Value less than pivot found")
        else:
            st.write("No value less than pivot found or iterator moving down list has passed iterator moving up list")

        #swap values at first and last so that values less than pivot are at the front of the list
        #and values greater than the pivot are at the end of the list
        if first < last:
            st.write("Swap values less than and greater than pivot")
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last, first], pivot_index=pivot_index, speed= speed)
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
            swap(list_to_sort, first, last)
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
        else:
            st.write("Iterator moving up and iterator moving down have passed each other")
            break

    #this swap ensures pivot is in the correct place in the array, with all smaller values to its left
    #and all larger values to its right
    st.write("Swap pivot with the last value less than the pivot")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last, pivot_index], speed= speed)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, pivot_index], speed= speed)
    swap(list_to_sort, pivot_index, last)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, pivot_index], speed= speed)
    pivot_index = last
    sorting_vis.render_array_with_pivot(list_to_sort, pivot_index=pivot_index, speed= speed)

    #recursively sort the left and right halves of the array (minus the pivot which is already in its sorted position)
    st.write("The pivot is now in its sorted position")
    st.write("Recursively sort the arrays to the left and right of the pivot")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[range(0, pivot_index)], pivot_index=pivot_index, speed= speed)
    left = quick_sort_rand_pivot(list_to_sort[:pivot_index])
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[range(pivot_index + 1, len(list_to_sort))], pivot_index=pivot_index, speed= speed)
    right = quick_sort_rand_pivot(list_to_sort[pivot_index + 1:])

    return left + [list_to_sort[pivot_index]] + right


#Quick Sort (in place) implementation that chooses a pivot more intelligently
def quick_sort_smart_pivot(list_to_sort: List, speed= 1, ascending: bool = True) -> list[Any]:

    if len(list_to_sort) <= 1: #base case
        sorting_vis.render_array_with_pivot(list_to_sort, speed= speed)
        st.write("This array consists of one element or less so it's sorted")
        return list_to_sort

    #choose median between first, middle, and last elements in array to be the pivot
    st.write("Find the median between first, middle, and last elements in array")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[0, len(list_to_sort) // 2, len(list_to_sort) - 1], speed= speed)
    first_element = list_to_sort[0]
    middle_element = list_to_sort[len(list_to_sort) // 2]
    last_element = list_to_sort[-1]
    pivots = [first_element, middle_element, last_element]
    pivots.sort()

    st.write("Choose the median element to be the pivot")
    #median is the first element
    if pivots[1] == first_element:
        pivot = first_element
    #median is the middle element
    elif pivots[1] == middle_element:
        pivot = middle_element
        pivot_index = len(list_to_sort) // 2
        sorting_vis.render_array_with_pivot(list_to_sort, pivot_index= pivot_index, speed= speed)
        st.write("Move pivot to index 0")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[0, pivot_index], speed= speed)
        sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[0, pivot_index], speed= speed)
        swap(list_to_sort, 0, pivot_index)
        sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[0, pivot_index], speed= speed)
    #median is the last element
    else:
        pivot = last_element
        pivot_index = len(list_to_sort) - 1
        sorting_vis.render_array_with_pivot(list_to_sort, pivot_index= pivot_index, speed= speed)
        st.write("Move pivot to index 0")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[0, pivot_index], speed= speed)
        sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[0, pivot_index], speed= speed)
        swap(list_to_sort, 0, pivot_index)
        sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[0, pivot_index], speed= speed)

    pivot_index = 0
    sorting_vis.render_array_with_pivot(list_to_sort, pivot_index= pivot_index, speed= speed)

    first = 1   #the index of values greater than the pivot starting at the front of the list
    last = len(list_to_sort) - 1 #the index of values less than the pivot starting at the end of the list

    #when first and last markers pass each other swap the pivot with last since last will be less than the pivot (since first passed it)
    #and every value above last will be greater than the pivot (since last already passed them)
    while first <= last:

        #find the first element from the start of the list greater than the pivot
        st.write("Search from left to right for a value greater than or equal to the pivot")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[first, last], pivot_index=pivot_index, speed= speed)
        while first < len(list_to_sort) - 1 and list_to_sort[first] < pivot:
            first += 1
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[first, last], pivot_index=pivot_index, speed= speed)
        if list_to_sort[first] > pivot:
            #ensures up iterator's green highlight doesn't get covered by down iterator's yellow highlight (which gets precedence in sorting_vis.render_array_with_pivot())
            if last == first:
                sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[first], pivot_index=pivot_index, speed= speed)
            else:
                sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
            st.write("Value greater than pivot found")
        else:
            st.write("No value greater than pivot found or iterator moving up list has passed iterator moving down list")

        #find the last element from the back of the list less than the pivot
        st.write("Search from right to left for a value less than or equal to the pivot")
        sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
        while last > 0 and list_to_sort[last] > pivot:
            last -= 1
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last], swap_indices=[first], pivot_index=pivot_index, speed= speed)
        if list_to_sort[last] < pivot:
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
            st.write("Value less than pivot found")
        else:
            st.write("No value less than pivot found or iterator moving down list has passed iterator moving up list")

        #swap values at first and last so that values less than pivot are at the front of the list
        #and values greater than the pivot are at the end of the list
        if first < last:
            st.write("Swap values less than and greater than pivot")
            sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last, first], pivot_index=pivot_index, speed= speed)
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
            swap(list_to_sort, first, last)
            sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, first], pivot_index=pivot_index, speed= speed)
        else:
            st.write("Iterator moving up and iterator moving down have passed each other")
            break

    #this swap ensures pivot is in the correct place in the array, with all smaller values to its left
    #and all larger values to its right
    st.write("Swap pivot with the last value less than the pivot")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[last, pivot_index], speed= speed)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, pivot_index], speed= speed)
    swap(list_to_sort, pivot_index, last)
    sorting_vis.render_array_with_pivot(list_to_sort, swap_indices=[last, pivot_index], speed= speed)
    pivot_index = last
    sorting_vis.render_array_with_pivot(list_to_sort, pivot_index=pivot_index, speed= speed)

    #recursively sort the left and right halves of the array (minus the pivot which is already in its sorted position)
    st.write("The pivot is now in its sorted position")
    st.write("Recursively sort the arrays to the left and right of the pivot")
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[range(0, pivot_index)], pivot_index=pivot_index, speed= speed)
    left = quick_sort_smart_pivot(list_to_sort[:pivot_index])
    sorting_vis.render_array_with_pivot(list_to_sort, highlight_indices=[range(pivot_index + 1, len(list_to_sort))], pivot_index=pivot_index, speed= speed)
    right = quick_sort_smart_pivot(list_to_sort[pivot_index + 1:])

    return left + [list_to_sort[pivot_index]] + right