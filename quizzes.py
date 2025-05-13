import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime

# Debugging: Print the current working directory and the path to the images
print("Current working directory:", os.getcwd())
print("Path to images folder:", os.path.join(os.getcwd(), "images"))

# Function to load leaderboard from CSV
def load_leaderboard():
    if os.path.exists('leaderboard.csv'):
        return pd.read_csv('leaderboard.csv').to_dict('records')
    return []

# Function to save leaderboard to CSV
def save_leaderboard(leaderboard):
    df = pd.DataFrame(leaderboard)
    df.to_csv('leaderboard.csv', index=False)

# Custom CSS for styling and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
    /* Main background and font settings */
    .stApp {
        background: linear-gradient(135deg, #FFE5D9 0%, #FEC5BB 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Title styling */
    h1 {
        color: #2D3142 !important;
        text-align: center;
        padding: 20px;
        animation: fadeIn 1s ease-in;
    }
    
    /* Card-like containers */
    .stButton>button {
        background: #FF8B94;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background: #FF6B6B;
        transform: translateY(-2px);
    }
    
    /* Radio buttons styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        animation: slideIn 0.5s ease-out;
        border: 2px solid #FF8B94;
    }
    
    /* Radio button text color */
    .stRadio > div > div {
        color: #2D3142 !important;
    }
    
    /* Radio button label color */
    .stRadio > div > div > label {
        color: #2D3142 !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: rgba(46, 213, 115, 0.2) !important;
        border-radius: 15px;
        padding: 20px;
        animation: bounceIn 0.5s ease-out;
    }
    
    /* Leaderboard styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px;
        padding: 20px;
        animation: fadeIn 1s ease-in;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); opacity: 0.8; }
        70% { transform: scale(0.9); opacity: 0.9; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Text color adjustments */
    .stMarkdown, .stText {
        color: #2D3142 !important;
    }
    
    /* Image container styling */
    .quiz-image {
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Dark mode overrides */
    @media (prefers-color-scheme: dark) {
        .stRadio > div {
            background: rgba(45, 49, 66, 0.9);
        }
        
        .stRadio > div > div {
            color: #FFFFFF !important;
        }
        
        .stRadio > div > div > label {
            color: #FFFFFF !important;
        }
        
        .stMarkdown, .stText {
            color: #FFFFFF !important;
        }
        
        .stDataFrame {
            background: rgba(45, 49, 66, 0.9) !important;
        }
        
        .css-1d391kg {
            background: rgba(45, 49, 66, 0.9);
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for quiz navigation
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = 0
if 'user_info_submitted' not in st.session_state:
    st.session_state.user_info_submitted = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = load_leaderboard()
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# List of quiz questions with images
quizzes = [
    {
        "question": "What do we use to type on a computer?",
        "image": "images/1.png",  # Keyboard
        "options": ["Mouse", "Keyboard", "Screen", "Speaker"],
        "correct": "Keyboard",
        "explanation": "A keyboard is what we use to type letters and numbers on a computer!"
    },
    {
        "question": "What do we use to put things from the computer onto paper?",
        "image": "images/2.png",  # Printer
        "options": ["Mouse", "Keyboard", "Screen", "Printer"],
        "correct": "Keyboard",
        "explanation": "A keyboard is what we use to type letters and numbers on a computer!"
    },
    {
        "question": "Which part of the computer shows us pictures and words?",
        "image": "images/2.png",  # Monitor
        "options": ["Keyboard", "Mouse", "Monitor", "Printer"],
        "correct": "Monitor",
        "explanation": "The monitor is like a TV screen that shows us everything on the computer!"
    },
    {
        "question": "What do we call the small arrow that moves when we move our mouse?",
        "image": "images/3.png",  # Cursor
        "options": ["Pointer", "Arrow", "Cursor", "Mouse"],
        "correct": "Cursor",
        "explanation": "The cursor is the little arrow that helps us click on things!"
    },
    {
        "question": "Which button do we click to start a program?",
        "image": "images/4.png",  # Start button
        "options": ["Stop", "Start", "Pause", "End"],
        "correct": "Start",
        "explanation": "The Start button helps us begin using a program!"
    },
    {
        "question": "What do we call the small pictures on our computer screen?",
        "image": "images/5.png",  # Icons
        "options": ["Pictures", "Icons", "Photos", "Drawings"],
        "correct": "Icons",
        "explanation": "Icons are small pictures that represent programs or files!"
    },
    {
        "question": "Which part of the computer helps us hear sounds?",
        "image": "images/1.png",  # Speaker
        "options": ["Monitor", "Keyboard", "Speaker", "Mouse"],
        "correct": "Speaker",
        "explanation": "Speakers help us hear music and sounds from the computer!"
    },
    {
        "question": "What do we call the place where we save our files?",
        "image": "images/6.jpeg",  # Folder
        "options": ["Box", "Folder", "Container", "Bag"],
        "correct": "Folder",
        "explanation": "A folder is like a digital container where we keep our files!"
    }
]

def main():
    st.title("🎮 Kids' Computer Quiz")
    
    # Display the futuro.jpg image at the top
    st.image("images/futuro.jpg", use_container_width=True)
    
    if not st.session_state.user_info_submitted:
        # User Information Form
        with st.form("user_info"):
            st.write("👋 Welcome to the Computer Quiz!")
            st.write("Let's learn about computers together!")
            name = st.text_input("What's your name?")
            age = st.number_input("How old are you?", min_value=5, max_value=12)
            submit_button = st.form_submit_button("Start Quiz")
            
            if submit_button and name and age:
                st.session_state.user_info_submitted = True
                st.session_state.name = name
                st.session_state.age = age
                st.session_state.start_time = time.time()  # Start the timer
                st.rerun()
    
    else:
        # Display user info with animation
        with st.sidebar:
            st.markdown("### 👤 Your Profile")
            st.markdown(f"**Name:** {st.session_state.name}")
            st.markdown(f"**Age:** {st.session_state.age}")
            
            # Display timer
            if st.session_state.start_time:
                elapsed_time = time.time() - st.session_state.start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                st.markdown(f"### ⏱️ Time: {minutes:02d}:{seconds:02d}")
        
        # Quiz interface
        if st.session_state.current_quiz < len(quizzes):
            current_quiz = quizzes[st.session_state.current_quiz]
            
            # Create columns for navigation
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col2:
                st.markdown(f"### Question {st.session_state.current_quiz + 1} of {len(quizzes)}")
                
                # Display image if available
                if "image" in current_quiz:
                    st.image(current_quiz["image"], use_container_width=True, caption="Look at this picture!")
                
                st.markdown(f"#### {current_quiz['question']}")
                answer = st.radio("Choose your answer:", current_quiz["options"], key=f"quiz_{st.session_state.current_quiz}")
                
                # Store the answer
                st.session_state.answers[st.session_state.current_quiz] = answer
                
                # Calculate score if this is a new answer
                if answer == current_quiz["correct"] and st.session_state.current_quiz not in st.session_state.answers:
                    st.session_state.score += 1
                    st.success(f"Great job! {current_quiz['explanation']}")
            
            # Navigation buttons with custom styling
            with col1:
                if st.button("⬅️ Previous") and st.session_state.current_quiz > 0:
                    st.session_state.current_quiz -= 1
                    st.rerun()
            
            with col3:
                if st.button("Next ➡️"):
                    st.session_state.current_quiz += 1
                    st.rerun()
        
        else:
            st.success("🎉 Quiz completed!")
            # Calculate final score by comparing answers with correct answers
            final_score = 0
            for i, quiz in enumerate(quizzes):
                if i in st.session_state.answers and st.session_state.answers[i] == quiz["correct"]:
                    final_score += 1
            
            # Calculate final time
            final_time = time.time() - st.session_state.start_time
            minutes = int(final_time // 60)
            seconds = int(final_time % 60)
            
            st.markdown(f"### Your final score: {final_score} out of {len(quizzes)}")
            st.markdown(f"### ⏱️ Time taken: {minutes:02d}:{seconds:02d}")
            
            # Add encouraging message based on score
            if final_score == len(quizzes):
                st.balloons()
                st.markdown("### 🌟 Perfect Score! You're a Computer Expert! 🌟")
            elif final_score >= len(quizzes) * 0.7:
                st.markdown("### 🎯 Great job! You know a lot about computers! 🎯")
            else:
                st.markdown("### 💪 Good try! Keep learning about computers! 💪")
            
            # Add score to leaderboard
            new_entry = {
                "name": st.session_state.name,
                "age": st.session_state.age,
                "score": final_score,
                "total_questions": len(quizzes),
                "time_taken": f"{minutes:02d}:{seconds:02d}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.leaderboard.append(new_entry)
            
            # Save leaderboard to CSV
            save_leaderboard(st.session_state.leaderboard)
            
            # Sort leaderboard by score (highest first) and time (fastest first)
            def sort_key(x):
                score = x["score"]
                # Handle entries without time_taken (old entries)
                if "time_taken" not in x:
                    return (score, 0)  # Put old entries at the end
                try:
                    minutes, seconds = map(int, x["time_taken"].split(":"))
                    return (score, -(minutes * 60 + seconds))
                except:
                    return (score, 0)
            
            st.session_state.leaderboard.sort(key=sort_key, reverse=True)
            
            # Display leaderboard
            st.markdown("### 🏆 Global Leaderboard")
            leaderboard_df = pd.DataFrame(st.session_state.leaderboard)
            if not leaderboard_df.empty:
                # Format the score column to show "X/Y"
                leaderboard_df["score"] = leaderboard_df.apply(
                    lambda row: f"{row['score']}/{row['total_questions']}", axis=1
                )
                # Select and rename columns for display
                display_columns = ["name", "age", "score", "timestamp"]
                column_names = {
                    "name": "Name",
                    "age": "Age",
                    "score": "Score",
                    "timestamp": "Date"
                }
                
                # Add time_taken column if it exists
                if "time_taken" in leaderboard_df.columns:
                    display_columns.insert(3, "time_taken")
                    column_names["time_taken"] = "Time"
                
                display_df = leaderboard_df[display_columns].rename(columns=column_names)
                st.dataframe(display_df, use_container_width=True)
                
                # Add download button for leaderboard
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Leaderboard",
                    data=csv,
                    file_name="quiz_leaderboard.csv",
                    mime="text/csv"
                )
            
            if st.button("🔄 Try Again"):
                st.session_state.current_quiz = 0
                st.session_state.user_info_submitted = False
                st.session_state.score = 0
                st.session_state.answers = {}
                st.session_state.start_time = None
                st.rerun()

if __name__ == "__main__":
    main()
