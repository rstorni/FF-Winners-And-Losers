import pandas as pd
from espn_api.football import League
from config import SWID, ESPN_S2, LEAGUE_ID, YEAR

def main():
    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)
    current_week = league.current_week
    prev_week = current_week - 1
    winners_data_row = []
    losers_data_row = []

    for matchup in league.box_scores(prev_week):
        # print(f"Home Score: {matchup.home_team} ({matchup.home_score}) VS Away Score: {matchup.away_team} ({matchup.away_score})")

        home_projection_diff = round(matchup.home_score - matchup.home_projected, 2)
        away_projection_diff = round(matchup.away_score - matchup.away_projected)
        score_diff = round(matchup.home_score - matchup.away_score, 2)
        home_team = {'team_name': matchup.home_team, 'score_diff': abs(score_diff), 'projection_diff': home_projection_diff} 
        away_team = {'team_name': matchup.away_team, 'score_diff': abs(score_diff), 'projection_diff': away_projection_diff}

        if score_diff > 0:
            winners_data_row.append(home_team)
            losers_data_row.append(away_team)
        else:
            winners_data_row.append(away_team)
            losers_data_row.append(home_team)
    
    winners = pd.DataFrame(winners_data_row)
    losers = pd.DataFrame(losers_data_row)

    print(winners.head())



if __name__ == "__main__":
    main()
