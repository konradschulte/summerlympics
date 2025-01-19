# pages/Main.py

import streamlit as st
from streamlit_extras.let_it_rain import rain
import time
import base64
import os
import pygame
import threading
import random
import pandas as pd

# -------------------------------------------------
# 1) Session State Initialization
# -------------------------------------------------
def initialize_session_state():
    if 'setup_complete' not in st.session_state:
        st.session_state.setup_complete = False
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
    if 'Games' not in st.session_state:
        st.session_state.Games = {}
    if 'total_games' not in st.session_state:
        st.session_state.total_games = 5
    if 'target_score' not in st.session_state:
        st.session_state.target_score = 0
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = {'background': '#FFD700', 'text': '#20B2AA'}
    if 'p1_score' not in st.session_state:
        st.session_state.p1_score = 0
    if 'p2_score' not in st.session_state:
        st.session_state.p2_score = 0
    if 'current_game' not in st.session_state:
        st.session_state.current_game = 1
    if 'games_played' not in st.session_state:
        st.session_state.games_played = []
    if 'show_minigame' not in st.session_state:
        st.session_state.show_minigame = False
    if 'celebration' not in st.session_state:
        st.session_state.celebration = None
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'balloons_shown' not in st.session_state:
        st.session_state.balloons_shown = False
    if 'warning' not in st.session_state:
        st.session_state.warning = False
    if 'game_over_handled' not in st.session_state:
        st.session_state.game_over_handled = False
    if 'game_winners' not in st.session_state:
        st.session_state.game_winners = {}
    if 'is_tie' not in st.session_state:
        st.session_state.is_tie = False

    # Available games for random expansion
    if 'available_games' not in st.session_state:
        st.session_state.available_games = [
            "Game A", "Game B", "Game C", "Game D", "Game E",
            "Game F", "Game G", "Game H", "Game I", "Game J"
        ]

    # For the slider
    if 'ingame_num_games_slider' not in st.session_state:
        st.session_state.ingame_num_games_slider = st.session_state.total_games

    # Sound logic
    if 'prev_p1_score' not in st.session_state:
        st.session_state.prev_p1_score = 0
    if 'prev_p2_score' not in st.session_state:
        st.session_state.prev_p2_score = 0
    if 'p1_streak' not in st.session_state:
        st.session_state.p1_streak = 0
    if 'p2_streak' not in st.session_state:
        st.session_state.p2_streak = 0
    if 'last_winner' not in st.session_state:
        st.session_state.last_winner = None
    if 'last_game_number' not in st.session_state:
        st.session_state.last_game_number = 0

# -------------------------------------------------
# 2) Score + Audio Logic
# -------------------------------------------------
def update_score(player, game_number):
    if player == 'p1':
        st.session_state.p1_score += game_number
    else:
        st.session_state.p2_score += game_number
    st.session_state.games_played.append(game_number)

def play_audio(file_path):
    pass
    #def play_sound():
    #    try:
    #        sound = pygame.mixer.Sound(file_path)
    #        sound.play()
    #    except Exception as e:
    #        print(f"Error playing sound {file_path}: {e}")
    #threading.Thread(target=play_sound, daemon=True).start()

def select_commentator_voice(winner, game_number):
    p1_score = st.session_state.p1_score
    p2_score = st.session_state.p2_score
    prev_p1_score = st.session_state.prev_p1_score
    prev_p2_score = st.session_state.prev_p2_score

    if winner == 'p1':
        winning = (p1_score >= st.session_state.target_score)
    else:
        winning = (p2_score >= st.session_state.target_score)

    is_first_game = (game_number == 1)
    prev_lead = prev_p1_score - prev_p2_score
    current_lead = p1_score - p2_score
    comeback = (prev_lead > 0 and current_lead < 0) or (prev_lead < 0 and current_lead > 0)

    if winner == 'p1':
        streak = (st.session_state.p1_streak >= 2)
    else:
        streak = (st.session_state.p2_streak >= 2)

    close_game = abs(p1_score - p2_score) <= 2

    if winning:
        file_prefix = 'winning'
        num_files = 6
    elif is_first_game:
        file_prefix = 'first'
        num_files = 4
    elif comeback:
        file_prefix = 'comeback'
        num_files = 10
    elif streak:
        file_prefix = 'streak'
        num_files = 10
    elif close_game:
        file_prefix = 'close'
        num_files = 6
    else:
        file_prefix = 'congrats'
        num_files = 8

    file_number = random.randint(1, num_files)
    commentator_file = f"sounds/{file_prefix}_{file_number}.mp3"
    return commentator_file

