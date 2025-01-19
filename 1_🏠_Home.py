# intro.py

import streamlit as st
import math
import os
import pygame
import random


st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

def initialize_session_state():
    if 'setup_complete' not in st.session_state:
        st.session_state.setup_complete = False
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = {'background': '#FFD700', 'text': '#727272'}  # Default theme
    if 'selected_theme_name' not in st.session_state:
        st.session_state.selected_theme_name = 'Default'
    if 'game_name' not in st.session_state:
        st.session_state.game_name = 'Summerlympics'
    if 'P1' not in st.session_state:
        st.session_state.P1 = 'Team A'
    if 'P2' not in st.session_state:
        st.session_state.P2 = 'Team B'
    if 'P1_avatar' not in st.session_state:
        st.session_state.P1_avatar = '+'
    if 'P2_avatar' not in st.session_state:
        st.session_state.P2_avatar = '+'
    if 'total_games' not in st.session_state:
        st.session_state.total_games = 10
    if 'available_games' not in st.session_state:
        st.session_state.available_games = []
    if 'game_slots' not in st.session_state:
        st.session_state.game_slots = [''] * st.session_state.total_games
    if 'Games' not in st.session_state:
        st.session_state.Games = {}
    if 'target_score' not in st.session_state:
        st.session_state.target_score = 0
    if 'num_games_slider' not in st.session_state:
        st.session_state.num_games_slider = st.session_state.total_games
    if 'game_winners' not in st.session_state:
        st.session_state.game_winners = {}

initialize_session_state()  # Initialize session state at the top

st.markdown(
    """
    <style>
    .reset-button {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 1;
    }
    .reset-button input[type="submit"] {
        background-color: rgb(29, 30, 36);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .reset-button input[type="submit"]:hover {
        background-color: rgb(230, 65, 65);
    }
    </style>
    <div class="reset-button">
        <form action="">
            <input type="submit" value="Reset">
        </form>
    </div>
    """, unsafe_allow_html=True
)

# Reset logic if necessary
if st.session_state.get('reset_clicked', False):
    initialize_session_state()

pygame.init()
pygame.mixer.init()

