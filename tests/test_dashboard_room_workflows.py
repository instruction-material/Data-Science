"""Exercise the course dashboard filters, charts and offline entrypoints."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "DSP-13-module-7-dashboards-with-altair-and-streamlit"
TRANSFER = ROOT / "DSP-14-module-7-dashboards-with-altair-and-streamlit-supplemental-2"
EXTENSION = ROOT / "DSP-15-module-7-dashboards-with-altair-and-streamlit-supplemental-3"


def run_cli(project, *arguments, role="solution"):
    return subprocess.run(
        [sys.executable, "-I", "-B", str(project / role / "main.py"), *arguments],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout


class DashboardRoomTests(unittest.TestCase):
    def dashboard(self, project, role="solution"):
        previous = sys.modules.pop("main", None)

        def restore_main():
            sys.modules.pop("main", None)
            if previous is not None:
                sys.modules["main"] = previous

        self.addCleanup(restore_main)
        app = AppTest.from_file(project / role / "dashboard.py", default_timeout=25).run()
        self.assertFalse(app.exception)
        return app

    def verify_chart(self, element, *, common_domain=None):
        chart = json.loads(element.proto.spec)
        self.assertEqual(chart["mark"]["type"], "bar")
        self.assertEqual(chart["encoding"]["x"]["field"], "room")
        self.assertEqual(chart["encoding"]["y"]["field"], "checkins")
        scale = chart["encoding"]["y"]["scale"]
        if common_domain is None:
            self.assertTrue(scale["zero"])
        else:
            self.assertEqual(scale, {"domain": common_domain, "nice": False})

    def test_project_roles_share_data_and_start_offline(self):
        for project in (CORE, TRANSFER, EXTENSION):
            with self.subTest(project=project.name):
                self.assertTrue(run_cli(project, role="starter").startswith("TODO:"))
                self.assertTrue(run_cli(project))
                self.assertEqual(
                    (project / "starter" / "data/sample.csv").read_bytes(),
                    (project / "solution" / "data/sample.csv").read_bytes(),
                )
        self.assertIn("Tuesday: 9 check-ins", run_cli(CORE, "--day", "Tuesday"))
        self.assertIn("Quiet: 0 check-ins", run_cli(TRANSFER, "--day", "Tuesday", "--room", "Quiet"))
        self.assertIn("No observation", run_cli(TRANSFER, "--day", "Wednesday", "--room", "Quiet"))
        self.assertIn("Shared check-in scale: 0 to 12", run_cli(EXTENSION, "--first", "Wednesday"))

    def test_native_starters_explain_the_missing_computation(self):
        for project in (CORE, TRANSFER, EXTENSION):
            with self.subTest(project=project.name):
                app = self.dashboard(project, role="starter")
                self.assertTrue(app.info[0].value.startswith("Complete "))
                self.assertEqual(len(app.get("vega_lite_chart")), 0)

    def test_core_day_control_updates_metric_table_and_chart(self):
        app = self.dashboard(CORE)
        self.assertEqual(app.metric[0].value, "18")
        self.verify_chart(app.get("vega_lite_chart")[0])
        app.selectbox[0].select("Tuesday").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "9")
        self.assertEqual(app.table[0].value.to_dict(orient="records"), [
            {"room": "Quiet", "checkins": 0}, {"room": "Studio", "checkins": 9},
        ])
        self.assertIn("Tuesday", app.caption[0].value)
        self.verify_chart(app.get("vega_lite_chart")[0])

    def test_transfer_recovers_from_empty_filter_and_preserves_measured_zero(self):
        app = self.dashboard(TRANSFER)
        app.selectbox[0].select("Tuesday")
        app.selectbox[1].select("Quiet").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "0")
        self.assertEqual(len(app.get("vega_lite_chart")), 1)
        app.selectbox[0].select("Wednesday").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.warning[0].value, "No observation for Quiet on Wednesday.")
        self.assertEqual(len(app.get("vega_lite_chart")), 0)
        self.assertEqual(len(app.table), 0)
        app.selectbox[1].select("All rooms").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "4")
        self.assertEqual(app.table[0].value.to_dict(orient="records"), [{"room": "Studio", "checkins": 4}])
        self.verify_chart(app.get("vega_lite_chart")[0])

    def test_extension_keeps_both_domains_identical_across_selections(self):
        app = self.dashboard(EXTENSION)
        for day_a, day_b in (("Monday", "Tuesday"), ("Tuesday", "Wednesday")):
            app.selectbox[0].select(day_a)
            app.selectbox[1].select(day_b).run()
            self.assertFalse(app.exception)
            self.assertEqual([title.value for title in app.subheader], [f"1. {day_a}", f"2. {day_b}"])
            charts = app.get("vega_lite_chart")
            self.assertEqual(len(charts), 2)
            for chart in charts:
                self.verify_chart(chart, common_domain=[0, 12])
        self.assertEqual(app.table[1].value.to_dict(orient="records"), [{"room": "Studio", "checkins": 4}])


if __name__ == "__main__":
    unittest.main()
