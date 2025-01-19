# Summerlympics Game

Summerlympics is a dynamic, interactive, team-based game built with Python and Streamlit. It offers an engaging user experience with customizable team configurations, dynamic theming, real-time audio commentary, and flexible game management. The game adapts in real-time to user input, providing a fun and immersive environment for playing various mini-games.

Features
- Interactive Setup: Customize team names, avatars, and game configurations through an intuitive UI.
- Dynamic Theming: Choose from predefined themes or create a custom look with background and text color pickers.
- Real-Time Audio Commentary: Enjoy dynamic audio feedback and commentary tailored to game events using pygame and playsound.
- Flexible Game Management: Randomize game order, add new games, and adjust the number of games dynamically.
- Responsive UI: Utilize Streamlit's layout and session state to manage a seamless and interactive gameplay experience.
- Game Summary: At the end of the game, view a comprehensive summary table including game outcomes and accumulated scores.

## Repository Structure

```plaintext
summerlympics/
├── 1_🏠_Home.py            # Home page script for game setup and customization
├── pages/
│   └── 2_🎲_Game.py         # Main gameplay logic, score tracking, and audio features
├── pictures/           # Directory for background images used in games
├── sounds/             # Directory for audio files (background music, commentary, effects)
├── requirements.txt    # List of Python dependencies
└── README.md           # This file
