import pandas as pd
from espn_api.football import League
from config import SWID, ESPN_S2, LEAGUE_ID, YEAR

def determine_winner(matchup, week_number, year): 
        home_projection_diff = round(matchup.home_score - matchup.home_projected, 2)
        away_projection_diff = round(matchup.away_score - matchup.away_projected)
        score_diff = round(matchup.home_score - matchup.away_score, 2)
        home_winstreak = matchup.home_team.streak_length if (matchup.home_team.streak_type == "WIN") else 0
        away_winstreak = matchup.away_team.streak_length if (matchup.away_team.streak_type == "WIN") else 0
        home_lossstreak = matchup.home_team.streak_length if (matchup.home_team.streak_type == "LOSS") else 0
        away_lossstreak = matchup.away_team.streak_length if (matchup.away_team.streak_type == "LOSS") else 0
        
        home_team = {'year': year, 
                     'week_number': week_number,
                     'team_name': matchup.home_team, 
                     'score_diff': abs(score_diff), 
                     'projection_diff': home_projection_diff, 
                     'win_streak': home_winstreak,
                     'loss_streak': home_lossstreak} 
        
        away_team = {'year': year, 
                     'week_number': week_number, 
                     'team_name': matchup.away_team, 
                     'score_diff': abs(score_diff), 
                     'projection_diff': away_projection_diff, 
                     'win_streak': away_winstreak,
                     'loss_streak': away_lossstreak}

        if score_diff > 0:
             winner = home_team 
             loser = away_team
        else:
            winner = away_team 
            loser = home_team

        return (winner, loser)

def rank_projection_diff(projection_diff):
     if projection_diff <= 0:
          return 0
     elif 0 < projection_diff <= 5:
          return 1
     elif 5 < projection_diff <= 10:
          return 2
     elif 10 < projection_diff <= 15:
          return 3
     elif 15 < projection_diff <= 20:
          return 4
     else:
          return 5


def rank_score_diff(score_diff):
     if score_diff <= 5:
          return 0
     elif 5 < score_diff <= 10:
          return 1
     elif 10 < score_diff <= 15:
          return 2
     elif 15 < score_diff <= 20:
          return 3
     elif 20 < score_diff <= 25:
          return 4
     else:
          return 5


def rank_win_streak(win_streak):
     if win_streak >= 5:
          return 5
     else:
          return win_streak
    
def enirich_win_df(df):
     enriched_df = df.copy()
     enriched_df['score_diff_rank'] = enriched_df['score_diff'].apply(rank_score_diff)
     enriched_df['projection_diff_rank'] = enriched_df['projection_diff'].apply(rank_projection_diff)
     enriched_df['win_streak_rank'] = enriched_df['win_streak'].apply(rank_win_streak)
     enriched_df['beast_score'] = enriched_df['win_streak_rank'] + enriched_df['projection_diff_rank'] + enriched_df['score_diff_rank']
     return enriched_df

def main():
    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)
    prev_week = league.current_week - 1
    winners_data_row = []
    losers_data_row = []

    for matchup in league.box_scores(prev_week):
        winner_loser = determine_winner(matchup, prev_week, YEAR)
        winners_data_row.append(winner_loser[0])
        losers_data_row.append(winner_loser[1])
    
    winners_base = pd.DataFrame(winners_data_row)
    losers_base = pd.DataFrame(losers_data_row)

    print("winners")
    print(winners_base.head())

    print("Enriched DF")
    print(enirich_win_df(winners_base).head())

    




if __name__ == "__main__":
    main()
