import logging
import requests
from bs4 import BeautifulSoup as soup
import json
import os

logger = logging.getLogger("logs")
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("logs"), logging.StreamHandler()],
)


class randomPicker:
    def __init__(self, setting):
        # Set song length parameters. It will be the same in all stages
        self.min_length = 90
        self.max_length = 295
        self.tb_min_length = 300
        self.tb_max_length = 420
        self.ar = (0.00, 10.00)

        # Set parameters for stages and mods
        if setting == "ro64" or setting == "round of 64":
            self.nm_rate = (5.80, 6.00)
            self.hr_rate = (5.40, 5.70)
            self.dt_rate = (4.05, 4.25)
            self.dt_range = (5.75, 5.95)
            self.tb_rate = (6.00, 6.15)
            self.dt_ar = (7.00, 8.00)

            self.message = "Round of 64 settings applied"

        elif setting == "ro32" or setting == "round of 32":

            self.nm_rate = (6.00, 6.20)
            self.hr_rate = (5.60, 5.90)
            self.dt_rate = (4.15, 4.35)
            self.dt_range = (5.95, 6.15)
            self.tb_rate = (6.20, 6.35)
            self.dt_ar = (7.00, 8.00)

            self.message = "Round of 32 settings applied"

        elif setting == "ro16" or setting == "round of 16":

            self.nm_rate = (6.20, 6.40)
            self.hr_rate = (5.80, 6.00)
            self.dt_rate = (4.30, 4.45)
            self.dt_range = (6.10, 6.35)
            self.tb_rate = (6.40, 6.55)
            self.dt_ar = (7.00, 8.00)

            self.message = "Round of 16 settings applied"

        elif setting == "qf" or setting == "quarterfinals":

            self.nm_rate = (6.40, 6.60)
            self.hr_rate = (5.90, 6.20)
            self.dt_rate = (4.40, 4.60)
            self.dt_range = (6.30, 6.55)
            self.tb_rate = (6.45, 6.55)
            self.dt_ar = (7.00, 8.50)

            self.message = "Quarterfinals settings applied"

        elif setting == "sf" or setting == "semifinals":

            self.nm_rate = (6.60, 6.80)
            self.hr_rate = (6.20, 6.45)
            self.dt_rate = (4.50, 4.65)
            self.dt_range = (6.50, 6.75)
            self.tb_rate = (6.65, 6.75)
            self.dt_ar = (7.00, 8.80)

            self.message = "Semifinals settings applied"

        elif setting == "f" or setting == "finals":

            self.nm_rate = (6.80, 7.00)
            self.hr_rate = (6.45, 6.80)
            self.dt_rate = (4.60, 4.80)
            self.dt_range = (6.70, 6.90)
            self.tb_rate = (6.95, 7.10)
            self.dt_ar = (7.00, 9.00)

            self.message = "Finals settings applied"

        elif setting == "gf" or setting == "grand finals":

            self.nm_rate = (7.00, 7.20)
            self.hr_rate = (6.75, 7.00)
            self.dt_rate = (4.80, 5.05)
            self.dt_range = (6.65, 6.90)
            self.tb_rate = (7.20, 7.50)
            self.dt_ar = (7.00, 9.00)

            self.message = "Grand Final settings applied"

        else:

            raise ValueError("Invalid Stage")

    # Apply corresponding parameters when mod is chosen
    def randomMapId(self, command):

        if command == "hd" or command == "nm":

            final_max_length = self.max_length
            final_min_length = self.min_length
            final_star_rate = self.nm_rate
            final_approach_rate = self.ar

        elif command == "hr":

            final_max_length = self.max_length
            final_min_length = self.min_length
            final_star_rate = self.hr_rate
            final_hr_range = self.nm_rate
            final_approach_rate = self.ar

        elif command == "dt":

            final_max_length = self.max_length
            final_min_length = self.min_length
            final_star_rate = self.dt_rate
            final_dt_range = self.dt_range
            final_approach_rate = self.dt_ar

        elif command == "tb":

            final_max_length = self.tb_max_length
            final_min_length = self.tb_min_length
            final_star_rate = self.tb_rate
            final_approach_rate = self.ar

        else:
            raise ValueError("Invalid mod settings")

        api_key = os.getenv("API_KEY")

        while True:
            # osusearch returns 5 mapsets that should fit the parameters
            # we only want the first one
            # osusearch pls give me a way to randomly generate 1 mapID thx
            url = f"https://osusearch.com/random/?statuses=Ranked&modes=Standard&min_length={final_min_length}&max_length={final_max_length}&star={final_star_rate}&ar={final_approach_rate}"
            r = requests.get(url).text
            html = soup(r, "html.parser")
            star_difficulty = html.tr.find_all("td")[3].text
            mapsetID = html.a.text

            api_url = f"https://osu.ppy.sh/api/get_beatmaps?k={api_key}&s={mapsetID}"

            r = requests.get(api_url)
            difficulties = json.loads(r.text)

            # we have to loop through all difficulties in the set because we're given the ID of the entire mapset
            for difficulty in difficulties:

                # pick the first map that falls within the star rating range
                if float(difficulty["difficultyrating"]) == float(star_difficulty):

                    beatmap_id = difficulty["beatmap_id"]

                    # need to make another request to determine star rating for difficulty changing mods
                    if command == "dt":

                        dt_url = f"https://osu.ppy.sh/api/get_beatmaps?k={api_key}&b={beatmap_id}&mods=64"
                        dt_r = requests.get(dt_url)
                        dt_data = json.loads(dt_r.text)
                        dt_sr = float(dt_data[0]["difficultyrating"])

                        if dt_sr >= final_dt_range[0] and dt_sr <= final_dt_range[1]:
                            return beatmap_id

                        else:
                            logger.info(
                                f"Map ID: {beatmap_id}\nSR: {dt_sr}*\nDT difficulty out of range. Finding new map."
                            )

                    elif command == "hr":

                        hr_url = f"https://osu.ppy.sh/api/get_beatmaps?k={api_key}&b={beatmap_id}&mods=16"
                        hr_r = requests.get(hr_url)
                        hr_data = json.loads(hr_r.text)
                        hr_sr = float(hr_data[0]["difficultyrating"])

                        if hr_sr >= final_hr_range[0] and hr_sr <= final_hr_range[1]:
                            return beatmap_id

                        else:
                            logger.info(
                                f"Map ID: {beatmap_id}\nSR: {hr_sr}*\nHR difficulty out of range. Finding new map."
                            )

                    else:
                        return beatmap_id
