import time

import streamlit as st
import matplotlib.pyplot as plt
import random

def generate_array(size, value):
    array = [random.randint(-100, 100) for _ in range(size)]
    array[random.randint(0, size - 1)] = value
    return array


def render_array(array, highlight_indices= None, selected_indices= None, not_found= False, speed= 1):
    boxes = ""
    for i, val in enumerate(array):
        if highlight_indices and i in highlight_indices:
            color = "#99FFCC"
        elif selected_indices and i in selected_indices:
            color = "#00CC66"
        elif not_found:
            color = "#FF6666"
        else:
            color = "#00CCCC"
        boxes += f"<div class='box' style='background-color:{color}'>{val}</div>"
    st.markdown(
        f"""
        <style>
        .array-container {{
            white-space: nowrap;  /* keeps boxes on one line */
            overflow-x: auto;      /* allows scrolling if too wide */
            padding: 10px 0;
        }}
        .box {{
            display: inline-block;
            width: 50px;
            height: 50px;
            line-height: 50px;
            border: 2px solid #FFFFFF;
            color: #000000;
            text-align: center;
            margin: 2px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 20px;
        }}
        </style>
        <div class="array-container">{boxes}</div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(1 / speed)