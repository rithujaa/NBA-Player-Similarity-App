# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from soccerplots.radar_chart import Radar

players = pd.read_csv("NBA/players_data.csv")

del players["Year"]
del players["Unnamed: 0"]

position = players["Pos"]

le = LabelEncoder()
le.fit(players['Pos'])
players['Pos'] = le.transform(players['Pos'])

teams = players["Tm"]
del players["Tm"]

def player_sim():

    X = players.iloc[:,1:28].values

    kmeans_model = KMeans(n_clusters = 3, init = 'k-means++', random_state = 3)
    kmeans_model.fit(X)
    labels = kmeans_model.labels_
    players["Cluster"] = labels
    return players

def euclidean_distance(point1, point2):
    distance = np.linalg.norm(point1 - point2)
    return distance

name = ""
comp_player = ""

def streamlit(players):
    st.title("NBA Player Similiarity App")
    st.markdown("The NBA Player Similarity app is a tool for basketball fans and analysts to find players who have similar statistical profiles to current NBA players. Simply enter the name of a player, and the app will generate a list of players who have similar stats in categories such as points per game, rebounds per game, assists per game, and more. With the NBA Player Similarity app, users can quickly and easily find players who have similar skills and contributions to the players they admire, making it a valuable resource for anyone interested in the history and analysis of the NBA.")
    name = st.selectbox('Enter player name', players['Player'].tolist())
    number = st.number_input("Choose the number of similar players", 10)
    
    players["Team"] = teams
    players["Position"] = position
    player_row = players[players["Player"] == name].iloc[0, 1:28].values
    cluster = players.loc[players["Player"] == name, "Cluster"].iloc[0]
    player_cluster = players.loc[players['Cluster'] == cluster]

    similarity = []

    for i in range(0,len(player_cluster)):
        point1 = player_row
        point2 = player_cluster.iloc[i, 1:28].values
        dis = 100 - euclidean_distance(point1, point2)
        similarity.append(dis)
    
    player_cluster["Similarity %"] = similarity

    similar_players = player_cluster.sort_values("Similarity %", ascending=False)
    similar_players = similar_players[["Player","Age","Position","Team","Similarity %"]].reset_index().drop(0).drop("index", axis=1)
    st.dataframe(similar_players.head(number), use_container_width=True)
    
    comp_player = st.selectbox('Choose a comparison player for Radar chart', similar_players["Player"].head(number).tolist())
    radarchart(name, comp_player)
    
def radarchart(name, comp_player):
    params = ["TRB", "AST", "STL", "BLK", "PTS", "3P", "2P", "FT", "MP", "FG%"]
    ranges = [(players["TRB"].min(), players["TRB"].max()), (players["AST"].min(), players["AST"].max()), (players["STL"].min(), players["STL"].max()), (players["BLK"].min(), players["BLK"].max()), (players["PTS"].min(), players["PTS"].max()), (players["3P"].min(), players["3P"].max()), (players["2P"].min(), players["2P"].max()), (players["FT"].min(), players["FT"].max()), (players["MP"].min(), players["MP"].max()), (players["FG%"].min(), players["FG%"].max())]

    player1 = players[players["Player"] == name]
    player1.reset_index(inplace=True)
    team1 = player1['Team'][0]
    player2 = players[players["Player"] == comp_player]
    player2.reset_index(inplace=True)
    team2 = player2['Team'][0]
    player1 = player1[params]
    player2 = player2[params]
    values = [player1.iloc[0].tolist()], [player2.iloc[0].tolist()]
    values2 = [[player1.iloc[0].tolist()], [player2.iloc[0].tolist()]]
    
    values = sum(values,[])
   
    title = dict(
    title_name = name,
    title_color ='#9B3647',
    subtitle_name = team1,
    subtitle_color ='#ABCDEF',
    title_name_2 = comp_player,
    title_color_2 ='#3282b8',
    subtitle_name_2 = team2,
    subtitle_color_2 ='#ABCDEF',
    title_fontsize = 18,
    subtitle_fontsize = 15,
    )

    radar = Radar(background_color="#121212", patch_color="#28252C", label_color="#F0FFF0",
              range_color="#F0FFF0")
                          
    fig,ax = radar.plot_radar(ranges = ranges, params = params, values = values, 
                           radar_color =['#9B3647', '#3282b8'], 
                           title=title, alphas=[0.55, 0.5], compare=True)
    
    st.pyplot(fig)


def main():
    data = player_sim()
    streamlit(data)
    
main()
