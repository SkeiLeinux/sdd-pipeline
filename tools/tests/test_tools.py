"""Regression tests for the pipeline tools.

Run from the repository root:  python -m unittest discover -s tools/tests -v

The example feature must stay clean (no errors). Every other test copies it to a
temporary folder, breaks one thing and expects the matching rule code.
"""

import copy
import io
import os
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)

import check  # noqa: E402
import sddlib  # noqa: E402
import slices  # noqa: E402
import snapshot  # noqa: E402
import sync_agents  # noqa: E402

ROOT = sddlib.ROOT
EXAMPLE = os.path.join(ROOT, "examples", "LIB-1-book-reservations")


def run_check(fdir, cfg=None, gate=None):
    cfg = cfg or sddlib.load_config(ROOT)
    report = check.Report(ROOT)
    check.check_feature(fdir, ROOT, cfg, report, gate)
    return report


def codes(report, sev=None):
    return {i[3] for i in report.items if sev is None or i[0] == sev}


def edit(path, old, new, count=1):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    assert old in text, "fixture text not found: %r" % old
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.replace(old, new, count))


class ExampleIsClean(unittest.TestCase):
    def test_no_errors(self):
        r = run_check(EXAMPLE)
        self.assertEqual(r.errors, 0, "\n".join(map(str, r.items)))

    def test_gate_contracts_passes(self):
        self.assertEqual(run_check(EXAMPLE, gate="contracts").errors, 0)

    def test_gate_ready_fails(self):
        r = run_check(EXAMPLE, gate="ready")
        self.assertIn("gate", codes(r, "E"))
        self.assertIn("link-spec", codes(r, "E"))

    def test_slices_up_to_date(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(slices.main([EXAMPLE, "--check"]), 0)

    def test_tool_skill_copies_in_sync(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(sync_agents.main(["--check"]), 0, "run python tools/sync_agents.py")


class Broken(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.f = os.path.join(self.tmp, "LIB-1-book-reservations")
        shutil.copytree(EXAMPLE, self.f)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def p(self, *parts):
        return os.path.join(self.f, *parts)

    def expect(self, code, sev="E", cfg=None, gate=None):
        r = run_check(self.f, cfg, gate)
        self.assertIn(code, codes(r, sev), "\n".join(map(str, r.items)))

    def test_duplicate_requirement(self):
        edit(self.p("requirements", "integration-catalog.md"), "| REQ-013 |", "| REQ-001 |")
        self.expect("req-dup")

    def test_unknown_source_section(self):
        edit(self.p("requirements", "integration-catalog.md"), "| 3, 5.3 |", "| 3, 7.9 |")
        self.expect("req-source")

    def test_wrong_column_count(self):
        edit(self.p("requirements", "integration-catalog.md"), "| IR | out | owned by the Catalog team |",
             "| IR | out |")
        self.expect("req-cols")

    def test_marker_on_decided_question(self):
        edit(self.p("specs", "SPEC-11-ui-my-reservations.md"), "## Layout", "## Layout\n\nBranch list [?Q-003].")
        self.expect("marker-closed")

    def test_marker_on_unknown_question(self):
        edit(self.p("specs", "SPEC-11-ui-my-reservations.md"), "## Layout", "## Layout\n\nSomething [?Q-099].")
        self.expect("link-q")

    def test_contract_coverage(self):
        edit(self.p("contracts", "README.md"),
             "| REQ-009 | internal audit log of the reservation service; no consumer in this feature |\n", "")
        self.expect("contract-coverage")

    def test_registry_and_card_disagree(self):
        edit(self.p("contracts", "CON-004-cancel-reservation.md"), "status: review", "status: draft")
        self.expect("contract-mismatch")

    def test_stale_slice(self):
        edit(self.p("source", "source.md"), "at least one available copy", "at least two available copies")
        self.expect("domain-slice")

    def test_section_not_in_index(self):
        edit(self.p("analysis.md"), "| 9 Open points | service-reservations | no requirements in this iteration: "
             "librarian override is postponed |\n", "")
        self.expect("domain-index")

    def test_ui_domain_without_screen_fields(self):
        path = self.p("requirements", "ui-reservations.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.split("## Screen fields")[0])
        self.expect("domain-ui")

    def test_cyrillic_lookalike_id(self):
        edit(self.p("specs", "SPEC-11-ui-my-reservations.md"), "## Layout", "## Layout\n\nSee RЕQ-024.")
        self.expect("id-cyrillic")

    def test_data_model_physical_type(self):
        edit(self.p("specs", "SPEC-02-reservation-data-model.md"), "| `member_id` | string |",
             "| `member_id` | varchar(64) |")
        self.expect("dm-type")

    def test_missing_template_section(self):
        edit(self.p("specs", "SPEC-02-reservation-data-model.md"), "## Migration", "## Moving data")
        self.expect("section")

    def test_api_method_needs_one_contract(self):
        edit(self.p("README.md"), "| REQ-007, REQ-016 | CON-004 |", "| REQ-007, REQ-016 | CON-003, CON-004 |")
        self.expect("plan-contracts")

    def test_plan_coverage(self):
        edit(self.p("README.md"), "| REQ-024, REQ-025, REQ-026 | CON-003, CON-004 |",
             "| REQ-024, REQ-025 | CON-003, CON-004 |")
        edit(self.p("specs", "SPEC-11-ui-my-reservations.md"), "requirements: [REQ-024, REQ-025, REQ-026]",
             "requirements: [REQ-024, REQ-025]")
        self.expect("plan-coverage")

    def test_spec_disagrees_with_plan(self):
        edit(self.p("specs", "SPEC-11-ui-my-reservations.md"), "requirements: [REQ-024, REQ-025, REQ-026]",
             "requirements: [REQ-024, REQ-025]")
        self.expect("spec-plan")

    def test_question_status(self):
        edit(self.p("decisions", "questions.md"), "- Status: open", "- Status: closed")
        self.expect("q-status")

    def test_envelope_rule(self):
        cfg = copy.deepcopy(sddlib.load_config(ROOT))
        cfg["api_response_required_keys"] = ["data"]
        self.expect("api-envelope", cfg=cfg)

    def test_gate_contracts_needs_review(self):
        edit(self.p("contracts", "README.md"), "status: review", "status: draft")
        self.expect("gate", gate="contracts")

    def test_trace_written(self):
        with redirect_stdout(io.StringIO()):
            check.main([self.f, "--trace"])
        text = "\n".join(sddlib.read_lines(self.p("traceability.md")))
        self.assertIn("| REQ-013 | integration-catalog | 3, 5.3 | out |", text)
        self.assertIn("In-scope active requirements: 24.", text)


class Refs(unittest.TestCase):
    NUMS = ["1", "2", "2.1", "2.2", "2.2.1", "3", "3.1", "4"]

    def test_subtree(self):
        self.assertEqual(sddlib.resolve_refs("2", self.NUMS)[0], {"2", "2.1", "2.2", "2.2.1"})

    def test_range_takes_subtree_of_end(self):
        self.assertEqual(sddlib.resolve_refs("2.2-3", self.NUMS)[0], {"2.2", "2.2.1", "3", "3.1"})

    def test_intro(self):
        self.assertEqual(sddlib.resolve_refs("2 (intro)", self.NUMS)[0], {"2"})

    def test_errors(self):
        self.assertTrue(sddlib.resolve_refs("9", self.NUMS)[1])
        self.assertTrue(sddlib.resolve_refs("3-2", self.NUMS)[1])
        self.assertTrue(sddlib.resolve_refs("intro text", self.NUMS)[1])


class Snapshot(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.inp = os.path.join(self.tmp, "in.md")
        self.out = os.path.join(self.tmp, "X-1", "source")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, text):
        with open(self.inp, "w", encoding="utf-8") as f:
            f.write(text)

    def run_snap(self, *extra):
        with redirect_stdout(io.StringIO()) as out:
            code = snapshot.main([self.inp, self.out] + list(extra))
        return code, out.getvalue()

    def test_numbered_input_kept(self):
        self.write("# Doc\n\n## 1 Intro\n\nText.\n\n### 1.1 Detail\n\nMore.\n\n```\n## not a heading\n```\n")
        code, _ = self.run_snap()
        self.assertEqual(code, 0)
        _, secs = sddlib.parse_source(os.path.join(self.out, "source.md"))
        self.assertEqual([s["num"] for s in secs], ["1", "1.1"])

    def test_unnumbered_needs_flag(self):
        self.write("# Doc\n\n## Intro\n\nText.\n")
        code, out = self.run_snap()
        self.assertEqual(code, 1)
        self.assertIn("--number", out)
        code, _ = self.run_snap("--number")
        self.assertEqual(code, 0)

    def test_immutable_and_changes(self):
        self.write("# Doc\n\n## Intro\n\nText.\n\n## Rules\n\nRule A.\n")
        self.assertEqual(self.run_snap("--number")[0], 0)
        self.assertEqual(self.run_snap("--number")[0], 2)
        self.write("# Doc\n\n## Intro\n\nText.\n\n## Rules\n\nRule B.\n\n## New part\n\nX.\n")
        self.assertEqual(self.run_snap("--number", "--force")[0], 0)
        changes = "\n".join(sddlib.read_lines(os.path.join(self.out, "changes.md")))
        self.assertTrue(re.search(r"\| changed \| 2 \| Rules \|", changes))
        self.assertTrue(re.search(r"\| added \| 3 \| New part \|", changes))


if __name__ == "__main__":
    unittest.main()