def p1_wins():
    st.session_state.prev_p1_score = st.session_state.p1_score
    st.session_state.prev_p2_score = st.session_state.p2_score

    gnum = st.session_state.current_game
    update_score('p1', gnum)
    st.session_state.celebration = 'p1'
    st.session_state.show_minigame = False
    st.session_state.current_game += 1

    if st.session_state.last_winner == 'p1':
        st.session_state.p1_streak += 1
    else:
        st.session_state.p1_streak = 1
        st.session_state.p2_streak = 0
    st.session_state.last_winner = 'p1'
    st.session_state.last_game_number = gnum

    # Store the winner of the game
    st.session_state.game_winners[gnum] = 'p1'

    if st.session_state.p1_score >= st.session_state.target_score:
        pass
    else:
        applause_file = f"sounds/applause_{random.randint(1,5)}.mp3"
        play_audio(applause_file)
        commentator_file = select_commentator_voice('p1', gnum)
        play_audio(commentator_file)

def p2_wins():
    st.session_state.prev_p1_score = st.session_state.p1_score
    st.session_state.prev_p2_score = st.session_state.p2_score

    gnum = st.session_state.current_game
    update_score('p2', gnum)
    st.session_state.celebration = 'p2'
    st.session_state.show_minigame = False
    st.session_state.current_game += 1

    if st.session_state.last_winner == 'p2':
        st.session_state.p2_streak += 1
    else:
        st.session_state.p2_streak = 1
        st.session_state.p1_streak = 0
    st.session_state.last_winner = 'p2'
    st.session_state.last_game_number = gnum

    # Store the winner of the game
    st.session_state.game_winners[gnum] = 'p2'

    if st.session_state.p2_score >= st.session_state.target_score:
        pass
    else:
        applause_file = f"sounds/applause_{random.randint(1,5)}.mp3"
        play_audio(applause_file)
        commentator_file = select_commentator_voice('p2', gnum)
        play_audio(commentator_file)

# -------------------------------------------------
# 3) Expand Games If Needed
# -------------------------------------------------
def expand_game_slots(old_total, new_total):
    if new_total <= old_total:
        return
    needed = new_total - old_total
    used = set(st.session_state.Games.values())
    avail = [g for g in st.session_state.available_games if g not in used]

    for i in range(needed):
        idx = old_total + i + 1
        if avail:
            random_game = random.choice(avail)
            avail.remove(random_game)
        else:
            random_game = random.choice(st.session_state.available_games)
        st.session_state.Games[idx] = random_game

# -------------------------------------------------
# 4) Update Single Game Slot (Missing from prior code)
# -------------------------------------------------
def update_game_slot(i):
    new_game = st.session_state[f"game_slot_{i}"]
    st.session_state.Games[i] = new_game

