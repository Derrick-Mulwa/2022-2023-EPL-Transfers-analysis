from bs4 import BeautifulSoup
import requests
import pandas as pd

url = r"https://www.goal.com/en-ke/lists/all-completed-premier-league-transfers-listed/bltee786573bd1d95b7#cscf7f5e9a2de3304a"
page_content = requests.get(url).content

soup = BeautifulSoup(page_content, "lxml")

teams_list = soup.find("article", class_="article_article__2fbG_ component-article")

teams = teams_list.find_all("li")

dataframe_columns = ['Team_name', 'Player', 'Nationality', 'Transfer_status', 'Previous club', 'New club', 'Fee']

transfer_df = pd.DataFrame(columns=dataframe_columns)

for team_content in teams:
    team = team_content.find("h2")
    try:
        team_name = team.text.replace(" transfers", "")

        header = team_content.find('h3', text='New signings')
        table = header.find_next_sibling('div')
        to_team_df = pd.read_html(str(table))[0]
        to_team_df["Team_name"] = team_name
        to_team_df["Transfer_status"] = "New signing"
        to_team_df["New club"] = team_name

        header = soup.find('h3', text='Departures')
        table = header.find_next_sibling('div')
        from_team_df = pd.read_html(str(table))[0]
        from_team_df["Team_name"] = team_name
        from_team_df["Transfer_status"] = "Departure"
        from_team_df["Previous club"] = team_name

        team_data = pd.concat([to_team_df, from_team_df])
        team_data.drop(columns="Unnamed: 4", inplace=True)

        new_columns_order = ['Team_name', 'Player', 'Nationality', 'Transfer_status', 'Previous club', 'New club',
                             'Fee']
        team_data = team_data.reindex(columns=new_columns_order)




    except:
        continue

    transfer_df = pd.concat([transfer_df, team_data])

transfer_df.reset_index(drop=True, inplace=True)

transfer_df.to_csv("transfers data.csv")
