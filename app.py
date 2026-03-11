import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import random

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = "👨‍🏫 Teacher Portal"
if 'sensory_mode' not in st.session_state:
    st.session_state.sensory_mode = "Standard"
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

# --- STUDENT DATA STATE (For Simulation) ---
subjects = ["Mathematics", "English", "Physics", "Chemistry", "Biology", "History"]
if 'student_data' not in st.session_state:
    core_team = ["Neema Ongaga", "Grace Naliaka", "Rayvins Otieno", "Hillary Lweya", "Tatiana A."]
    extended_class = [
        "Omondi Kevin", "Wanjiku Mary", "Kipchoge Eliud", "Mutua Brian", "Akinyi Sarah", 
        "Odhiambo John", "Njoroge Peter", "Kamau Jane", "Waithera Lucy", "Ochieng David", 
        "Anyango Faith", "Mwangi Paul", "Kariuki Simon", "Wamalwa Chris", "Nekesa Joy", 
        "Ouma Daniel", "Atieno Rose", "Kiprono Felix", "Chebet Mercy", "Onyango Tom"
    ]
    all_25_students = core_team + extended_class
    
    # Initialize data with random scores and a hidden "Compliance" level
    initial_data = []
    for student in all_25_students:
        scores = {subj: random.randint(50, 85) for subj in subjects}
        compliance = random.choice(["High", "Moderate", "Poor"])
        
        # Give the core team High compliance so they look good for the pitch!
        if student in core_team: compliance = "High"
            
        student_record = {"Student Name": student, "Compliance": compliance, "Path_Restructured": False}
        student_record.update(scores)
        initial_data.append(student_record)
        
    st.session_state.student_data = initial_data

