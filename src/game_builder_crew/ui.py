import streamlit as st
from crew import build_crew
import subprocess
import os
import sys


# PAGE CONFIG
st.set_page_config(
    page_title="Game Builder Crew",
    page_icon="🎮",
    layout="wide"
)


# BRAND ICON
st.image(
    "https://cdn-icons-png.flaticon.com/512/906/906175.png",
    width=80
)


# STYLE
st.markdown("""
<style>
.big-title {
    font-size:42px;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)


# SIDEBAR SETTINGS
with st.sidebar:
    st.title("🎮 Game Builder Crew")

    game_type = st.selectbox(
        "Game Genre",
        ["Snake", "Platformer", "Puzzle", "Racing", "Shooter", "Custom"]
    )

    difficulty = st.select_slider(
        "Difficulty Level",
        ["Easy", "Medium", "Advanced"]
    )

    engine = st.selectbox(
        "Game Engine",
        ["pygame", "arcade", "tkinter"]
    )

    st.info(
        "AI agents collaborate to generate playable games automatically."
    )


# HEADER
st.markdown(
    '<div class="big-title">AI Game Builder Studio</div>',
    unsafe_allow_html=True
)

st.write(
    "Describe your game idea and generate playable Python code instantly."
)


# USER INPUT
custom_prompt = st.text_input(
    "Describe your game:",
    placeholder="Example: A space shooter with enemy waves and scoring system"
)


# BUTTON
generate_button = st.button("🚀 Generate Game")


# MAIN OUTPUT
if generate_button:

    if custom_prompt.strip() == "":
        st.warning("Please describe your game idea.")

    else:

        full_prompt = f"""
        Create a {difficulty} level {game_type} game
        using {engine}.

        Game description:
        {custom_prompt}
        """

        progress = st.progress(0)

        progress.progress(30, text="Initializing AI Game Designers...")

        crew = build_crew(full_prompt)

        progress.progress(60, text="Agents are writing the code (this might take 1-2 minutes)...")

        result = crew.kickoff()

        progress.progress(100, text="Finalizing build...")

        st.success("Game generated successfully!")

        # SAVE GENERATED GAME
        import re
        game_file = "generated_game.py"
        
        # Strip markdown and conversational text
        final_code = str(result)
        code_match = re.search(r'```(?:python)?\n(.*?)\n```', final_code, re.DOTALL)
        if code_match:
            final_code = code_match.group(1)

        with open(game_file, "w", encoding="utf-8") as f:
            f.write(final_code)


        # TWO PANEL LAYOUT
        left_col, right_col = st.columns(2)


        # LEFT PANEL → CODE VIEW
        with left_col:

            st.subheader("🧠 Generated Code")

            st.code(final_code, language="python")

            st.download_button(
                label="⬇ Download Game File",
                data=final_code,
                file_name="generated_game.py",
                mime="text/python"
            )


        # RIGHT PANEL → LIVE DEMO
        with right_col:

            st.subheader("🎮 Game Demo Preview")

            st.write(
                "Click below to run the generated game."
            )

            if st.button("▶ Run Game Demo"):

                try:
                    import sys
                    
                    if not os.path.exists(game_file):
                        st.error("No game generated yet! Please generate a game first.")
                    else:
                        subprocess.Popen(
                            [sys.executable, game_file],
                            shell=False
                        )
                        st.success("Game launched successfully!")
            
                except Exception as e:
                    st.error(f"Failed to launch game: {e}")