class ArchitectureAgent:

    def generate(self, requirements):

        return {
            "frontend": "ReactJS",
            "backend": "FastAPI",
            "database": "SQLite",
            "authentication": "JWT",
            "deployment": [
                "Vercel",
                "Render"
            ]
        }