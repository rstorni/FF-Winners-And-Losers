import pandas as pd
import time
from espn_api.football import League
from config import SWID, ESPN_S2, LEAGUE_ID, YEAR
from image_gen import generate_image, add_text
from prompt_gen import create_majestic_prompt
from data_gen import process_matchup, enriches_teams_dataframe


def main():
	league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)
	prev_week = league.current_week - 1
	team_data = []

	for matchup in league.box_scores(prev_week):
		for team in process_matchup(matchup, prev_week, YEAR):
			team_data.append(team)
			
	teams_base_df = pd.DataFrame(team_data)
	teams_enriched_df = enriches_teams_dataframe(teams_base_df)
	print(teams_enriched_df.head(16))

	for team, beast_score in zip(winners_enriched_df['team_name'], winners_enriched_df["beast_score"]):
		print(f"{team}, score:{beast_score}")
		top_text = f"what it feels like to be: {team.team_name}"
		bottom_text = f"Going into week {league.current_week}"

		prompt = create_majestic_prompt("galloping horses", beast_score, time.time())
		print(prompt)
		image = generate_image(prompt, "prompthero/openjourney")
		image = add_text(image, top_text, 50, 50, 20)
		image = add_text(image, bottom_text, 50, 450, 20)
		image.save(f"Images/{team.team_name.replace(' ', '_')}_week{league.current_week}_score{beast_score}.png")
	 


if __name__ == "__main__":
	main()
