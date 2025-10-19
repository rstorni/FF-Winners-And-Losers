import pandas as pd
import time
from espn_api.football import League
from config import SWID, ESPN_S2, LEAGUE_ID, YEAR
from image_gen import generate_image, add_text, generate_image_vertexAI
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

	for team, beast_score, result in zip(teams_enriched_df['team_name'], teams_enriched_df["beast_score"], teams_enriched_df['result']):
		print(f"{team}, score:{beast_score}")
		top_text = f"What it feels like to be:\n{team.team_name}"
		bottom_text = f"Going into week {league.current_week}"

		theme = "galloping horses" if result == "WIN" else "disapointed cickens, penguins, or rats"

		prompt = create_majestic_prompt(theme, result, beast_score, time.time())
		print(f"{prompt} \n\n")
		image = generate_image_vertexAI(prompt)
		if image is None:
			print(f"Failed to generate image for {team.team_name}")
			continue
		image = add_text(image, top_text, 300, 50, 45)
		image = add_text(image, bottom_text, 300, 900, 45)
		image.save(f"Images/{team.team_name.replace(' ', '_')}_week{league.current_week}_score{beast_score}.png")
	 


if __name__ == "__main__":
	main()
