# Crew definition
from crewai import Agent, Task, Crew, LLM
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

free_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)


def load_yaml(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


agents_config = load_yaml("src/game_builder_crew/config/agents.yaml")
tasks_config = load_yaml("src/game_builder_crew/config/tasks.yaml")


game_designer = Agent(
    role=agents_config["game_designer"]["role"],
    goal=agents_config["game_designer"]["goal"],
    backstory=agents_config["game_designer"]["backstory"],
    llm=free_llm,
    verbose=True
)

game_developer = Agent(
    role=agents_config["game_developer"]["role"],
    goal=agents_config["game_developer"]["goal"],
    backstory=agents_config["game_developer"]["backstory"],
    llm=free_llm,
    verbose=True
)

code_reviewer = Agent(
    role=agents_config["code_reviewer"]["role"],
    goal=agents_config["code_reviewer"]["goal"],
    backstory=agents_config["code_reviewer"]["backstory"],
    llm=free_llm,
    verbose=True
)


def build_crew(game_request):

    design_task = Task(
        description=f"Create concept for this game: {game_request}",
        expected_output=tasks_config["design_game"]["expected_output"],
        agent=game_designer
    )

    develop_task = Task(
        description=tasks_config["develop_game"]["description"],
        expected_output=tasks_config["develop_game"]["expected_output"],
        agent=game_developer
    )

    review_task = Task(
        description=tasks_config["review_game"]["description"],
        expected_output=tasks_config["review_game"]["expected_output"],
        agent=code_reviewer
    )

    return Crew(
        agents=[game_designer, game_developer, code_reviewer],
        tasks=[design_task, develop_task, review_task],
        verbose=True
    )