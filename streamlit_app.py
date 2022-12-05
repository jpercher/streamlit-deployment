
import streamlit as st
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
from math import pi, dist,sqrt
import numpy as np
from copy import deepcopy
from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw

dirname = os.path.dirname(__file__)
dirname_excel = join(join(dirname,"excel"))

ds_path = join(dirname_excel, '.DS_Store')

if os.path.exists(ds_path):
    os.remove(ds_path)

excel_path = join(dirname_excel,listdir(dirname_excel)[0])

df = pd.read_csv(excel_path,delimiter=";",encoding ='ISO-8859-1')

def plot_id_card(solution_name,df):
    # number of variable
    categories=list(df)[1:-3]
    N = len(categories)

    X_VERTICAL_TICK_PADDING = 45
    X_HORIZONTAL_TICK_PADDING = 5 
     
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=df[df["Nom de la solution"]==solution_name].drop(["Nom de la solution","description", "Link","path"],axis=1).values.flatten().tolist()
    values += values[:1]
     
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    H0 = np.zeros(len(angles))
    H1 = np.ones(len(angles)) * 0.5
    H2 = np.ones(len(angles)) *10
     
    # Initialise the spider plot
    fig = plt.figure(figsize=(5,10))
    ax = plt.subplot(111, polar=True)

    ax.grid("pink",linestyle='-', linewidth=2)
    ax.set_facecolor("#18646c")

    # Draw one axe per variable + add labels
    orient = ["center", "left", "center", "left"]

    plt.xticks(angles[:-1], categories, size=15)
     
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0,1,2,3,4], ["0","1","2","3","4"], size=15,color="WHITE")
    plt.ylim(0,4)
    
    # Spacing label
    XTICKS = ax.xaxis.get_major_ticks()
    for tick in XTICKS[0::2]:
        tick.set_pad(X_VERTICAL_TICK_PADDING)
        
    for tick in XTICKS[1::2]:
        tick.set_pad(X_HORIZONTAL_TICK_PADDING)

    ax.set_rlabel_position(50)  # Move radial labels away from plotted line

        
    # Plot data
    ax.plot(angles, values, c="White", linewidth=2, label=categories)
    ax.scatter(angles, values, s=50, c="White", zorder=10)


    
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.25)

    # Show the graph
    st.pyplot(fig)

def write_good_chain(liste):
    l1 = len(liste[0])
    l2 = len(liste[1])
    l3 = len(liste[2])
    res = ""
    return res

def main():
    
    st.sidebar.image("./images/caplogo invent 2.png")

    st.title("BENCHMARK​ CARBON ASSESSMENT​")
    st.header('Motivations')
    st.markdown("- Identify existing carbon assessment market solutions for scope 3​")
    st.markdown("- Understanding the market and industry initiatives​")
    st.markdown('- Capture the evolution of the market and the new technological perspectives​')
    st.header('Overview of our methodology')
    st.image('./images/methodo.png')
    st.header('Guidelines')
    st.markdown("In the sidebar menu, note each of the following features from **not important** to **very important** based on their relevance to your project requirements. ")    
    st.sidebar.title("Features Prioritization")
    # If the user doesn't want to select which features to control, these will be used.
    default_control_features = ["Emission Measurement​", "Action Plan Definition​", "Automation​","Upskilling"]


    # Insert user-controlled values from sliders into the feature vector.
    vector = []
    for feature in default_control_features:
        dic = {'Not Important':1, "Important":2, "Very Important":3}
        #feature_value = st.sidebar.slider(feature, 0, 3,0,1)
        feature_value = st.sidebar.select_slider(f'How {feature} is important for your company ?',options=['Not Important', 'Important', 'Very Important'],value="Important")
        vector.append(dic[f"{feature_value}"])
        st.sidebar.write('\n')
        st.sidebar.write('\n')
        
    if vector != [0,0,0,0]:
        # Generate a new image from this feature vector (or retrieve it from the cache).
        df_res = deepcopy(df)

        #df_res.loc[:,"total"] = vector[0]*df["Emission"] + vector[1]*df["Action Plan"] +vector[2]*df["Automation"] +vector[3]*df["Upskilling"]

        df_res.loc[:,"total"] = (vector[0]-df_res["Emission"])**2 + (vector[1]-df_res["Action Plan"])**2 +(vector[2]-df_res["Automation"])**2 +(vector[3]-df_res["Upskilling"])**2
        df_res["total"] = df_res["total"].apply(lambda x: sqrt(x))
        
        #df_res = df_res[df_res["total"] == df_res["total"].max()]
        df_best = df_res[df_res["total"] == df_res["total"].min()]

        
        solution_name = df_best["Nom de la solution"].values[0]
        
        descrip = df[df["Nom de la solution"]==solution_name]["description"].values[0]
        website = df[df["Nom de la solution"]==solution_name]["Link"].values[0]
        path = df[df["Nom de la solution"]==solution_name]["path"].values[0]
            
        #st.header(f'Your Solution : {solution_name}')
        st.image(f'./images/logo/{path}')
        for i in range (2):
            st.write("\n")
        plot_id_card(solution_name,df)
        st.subheader("Description :")
        st.write(descrip)
        st.subheader("Website :")
        st.write(website)
        list_solutions = list(df_res.sort_values(by = 'total', ascending = True)["Nom de la solution"].values)[1:4]
        font = ImageFont.truetype("./font/arial.ttf", 80)

        img = Image.open('./images/podium.jpeg') 
        draw = ImageDraw.Draw(img)
        draw.text((327-len(list_solutions[0])/2*40, 680),f"{list_solutions[0]}",(0,0,0),font=font)
        draw.text((1055-len(list_solutions[1])/2*40, 680),f"{list_solutions[1]}",(0,0,0),font=font)
        draw.text((1740-len(list_solutions[2])/2*40, 680),f"{list_solutions[2]}",(0,0,0),font=font)

        for i in range (2):
            st.write("\n")
        st.header('Alternative Solutions')
        
        st.image(img)

       


if __name__ == "__main__":
    main()
