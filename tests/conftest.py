"""Shared fixtures and test parametrization for agent-skills tests."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest
from skills_ref import read_properties

SKILLS_DIR = Path(__file__).parent.parent / "skills"


@dataclass
class TriggerCase:
    skill_path: Path
    skill_name: str
    query: str
    should_trigger: bool


def _all_skill_paths() -> list[Path]:
    return sorted(p.parent for p in SKILLS_DIR.glob("*/SKILL.md"))


def _collect_trigger_cases() -> list[TriggerCase]:
    cases = []
    for skill_path in _all_skill_paths():
        trigger_file = skill_path / "evals" / "trigger-evals.json"
        if not trigger_file.exists():
            continue
        props = read_properties(skill_path)
        for case in json.loads(trigger_file.read_text()):
            cases.append(TriggerCase(
                skill_path=skill_path,
                skill_name=props.name,
                query=case["query"],
                should_trigger=case["should_trigger"],
            ))
    return cases


def _trigger_case_id(case: TriggerCase) -> str:
    label = "should-trigger" if case.should_trigger else "no-trigger"
    return f"{case.skill_name}[{label}] {case.query[:50]}"


def pytest_addoption(parser):
    parser.addoption(
        "--skill",
        default=None,
        metavar="NAME",
        help="Only run tests for the named skill (e.g. --skill gitbook-docs)",
    )


def pytest_collection_modifyitems(config, items):
    skill = config.getoption("--skill")
    if not skill:
        return
    filtered = []
    for item in items:
        # Filter skill_path fixture (structure tests)
        if hasattr(item, "callspec") and "skill_path" in item.callspec.params:
            if item.callspec.params["skill_path"].name != skill:
                continue
        # Filter trigger_case fixture (trigger tests)
        if hasattr(item, "callspec") and "trigger_case" in item.callspec.params:
            if item.callspec.params["trigger_case"].skill_name != skill:
                continue
        filtered.append(item)
    items[:] = filtered


@pytest.fixture(
    params=_all_skill_paths(),
    ids=lambda p: p.name,
)
def skill_path(request) -> Path:
    return request.param


@pytest.fixture(
    params=_collect_trigger_cases(),
    ids=_trigger_case_id,
)
def trigger_case(request) -> TriggerCase:
    return request.param


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.failed and "tmp_path" in item.funcargs:
        rep.sections.append(("Artifacts", str(item.funcargs["tmp_path"])))
