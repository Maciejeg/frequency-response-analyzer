import streamlit as st
from test import test_thd

_, x, y = test_thd()

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x,y)
st.pyplot(fig)

fig, ax = plt.subplots()
ax.plot(x,y)
st.pyplot(fig)