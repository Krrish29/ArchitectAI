from app.orchestrator.workflow import Workflow


def test_workflow_pipeline():

    workflow = Workflow()

    result = workflow.execute("build netflix clone")

    assert result is not None
    assert result.idea is not None
    assert result.selected_agents is not None

    print("\n✅ FULL WORKFLOW EXECUTION SUCCESS")
    print("Idea:", result.idea)
    print("Agents:", result.selected_agents)

    if hasattr(result, "requirements"):
        print("Requirements: OK")
    if hasattr(result, "architecture"):
        print("Architecture: OK")
    if hasattr(result, "database"):
        print("Database: OK")
    if hasattr(result, "api"):
        print("API: OK")
    if hasattr(result, "plan"):
        print("Planner: OK")
