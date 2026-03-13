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
    
    initial_data = []
    for student in all_25_students:
        # Generate baseline scores (acting as historical support levels)
        baselines = {f"{sub}_base": random.randint(45, 80) for sub in subjects}
        scores = {sub: baselines[f"{sub}_base"] for sub in subjects} # Current starts at baseline
        
        compliance = random.choice(["High", "Moderate", "Poor"])
        if student in core_team: compliance = "High" # Core team always bullish
            
        student_record = {"Student Name": student, "Compliance": compliance, "Path_Restructured": False}
        student_record.update(baselines)
        student_record.update(scores)
        initial_data.append(student_record)
        
    st.session_state.student_data = initial_data

# --- CONFIG & STYLING ---
st.set_page_config(page_title="EduAI Dashboard", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #f4f7f9;}
    h1, h2, h3 {color: #1e293b;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    div[data-testid="stSidebar"] {background-color: #f8fafc; border-right: 1px solid #e2e8f0;}
    div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] label {color: #334155 !important;}
    div[data-testid="stSidebar"] .stRadio label {color: #334155 !important; font-weight: 500;}
    hr {border-color: #e2e8f0;}
    </style>
""", unsafe_allow_html=True)

# --- DYNAMIC ACCESSIBILITY CSS ---
if st.session_state.get('logged_in'):
    if st.session_state.sensory_mode == "Lexical Clarity (Dyslexia-Friendly)":
        st.markdown("""<style>.main {background-color: #FDFBF7 !important;} h1, h2, h3, p, span, div, label, li {font-family: 'Verdana', sans-serif !important; letter-spacing: 1px !important; line-height: 1.8 !important; font-size: 1.1rem !important; color: #1e293b !important;}</style>""", unsafe_allow_html=True)
    elif st.session_state.sensory_mode == "Neuro-Focus (ADHD-Friendly)":
        st.markdown("""<style>[data-testid="stSidebar"] {display: none !important;} .main {background-color: #ffffff !important;} .stMetric {box-shadow: none !important; border: 2px solid #000 !important;} h1, h2, h3, p {color: #000000 !important;}</style>""", unsafe_allow_html=True)

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
            username = st.text_input("Username", placeholder="e.g., Julius")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            role_select = st.selectbox("Select Account Type", ["👨‍🏫 Teacher Portal", "👨‍👩‍👧 Parent Portal", "🎓 Student Portal"])
            
            st.markdown("---")
            
            needs_accommodation = st.checkbox("I require accessibility accommodations (Special Needs UI)")
            
            if needs_accommodation:
                sensory_mode = st.selectbox(
                    "Select your specific cognitive/sensory profile:", 
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
    st.stop()

# --- SIDEBAR NAV ---
st.sidebar.markdown("### 🎓 EduAI Core")
st.sidebar.caption("GLUK Datathon 2026 - Kisumu")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown(f"**User:** {st.session_state.username}")
st.sidebar.markdown(f"**UI Profile:** {st.session_state.sensory_mode}")
st.sidebar.markdown("---")

role_options = ["👨‍🏫 Teacher Portal", "👨‍👩‍👧 Parent Portal", "🎓 Student Portal"]
default_idx = role_options.index(st.session_state.role) if st.session_state.role in role_options else 0
role = st.sidebar.radio("", role_options, index=default_idx)

st.sidebar.markdown("---")
st.sidebar.success("System Status: **Online**\n\nPredictive Engine: **Active**")

# --- SIMULATION ENGINE (TEACHER SIDEBAR) ---
if role == "👨‍🏫 Teacher Portal":
    st.sidebar.markdown("---")
    st.sidebar.warning("⚙️ **Simulation Engine**")
    st.sidebar.caption("Simulate 1 week of AI-guided learning.")
    if st.sidebar.button("▶️ Run Weekly Simulation", use_container_width=True):
        with st.spinner("Simulating week... Applying AI strategies..."):
            time.sleep(1)
            for student in st.session_state.student_data:
                if student["Compliance"] == "High":
                    for sub in subjects: student[sub] = min(100, student[sub] + random.randint(2, 6))
                    student["Path_Restructured"] = False
                elif student["Compliance"] == "Moderate":
                    for sub in subjects: student[sub] = min(100, student[sub] + random.randint(-2, 3))
                    student["Path_Restructured"] = False
                else:
                    for sub in subjects: student[sub] = max(0, student[sub] - random.randint(3, 8))
                    student["Path_Restructured"] = True
        st.sidebar.success("Simulation Complete! Gradebook updated.")

# --- SIMULATION ENGINE (STUDENT SIDEBAR - DEVELOPER MODE) ---
if role == "🎓 Student Portal":
    current_student = next((s for s in st.session_state.student_data if s["Student Name"].lower().startswith(st.session_state.username.lower())), st.session_state.student_data[0])
    
    st.sidebar.markdown("---")
    st.sidebar.warning("🛠️ **Developer Tools (Simulation)**")
    st.sidebar.caption("Test how the AI adapts to user compliance.")
    
    if st.sidebar.button("🟢 Complied (Followed AI Path)", use_container_width=True):
        for sub in subjects: current_student[sub] = min(100, current_student[sub] + random.randint(5, 12))
        current_student["Compliance"] = "High"
        current_student["Path_Restructured"] = False
        st.rerun()
        
    if st.sidebar.button("🔴 Did Not Comply (Ignored AI)", use_container_width=True):
        for sub in subjects: current_student[sub] = max(0, current_student[sub] - random.randint(8, 15))
        current_student["Compliance"] = "Poor"
        current_student["Path_Restructured"] = True
        st.rerun()

if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()


# ==========================================
# TEACHER PORTAL
# ==========================================
if role == "👨‍🏫 Teacher Portal":
    st.markdown("<h1 style='font-size: 2.5rem; margin-bottom: 0;'>Educator Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"Welcome back, **{st.session_state.username}**. Here is the live, predictive academic data.")
    
    # Process data into DataFrame
    df_data = []
    for s in st.session_state.student_data:
        total_current = sum(s[sub] for sub in subjects)
        total_base = sum(s[f"{sub}_base"] for sub in subjects)
        improvement = total_current - total_base
        row = [s["Student Name"], s["Compliance"]] + [s[sub] for sub in subjects] + [improvement, total_current]
        df_data.append(row)
        
    full_class_df = pd.DataFrame(df_data, columns=["Student Name", "AI Compliance"] + subjects + ["Improvement", "Total Score"])
    full_class_df = full_class_df.sort_values(by="Total Score", ascending=False)
    
    # KPI Metrics - New "Intervention Priority" logic
    intervention_count = len(full_class_df[(full_class_df["AI Compliance"] == "High") & (full_class_df["Total Score"] < 350)])
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Enrolled Students", value=len(st.session_state.student_data), delta="Full Roster Active")
    col2.metric(label="Intervention Priority", value=intervention_count, delta="High Effort, Low Yield", delta_color="off", help="Students who are complying with the AI but still missing target scores.")
    col3.metric(label="CBC Competencies Mapped", value=random.randint(800, 950), delta=f"{random.randint(10, 50)} Added Today")
    
    st.markdown("---")
    
    st.subheader("📊 Class Performance Gradebook")
    st.markdown("Watch scores fluctuate. **Improvement** tracks the net delta from their baseline.")
    
    # Calculate Class Mean row
    numeric_cols = subjects + ["Improvement", "Total Score"]
    means = full_class_df[numeric_cols].mean().round(1)
    mean_row = pd.DataFrame([["🏫 CLASS AVERAGE", "-"] + means.tolist()], columns=full_class_df.columns)
    display_df = pd.concat([full_class_df, mean_row], ignore_index=True)

    # Styling function
    def style_gradebook(row):
        styles = [''] * len(row)
        if row['Student Name'] == "🏫 CLASS AVERAGE":
            return ['background-color: #e2e8f0; font-weight: bold; color: #1e293b'] * len(row)
            
        for i, col in enumerate(display_df.columns):
            val = row[col]
            if col in subjects and isinstance(val, (int, float)):
                if val < 50: styles[i] = 'color: #dc2626; font-weight: 500' # Red
                elif val >= 80: styles[i] = 'color: #059669; font-weight: 500' # Green
            elif col == "Improvement" and isinstance(val, (int, float)):
                if val > 0: styles[i] = 'color: #059669; font-weight: bold' # Green delta
                elif val < 0: styles[i] = 'color: #dc2626; font-weight: bold' # Red delta
            elif col == "Total Score":
                styles[i] = 'background-color: #f8fafc; font-weight: bold'
            elif col == "AI Compliance":
                if val == "High": styles[i] = 'color: #059669; font-weight: bold'
                elif val == "Poor": styles[i] = 'color: #dc2626; font-weight: bold'
        return styles

    st.dataframe(
        display_df.style.apply(style_gradebook, axis=1).format({col: "{:.1f}" for col in numeric_cols}, na_rep="-"),
        use_container_width=True,
        hide_index=True,
        height=450
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("🤖 CBC Auto-Diagnostician")
        st.markdown("Paste observation notes to auto-map to the CBC portfolio.")
        obs_text = st.text_area("Teacher Observation:", value="Student successfully built a basic circuit. They troubleshooted a loose connection independently.", height=100)
        if st.button("Map Competency", type="primary"):
            with st.spinner("Mapping to CBC framework..."):
                time.sleep(1)
                st.success("Mapped to: Practical Application & Problem Solving ✅")

    with col_right:
        st.subheader("🕸️ Class Competency Mapping")
        # CBC Diagrammatic Representation (Radar Chart)
        cbc_pillars = ['Communication', 'Critical Thinking', 'Creativity', 'Citizenship', 'Self-Efficacy', 'Digital Literacy', 'Learning to Learn']
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[85, 90, 75, 88, 70, 95, 80],
            theta=cbc_pillars,
            fill='toself',
            line_color='#3b82f6',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ==========================================
# PARENT PORTAL
# ==========================================
elif role == "👨‍👩‍👧 Parent Portal":
    st.title("Parent Portal: Academic Tracker")
    st.markdown("Welcome! Review your child's adaptive learning strategy.")
    
    selected_student = st.selectbox("Select Student:", ["Grace Naliaka", "Neema Ongaga", "Rayvins Otieno", "Hillary Lweya"])
    student_record = next((s for s in st.session_state.student_data if s["Student Name"] == selected_student), None)
    
    if student_record:
        st.markdown(f"### 📊 {selected_student}'s Current Standings")
        
        if student_record["Path_Restructured"]:
            st.error("⚠️ **Alert:** EduAI has detected a recent drop in performance. The study path has been restructured to focus on foundational concepts.")
        elif student_record["Compliance"] == "High":
            st.success("✅ **Excellent:** Highly compliant with the AI study path. Seeing steady growth.")
            
        cols = st.columns(6)
        for i, sub in enumerate(subjects):
            val = student_record[sub]
            delta = "On Track" if val >= 60 else "Needs Review"
            color = "normal" if val >= 60 else "inverse"
            cols[i].metric(label=sub, value=f"{val}%", delta=delta, delta_color=color)

    st.markdown("---")
    st.subheader("🗺️ Active Study Strategy")
    st.markdown(f"Here is how the EduAI system is adapting the curriculum to reach target goals.")
    
    st.markdown("""
    | Day | Intervention Type | Status | Educator/AI Notes |
    | :--- | :--- | :--- | :--- |
    | **Monday** | Algebra Baseline | 🟢 Completed | *Identified fractions as a core gap.* |
    | **Wednesday** | Visual Fractions | 🟢 Completed | *Adapted materials to match visual learning profile.* |
    | **Today** | EduAI Tutor Model | 🟡 Pending | *AI-guided interactive lesson.* |
    """)

# ==========================================
# STUDENT PORTAL
# ==========================================
elif role == "🎓 Student Portal":
    current_student = next((s for s in st.session_state.student_data if s["Student Name"].lower().startswith(st.session_state.username.lower())), st.session_state.student_data[0])

    # --- PORTAL UI ---
    if st.session_state.sensory_mode == "Neuro-Focus (ADHD-Friendly)":
        st.warning("🎯 **Neuro-Focus Mode Active:** Extraneous dashboard elements are hidden to support deep work.")
        st.title(f"Ready to learn, {st.session_state.username}?")
        
        if current_student["Path_Restructured"]:
            st.error("⚠️ **ROUTE RECALCULATED:** Performance drop detected. Let's focus on the basics today.")
            
        st.markdown("### Your Current Assignment:")
        st.info("⏱️ **AI Interactive Teaching Module**")
        
        # Link button routing directly to your external AI model
        st.link_button("Launch AI Teaching Model", "https://eduaibrain-6bhvtrmivnvozjfrwpqbak.streamlit.app/", type="primary", use_container_width=True)
                
    else:
        st.title(f"Student Portal: {st.session_state.username}'s Journey")
        st.markdown("Welcome to your EduAI Command Center. Let's hit those academic goals! 🚀")
        
        if current_student["Path_Restructured"]:
             st.error("⚠️ **ROUTE RECALCULATED:** Edu_AI detected a drop in performance. Your study path has been dynamically restructured to reinforce foundational concepts. Bearish trend detected, let's buy the dip!")
             
        # Generate personalized breakout chart
        st.markdown(f"#### 📈 Your Predictive Forecasting Chart (Mathematics)")
        dates = pd.date_range(start="2026-01-01", periods=10, freq='W')
        base_score = current_student["Mathematics_base"]
        curr_score = current_student["Mathematics"]
        
        hist_grades = [base_score + random.randint(-4, 4) for _ in range(5)] + [curr_score] + [None]*4
        
        if current_student["Path_Restructured"]:
            # Bearish trajectory if they didn't comply
            forecast = [None]*5 + [curr_score] + [curr_score - i*random.randint(1, 4) for i in range(1, 5)]
            trend_color = "#dc2626"
            target_val = 50
        else:
            # Bullish breakout if they complied
            forecast = [None]*5 + [curr_score] + [curr_score + i*random.randint(2, 6) for i in range(1, 5)]
            trend_color = "#10b981"
            target_val = min(100, forecast[-1] + 2)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates[:6], y=hist_grades[:6], mode='lines+markers', name='Actual Performance', line=dict(color='#3b82f6', width=3)))
        fig.add_trace(go.Scatter(x=dates[5:], y=forecast[5:], mode='lines+markers', name='AI Predicted Trajectory', line=dict(color=trend_color, width=3, dash='dash')))
        fig.add_hline(y=target_val, line_dash="dot", annotation_text="AI Target", line_color="#f59e0b")
        
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("### Next Required Module\n**Interactive AI Teaching Model**\n\nLaunch your custom learning environment.")
            
            # Link button routing directly to your external AI model
            st.link_button("Launch AI Teaching Model", "https://eduaibrain-6bhvtrmivnvozjfrwpqbak.streamlit.app/", type="primary")
                
        with col2:
            if current_student["Path_Restructured"]: msg = "We hit a resistance level! Time to restructure and build a new foundation."
            else: msg = "Massive breakout! Your overall trajectory is trending upward. Keep holding!"
            st.success(f"### Edu_AI Tutor\n*\"{msg}\"*")

st.markdown("---")
st.caption("Developed by Team EduAI for the GLUK")
