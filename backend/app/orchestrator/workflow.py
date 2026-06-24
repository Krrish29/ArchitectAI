from app.agents.supervisor_agent import SupervisorAgent
from app.agents.registry import AGENTS
from app.agents.dependencies import DEPENDENCIES
from app.schemas.final_response import FinalResponse


class Workflow:

    def __init__(self):
        self.supervisor = SupervisorAgent()

    def execute(self, idea: str):

        # Supervisor Decision
        decision = self.supervisor.decide(idea)

        selected_agents = decision["selected_agents"]
        reasoning = decision["reasoning"]

        # Resolve Dependencies
        execution_order = []

        for agent in selected_agents:

            for dependency in DEPENDENCIES.get(agent, []):

                if dependency not in execution_order:
                    execution_order.append(dependency)

            if agent not in execution_order:
                execution_order.append(agent)

        print("\nEXECUTION ORDER:")
        for agent in execution_order:
            print(f"✓ {agent}")

        # Outputs
        requirements = None
        architecture = None
        database = None
        api = None
        plan = None

        # Execute Agents
        for agent_name in execution_order:

            print(f"\nRunning -> {agent_name}")

            agent = AGENTS[agent_name]

            if agent_name == "requirement":
                requirements = agent.generate(idea)

            elif agent_name == "architecture":
                architecture = agent.generate(requirements)

            elif agent_name == "database":
                database = agent.generate(requirements)

            elif agent_name == "api":
                api = agent.generate(
                    requirements,
                    architecture,
                    database,
                )

            elif agent_name == "planner":
                plan = agent.generate(
                    requirements,
                    architecture,
                )

        # Final Response
        return FinalResponse(
            idea=idea,
            selected_agents=execution_order,
            reasoning=reasoning,
            requirements=requirements,
            architecture=architecture,
            database=database,
            api=api,
            plan=plan,
        )
