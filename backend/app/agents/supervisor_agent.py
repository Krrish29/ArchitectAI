from app.services.llm_service import LLMService
from app.services.json_parser import extract_json
from app.schemas.supervisor_schema import SupervisorResponse


class SupervisorAgent:

    def __init__(self):
        self.llm = LLMService()

    def decide(self, idea: str):

        prompt = f"""
You are an AI Engineering Manager.

Your task is to determine which agents are required
to fulfill the user's request.

AVAILABLE AGENTS

1. requirement
   Generates requirements and features.

2. architecture
   Designs system architecture and tech stack.

3. database
   Designs entities, relationships and indexes.

4. api
   Generates REST APIs and request/response schemas.

5. planner
   Creates implementation roadmap.

PROJECT IDEA:
"{idea}"

INSTRUCTIONS

- Think step by step.
- Select only the agents that are required.
- Never return invalid agent names.
- Never return duplicate agents.
- Never return an empty list.
- Return only valid JSON.

Return this schema:

{{
  "selected_agents": [],
  "reasoning": {{
    "agent_name": "why this agent was selected"
  }}
}}
"""

        response = self.llm.generate(prompt)

        print("===== RAW SUPERVISOR RESPONSE =====")
        print(response)

        try:
            data = extract_json(response)

            supervisor_response = SupervisorResponse(**data)

        except Exception as e:
            print("===== SUPERVISOR PARSE ERROR =====")
            print(e)
            print(response)

            raise ValueError("Supervisor produced invalid JSON.")

        valid_agents = {
            "requirement",
            "architecture",
            "database",
            "api",
            "planner",
        }

        selected_agents = [
            agent
            for agent in supervisor_response.selected_agents
            if agent in valid_agents
        ]

        if not selected_agents:
            raise ValueError("Supervisor returned no agents.")

        print("\n" + "=" * 60)
        print("ARCHITECTAI :: SUPERVISOR AGENT")
        print("=" * 60)

        print(f"\nPROJECT: {idea}")

        print("\nSELECTED AGENTS:")

        for agent in selected_agents:
            print(f"✓ {agent}")

            reason = supervisor_response.reasoning.get(agent)

            if reason:
                print(f"  ↳ {reason}")

        print("=" * 60)

        return {
            "selected_agents": selected_agents,
            "reasoning": supervisor_response.reasoning,
        }
