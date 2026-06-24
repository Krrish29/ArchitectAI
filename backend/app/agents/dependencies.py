DEPENDENCIES = {
    "requirement": [],
    "architecture": ["requirement"],
    "database": ["requirement"],
    "api": [
        "requirement",
        "architecture",
        "database",
    ],
    "planner": [
        "requirement",
        "architecture",
        "database",
        "api",
    ],
}
