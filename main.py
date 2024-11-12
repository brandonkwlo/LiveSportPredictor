import streamlit as st
from cerebras.cloud.sdk import Cerebras
import statsapi # for MLB-StatsAPI
 
cerebras_key = st.secrets["CEREBRAS_API_KEY"]
client = Cerebras(api_key=cerebras_key)

def display_player_stats(id, type):
    df = statsapi.player_stats(id, group = type, type = "career" )
    return st.write(df)

def get_unique_teams(data):
    team_list = set()
    for team in data["teams"]:
        name = team.get('parentOrgName')
        id = team.get('parentOrgId')
        if name and id:
            team_list.add((name, id))

    return sorted(team_list)

def get_roster(data):
    players_list = set()
    for player in data["roster"]:
        players_list.add((player['person']['fullName'], player['person']['id']))

    return sorted(players_list)
    

def main():
    st.title("Live Sports Predictor")

    st.sidebar.header("Settings")
    selected_sport = st.sidebar.selectbox("Select Sport", ["Basketball", "Baseball", "Formula 1", "Football"])


    if selected_sport == "Baseball":
        teams = get_unique_teams(statsapi.get('teams'))
        selected_team = st.sidebar.selectbox("Select Team", [team_name for team_name, _ in teams], key="team_select")
        
        id = 0
        for team_name, team_id in teams:
            if selected_team == team_name:
                id = team_id

        roster = get_roster(statsapi.get('team_roster', {'teamId': id}))
        player = st.sidebar.selectbox("Select Player", [name for name, _ in roster], key="player_select")

        player_id = 0
        for pname, pid in roster:
            if player == pname:
                player_id = pid
                break

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Player Analysis")

        if selected_sport == "Baseball":
            all = ['hitting', 'pitching', 'fielding']
            for i in all:
                display_player_stats(player_id, i)

    with col2:
        st.subheader("Predictions")

if __name__ == "__main__":
    main()