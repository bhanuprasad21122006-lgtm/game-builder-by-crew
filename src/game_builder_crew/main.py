# Main entry point for the game builder crew
from crew import build_crew

if __name__ == "__main__":

    game_request = input("Enter game idea: ")

    crew = build_crew(game_request)

    result = crew.kickoff()

    print(result)