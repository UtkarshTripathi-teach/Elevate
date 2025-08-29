import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import random

from data_manager import DataManager
from ml_analyzer import MLAnalyzer
from gamification import GamificationSystem
from pdf_exporter import PDFExporter
from utils import format_time, calculate_streak

# Configure page
st.set_page_config(
    page_title="⏏︎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
if 'gamification' not in st.session_state:
    st.session_state.gamification = GamificationSystem()

def main():
    st.title("⏏︎ Elevate")
    st.markdown("*Your next level in learning*")
    
    # User selection/creation
    if st.session_state.current_user is None:
        show_user_selection()
    else:
        show_main_app()

def show_user_selection():
    st.header("Welcome to Elevate!")
    
    # Authentication tabs
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        users = st.session_state.data_manager.get_all_users()
        if users:
            with st.form("login_form"):
                selected_user = st.selectbox("Choose your username:", users)
                password = st.text_input("Password:", type="password", placeholder="Enter your password")
                login_submitted = st.form_submit_button("Login")
                
                if login_submitted:
                    if password:
                        success, message = st.session_state.data_manager.authenticate_user(selected_user, password)
                        if success:
                            st.session_state.current_user = selected_user
                            st.success(f"Welcome back, {selected_user}! ")
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter your password!")
        else:
            st.info("No existing users found. Create a new account in the Sign Up tab!")
    
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("signup_form"):
            new_username = st.text_input("Username:", placeholder="Choose a username")
            new_password = st.text_input("Password:", type="password", placeholder="Create a secure password")
            confirm_password = st.text_input("Confirm Password:", type="password", placeholder="Re-enter your password")
            signup_submitted = st.form_submit_button("Create Account")
            
            if signup_submitted:
                if new_username and new_username.strip() and new_password and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 6:
                            success, message = st.session_state.data_manager.create_user(new_username.strip(), new_password)
                            if success:
                                st.session_state.current_user = new_username.strip()
                                st.success(f"Welcome, {new_username}! Your account has been created!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Password must be at least 6 characters long!")
                    else:
                        st.error("Passwords don't match!")
                else:
                    st.error("Please fill in all fields!")
        
        st.info("💡 **Password Requirements:**\n- At least 6 characters long\n- Choose something you'll remember!")

def show_main_app():
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<h1 style="font-size:48px;">⏏︎ Elevate</h1>', unsafe_allow_html=True)
        st.markdown(f'<h1 style="font-size:24px;">Welcome, {st.session_state.current_user}!',unsafe_allow_html=True)
        st.markdown(f'*your* *next* *level* *in* **learning!**')
        
        # Display user stats
        user_data = st.session_state.data_manager.get_user_data(st.session_state.current_user)
        if not user_data.empty:
            total_xp = st.session_state.gamification.calculate_total_xp(user_data)
            current_streak = calculate_streak(user_data)
            level = st.session_state.gamification.get_level(total_xp)
            
            st.metric("🏆 Level", level)
            st.metric("⭐ Total XP", total_xp)
            st.metric("🔥 Current Streak", f"{current_streak} days")
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "Navigate to:",
            ["Dashboard", "Log Study Session", "Weakness Analysis", 
             "Practice Quiz", "Progress Reports", "Settings","Placement Prediction"]
        )


        st.markdown("---")
        
        if st.button("Logout"):
            st.session_state.current_user = None
            st.rerun()
    
    # Main content
    if page == "Dashboard":
        show_dashboard()
    elif page == "Log Study Session":
        show_study_logging()
    elif page == "Weakness Analysis":
        show_weakness_analysis()
    elif page == "Practice Quiz":
        show_quiz_section()
    elif page == "Progress Reports":
        show_progress_reports()
    elif page == "Settings":
        show_settings()
    elif page == "Placement Prediction":
        show_placement_prediction()
        
def show_quiz_section():
    st.header("Launching soon 🚀 ")
    st.image("https://i.pinimg.com/originals/17/44/1e/17441ef826077986a1ee601f45e6bdfa.gif", width=225)
    st.markdown("*We are working on Quiz feature*")


