from app.schemas.final_response import FinalResponse


class BlueprintSummaryService:
    """
    Converts a FinalResponse into a compact textual summary.

    This summary is intentionally concise so it can be sent to
    small language models (e.g. Qwen2.5:3B) without consuming
    unnecessary context.

    The summary is used by:
    - Supervisor update analysis
    - Blueprint Chat (future)
    - AI Suggestions (future)
    - Version Diff (future)
    """

    def build(self, blueprint: FinalResponse) -> str:
        lines = []

        # --------------------------------------------------
        # Project
        # --------------------------------------------------
        lines.append("PROJECT")
        lines.append(blueprint.idea)
        lines.append("")

        # --------------------------------------------------
        # Requirements
        # --------------------------------------------------
        if blueprint.requirements:
            req = blueprint.requirements

            lines.append("REQUIREMENTS")

            if req.project_name:
                lines.append(f"Project Name: {req.project_name}")

            if req.features:
                lines.append("Features:")

                for feature in req.features:
                    lines.append(f"- {feature}")

            lines.append("")

        # --------------------------------------------------
        # Architecture
        # --------------------------------------------------
        if blueprint.architecture:
            lines.append("ARCHITECTURE")
            lines.append(str(blueprint.architecture))
            lines.append("")

        # --------------------------------------------------
        # Database
        # --------------------------------------------------
        if blueprint.database:
            lines.append("DATABASE")
            lines.append(str(blueprint.database))
            lines.append("")

        # --------------------------------------------------
        # API
        # --------------------------------------------------
        if blueprint.api:
            lines.append("API")
            lines.append(str(blueprint.api))
            lines.append("")

        # --------------------------------------------------
        # Planner
        # --------------------------------------------------
        if blueprint.plan:
            lines.append("IMPLEMENTATION PLAN")
            lines.append(str(blueprint.plan))
            lines.append("")

        return "\n".join(lines).strip()
