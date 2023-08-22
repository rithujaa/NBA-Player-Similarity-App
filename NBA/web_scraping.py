#!/usr/bin/env python
# coding: utf-8

# In[4]:


get_ipython().system('pip install selenium')
get_ipython().system('pip install chromedriver-binary')
get_ipython().system('pip install webdriver_manager')
get_ipython().system('pip install beautifulsoup4')


# In[ ]:


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.basketball-reference.com/leagues/NBA_2022_per_game.html")
driver.execute_script("window.scrollTo(1,10000)")
time.sleep(2)

html = driver.page_source

with open("/Users/rithujaa/Desktop/NBA/2022.html", "w+") as f:
    f.write(html)

with open("/Users/rithujaa/Desktop/NBA/2022.html") as f:
    page = f.read()
    
soup = BeautifulSoup(page, "html.parser")
soup.find('tr', class_ = "thead").decompose()
player_table = soup.find(id="per_game_stats")
player = pd.read_html(str(player_table))[0]    
player.to_csv("/Users/rithujaa/Desktop/NBA/raw_data.csv")

players = pd.read_csv("/Users/rithujaa/Desktop/NBA/raw_data.csv")
players = players.fillna(0)
del players["Unnamed: 0"]
del players["Rk"]

players["Year"] = "2022"

def single_row(df):
    if df.shape[0] == 1:
        return df
    else:
        row = df[df["Tm"] == "TOT"]
        row["Tm"] = df.iloc[-1,:]["Tm"]
        row["Pos"] = df.iloc[-1,:]["Pos"]
        return row

players = players.groupby(["Player", "Year"]).apply(single_row)

players.index = players.index.droplevel() #run it two times to remove the first 2 index columns

players.to_csv("/Users/rithujaa/Desktop/NBA/players_data.csv")