def show_dashboard():
    st.header("Study Dashboard")
    
    user_data = st.session_state.data_manager.get_user_data(st.session_state.current_user)
    
    if user_data.empty:
        st.info("Start your learning journey by logging your first study session!")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_time = user_data['duration_minutes'].sum()
    total_sessions = len(user_data)
    avg_confidence = user_data['confidence_rating'].mean()
    current_streak = calculate_streak(user_data)
    
    with col1:
        st.metric("Total Study Time", format_time(total_time))
    with col2:
        st.metric("Total Sessions", total_sessions)
    with col3:
        st.metric("Avg Confidence", f"{avg_confidence:.1f}/5")
    with col4:
        st.metric("Current Streak", f"{current_streak} days")
    
    # Recent activity and charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Study Time Trend")
        daily_data = user_data.groupby('date')['duration_minutes'].sum().reset_index()
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        
        fig = px.line(daily_data, x='date', y='duration_minutes',
                     title="Daily Study Time",
                     labels={'duration_minutes': 'Minutes', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Subject Distribution")
        subject_time = user_data.groupby('subject')['duration_minutes'].sum()
        
        fig = px.pie(values=subject_time.values, names=subject_time.index,
                    title="Time Spent by Subject")
        st.plotly_chart(fig, use_container_width=True)
    
    # recent sessions
    st.subheader("Recent Study Sessions")
    recent_sessions = user_data.tail(5)[['date', 'subject', 'chapter', 'duration_minutes', 'confidence_rating']]
    st.dataframe(recent_sessions, use_container_width=True)

def show_study_logging():
    st.header("Log Study Session")
    
    with st.form("study_session_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("Subject:", placeholder="e.g., Python, Cloud Computing")
            chapter = st.text_input("Chapter/Topic:", placeholder="e.g., Loop's, File Handling")
            duration = st.number_input("Duration (minutes):", min_value=1, max_value=1440, value=30)
        
        with col2:
            confidence = st.select_slider(
                "Confidence Rating:",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: f"{x} {'⭐' * x}"
            )
            study_date = st.date_input("Study Date:", value=datetime.now().date())
            notes = st.text_area("Notes (optional):", placeholder="Key learnings, difficulties faced...")
        
        submitted = st.form_submit_button("Log Session")
        
        if submitted:
            if subject and chapter:
                success = st.session_state.data_manager.log_study_session(
                    st.session_state.current_user,
                    subject, chapter, duration, confidence, study_date, notes
                )
                
                if success:
                    # calculate XP gained
                    xp_gained = st.session_state.gamification.calculate_session_xp(duration, confidence)
                    
                    st.success(f"Session logged successfully! You gained {xp_gained} XP!")
                    
                    # check for level up
                    user_data = st.session_state.data_manager.get_user_data(st.session_state.current_user)
                    total_xp = st.session_state.gamification.calculate_total_xp(user_data)
                    new_level = st.session_state.gamification.get_level(total_xp)
                    old_level = st.session_state.gamification.get_level(total_xp - xp_gained)
                    
                    if new_level > old_level:
                        st.balloons()
                        st.success(f"LEVEL UP! You've reached Level {new_level}!")
                    
                    # Show streak info
                    streak = calculate_streak(user_data)
                    if streak > 1:
                        st.info(f"Amazing! You're on a {streak}-day study streak!")
                else:
                    st.error("Failed to log session. Please try again.")
            else:
                st.error("Please fill in both Subject and Chapter fields.")

def show_weakness_analysis():
    st.header("AI-Powered Weakness Analysis")
    st.markdown("---")
    
    user_data = st.session_state.data_manager.get_user_data(st.session_state.current_user)
    
    if len(user_data) < 5:
        st.warning("Need at least 5 study sessions for accurate analysis. Keep logging your sessions!")
        return
    
    analyzer = MLAnalyzer()
    
    try:
        # Perform analysis
        weak_topics, recommendations = analyzer.analyze_weaknesses(user_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Areas Needing Attention")
            st.markdown("---")
            st.image("https://i.pinimg.com/originals/42/36/d0/4236d00b6df31c5c1dab3566fa61ff3c.gif", width=225)
            st.markdown("*We are working on this feature*")

        
        with col2:
            st.subheader("Personalized Recommendations")
            st.markdown("---")
            for rec in recommendations:
                st.info(rec)
        
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")

def show_progress_reports():
    st.header("Progress Reports")
    
    user_data = st.session_state.data_manager.get_user_data(st.session_state.current_user)
    
    if user_data.empty:
        st.info("No data available for reports. Start logging your study sessions!")
        return
    
    # time period selector
    period = st.selectbox("Select Time Period:", 
                         ["Last 7 days", "Last 30 days", "Last 90 days", "All time"])
    
    # Filter data based on period
    end_date = datetime.now().date()
    if period == "Last 7 days":
        start_date = end_date - timedelta(days=7)
    elif period == "Last 30 days":
        start_date = end_date - timedelta(days=30)
    elif period == "Last 90 days":
        start_date = end_date - timedelta(days=90)
    else:
        start_date = user_data['date'].min()
    
    filtered_data = user_data[
        (pd.to_datetime(user_data['date']).dt.date >= start_date) &
        (pd.to_datetime(user_data['date']).dt.date <= end_date)
    ]
    
    if filtered_data.empty:
        st.warning("No data available for the selected period.")
        return
    
    # generate comprehensive report
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Study Statistics")
        total_time = filtered_data['duration_minutes'].sum()
        avg_session = filtered_data['duration_minutes'].mean()
        total_sessions = len(filtered_data)
        unique_subjects = filtered_data['subject'].nunique()
        
        st.metric("Total Study Time", format_time(total_time))
        st.metric("Total Sessions", total_sessions)
        st.metric("Average Session", f"{avg_session:.1f} min")
        st.metric("Subjects Studied", unique_subjects)
    
    with col2:
        st.subheader("Performance Metrics")
        avg_confidence = filtered_data['confidence_rating'].mean()
        confidence_trend = "📈" if filtered_data['confidence_rating'].tail(5).mean() > filtered_data['confidence_rating'].head(5).mean() else "📉"
        
        st.metric("Average Confidence", f"{avg_confidence:.1f}/5")
        st.metric("Confidence Trend", confidence_trend)
    
    # Detailed charts
    st.subheader("Detailed Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Time Analysis", "Confidence Tracking", "Subject Performance"])
    
    with tab1:
        # Daily study time
        daily_data = filtered_data.groupby('date')['duration_minutes'].sum().reset_index()
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        
        fig = px.bar(daily_data, x='date', y='duration_minutes',
                    title="Daily Study Time Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Confidence over time
        confidence_data = filtered_data.copy()
        confidence_data['date'] = pd.to_datetime(confidence_data['date'])
        
        fig = px.scatter(confidence_data, x='date', y='confidence_rating',
                        color='subject', title="Confidence Rating Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Subject performance
        subject_stats = filtered_data.groupby('subject').agg({
            'duration_minutes': 'sum',
            'confidence_rating': 'mean'
        }).reset_index()
        
        fig = px.bar(subject_stats, x='subject', y='duration_minutes',
                    title="Total Study Time by Subject")
        st.plotly_chart(fig, use_container_width=True)
    
    # Export option
    st.subheader("Export Report")
    if st.button("Download PDF Report"):
        try:
            pdf_exporter = PDFExporter()
            pdf_buffer = pdf_exporter.generate_report(
                st.session_state.current_user, filtered_data, period
            )
            
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name=f"study_report_{st.session_state.current_user}_{period.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Failed to generate PDF: {str(e)}")

def show_settings():
    st.header("Settings")
    
    tab1, tab2, tab3 = st.tabs(["Profile", "Data Management", "Preferences"])
    
    with tab1:
        st.subheader("Profile Information")
        user_data = st.session_state.data_manager.get_user_data(st.session_state.current_user)
        
        if not user_data.empty:
            first_session = user_data['date'].min()
            total_sessions = len(user_data)
            total_time = user_data['duration_minutes'].sum()
            
            st.info(f"**Member since:** {first_session}")
            st.info(f"**Total sessions:** {total_sessions}")
            st.info(f"**Total study time:** {format_time(total_time)}")
    
    with tab2:
        st.subheader("Data Management")
        
        # Export all data
        if st.button("Export All Data (CSV)"):
            user_data = st.session_state.data_manager.get_user_data(st.session_state.current_user)
            csv = user_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"study_data_{st.session_state.current_user}.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        
        # Danger zone
        st.subheader("Danger Zone")
        if st.button("Delete All Data", type="secondary"):
            if st.button("Confirm Delete", type="secondary"):
                if st.session_state.data_manager.delete_user_data(st.session_state.current_user):
                    st.success("All data deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete data!")
    
    with tab3:
        st.subheader("Gamification Preferences")
        st.info("Gamification features are always enabled to keep you motivated! ")
        
        st.subheader("Display Preferences")
        st.info("Using default Streamlit theme for optimal performance.")

def show_placement_prediction():
    import pickle
    import numpy as np

    st.header("Placement Prediction")
    st.markdown("- *based* *on* *Kaggle* *Dataset*")
    image = "kagglelogo.png"
    st.image(image, width=120)
    # st.markdown("![Foo](kagglelogo.png)(https://www.kaggle.com/datasets/ruchikakumbhar/placement-prediction-dataset/data)")

    with st.expander("About Placement Predict", expanded=True):
        st.markdown("""
        ### About Placement Predict  
        The **Placement Predict** feature helps you estimate your chances of getting placed based on your academic profile, skills, and training details.  

        ### Features Explained  
        - **CGPA** → Your overall academic performance in college (higher CGPA improves chances).  
        - **Internships** → Number of internships you have completed (practical exposure matters).  
        - **Projects** → Academic or personal projects showcasing your technical/problem-solving skills.  
        - **Workshops/Certifications** → Extra courses, certifications, or workshops attended (skill-building).  
        - **Aptitude Test Score** → Performance in logical, quantitative, or verbal aptitude tests.  
        - **Soft Skills Rating** → Communication, teamwork, and leadership qualities.  
        - **Extracurricular Activities** → Participation in sports, clubs, or cultural events (shows overall personality).  
        - **Placement Training** → Whether you attended college/company placement training programs.  
        - **SSC Marks** → 10th grade academic score (foundation knowledge).  
        - **HSC Marks** → 12th grade academic score (pre-college preparation).  

        ### How it works  
        - Enter your details for the above fields.  
        - The system uses a **machine learning model** trained on real placement data to analyze your profile.  
        - With one click on **“Predict Placement”**, it gives you:  
          - **Likely to be Placed**  
          - **Unlikely to be Placed**  

        **Note**: This is a predictive tool, not a guarantee. Results depend on data trends and should be used as guidance only.  
        """)


    # Load model + scaler
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("placement_prediction_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Input fields (same 10 features, exclude StudentID)
    cgpa = st.number_input("CGPA", 0.0, 10.0, 7.0, step=0.1)
    internships = st.number_input("Internships (count)", 0, 10, 0, step=1)
    projects = st.number_input("Projects (count)", 0, 10, 0, step=1)
    workshops = st.number_input("Workshops/Certifications (count)", 0, 20, 0, step=1)
    aptitude = st.number_input("Aptitude Test Score", 0, 100, 50, step=1)
    softskills = st.slider("Soft Skills Rating (1-10)", 1, 10, 5)
    extra = st.slider("Extracurricular Activities (1-10)", 1, 10, 5)
    training = st.selectbox("Placement Training", ["Yes", "No"])
    ssc_marks = st.number_input("SSC Marks:10th grade (%)", 0.0, 100.0, 60.0, step=0.1)
    hsc_marks = st.number_input("HSC Marks:12th grade (%)", 0.0, 100.0, 60.0, step=0.1)

    training_map = {"Yes": 1, "No": 0}

    features = np.array([
        cgpa, internships, projects, workshops,
        aptitude, softskills, extra, training_map[training],
        ssc_marks, hsc_marks
    ]).reshape(1, -1)

    features_scaled = scaler.transform(features)

    if st.button("Predict Placement"):
        prediction = model.predict(features_scaled)[0]
        import time
        random.seed(132)
        progress_bar = st.progress(0)
        placeholder = st.empty()
        placeholder.subheader('Predicting  Placement') 
        
        place = st.empty()
        place.image('https://cdn.dribbble.com/userupload/23163669/file/original-33613fcd16243932816ae19cd4d8501d.gif',width = 330)
        
        for i in range(100):
            time.sleep(0.05)
            progress_bar.progress(i + 1)
        
        if prediction == 1:
            body = f'Candidate is likely to be Placed.'
            placeholder.empty()
            place.empty()
            st.success(body)
            progress_bar = st.progress(0)
        else:
            body = 'Candidate is unlikely to be Placed.'
            placeholder.empty()
            place.empty()
            st.warning(body)
            progress_bar = st.progress(0)

if __name__ == "__main__":
    main()
