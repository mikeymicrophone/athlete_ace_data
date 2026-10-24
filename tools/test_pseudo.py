"""Check the generated pseudo catalog without Rails or network access."""
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1] / "pseudo"


class PseudoCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = [record for path in sorted(ROOT.glob("*.yml"))
                       for record in yaml.safe_load(path.read_text())["records"]]
        cls.by_code = {record["code"]: record for record in cls.records}
        cls.by_type = defaultdict(list)
        for record in cls.records:
            cls.by_type[record["type"]].append(record)

    def test_coverage_and_unique_resolvable_codes(self):
        self.assertEqual(len(self.records), len(self.by_code))
        expected = {"League": 3, "Season": 9, "Team": 24, "Conference": 6,
                    "Division": 12, "Campaign": 72, "Player": 472,
                    "Contract": 1416, "Activation": 1416, "Stint": 1416,
                    "Game": 567, "ContestGame": 567, "TitleAward": 18}
        for kind, count in expected.items():
            self.assertEqual(len(self.by_type[kind]), count, kind)
        self.assertNotIn("Appearance", self.by_type)
        for record in self.records:
            for reference in record["references"].values():
                self.assertIn(reference, self.by_code, record["code"])

    def test_rosters_contracts_and_assignments_cover_every_season(self):
        memberships = Counter()
        histories = defaultdict(list)
        for activation in self.by_type["Activation"]:
            refs = activation["references"]
            campaign = self.by_code[refs["campaign"]]
            contract = self.by_code[refs["contract"]]
            player = self.by_code[refs["player"]]
            team = campaign["references"]["team"]
            self.assertEqual(contract["references"]["player"], player["code"])
            self.assertEqual(contract["references"]["team"], team)
            season = self.by_code[campaign["references"]["season"]]
            for field in ("start_date", "end_date"):
                self.assertEqual(activation["attributes"][field], contract["attributes"][field])
            self.assertLessEqual(contract["attributes"]["start_date"], season["attributes"]["start_date"])
            self.assertGreaterEqual(contract["attributes"]["end_date"], season["attributes"]["playoff_end_date"])
            memberships[campaign["code"]] += 1
            histories[player["code"]].append(team)
        self.assertEqual(set(memberships), {r["code"] for r in self.by_type["Campaign"]})
        self.assertEqual(Counter(memberships.values()), {12: 24, 24: 24, 23: 24})
        self.assertTrue(all(len(teams) == 3 for teams in histories.values()))
        self.assertEqual(sum(len(set(teams)) > 1 for teams in histories.values()), 48)
        for campaign in self.by_type["Campaign"]:
            division = self.by_code[campaign["references"]["division"]]
            self.assertEqual(division["references"]["conference"], campaign["references"]["conference"])

    def test_regular_schedules_have_every_pair_home_and_away_without_double_booking(self):
        entries = defaultdict(list)
        links = defaultdict(list)
        for entry in self.by_type["Contestant"]:
            entries[entry["references"]["contest"]].append(entry)
        for link in self.by_type["ContestGame"]:
            links[link["references"]["contest"]].append(link)
        for contest in self.by_type["Contest"]:
            if contest["attributes"]["kind"] != "regular_season":
                continue
            self.assertEqual(len(links[contest["code"]]), 56)
            pairs = Counter()
            bookings = set()
            for link in links[contest["code"]]:
                game = self.by_code[link["references"]["game"]]
                game_entries = entries[game["code"]]
                self.assertEqual(len(game_entries), 2)
                sides = {entry["attributes"]["tiebreakers"]["side"]: entry["references"]["campaign"]
                         for entry in game_entries}
                self.assertNotEqual(sides["home"], sides["away"])
                pairs[(sides["home"], sides["away"])] += 1
                for campaign in sides.values():
                    booking = (campaign, game["attributes"]["begin_date"])
                    self.assertNotIn(booking, bookings)
                    bookings.add(booking)
                    self.assertEqual(game["references"]["season"], self.by_code[campaign]["references"]["season"])
            self.assertEqual(len(pairs), 56)
            self.assertEqual(set(pairs.values()), {1})

    def test_game_membership_dates_rounds_and_title_winners(self):
        for link in self.by_type["ContestGame"]:
            game = self.by_code[link["references"]["game"]]
            contest = self.by_code[link["references"]["contest"]]
            played_on = date.fromisoformat(game["attributes"]["begin_date"])
            self.assertGreaterEqual(played_on, date.fromisoformat(contest["attributes"]["begin_date"]))
            self.assertLessEqual(played_on, date.fromisoformat(contest["attributes"]["end_date"]))
            if contest["attributes"]["kind"] == "playoffs":
                self.assertIn(link["attributes"]["metadata"]["round"],
                              [r["key"] for r in contest["attributes"]["format_rules"]["rounds"]])
        for award in self.by_type["TitleAward"]:
            winner = self.by_code[award["references"]["winner"]]
            self.assertEqual(winner["references"]["contest"], award["references"]["contest"])


if __name__ == "__main__":
    unittest.main()