# --- CONFIG & STYLING ---
st.set_page_config(page_title="EduAI Dashboard", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# Custom CSS: Crisp, Professional Light Theme
st.markdown("""
    <style>
    .main {background-color: #f4f7f9;}
    h1, h2, h3 {color: #1e293b;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    div[data-testid="stSidebar"] {background-color: #ffffff; border-right: 1px solid #e2e8f0;}
    div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] label {color: #334155 !important;}
    div[data-testid="stSidebar"] .stRadio label {color: #334155 !important;}
    hr {border-color: #e2e8f0;}
</style>
""", unsafe_allow_html=True)

# --- DYNAMIC ACCESSIBILITY CSS ---
if st.session_state.get('logged_in'):
    if st.session_state.sensory_mode == "Lexical Clarity (Dyslexia-Friendly)":
        st.markdown("""
            <style>
            .main {background-color: #FDFBF7 !important;}
            h1, h2, h3, p, span, div, label, li {
                font-family: 'Verdana', sans-serif !important;
                letter-spacing: 1px !important;
                line-height: 1.8 !important;
                font-size: 1.1rem !important;
                color: #1e293b !important;
            }
            </style>
        """, unsafe_allow_html=True)
    elif st.session_state.sensory_mode == "Neuro-Focus (ADHD-Friendly)":
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {display: none !important;}
            .main {background-color: #ffffff !important;}
            .stMetric {box-shadow: none !important; border: 2px solid #000 !important;}
            h1, h2, h3, p {color: #000000 !important;}
            </style>
        """, unsafe_allow_html=True)

# ==========================================
# LOGIN SCREEN (GATEWAY)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #1e293b;'>🎓 EduAI Platform</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>GLUK Women in Tech Datathon 2026</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.container(border=True)
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="e.g., rayvins_o")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            role_select = st.selectbox("Select Account Type", ["👨‍🏫 Teacher Portal", "👨‍👩‍👧 Parent Portal", "🎓 Student Portal"])
            
            st.markdown("---")
            
            # Accessibility Checkbox Logic
            needs_accommodation = st.checkbox("I require accessibility accommodations (Special Needs UI)")
            
            if needs_accommodation:
                st.caption("Accessibility Settings")
                sensory_mode = st.selectbox(
                    "Select your preferred sensory profile:", 
                    ["Lexical Clarity (Dyslexia-Friendly)", "Neuro-Focus (ADHD-Friendly)"],
                    help="Customizes the UI to match your learning needs."
                )
            else:
                sensory_mode = "Standard"
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Secure Login", use_container_width=True)
            
            if submitted:
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role_select
                    st.session_state.sensory_mode = sensory_mode
                    st.rerun()
                else:
                    st.error("Please enter both username and password to continue.")
    st.stop() # Halts execution here until successfully logged in

# --- SIDEBAR NAV ---
st.sidebar.title("🎓 EduAI Core")
st.sidebar.caption("GLUK Datathon 2026 - Kisumu")
st.sidebar.markdown(f"**User:** {st.session_state.username}")
st.sidebar.markdown(f"**UI Profile:** {st.session_state.sensory_mode}")
st.sidebar.markdown("---")

role_options = ["👨‍🏫 Teacher Portal", "👨‍👩‍👧 Parent Portal", "🎓 Student Portal"]
# Ensure the session state role exists in options to prevent ValueError
default_idx = role_options.index(st.session_state.role) if st.session_state.role in role_options else 0
role = st.sidebar.radio("Select Dashboard View:", role_options, index=default_idx)

st.sidebar.markdown("---")
st.sidebar.success("System Status: **Online**\n\nPredictive Engine: **Active**")

# --- SIMULATION ENGINE (TEACHER SIDEBAR) ---
if role == "👨‍🏫 Teacher Portal":
    st.sidebar.markdown("---")
    st.sidebar.warning("⚙️ **Simulation Engine**")
    st.sidebar.caption("Simulate 1 week of AI-guided learning. Students who comply with the AI will see score increases.")
    if st.sidebar.button("▶️ Run Weekly Simulation", use_container_width=True):
        with st.spinner("Simulating week... Applying AI strategies..."):
            time.sleep(1.5)
            # Update scores based on compliance
            for student in st.session_state.student_data:
                if student["Compliance"] == "High":
                    for sub in subjects:
                        student[sub] = min(100, student[sub] + random.randint(2, 6))
                    student["Path_Restructured"] = False
                elif student["Compliance"] == "Moderate":
                    for sub in subjects:
                        student[sub] = min(100, student[sub] + random.randint(-2, 3))
                    student["Path_Restructured"] = False
                else: # Poor Compliance
                    for sub in subjects:
                        student[sub] = max(0, student[sub] - random.randint(3, 8))
                    student["Path_Restructured"] = True # Trigger the restructuring alert
        st.sidebar.success("Simulation Complete! Data updated.")

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

# ==========================================
# TEACHER PORTAL
# ==========================================
if role == "👨‍🏫 Teacher Portal":
    st.title("Educator Dashboard")
    st.markdown("Welcome back, **Mr. Omondi**. Here is the live, predictive academic data for your classes at GLUK High.")
    
    # Process the session state data into a DataFrame
    df_data = []
    for s in st.session_state.student_data:
        total_score = sum(s[sub] for sub in subjects)
        row = [s["Student Name"], s["Compliance"]] + [s[sub] for sub in subjects] + [total_score]
        df_data.append(row)
        
    full_class_df = pd.DataFrame(df_data, columns=["Student Name", "AI Compliance"] + subjects + ["Total Score"])
    full_class_df = full_class_df.sort_values(by="Total Score", ascending=False)
    
    # KPI Metrics
    at_risk_count = len(full_class_df[full_class_df["Total Score"] < 350])
    high_compliance_count = len(full_class_df[full_class_df["AI Compliance"] == "High"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Enrolled Students", value=len(st.session_state.student_data), delta="Full Roster Active")
    col2.metric(label="At-Risk Learners (Total < 350)", value=at_risk_count, delta_color="inverse")
    col3.metric(label="High AI Compliance Rate", value=f"{int((high_compliance_count/len(st.session_state.student_data))*100)}%")
    
    st.markdown("---")
    
    # Row 2: Gradebook and Diagnostician
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📊 Class Performance Gradebook")
        st.markdown("Watch scores fluctuate based on the student's compliance with their AI-generated study path.")
        
        # Style the dataframe for a professional look
        def color_scores(val):
            if isinstance(val, int):
                if val < 50: return 'color: #dc2626; font-weight: 500' # Red for failing
                elif val >= 80 and val <= 100: return 'color: #059669; font-weight: 500' # Green for distinction
                elif val > 300: return 'background-color: #f1f5f9; font-weight: bold; color: #1e293b' # Formatting for Total Score
            elif val == "High": return 'color: #059669; font-weight: bold'
            elif val == "Poor": return 'color: #dc2626; font-weight: bold'
            return ''
            
        st.dataframe(
            full_class_df.style.map(color_scores),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with col_right:
        st.subheader("🤖 Auto-Diagnostician")
        st.markdown("Paste observation notes below to auto-map to the CBC portfolio.")
        
        obs_text = st.text_area("Teacher Observation:", 
                                value="Student successfully built a basic circuit using a battery and bulb. They troubleshooted a loose connection independently.",
                                height=150)
        
        if st.button("Map Competency", type="primary"):
            with st.spinner("Analyzing text & mapping to CBC framework..."):
                time.sleep(1.5)
                st.success("Mapped Successfully! ✅")
                st.info(f"**Category:** Practical Application & Problem Solving\n\n**Subject:** Physics\n\n**Confidence Score:** {random.randint(88, 99)}%")

# ==========================================
# PARENT PORTAL
# ==========================================
elif role == "👨‍👩‍👧 Parent Portal":
    st.title("Parent Portal: Academic Tracker")
    st.markdown("Welcome! Review your child's adaptive learning strategy.")
    
    selected_student = st.selectbox("Select Student:", ["Grace Naliaka", "Neema Ongaga", "Rayvins Otieno", "Hillary Lweya"])
    
    # Find student data
    student_record = next((s for s in st.session_state.student_data if s["Student Name"] == selected_student), None)
    
    if student_record:
        st.markdown(f"### 📊 {selected_student}'s Current Standings")
        
        if student_record["Path_Restructured"]:
            st.error("⚠️ **Alert:** EduAI has detected a recent drop in performance. The study path has been completely restructured to focus on foundational concepts.")
        elif student_record["Compliance"] == "High":
            st.success("✅ **Excellent:** Grace is highly compliant with her AI study path and is seeing steady growth.")
            
        # Display current grades in a clean format
        cols = st.columns(6)
        for i, sub in enumerate(subjects):
            val = student_record[sub]
            delta = "On Track" if val >= 60 else "Needs Review"
            color = "normal" if val >= 60 else "inverse"
            cols[i].metric(label=sub, value=f"{val}%", delta=delta, delta_color=color)

    st.markdown("---")
    st.subheader("🗺️ Active Study Strategy")
    st.markdown(f"Here is how the EduAI system is adapting {selected_student.split()[0]}'s curriculum to reach their target goal.")
    
    st.markdown("""
    | Day | Intervention Type | Status | Educator/AI Notes |
    | :--- | :--- | :--- | :--- |
    | **Monday** | Algebra Baseline Assessment | 🟢 Completed | *Identified fractions as a core knowledge gap.* |
    | **Wednesday** | Dynamic Re-route: Visual Fractions | 🟢 Completed | *Adapted text materials into visual models to match learning profile.* |
    | **Today** | Practice Assessment | 🟡 Pending | *Estimated time: 15 mins. Focus on lowest common denominators.* |
    | **Saturday** | Orbit AI: Review Session | ⚪ Upcoming | *Weekend consolidation of the week's challenging concepts.* |
    """)

    st.button(f"Send Encouragement Nudge to {selected_student.split()[0]}'s Device", use_container_width=True)

# ==========================================
# STUDENT PORTAL
# ==========================================
elif role == "🎓 Student Portal":

    # Grab the logged-in user's data (default to Neema if they typed something random)
    current_student = next((s for s in st.session_state.student_data if s["Student Name"].lower().startswith(st.session_state.username.lower())), st.session_state.student_data[0])

    # --- QUIZ LOGIC HELPER FUNCTIONS ---
    def render_mini_quiz():
        st.markdown("### 📝 Algebra Practice Quiz: Lowest Common Denominators")
        st.info("Answer the questions below. Orbit AI will adjust your strategy based on the results.")
        
        with st.form("mini_quiz_form"):
            q1 = st.radio("1. What is the lowest common denominator for the fractions 1/4 and 1/6?", ["8", "10", "12", "24"])
            q2 = st.radio("2. If you want to add 1/3 and 1/4, what denominator must you use?", ["7", "12", "34", "1"])
            
            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                score = 0
                if q1 == "12": score += 50
                if q2 == "12": score += 50
                st.session_state.quiz_score = score
                st.session_state.quiz_submitted = True
                st.rerun()

    def render_quiz_results():
        if st.session_state.quiz_score == 100:
            st.success(f"🎉 Perfect Score! You got {st.session_state.quiz_score}%.")
            st.balloons()
        else:
            st.warning(f"👍 Good effort! You scored {st.session_state.quiz_score}%. We'll queue up some review materials.")
            
        st.markdown("Orbit AI has logged your progress and successfully updated your forecasted trajectory.")
        
        if st.button("Return to Dashboard"):
            st.session_state.quiz_active = False
            st.session_state.quiz_submitted = False
            st.rerun()

    # --- PORTAL UI ---
    if st.session_state.sensory_mode == "Neuro-Focus (ADHD-Friendly)":
        st.warning("🎯 **Neuro-Focus Mode Active:** Extraneous dashboard elements are hidden to support deep work.")
        st.title(f"Ready to learn, {st.session_state.username}?")
        
        if current_student["Path_Restructured"] and not st.session_state.quiz_active:
            st.error("⚠️ **ROUTE RECALCULATED:** We noticed a drop in your recent performance. Orbit AI has restructured your path. Let's focus on the basics today.")
            
        if st.session_state.quiz_submitted:
            render_quiz_results()
        elif st.session_state.quiz_active:
            render_mini_quiz()
        else:
            st.markdown("### Your Current Assignment:")
            st.info("⏱️ **15-Minute Algebra Practice Quiz**\n\nObjective: Master lowest common denominators.")
            if st.button("Start Assignment", type="primary", use_container_width=True):
                st.session_state.quiz_active = True
                st.rerun()
                
        st.markdown("---")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.quiz_active = False
            st.rerun()
        
    else:
        st.title(f"Student Portal: {st.session_state.username}'s Journey")
        st.markdown("Welcome to your EduAI Command Center. Let's hit those academic goals! 🚀")
        
        # Display the dynamic restructuring alert
        if current_student["Path_Restructured"] and not st.session_state.quiz_active:
             st.warning("⚠️ **ROUTE RECALCULATED:** Orbit AI detected a drop in performance metrics. Your study path has been dynamically restructured to reinforce foundational concepts.")
             
        if st.session_state.quiz_submitted:
            render_quiz_results()
        elif st.session_state.quiz_active:
            render_mini_quiz()
        else:
            
            # Show current grades overview
            st.markdown("#### Your Current Standing:")
            cols = st.columns(6)
            for i, sub in enumerate(subjects):
                cols[i].metric(label=sub, value=f"{current_student[sub]}%")
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.info("### Next Required Module\n**Algebra Practice Quiz**\n\nEstimated time: 15 mins")
                if st.button("Start Module", type="primary"):
                    st.session_state.quiz_active = True
                    st.rerun()
            with col2:
                if current_student["Compliance"] == "High":
                    msg = "Your overall trajectory is trending upward! Keep up the high compliance with your study path!"
                else:
                    msg = "Let's increase our study compliance this week to get those numbers back up!"
                st.success(f"### Orbit AI Tutor\n*\"{msg}\"*")

st.markdown("---")
st.caption("EduAI © 2026 | Developed for the GLUK Women in Tech Datathon")