def play_audio(file_path):
    """Play an audio file using pygame.mixer."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def apply_theme():
    color = st.session_state.selected_theme.get('background', '#FFD700')
    color_m = st.session_state.selected_theme.get('text', '#727272')
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {color};
                color: {color_m};
            }}
            .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp div, .stApp label, .stApp span {{
                color: {color_m};
            }}
            .range-labels {{
                display: flex;
                justify-content: space-between;
                margin-top: -20px;
                font-size: 12px;
                color: gray;
            }}
            .add-game {{
                margin-top: 10px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def show_intro_page():
    st.title("Game Setup")

    # Hall of Fame Section
    st.subheader("Replay from Hall of Fame")
    hof_games = {
        'Floridalympics 2024': {
            'game_name': 'Floridalympics',
            'P1': 'Ladies',
            'P2': 'Gentlemen',
            'color_background': '#FFD700',
            'color_text': '#20B2AA',
            'song': 'Europapa',
            'P1_avatar': '👸',
            'P2_avatar': '👨',
            'Games': [
                'Flip Suck Lick',
                'I am a Peach',
                'Music Quiz',
                'Beer Mile',
                'Who am I',
                'Flunkyball',
                'Pi Memorizing',
                'Water Egg Relay',
                'Beerpong',
                'Guessing Quiz',
                'Water Tic Tac Toe',
                'Bangers',
                'Limbo',
                'Yes No Uh',
                'Kaputtmachen'
            ]
        },
        'Summerlympics 2023': {
            'game_name': 'Summerlympics 3.0 - Schultenbräu Edition',
            'P1': 'Push',
            'P2': 'BigNaz',
            'color_background': '#FFD700',
            'color_text': '#727272',
            'song': 'Schultenbräu',
            'P1_avatar': '🫸',
            'P2_avatar': '🥜',
            'Games': [
                'Flip Suck Lick',
                'I am a Peach',
                'Music Quiz',
                'Kaputtmachen',
                'Who am I',
                'Flunkyball',
                'Spikeball',
                'Beerpong',
                'Bangers',
                'Beer Mile',
                'Jeu de boules',
                'Last man standing',
                'Guessing Quiz',
                'Speedrolling',
                'Music Video'
            ]
        },
        'Summerlympics 2022': {
            'game_name': 'Summerlympics',
            'P1': 'Couple Trouble',
            'P2': 'Cockinators',
            'color_background': '#FFD700',
            'color_text': '#727272',
            'song': 'Layla',
            'P1_avatar': '👫',
            'P2_avatar': '🍆',
            'Games': [
                'Flip Suck Lick',
                'I am a Peach',
                'Music Quiz',
                'Kaputtmachen',
                'Who am I',
                'Flunkyball',
                'Spikeball',
                'Beerpong',
                'Bangers',
                'Beer Mile',
                'Jeu de boules',
                'Last man standing',
                'Guessing Quiz',
                'Speedrolling',
                'Music Video'
            ]
        },
        'Birthday Battle 2022': {
            'game_name': 'Birthday Battle',
            'P1': 'Laura',
            'P2': 'Niklas',
            'color_background': '#FFD700',
            'color_text': '#727272',
            'song': 'YMCA',
            'P1_avatar': '🦹',
            'P2_avatar': '🦸‍♂️',
            'Games': [
                'Flip Suck Lick',
                'I am a Peach',
                'Who am I',
                'Flunkyball',
                'Spikeball',
                'Three legged race',
                'Beerpong',
                'Music Video',
                'Workout',
                'Bangers',
                'Egg Relay',
                'Jeu de boules',
                'Civil War',
                'Minigolf',
                'Yes No Uh']
        }
    }
    
    cols = st.columns(len(hof_games))
    for idx, (name, details) in enumerate(hof_games.items()):
        with cols[idx]:
            button_label = f"{name}"
            button_clicked = st.button(button_label, key=f"hof_{name}")
            if button_clicked:
                play_audio(f"sounds/{details['song']}.mp3")
                st.session_state.game_name = details['game_name']
                st.session_state.P1 = details['P1']
                st.session_state.P2 = details['P2']
                st.session_state.P1_avatar = details['P1_avatar']
                st.session_state.P2_avatar = details['P2_avatar']
                st.session_state.selected_theme = {
                    'background': details['color_background'],
                    'text': details['color_text']
                }
                st.session_state.selected_theme_name = 'Custom'
                st.session_state["num_games_slider"] = len(details['Games'])
                st.session_state.total_games = len(details['Games'])
                st.session_state.Games = {i+1: details['Games'][i] for i in range(len(details['Games']))}
                st.session_state.game_slots = details['Games']
                st.session_state.available_games = list(set(details['Games']))
                for i in range(len(details['Games'])):
                    st.session_state[f"game_slot_{i}"] = details['Games'][i]
                st.rerun()

    apply_theme()

    st.subheader("Customize Your Game")
    game_name = st.text_input("Enter the Game Name", value=st.session_state.game_name)
    st.session_state.game_name = game_name

    st.markdown(
        """
        <style>
        [data-baseweb="input"] input {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 0.75, 7])
    with col1:
        st.markdown(f"""
        <div style="border: 2px dashed; border-radius: 50%; width: 75px; height: 75px; display: flex; align-items: center; justify-content: center; font-size: 60px; margin: 0 auto;">
            {st.session_state.P1_avatar}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        def update_p1_avatar():
            st.session_state.P1_avatar = st.session_state.player1_emoji
        st.text_input(
            "Avatar",
            value=st.session_state.P1_avatar,
            key="player1_emoji",
            #label_visibility="hidden",
            max_chars=2,
            on_change=update_p1_avatar
        )
    with col3:
        P1 = st.text_input("Enter the name of Team 1", value=st.session_state.P1, key="player1_name")
        st.session_state.P1 = P1
    
    col1, col2, col3 = st.columns([1, 0.75, 7])
    with col1:
        st.markdown(f"""
        <div style="border: 2px dashed; border-radius: 50%; width: 75px; height: 75px; display: flex; align-items: center; justify-content: center; font-size: 60px; margin: 0 auto;">
            {st.session_state.P2_avatar}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        def update_p2_avatar():
            st.session_state.P2_avatar = st.session_state.player2_emoji
        st.text_input(
            "Avatar",
            value=st.session_state.P2_avatar,
            key="player2_emoji",
            #label_visibility="hidden",
            max_chars=2,
            on_change=update_p2_avatar
        )
    with col3:
        P2 = st.text_input("Enter the name of Team 2", value=st.session_state.P2, key="player2_name")
        st.session_state.P2 = P2

    st.subheader("Select Number of Games")
    num_games = st.slider(
        'Select the number of games to play:',
        min_value=5,
        max_value=15,
        step=1,
        key="num_games_slider"
    )
    st.session_state.total_games = num_games

    if len(st.session_state.game_slots) < num_games:
        st.session_state.game_slots.extend([''] * (num_games - len(st.session_state.game_slots)))
    elif len(st.session_state.game_slots) > num_games:
        st.session_state.game_slots = st.session_state.game_slots[:num_games]

    st.markdown("""
    <div class="range-labels">
        <span>Short (5)</span>
        <span>Medium (10)</span>
        <span>Long (15)</span>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Assign Games to Each Slot")
    predefined_games = [
        'Bangers', 'Beerpong', 'Beer Mile', 'Civil War', 'Egg Relay',
        'Flip Suck Lick', 'Flunkyball', 'Guessing Quiz', 'I am a Peach',
        'Jeu de Boules', 'Kaputtmachen', 'Last Man Standing', 'Limbo',
        'Minigolf', 'Music Quiz', 'Music Video', 'Pi Memorizing',
        'Speedrolling', 'Spikeball', 'Three Legged Race', 'Water Egg Relay',
        'Waterpolo', 'Water Tic Tac Toe', 'Workout', 'Who am I', 'Yes No Uh'
    ]

    if not st.session_state.available_games:
        st.session_state.available_games = predefined_games.copy()
    else:
        for game in predefined_games:
            if game not in st.session_state.available_games:
                st.session_state.available_games.append(game)

    st.markdown('<div class="add-game">', unsafe_allow_html=True)
    new_game = st.text_input("Add a new game to the list:")
    if st.button("Add Game"):
        if new_game.strip() != '':
            if new_game not in st.session_state.available_games:
                st.session_state.available_games.append(new_game.strip())
                st.success(f"Added '{new_game.strip()}' to available games.")
                new_game = ''
            else:
                st.warning(f"'{new_game.strip()}' is already in the list.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Shuffle game order"):
        assigned_games_list = [game for game in st.session_state.game_slots if game]
        random.shuffle(assigned_games_list)
        for i in range(len(assigned_games_list)):
            st.session_state.game_slots[i] = assigned_games_list[i]

    if st.button("Randomly select games from the list"):
        available_games_set = set(st.session_state.available_games)
        if len(available_games_set) >= num_games:
            random_games = random.sample(list(available_games_set), num_games)
            for i in range(num_games):
                st.session_state.game_slots[i] = random_games[i]
        else:
            st.warning("Not enough games in the available games list to select randomly.")

    st.write("### Game Slots")

    def update_game_slot(i):
        st.session_state.game_slots[i] = st.session_state[f"game_slot_{i}"]

    for i in range(num_games):
        key_name = f"game_slot_{i}"
        if key_name not in st.session_state:
            st.session_state[key_name] = st.session_state.game_slots[i]

        st.selectbox(
            f"Game {i+1}",
            options=[''] + st.session_state.available_games,
            index=([''] + st.session_state.available_games).index(st.session_state.game_slots[i]) if st.session_state.game_slots[i] in st.session_state.available_games else 0,
            key=key_name,
            on_change=update_game_slot,
            args=(i,)
        )

    st.subheader("Select Theme")
    themes = {
        'Default': {'background': '#FFD700', 'text': '#727272'},
        'Ocean': {'background': '#1E90FF', 'text': '#FFFFFF'},
        'Forest': {'background': '#228B22', 'text': '#FFFFFF'},
        'Sunset': {'background': '#FF4500', 'text': '#FFFFFF'},
        'Night': {'background': '#2F4F4F', 'text': '#FFFFFF'},
        'Custom': {'background': '', 'text': ''}
    }

    def update_theme():
        selected_theme_name = st.session_state['selected_theme_name']
        st.session_state.selected_theme_name = selected_theme_name
        if selected_theme_name == 'Custom':
            background_color = st.session_state.get('background_color_picker', '#FFD700')
            text_color = st.session_state.get('text_color_picker', '#727272')
            st.session_state.selected_theme = {'background': background_color, 'text': text_color}
        else:
            st.session_state.selected_theme = themes[selected_theme_name]
        apply_theme()

    st.selectbox(
        "Choose a theme:",
        options=list(themes.keys()),
        index=list(themes.keys()).index(st.session_state.selected_theme_name),
        key='selected_theme_name',
        on_change=update_theme
    )

    if st.session_state.selected_theme_name == 'Custom':
        st.color_picker(
            "Pick a background color:",
            value=st.session_state.selected_theme.get('background', '#FFD700'),
            key='background_color_picker',
            on_change=update_theme
        )
        st.color_picker(
            "Pick a text color:",
            value=st.session_state.selected_theme.get('text', '#727272'),
            key='text_color_picker',
            on_change=update_theme
        )

    apply_theme()

    if st.button("Start Game"):
        # Validate that all game slots are filled
        if any(slot == '' for slot in st.session_state.game_slots):
            st.error("Please assign a game to each game slot.")
            return

        all_games = st.session_state.game_slots[:num_games]
        st.session_state.Games = {i+1: all_games[i] for i in range(len(all_games))}

        total_points = num_games * (num_games + 1) // 2
        target_score = math.floor(total_points / 2) + 1
        st.session_state.target_score = target_score

        st.session_state.setup_complete = True
        st.session_state.p1_score = 0
        st.session_state.p2_score = 0
        st.session_state.current_game = 1
        st.session_state.games_played = []
        st.session_state.show_minigame = False
        st.session_state.celebration = None
        st.session_state.winner = None
        st.session_state.game_over = False
        st.session_state.balloons_shown = False
        st.session_state.warning = False
        st.session_state.game_over_handled = False
        st.session_state.game_winners.clear()

        st.switch_page("pages/2_🎲_Game.py")
        st.stop()

show_intro_page()