# -------------------------------------------------
# 5) Dynamic Minimum for the Slider
# -------------------------------------------------
def compute_min_slider():
    """
    We want the smallest n in [5..15] such that:
      - n >= games already played
      - target_score(n) > max_score
    (so picking n won't cause immediate/retroactive win)
    If none found, we skip showing the slider.
    """
    played = len(st.session_state.games_played)
    max_score_now = max(st.session_state.p1_score, st.session_state.p2_score)

    for n in range(5, 15):
        if n < played:
            continue
        # target = (n*(n+1)//2)//2 + 1
        total_pts = n*(n+1)//2
        target = (total_pts//2)+1
        if target > max_score_now:
            return n
        
    return 14

# -------------------------------------------------
# 6) Main
# -------------------------------------------------
def main():
    initialize_session_state()

    # Check if game setup is complete
    if not st.session_state.setup_complete:
        st.warning("Please complete the game setup on the Home page.")
        st.stop()

    # Check if game is a tie: add one final game
    if len(st.session_state.games_played) == st.session_state.total_games:
        # If tied, add one final game
        if st.session_state.p1_score == st.session_state.p2_score:
            st.session_state.game_over = False
            old_total = st.session_state.total_games
            st.session_state.total_games += 1
            expand_game_slots(old_total, st.session_state.total_games)

            # Recompute target
            new_n = st.session_state.total_games
            total_pts = new_n*(new_n+1)//2
            st.session_state.target_score = (total_pts//2) + 1

            # IMPORTANT: Update the slider to match the new total
            st.session_state.ingame_num_games_slider = st.session_state.total_games

            st.session_state.current_game = st.session_state.total_games

            st.session_state.is_tie = True

    # If game is over, skip
    if (st.session_state.p1_score >= st.session_state.target_score) or (st.session_state.p2_score >= st.session_state.target_score):
        with st.sidebar:
            st.write("Game is over. Return to Home to start a new round.")

            st.markdown("""---""")  # a horizontal line as a separator (optional)

            st.markdown(
                """
                <div style="text-align: center;">
                    <!-- LinkedIn -->
                    <a href="https://www.linkedin.com/in/konradschulte/" target="_blank" style="text-decoration: none; margin-right: 24px; color: inherit;">
                        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="22px" style="margin-right:8px; filter: brightness(0.1) invert(1)"/>
                        LinkedIn
                    </a>
                    <!-- GitHub -->
                    <a href="https://github.com/konradschulte" target="_blank" style="text-decoration: none; color: inherit;">
                        <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="22px" style="margin-right:8px; filter: brightness(0.1) invert(1)"/>
                        GitHub
                    </a>
                </div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    <!-- Email link -->
                    <a href="mailto:konrad.schulte3@gmx.de" style="text-decoration: none; color: inherit;">
                        Feedback
                    </a>
                </div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    © Konrad Schulte
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        # compute dynamic min
        dynamic_min = compute_min_slider()
        # If None => skip slider (a team effectively already won or is forced to 15)
        # if dynamic_min is None:
        #     with st.sidebar:
        #         st.subheader("Live Game Customization")
        #         st.write("No valid total left. A team effectively has enough points to win.")
        if dynamic_min >= 14:
            # If dynamic_min is 15, we can't do slider in range(15..15) b/c Streamlit
            with st.sidebar:
                st.subheader("Live Game Customization")
                st.write("Total games cannot be reduced anymore.")

                # Colors
                def update_colors():
                    st.session_state.selected_theme['background'] = st.session_state.bg_picker
                    st.session_state.selected_theme['text'] = st.session_state.txt_picker

                st.color_picker(
                    "Background Color",
                    value=st.session_state.selected_theme['background'],
                    key='bg_picker',
                    on_change=update_colors
                )
                st.color_picker(
                    "Text Color",
                    value=st.session_state.selected_theme['text'],
                    key='txt_picker',
                    on_change=update_colors
                )
                st.markdown(f"""
                    <style>
                        .stApp {{
                            background-color: {st.session_state.selected_theme['background']} !important;
                        }}
                        h1, h2, h3, h4, h5, h6, p, div, label, span {{
                            color: {st.session_state.selected_theme['text']} !important;
                        }}
                    </style>
                """, unsafe_allow_html=True)

                # Team Config
                def update_p1_name_callback():
                    st.session_state.P1 = st.session_state.p1_name_input

                def update_p1_emoji_callback():
                    st.session_state.P1_avatar = st.session_state.p1_emoji_input

                def update_p2_name_callback():
                    st.session_state.P2 = st.session_state.p2_name_input

                def update_p2_emoji_callback():
                    st.session_state.P2_avatar = st.session_state.p2_emoji_input

                st.text_input(
                    "Team 1 Name",
                    value=st.session_state.P1,
                    key="p1_name_input",
                    on_change=update_p1_name_callback
                )
                st.text_input(
                    "Team 1 Avatar",
                    value=st.session_state.P1_avatar,
                    max_chars=2,
                    key="p1_emoji_input",
                    on_change=update_p1_emoji_callback
                )

                st.text_input(
                    "Team 2 Name",
                    value=st.session_state.P2,
                    key="p2_name_input",
                    on_change=update_p2_name_callback
                )
                st.text_input(
                    "Team 2 Avatar",
                    value=st.session_state.P2_avatar,
                    max_chars=2,
                    key="p2_emoji_input",
                    on_change=update_p2_emoji_callback
                )

                # Unplayed game config
                for i in range(1, st.session_state.total_games+1):
                    if i not in st.session_state.games_played:
                        if i not in st.session_state.Games:
                            st.session_state.Games[i] = f"Game {i}"
                        available_opts = [''] + st.session_state.available_games
                        current_game_value = st.session_state.Games.get(i, '')
                        idx = 0
                        if current_game_value in available_opts:
                            idx = available_opts.index(current_game_value)
                        sb_key = f"game_slot_{i}"
                        st.selectbox(
                            f"Game {i}",
                            options=available_opts,
                            index=idx,
                            key=sb_key,
                            on_change=update_game_slot,
                            args=(i,)
                        )
                
                st.markdown("""---""")  # a horizontal line as a separator (optional)

                st.markdown(
                    """
                    <div style="text-align: center;">
                        <!-- LinkedIn -->
                        <a href="https://www.linkedin.com/in/konradschulte/" target="_blank" style="text-decoration: none; margin-right: 24px; color: inherit;">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="22px" style="margin-right:8px; filter: brightness(0.1) invert(1)"/>
                            LinkedIn
                        </a>
                        <!-- GitHub -->
                        <a href="https://github.com/konradschulte" target="_blank" style="text-decoration: none; color: inherit;">
                            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="22px" style="margin-right:8px; filter: brightness(0.1) invert(1)"/>
                            GitHub
                        </a>
                    </div>
                    <div style="text-align: center; margin-top: 0.5rem;">
                        <!-- Email link -->
                        <a href="mailto:konrad.schulte3@gmx.de" style="text-decoration: none; color: inherit;">
                            Feedback
                        </a>
                    </div>
                    <div style="text-align: center; margin-top: 0.5rem;">
                        © Konrad Schulte
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:
            # Show slider from [dynamic_min..15]
            with st.sidebar:
                st.subheader("Live Game Customization")

                old_total = st.session_state.total_games
                old_slider_val = st.session_state.ingame_num_games_slider

                # If stored slider < dynamic_min => clamp it
                if old_slider_val < dynamic_min:
                    old_slider_val = dynamic_min

                # Render the slider
                new_val = st.slider(
                    "Number of Games",
                    min_value=dynamic_min,
                    max_value=15,
                    value=old_slider_val,
                    key="ingame_num_games_slider"
                )

                # If changed
                if new_val != old_total:
                    st.session_state.total_games = new_val
                    total_pts = new_val*(new_val+1)//2
                    st.session_state.target_score = (total_pts//2)+1
                    # expand if bigger
                    if new_val > old_total:
                        expand_game_slots(old_total, new_val)

                # If target_score is 0 => set
                if st.session_state.target_score == 0:
                    pts = st.session_state.total_games*(st.session_state.total_games+1)//2
                    st.session_state.target_score = (pts//2)+1

                # Colors
                def update_colors():
                    st.session_state.selected_theme['background'] = st.session_state.bg_picker
                    st.session_state.selected_theme['text'] = st.session_state.txt_picker

                st.color_picker(
                    "Background Color",
                    value=st.session_state.selected_theme['background'],
                    key='bg_picker',
                    on_change=update_colors
                )
                st.color_picker(
                    "Text Color",
                    value=st.session_state.selected_theme['text'],
                    key='txt_picker',
                    on_change=update_colors
                )
                st.markdown(f"""
                    <style>
                        .stApp {{
                            background-color: {st.session_state.selected_theme['background']} !important;
                        }}
                        h1, h2, h3, h4, h5, h6, p, div, label, span {{
                            color: {st.session_state.selected_theme['text']} !important;
                        }}
                    </style>
                """, unsafe_allow_html=True)

                # Team Config
                def update_p1_name_callback():
                    st.session_state.P1 = st.session_state.p1_name_input

                def update_p1_emoji_callback():
                    st.session_state.P1_avatar = st.session_state.p1_emoji_input

                def update_p2_name_callback():
                    st.session_state.P2 = st.session_state.p2_name_input

                def update_p2_emoji_callback():
                    st.session_state.P2_avatar = st.session_state.p2_emoji_input

                st.text_input(
                    "Team 1 Name",
                    value=st.session_state.P1,
                    key="p1_name_input",
                    on_change=update_p1_name_callback
                )
                st.text_input(
                    "Team 1 Avatar",
                    value=st.session_state.P1_avatar,
                    max_chars=2,
                    key="p1_emoji_input",
                    on_change=update_p1_emoji_callback
                )

                st.text_input(
                    "Team 2 Name",
                    value=st.session_state.P2,
                    key="p2_name_input",
                    on_change=update_p2_name_callback
                )
                st.text_input(
                    "Team 2 Avatar",
                    value=st.session_state.P2_avatar,
                    max_chars=2,
                    key="p2_emoji_input",
                    on_change=update_p2_emoji_callback
                )

                # Unplayed game config
                for i in range(1, st.session_state.total_games+1):
                    if i not in st.session_state.games_played:
                        if i not in st.session_state.Games:
                            st.session_state.Games[i] = f"Game {i}"
                        available_opts = [''] + st.session_state.available_games
                        current_game_value = st.session_state.Games.get(i, '')
                        idx = 0
                        if current_game_value in available_opts:
                            idx = available_opts.index(current_game_value)
                        sb_key = f"game_slot_{i}"
                        st.selectbox(
                            f"Game {i}",
                            options=available_opts,
                            index=idx,
                            key=sb_key,
                            on_change=update_game_slot,
                            args=(i,)
                        )
                
                st.markdown("""---""")  # a horizontal line as a separator (optional)

                st.markdown(
                    """
                    <div style="text-align: center;">
                        <!-- LinkedIn -->
                        <a href="https://www.linkedin.com/in/konradschulte/" target="_blank" style="text-decoration: none; margin-right: 24px; color: inherit;">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="22px" style="margin-right:8px; filter: brightness(0.1) invert(1)"/>
                            LinkedIn
                        </a>
                        <!-- GitHub -->
                        <a href="https://github.com/konradschulte" target="_blank" style="text-decoration: none; color: inherit;">
                            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="22px" style="margin-right:8px; filter: brightness(0.1) invert(1)"/>
                            GitHub
                        </a>
                    </div>
                    <div style="text-align: center; margin-top: 0.5rem;">
                        <!-- Email link -->
                        <a href="mailto:konrad.schulte3@gmx.de" style="text-decoration: none; color: inherit;">
                            Feedback
                        </a>
                    </div>
                    <div style="text-align: center; margin-top: 0.5rem;">
                        © Konrad Schulte
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
    # -------------------------------------------------
    # (B) Main Layout
    # -------------------------------------------------
    st.markdown(
        f"""
        <style>
            ::-webkit-scrollbar {{
                width: 0px;
                background: transparent;
            }}
            html, body {{
                overflow: hidden;
                height: 100%;
                margin: 0;
                padding: 0;
            }}
            .stApp {{
                background-color: {st.session_state.selected_theme['background']};
                overflow: hidden;
                height: 100vh;
            }}
            h1, h2, h3, h4, h5, h6, p, div, label, span {{
                color: {st.session_state.selected_theme['text']};
            }}
            .score-box {{
                background-color: black;
                color: white;
                text-align: center;
                font-size: 30px;
                padding: 10px;
            }}
            div.stButton > button {{
                background-color: rgba(0, 0, 0, 0.2) !important;
                color: {st.session_state.selected_theme['text']} !important;
                border: 2px solid black !important;
                font-size: 20px;
                width: 100%;
            }}
            .center-text {{
                text-align: center;
                font-size: 24px;
            }}
            .warning-text {{
                text-align: center;
                color: red;
                font-size: 24px;
            }}
            .stProgress > div > div > div > div {{
                background-color: {st.session_state.selected_theme['text']};
            }}
            .stProgress > div > div > div {{
                background-color: black;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.game_name}</h1>", unsafe_allow_html=True)

    # Scores
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center;">
                <div style="width: 75px; height: 75px;
                            display: flex; align-items: center;
                            justify-content: center;
                            font-size: 60px; margin-right: 15px;">
                    {st.session_state.P1_avatar}
                </div>
                <h2 style='text-align: center; margin: 0;'>{st.session_state.P1}</h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='score-box'>{st.session_state.p1_score}</div>", unsafe_allow_html=True)

        if st.session_state.target_score > 0:
            prog_p1 = min(st.session_state.p1_score/st.session_state.target_score, 1.0)
        else:
            prog_p1 = 0
        st.progress(prog_p1)

    with col2:
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center;">
                <div style="width: 75px; height: 75px;
                            display: flex; align-items: center;
                            justify-content: center;
                            font-size: 60px; margin-right: 15px;">
                    {st.session_state.P2_avatar}
                </div>
                <h2 style='text-align: center; margin: 0;'>{st.session_state.P2}</h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='score-box'>{st.session_state.p2_score}</div>", unsafe_allow_html=True)

        if st.session_state.target_score > 0:
            prog_p2 = min(st.session_state.p2_score/st.session_state.target_score, 1.0)
        else:
            prog_p2 = 0
        st.progress(prog_p2)

    # Games
    st.markdown(f"<h2 style='text-align: center;'>Games</h2>", unsafe_allow_html=True)
    total_g = st.session_state.total_games
    if total_g < 1:
        st.warning("No games defined.")
        st.stop()

    gcols = st.columns(total_g)
    for i in range(1, total_g+1):
        with gcols[i-1]:
            if i in st.session_state.games_played:
                st.button("✔️", disabled=True, key=f"game_{i}")
            else:
                if st.button(f"{i}", key=f"game_{i}"):
                    # next game in correct order
                    if i == st.session_state.current_game and not st.session_state.game_over:
                        st.session_state.show_minigame = True
                        st.session_state.current_game = i
                        st.session_state.celebration = None
                        st.session_state.warning = False
                        st.session_state.is_tie = False
                    else:
                        st.session_state.warning = True

    if st.session_state.warning:
        st.write("<div class='warning-text'>Please play the games in order!</div>", unsafe_allow_html=True)

    # Confetti
    if st.session_state.celebration:
        if st.session_state.celebration == 'p1':
            rain(emoji=st.session_state.P1_avatar, font_size=75, falling_speed=5, animation_length=1)
        else:
            rain(emoji=st.session_state.P2_avatar, font_size=75, falling_speed=5, animation_length=1)
        st.session_state.celebration = None

    # Minigame
    def get_base64_image(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    if st.session_state.show_minigame and not st.session_state.game_over:
        gnum = st.session_state.current_game
        gname = st.session_state.Games.get(gnum, f"Game {gnum}")

        # possible background
        if os.path.exists(f"pictures/{gname}.png"):
            b64 = get_base64_image(f"pictures/{gname}.png")
            st.markdown(
                f"""
                <style>
                    .stApp {{
                        background-color: {st.session_state.selected_theme['background']};
                        background-image: url("data:image/png;base64,{b64}");
                        background-size: contain;
                        background-repeat: no-repeat;
                        background-position: bottom center;
                        overflow: hidden;
                        height: 100vh;
                        background-attachment: fixed;
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )

        st.markdown(f"<h2 style='text-align: center;'>Game {gnum}: {gname}</h2>", unsafe_allow_html=True)
        st.markdown("<div class='center-text'>Who won?</div>", unsafe_allow_html=True)

        c1, _, c2 = st.columns([1,1,1])
        with c1:
            st.button(st.session_state.P1, key=f'p1_win_{gnum}', on_click=p1_wins)
        with c2:
            st.button(st.session_state.P2, key=f'p2_win_{gnum}', on_click=p2_wins)

    # Check tie
    if st.session_state.is_tie:
        # Custom CSS for styling the warning message
        #st.session_state.selected_theme = {'background': '#FFD700', 'text': '#20B2AA'}
        st.markdown(
            """
            <style>
            .center-warning {
                display: flex;
                justify-content: center;
                align-items: center;
                color: {st.session_state.selected_theme.text}; /* Bootstrap warning text color */
                background-color: {st.session_state.selected_theme.background}; /* Bootstrap warning background color */
                padding: 1rem;
                border-radius: 0.5rem;
                font-size: 1.5rem;
                font-weight: bold;
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Display the styled message
        st.markdown(
            """
            <div class="center-warning">
                It's a tie! A final game has been automatically added.
                <br>
                You can change the final game in the sidebar. Good luck!
            </div>
            """,
            unsafe_allow_html=True
        )

    # Check game over
    if not st.session_state.game_over_handled:
        if st.session_state.p1_score >= st.session_state.target_score:
            st.session_state.game_over = True
            st.session_state.winner = st.session_state.P1
            st.session_state.winner_id = 'p1'
        elif st.session_state.p2_score >= st.session_state.target_score:
            st.session_state.game_over = True
            st.session_state.winner = st.session_state.P2
            st.session_state.winner_id = 'p2'

    # End screen
    if st.session_state.game_over and not st.session_state.game_over_handled:
        if not st.session_state.balloons_shown:
            st.balloons()
            st.session_state.balloons_shown = True

        ph = st.empty()
        ph.markdown(
            f"<h1 style='text-align: center;'>Congratulations, {st.session_state.winner}!</h1>",
            unsafe_allow_html=True
        )
        applause_file = f"sounds/applause_{random.randint(1,5)}.mp3"
        play_audio(applause_file)

        cfile = select_commentator_voice(st.session_state.winner_id, st.session_state.last_game_number)
        play_audio(cfile)

        time.sleep(4)
        ph.empty()

        # Summary table
        # Build the DataFrame
        data = []
        # Initialize a dictionary to keep track of cumulative scores for each player
        cumulative_scores = {'p1': 0, 'p2': 0}

        for gnum in sorted(st.session_state.game_winners.keys()):
            winner_id = st.session_state.game_winners[gnum]
            
            # Increment the cumulative score for the winner
            cumulative_scores[winner_id] += int(gnum)

            # Combine avatar and name based on the winner
            if winner_id == 'p1':
                winner_display = f"{st.session_state.P1_avatar} {st.session_state.P1}" 
            else:
                winner_display = f"{st.session_state.P2_avatar} {st.session_state.P2}"

            game_title = st.session_state.Games.get(gnum, f"Game {gnum}")

            # Append a new entry with the accumulated score for this winner
            data.append({
                "Game Number": gnum, 
                "Game Title": game_title, 
                "Winner": winner_display,
                "Accumulated Score": cumulative_scores[winner_id]  # New column for accumulated score
            })

        df = pd.DataFrame(data)

        # Create a styled DataFrame and add CSS to hide the index
        styled_df = (
            df.style
            .set_properties(**{'text-align': 'center'})  # Center text in cells
            .set_table_styles([
                # Style table headers
                {
                    "selector": "th",
                    "props": [
                        ("background-color", st.session_state.selected_theme['background']),
                        ("color", st.session_state.selected_theme['text']),
                        ("border", "1px solid black"),
                        ("padding", "8px"),
                        ("text-align", "center")
                    ]
                },
                # Style table data cells
                {
                    "selector": "td",
                    "props": [
                        ("background-color", st.session_state.selected_theme['background']),
                        ("color", st.session_state.selected_theme['text']),
                        ("border", "1px solid black"),
                        ("padding", "8px"),
                        ("text-align", "center")
                    ]
                },
                # Center the table itself
                {
                    "selector": "",
                    "props": [
                        ("margin-left", "auto"),
                        ("margin-right", "auto")
                    ]
                },
                # Hide index header and row labels
                {
                    "selector": ".row_heading", 
                    "props": [("display", "none")]
                },
                {
                    "selector": "th.blank",  # if there's a blank top-left header cell
                    "props": [("display", "none")]
                }
            ])
        )

        # Convert the styled DataFrame to HTML without index
        table_html = styled_df.to_html(index=False)

        # Wrap the table in a div to center it horizontally
        st.markdown(
            f"<div style='display: flex; justify-content: center;'>{table_html}</div>", 
            unsafe_allow_html=True
        )


        st.session_state.game_over_handled = True
        st.success("Game over! You can restart the game from the Home page.")


# -------------------------------------------------
# 7) Run
# -------------------------------------------------
main()
