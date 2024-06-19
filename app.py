import streamlit as st
from lida import Manager, llm, TextGenerationConfig
import openai
from PIL import Image
from io import BytesIO
import base64


import os
openai.api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

lida = Manager(text_gen = llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-4o", use_cache=True)

st.title('lida')

main = st.sidebar.selectbox('What would you like to do?', options=['summarization and visualisation','user based visualisation'])

if main=='summarization and visualisation':
    st.subheader("data summarization and visualisation")
    file = st.file_uploader("uploud your file",type="csv")
    if file is not None:
        path_to_save = "data.csv"
        with open(path_to_save,"wb") as f:
            f.write(file.getvalue())
        summary = lida.summarize("data.csv", summary_method="default", textgen_config=textgen_config)
        st.write(summary)
        goals = lida.goals(summary, n=3, textgen_config=textgen_config)
        for goal in goals:
            st.write(goal)
        for i in range(3):
            library = "seaborn"
            textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
            charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)  
            img_base64_string = charts[0].raster
            img = base64_to_image(img_base64_string)
            st.image(img)

elif main=='user based visualisation':
    st.subheader("Ask questions to generate a graph")
    file = st.file_uploader("uploud your file",type="csv")
    if file is not None:
        path_to_save = "data.csv"
        with open(path_to_save,"wb") as f:
            f.write(file.getvalue())
    text_area = st.text_area("Query your Data to Generate Graph", height=200)
    if st.button("generate graph"):
        if len(text_area) > 0:
            st.info("Your Query: " + text_area)
            lida = Manager(text_gen = llm("openai")) 
            textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
            summary = lida.summarize("data.csv", summary_method="default", textgen_config=textgen_config)
            user_query = text_area
            charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)  
            charts[0]
            image_base64 = charts[0].raster
            img = base64_to_image(image_base64)
            st.image(img)

