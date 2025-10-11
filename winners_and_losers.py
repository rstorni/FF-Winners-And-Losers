import pandas as pd
from espn_api.football import League
from config import SWID, ESPN_S2, LEAGUE_ID, YEAR

def determine_winner(matchup): 
        home_projection_diff = round(matchup.home_score - matchup.home_projected, 2)
        away_projection_diff = round(matchup.away_score - matchup.away_projected)
        score_diff = round(matchup.home_score - matchup.away_score, 2)
        home_team = {'team_name': matchup.home_team, 'score_diff': abs(score_diff), 'projection_diff': home_projection_diff} 
        away_team = {'team_name': matchup.away_team, 'score_diff': abs(score_diff), 'projection_diff': away_projection_diff}

        if score_diff > 0:
             winner = home_team 
             loser = away_team
        else:
            winner = away_team 
            loser = home_team
        return (winner, loser)

def score_winning_df(winners):
     pass

def score_losing_df(losers):
     pass
     
def main():
    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)
    current_week = league.current_week
    prev_week = current_week - 1
    winners_data_row = []
    losers_data_row = []

    for matchup in league.box_scores(prev_week):
        winner_loser = determine_winner(matchup)
        winners_data_row.append(winner_loser[0])
        losers_data_row.append(winner_loser[1])
    
    winners = pd.DataFrame(winners_data_row)
    losers = pd.DataFrame(losers_data_row)

    print(winners.head())



if __name__ == "__main__":
    main()
