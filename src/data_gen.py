import pandas as pd

def projection_differential(score, projection) -> int:
	return round(score - projection, 2)

def score_differential(home_score, away_score) -> int:
	return round(home_score - away_score, 2)

def rank_projection_diff(projection_diff, result) -> int:
	is_winner = (result == "WIN")
	if is_winner:
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
	else:
		if projection_diff >= 0:
		   return 0
		elif 0 > projection_diff >= -5:
		   return -1 
		elif -5 > projection_diff >= -10:
		   return -2 
		elif -10 > projection_diff >= -15:
		   return -3
		elif -15 > projection_diff >= -20:
		   return -4 
		else:
		   return -5 
	 
def rank_score_diff(score_diff, result) -> int:
	is_winner = (result == "WIN")
	if score_diff <= 5:
		return 0 
	elif 5 < score_diff <= 10:
		return 1 if is_winner else -1
	elif 10 < score_diff <= 15:
		return 2 if is_winner else -2
	elif 15 < score_diff <= 20:
		return 3 if is_winner else -3
	elif 20 < score_diff <= 25:
		return 4 if is_winner else -4
	else:
		return 5 if is_winner else -5

def rank_streak(streak, result, streak_type) -> int:
	is_winner = (result == "WIN")
	if result !=  streak_type:
		return 0
	elif streak >= 5:
		return 5 if is_winner else -5
	else:
		return streak if is_winner else -streak

def process_matchup(matchup, week_number, year) -> tuple: 
	home_projection_diff = projection_differential(matchup.home_score, matchup.home_projected)
	away_projection_diff = projection_differential(matchup.away_score, matchup.away_projected)
	score_diff = score_differential(matchup.home_score, matchup.away_score)
	
	home_team = {'year': year, 
				 'week_number': week_number,
				 'team_name': matchup.home_team,
				 'result' : "WIN" if score_diff > 0 else "LOSS",
				 'score_diff': abs(score_diff), 
				 'projection_diff': home_projection_diff,
				 'streak_type' : matchup.home_team.streak_type,
				 'streak_length' : matchup.home_team.streak_length}
	
	away_team = {'year': year, 
				 'week_number': week_number, 
				 'team_name': matchup.away_team, 
				 'result' : "LOSS" if score_diff > 0 else "WIN",
				 'score_diff': abs(score_diff), 
				 'projection_diff': away_projection_diff, 
				 'streak_type' : matchup.home_team.streak_type,
				 'streak_length' : matchup.home_team.streak_length}
	
	return (home_team, away_team)

def enriches_teams_dataframe(team_df) -> pd.DataFrame:
	enriched_df = team_df.copy()
	enriched_df['score_diff_rank'] = enriched_df.apply(lambda row: rank_score_diff(row['score_diff'], row['result']), axis=1)
	enriched_df['projection_diff_rank'] = enriched_df.apply(lambda row: rank_projection_diff(row['projection_diff'], row['result']), axis=1)
	enriched_df['streak_rank'] = enriched_df.apply(lambda row: rank_streak(row['streak_length'], row['result'], row['streak_type']), axis=1)
	enriched_df['beast_score'] = enriched_df['streak_rank'] + enriched_df['projection_diff_rank'] + enriched_df['score_diff_rank']
	return enriched_df
