from app.orchestrator.dependency_resolver import resolve_execution_plan


def test_resolve_execution_plan_api():
    plan = resolve_execution_plan(["api"])
    assert plan == ["requirement", "database", "api"]


def test_resolve_execution_plan_planner():
    plan = resolve_execution_plan(["planner"])
    assert plan == ["requirement", "planner"]


def test_resolve_execution_plan_multiple_selected():
    plan = resolve_execution_plan(["api", "architecture"])
    assert plan == ["requirement", "architecture", "database", "api"]
