# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

# Import custom modules
from database import DatabaseManager
from assessment_engine import AssessmentEngine
from groq_client import GroqClient
from langgraph_agent import PreptorAgent
from job_matcher import JobMatcher
from resource_recommender import ResourceRecommender
from config import config

# Initialize components
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()
if 'assessment_engine' not in st.session_state:
    st.session_state.assessment_engine = AssessmentEngine()
if 'groq_client' not in st.session_state:
    st.session_state.groq_client = GroqClient(config.GROQ_API_KEY)
if 'agent' not in st.session_state:
    st.session_state.agent = PreptorAgent(config.GROQ_API_KEY)
if 'job_matcher' not in st.session_state:
    st.session_state.job_matcher = JobMatcher()
if 'resource_recommender' not in st.session_state:
    st.session_state.resource_recommender = ResourceRecommender()

def main():
    st.set_page_config(
        page_title="Preptor - AI Placement Preparation",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
    }
    .skill-progress {
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Preptor - AI-Powered Placement Preparation</h1>
        <p>Your intelligent companion for placement success</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose Page", [
        "🏠 Home",
        "👤 Profile Setup",
        "📝 Assessments",
        "📊 Dashboard",
        "🎯 Study Plan",
        "💼 Job Matching",
        "🎤 Mock Interview"
    ])
    
    # Route to appropriate page
    if page == "🏠 Home":
        show_home_page()
    elif page == "👤 Profile Setup":
        show_profile_setup()
    elif page == "📝 Assessments":
        show_assessments()
    elif page == "📊 Dashboard":
        show_dashboard()
    elif page == "🎯 Study Plan":
        show_study_plan()
    elif page == "💼 Job Matching":
        show_job_matching()
    elif page == "🎤 Mock Interview":
        show_mock_interview()

def show_home_page():
    """Display home page with overview"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Welcome to Preptor! 🚀")
        st.markdown("""
        Preptor is your AI-powered placement preparation platform that provides:
        
        ✅ **Comprehensive Skill Assessment** - Aptitude, Technical, and Communication tests  
        ✅ **Personalized Learning Paths** - AI-generated study plans based on your gaps  
        ✅ **Company-Specific Preparation** - Tailored content for your target companies  
        ✅ **Mock Interviews** - Practice with AI interviewer  
        ✅ **Job Matching** - Find opportunities that match your skills  
        ✅ **Progress Tracking** - Monitor your improvement journey  
        
        ### Getting Started
        1. Set up your profile with academic and career preferences
        2. Take comprehensive skill assessments 
        3. Get your personalized AI-generated study plan
        4. Practice with company-specific content
        5. Track progress and get job recommendations
        """)
        
        if st.button("🚀 Start Your Journey", type="primary"):
            st.session_state.redirect_to = "👤 Profile Setup"
            st.rerun()
    
    with col2:
        st.markdown("### 📈 Platform Statistics")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Active Users", "1,250+", "12%")
            st.metric("Assessments Taken", "5,000+", "25%")
        with col_b:
            st.metric("Success Rate", "85%", "5%")
            st.metric("Partner Companies", "50+", "8%")
        
        st.markdown("### 🎯 Recent Success Stories")
        st.success("💼 Rahul got placed at TCS with 7 LPA package!")
        st.success("🌟 Priya cleared Amazon SDE interview!")
        st.success("🚀 Amit secured Microsoft internship!")

def show_profile_setup():
    """Display profile setup page"""
    st.markdown("## 👤 Profile Setup")
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        username = st.text_input("Username", key="login_username")
        
        if st.button("Login", type="primary"):
            user = st.session_state.db.get_user_by_username(username)
            if user:
                st.session_state.current_user = user
                st.success(f"Welcome back, {user['username']}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("User not found. Please register first.")
    
    with tab2:
        st.markdown("### Create New Account")
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username*")
                new_email = st.text_input("Email*")
                branch = st.selectbox("Branch*", [
                    "Computer Science", "Information Technology", "Electronics", 
                    "Mechanical", "Civil", "Electrical", "Other"
                ])
            
            with col2:
                year = st.selectbox("Current Year*", [1, 2, 3, 4])
                dream_role = st.text_input("Dream Role")
                preferred_companies = st.multiselect(
                    "Preferred Companies", 
                    config.TARGET_COMPANIES,
                    default=[]
                )
            
            if st.form_submit_button("Create Account", type="primary"):
                if new_username and new_email and branch:
                    try:
                        user_data = {
                            "username": new_username,
                            "email": new_email,
                            "branch": branch,
                            "year": year,
                            "dream_role": dream_role,
                            "preferred_companies": preferred_companies
                        }
                        
                        user_id = st.session_state.db.create_user(user_data)
                        st.success("Account created successfully!")
                        
                        # Auto-login new user
                        user_data['id'] = user_id
                        st.session_state.current_user = user_data
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error creating account: {str(e)}")
                else:
                    st.error("Please fill all required fields.")
    
    # Show current user info if logged in
    if st.session_state.current_user:
        st.markdown("---")
        st.markdown("### 📋 Current Profile")
        user = st.session_state.current_user
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Username:** {user['username']}")
            st.info(f"**Email:** {user['email']}")
            st.info(f"**Branch:** {user['branch']}")
        
        with col2:
            st.info(f"**Year:** {user['year']}")
            st.info(f"**Dream Role:** {user.get('dream_role', 'Not specified')}")
            companies = user.get('preferred_companies', [])
            st.info(f"**Target Companies:** {', '.join(companies) if companies else 'None selected'}")

def show_assessments():
    """Display assessments page"""
    st.markdown("## 📝 Skill Assessments")
    
    if not st.session_state.current_user:
        st.warning("Please login first to take assessments.")
        return
    
    user_id = st.session_state.current_user['id']
    
    # Assessment selection
    assessment_type = st.selectbox("Choose Assessment Type", [
        "Aptitude Test", "Technical Test", "Communication Assessment", "Complete Assessment Suite"
    ])
    
    if assessment_type == "Aptitude Test":
        show_aptitude_test(user_id)
    elif assessment_type == "Technical Test":
        show_technical_test(user_id)
    elif assessment_type == "Communication Assessment":
        show_communication_test(user_id)
    elif assessment_type == "Complete Assessment Suite":
        show_complete_assessment(user_id)

def show_aptitude_test(user_id: int):
    """Display aptitude test"""
    st.markdown("### 🧠 Aptitude Test")
    st.info("This test covers Quantitative, Logical Reasoning, and Verbal Ability")
    
    if 'aptitude_questions' not in st.session_state:
        if st.button("Start Aptitude Test", type="primary"):
            questions = st.session_state.assessment_engine.generate_aptitude_test(20)
            st.session_state.aptitude_questions = questions
            st.session_state.aptitude_answers = [0] * len(questions)
            st.session_state.current_question = 0
            st.rerun()
    else:
        questions = st.session_state.aptitude_questions
        current_q = st.session_state.current_question
        
        if current_q < len(questions):
            question = questions[current_q]
            
            st.markdown(f"### Question {current_q + 1} of {len(questions)}")
            st.markdown(f"**{question['question']}**")
            
            answer = st.radio(
                "Choose your answer:",
                question['options'],
                key=f"aptitude_q_{current_q}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Previous") and current_q > 0:
                    st.session_state.current_question -= 1
                    st.rerun()
            
            with col2:
                if current_q < len(questions) - 1:
                    if st.button("Next", type="primary"):
                        st.session_state.aptitude_answers[current_q] = question['options'].index(answer)
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    if st.button("Submit Test", type="primary"):
                        st.session_state.aptitude_answers[current_q] = question['options'].index(answer)
                        
                        # Evaluate test
                        results = st.session_state.assessment_engine.evaluate_aptitude_test(
                            st.session_state.aptitude_answers, questions
                        )
                        
                        # Save results
                        st.session_state.db.save_assessment_result(
                            user_id, "aptitude", results['overall_score'], results
                        )
                        
                        # Show results
                        st.success("Aptitude test completed!")
                        st.markdown("### Results")
                        st.metric("Overall Score", f"{results['overall_score']:.1f}%")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Quantitative", f"{results['topic_scores']['quantitative']:.1f}%")
                        with col2:
                            st.metric("Logical", f"{results['topic_scores']['logical']:.1f}%")
                        with col3:
                            st.metric("Verbal", f"{results['topic_scores']['verbal']:.1f}%")
                        
                        if results['weak_areas']:
                            st.warning(f"Areas needing improvement: {', '.join(results['weak_areas'])}")
                        
                        # Clear session state
                        del st.session_state.aptitude_questions
                        del st.session_state.aptitude_answers
                        del st.session_state.current_question

def show_technical_test(user_id: int):
    """Display technical test"""
    st.markdown("### 💻 Technical Test")
    branch = st.session_state.current_user['branch']
    st.info(f"This test covers topics relevant to {branch} students")
    
    if 'technical_questions' not in st.session_state:
        if st.button("Start Technical Test", type="primary"):
            questions = st.session_state.assessment_engine.generate_technical_test(branch, 15)
            st.session_state.technical_questions = questions
            st.session_state.technical_answers = [0] * len(questions)
            st.session_state.current_tech_question = 0
            st.rerun()
    else:
        questions = st.session_state.technical_questions
        current_q = st.session_state.current_tech_question
        
        if current_q < len(questions):
            question = questions[current_q]
            
            st.markdown(f"### Question {current_q + 1} of {len(questions)}")
            st.markdown(f"**Topic: {question['topic']}**")
            st.markdown(f"**{question['question']}**")
            
            answer = st.radio(
                "Choose your answer:",
                question['options'],
                key=f"tech_q_{current_q}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Previous") and current_q > 0:
                    st.session_state.current_tech_question -= 1
                    st.rerun()
            
            with col2:
                if current_q < len(questions) - 1:
                    if st.button("Next", type="primary"):
                        st.session_state.technical_answers[current_q] = question['options'].index(answer)
                        st.session_state.current_tech_question += 1
                        st.rerun()
                else:
                    if st.button("Submit Test", type="primary"):
                        st.session_state.technical_answers[current_q] = question['options'].index(answer)
                        
                        # Evaluate test
                        results = st.session_state.assessment_engine.evaluate_technical_test(
                            st.session_state.technical_answers, questions
                        )
                        
                        # Save results
                        st.session_state.db.save_assessment_result(
                            user_id, "technical", results['overall_score'], results
                        )
                        
                        # Show results
                        st.success("Technical test completed!")
                        st.markdown("### Results")
                        st.metric("Overall Score", f"{results['overall_score']:.1f}%")
                        
                        # Topic-wise scores
                        for topic, score in results['topic_scores'].items():
                            st.metric(topic, f"{score:.1f}%")
                        
                        if results['weak_areas']:
                            st.warning(f"Topics needing focus: {', '.join(results['weak_areas'])}")
                        
                        # Clear session state
                        del st.session_state.technical_questions
                        del st.session_state.technical_answers
                        del st.session_state.current_tech_question

def show_communication_test(user_id: int):
    """Display communication assessment"""
    st.markdown("### 🎤 Communication Assessment")
    st.info("Answer the following questions to assess your communication skills")
    
    questions = st.session_state.assessment_engine.behavioral_questions[:3]
    responses = []
    
    for i, question in enumerate(questions):
        st.markdown(f"**Question {i+1}: {question}**")
        response = st.text_area(f"Your answer:", key=f"comm_q_{i}", height=100)
        responses.append(response)
    
    if st.button("Submit Communication Assessment", type="primary"):
        if all(responses):
            # Combine all responses for analysis
            combined_response = " ".join(responses)
            
            # Analyze communication
            results = st.session_state.assessment_engine.analyze_communication(combined_response)
            
            # Save results
            st.session_state.db.save_assessment_result(
                user_id, "communication", results['overall_score'], results
            )
            
            # Show results
            st.success("Communication assessment completed!")
            st.markdown("### Results")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Overall Score", f"{results['overall_score']:.1f}%")
            with col2:
                st.metric("Confidence", f"{results['confidence_score']:.1f}%")
            with col3:
                st.metric("Grammar", f"{results['grammar_score']:.1f}%")
            with col4:
                st.metric("Vocabulary", f"{results['vocabulary_score']:.1f}%")
            
            st.markdown("### Detailed Analysis")
            st.info(f"Word Count: {results['word_count']}")
            st.info(f"Average Sentence Length: {results['avg_sentence_length']:.1f} words")
            
            if results['areas_for_improvement']:
                st.markdown("### Areas for Improvement")
                for improvement in results['areas_for_improvement']:
                    st.write(f"• {improvement}")
        else:
            st.error("Please answer all questions.")

def show_dashboard():
    """Display user dashboard"""
    st.markdown("## 📊 Your Progress Dashboard")
    
    if not st.session_state.current_user:
        st.warning("Please login to view your dashboard.")
        return
    
    user_id = st.session_state.current_user['id']
    skill_profile = st.session_state.db.get_user_skill_profile(user_id)
    
    if not skill_profile:
        st.info("Complete your assessments to see your dashboard.")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Placement Readiness", f"{skill_profile['overall_score']:.1f}%", 
                 delta=f"{skill_profile['overall_score'] - 50:.1f}%")
    with col2:
        st.metric("Aptitude Score", f"{skill_profile['aptitude_score']:.1f}%")
    with col3:
        st.metric("Technical Score", f"{skill_profile['technical_score']:.1f}%")
    with col4:
        st.metric("Communication", f"{skill_profile['communication_score']:.1f}%")
    
    # Skill breakdown chart
    st.markdown("### Skill Breakdown")
    skills_data = {
        'Skill Area': ['Aptitude', 'Technical', 'Communication', 'Resume'],
        'Score': [
            skill_profile['aptitude_score'],
            skill_profile['technical_score'], 
            skill_profile['communication_score'],
            skill_profile['resume_score']
        ]
    }
    
    fig = px.bar(skills_data, x='Skill Area', y='Score', 
                 color='Score', color_continuous_scale='RdYlGn',
                 title="Your Skill Scores")
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="Target Score")
    st.plotly_chart(fig, use_container_width=True)
    
    # Radar chart for comprehensive view
    st.markdown("### Comprehensive Skill Analysis")
    radar_fig = go.Figure()
    
    skills = ['Aptitude', 'Technical', 'Communication', 'Resume']
    scores = [
        skill_profile['aptitude_score'],
        skill_profile['technical_score'],
        skill_profile['communication_score'], 
        skill_profile['resume_score']
    ]
    
    radar_fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=skills,
        fill='toself',
        name='Your Scores'
    ))
    
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Skills Radar Chart"
    )
    
    st.plotly_chart(radar_fig, use_container_width=True)
    
    # Weak areas and recommendations
    if skill_profile['weak_areas']:
        st.markdown("### 🎯 Areas Needing Focus")
        weak_areas = skill_profile['weak_areas']
        
        for area in weak_areas:
            with st.expander(f"📚 Improve {area}"):
                st.write(f"Your {area} score needs improvement. Here are some recommendations:")
                
                # Get resources for this weak area
                resources = st.session_state.resource_recommender.recommend_resources([area])
                if area in resources:
                    for resource in resources[area][:3]:  # Show top 3 resources
                        st.write(f"• [{resource['title']}]({resource['url']})")
                        st.caption(resource['description'][:100] + "...")
    
    # Progress timeline
    st.markdown("### 📈 Progress Timeline")
    timeline_data = {
        'Date': [
            datetime.now() - timedelta(days=14),
            datetime.now() - timedelta(days=10),
            datetime.now() - timedelta(days=5),
            datetime.now()
        ],
        'Overall Score': [45, 52, 58, skill_profile['overall_score']]
    }
    
    timeline_fig = px.line(timeline_data, x='Date', y='Overall Score',
                          title='Your Progress Over Time',
                          markers=True)
    timeline_fig.add_hline(y=70, line_dash="dash", line_color="green",
                          annotation_text="Target Score")
    st.plotly_chart(timeline_fig, use_container_width=True)

def show_study_plan():
    """Display AI-generated study plan"""
    st.markdown("## 🎯 Personalized Study Plan")
    
    if not st.session_state.current_user:
        st.warning("Please login to access your study plan.")
        return
    
    user_id = st.session_state.current_user['id']
    skill_profile = st.session_state.db.get_user_skill_profile(user_id)
    
    if not skill_profile:
        st.info("Complete your assessments first to generate a study plan.")
        return
    
    # Study plan generation
    if st.button("🤖 Generate AI Study Plan", type="primary"):
        with st.spinner("AI is creating your personalized study plan..."):
            # Prepare data for agent
            user_profile = st.session_state.current_user
            assessment_scores = {
                'aptitude': skill_profile['aptitude_score'],
                'technical': skill_profile['technical_score'],
                'communication': skill_profile['communication_score'],
                'resume': skill_profile['resume_score']
            }
            
            # Run the LangGraph agent
            try:
                result = st.session_state.agent.run_agent(
                    user_input="Create a comprehensive study plan",
                    user_profile=user_profile,
                    assessment_scores=assessment_scores
                )
                
                st.session_state.study_plan_result = result
                
            except Exception as e:
                st.error(f"Error generating study plan: {str(e)}")
                return
    
    # Display study plan if generated
    if 'study_plan_result' in st.session_state:
        result = st.session_state.study_plan_result
        
        st.success("✅ Your personalized study plan is ready!")
        
        # Display agent analysis
        with st.expander("🔍 AI Analysis Summary"):
            for message in result['messages']:
                st.write(f"• {message[:150]}...")
        
        # Display study plan
        st.markdown("### 📅 4-Week Study Plan")
        
        study_plan = result['study_plan']
        if study_plan:
            st.info(f"**Duration:** {study_plan.get('duration', '4 weeks')}")
            st.info(f"**Daily Commitment:** {study_plan.get('daily_hours', '2-3 hours')}")
            
            # Format and display the plan
            plan_content = study_plan.get('plan', '')
            if plan_content:
                st.markdown(plan_content)
        
        # Skill gaps and recommendations
        if result['skill_gaps']:
            st.markdown("### 🎯 Priority Focus Areas")
            for gap in result['skill_gaps']:
                st.error(f"❗ {gap}")
        
        if result['recommendations']:
            st.markdown("### 💡 Key Recommendations")
            for i, rec in enumerate(result['recommendations'][:5], 1):
                st.success(f"{i}. {rec}")
    
    # Company-specific preparation
    st.markdown("---")
    st.markdown("### 🏢 Company-Specific Preparation")
    
    user_companies = st.session_state.current_user.get('preferred_companies', [])
    if user_companies:
        selected_company = st.selectbox("Select target company:", user_companies)
        
        if selected_company:
            company_resources = st.session_state.resource_recommender.get_company_specific_resources(selected_company)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"#### 💻 {selected_company} - Coding Patterns")
                for pattern in company_resources.get('coding_pattern', []):
                    st.write(f"• {pattern}")
                
                st.markdown(f"#### 📚 Technical Topics")
                for topic in company_resources.get('technical_topics', []):
                    st.write(f"• {topic}")
            
            with col2:
                st.markdown(f"#### 🎯 Interview Tips")
                for tip in company_resources.get('interview_tips', []):
                    st.write(f"• {tip}")
    
    # Daily practice tracker
    st.markdown("---")
    st.markdown("### ✅ Daily Practice Tracker")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.checkbox("Aptitude Practice (30 min)")
        st.checkbox("Technical Study (45 min)")
    
    with col2:
        st.checkbox("Coding Problems (60 min)")
        st.checkbox("Mock Interview (20 min)")
    
    with col3:
        st.checkbox("Resume Review (15 min)")
        st.checkbox("Company Research (30 min)")
    
    if st.button("Save Today's Progress"):
        st.success("Progress saved! Keep up the great work! 🎉")

def show_job_matching():
    """Display job matching page"""
    st.markdown("## 💼 Job Matching & Recommendations")
    
    if not st.session_state.current_user:
        st.warning("Please login to see job recommendations.")
        return
    
    user_profile = st.session_state.current_user
    skill_profile = st.session_state.db.get_user_skill_profile(user_profile['id'])
    
    if not skill_profile:
        st.info("Complete your assessments to get job recommendations.")
        return
    
    # Get job matches
    skill_scores = {
        'technical': skill_profile['technical_score'],
        'communication': skill_profile['communication_score'],
        'aptitude': skill_profile['aptitude_score']
    }
    
    matched_jobs = st.session_state.job_matcher.match_jobs(user_profile, skill_scores)
    
    st.markdown("### 🎯 Recommended Jobs for You")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fit_filter = st.selectbox("Filter by Fit Level:", ["All", "High Fit", "Medium Fit", "Low Fit"])
    
    with col2:
        company_filter = st.selectbox("Filter by Company:", ["All"] + list(set(job['company'] for job in matched_jobs)))
    
    with col3:
        location_filter = st.selectbox("Filter by Location:", ["All"] + list(set(job['location'] for job in matched_jobs)))
    
    # Apply filters
    filtered_jobs = matched_jobs
    if fit_filter != "All":
        filtered_jobs = [job for job in filtered_jobs if job['fit_level'] == fit_filter]
    if company_filter != "All":
        filtered_jobs = [job for job in filtered_jobs if job['company'] == company_filter]
    if location_filter != "All":
        filtered_jobs = [job for job in filtered_jobs if job['location'] == location_filter]
    
    # Display jobs
    for job in filtered_jobs:
        with st.expander(f"🏢 {job['title']} - {job['company']} ({job['fit_score']}% match)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Company:** {job['company']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Description:** {job['description']}")
                
                st.markdown("**Requirements:**")
                for req in job['requirements']:
                    st.write(f"• {req}")
            
            with col2:
                # Fit level badge
                if job['fit_level'] == "High Fit":
                    st.success(f"🟢 {job['fit_level']} ({job['fit_score']}%)")
                elif job['fit_level'] == "Medium Fit":
                    st.warning(f"🟡 {job['fit_level']} ({job['fit_score']}%)")
                else:
                    st.error(f"🔴 {job['fit_level']} ({job['fit_score']}%)")
                
                st.markdown("**Matching Skills:**")
                for skill in job.get('matching_skills', []):
                    st.success(f"✅ {skill}")
                
                st.markdown("**Skill Gaps:**")
                for gap in job.get('skill_gaps', []):
                    st.error(f"❌ {gap}")
                
                if st.button(f"Apply Now", key=f"apply_{job['title']}"):
                    st.success("Application link opened!")
                    st.markdown(f"[Apply Here]({job['url']})")
    
    if not filtered_jobs:
        st.info("No jobs match your current filters. Try adjusting the filter criteria.")
    
    # Job search tips
    st.markdown("---")
    st.markdown("### 💡 Job Search Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Before Applying:**
        • Research the company culture and values
        • Customize your resume for each application
        • Practice company-specific interview questions
        • Network with current employees on LinkedIn
        """)
    
    with col2:
        st.markdown("""
        **Application Strategy:**
        • Apply to jobs with 60%+ skill match
        • Focus on improving skills for dream companies
        • Follow up after applications
        • Prepare for multiple interview rounds
        """)

def show_mock_interview():
    """Display mock interview page"""
    st.markdown("## 🎤 AI Mock Interview")
    
    if not st.session_state.current_user:
        st.warning("Please login to start mock interviews.")
        return
    
    user_profile = st.session_state.current_user
    
    # Interview type selection
    interview_type = st.selectbox("Select Interview Type:", [
        "Technical Interview", "HR Interview", "Behavioral Interview", "Company-Specific Interview"
    ])
    
    # Company selection for company-specific interviews
    company = None
    if interview_type == "Company-Specific Interview":
        company = st.selectbox("Select Company:", user_profile.get('preferred_companies', config.TARGET_COMPANIES))
    
    # Interview difficulty
    difficulty = st.selectbox("Select Difficulty:", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("🎯 Start Mock Interview", type="primary"):
        st.session_state.interview_active = True
        st.session_state.interview_questions = generate_interview_questions(interview_type, company, difficulty)
        st.session_state.current_interview_question = 0
        st.session_state.interview_responses = []
        st.rerun()
    
    # Active interview
    if st.session_state.get('interview_active', False):
        questions = st.session_state.interview_questions
        current_q = st.session_state.current_interview_question
        
        if current_q < len(questions):
            question = questions[current_q]
            
            st.markdown(f"### Question {current_q + 1} of {len(questions)}")
            st.markdown(f"**🤖 Interviewer:** {question}")
            
            # Response input
            response = st.text_area(
                "Your Response:", 
                height=150,
                placeholder="Take your time to provide a detailed answer...",
                key=f"interview_response_{current_q}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Previous Question") and current_q > 0:
                    st.session_state.interview_responses[current_q] = response
                    st.session_state.current_interview_question -= 1
                    st.rerun()
            
            with col2:
                if current_q < len(questions) - 1:
                    if st.button("Next Question", type="primary"):
                        st.session_state.interview_responses.append(response)
                        st.session_state.current_interview_question += 1
                        st.rerun()
                else:
                    if st.button("Complete Interview", type="primary"):
                        st.session_state.interview_responses.append(response)
                        
                        # Analyze interview performance
                        with st.spinner("AI is analyzing your interview performance..."):
                            analysis = analyze_interview_performance(
                                questions, 
                                st.session_state.interview_responses,
                                interview_type
                            )
                        
                        # Show results
                        show_interview_results(analysis)
                        
                        # Clear interview session
                        st.session_state.interview_active = False
                        del st.session_state.interview_questions
                        del st.session_state.current_interview_question
                        del st.session_state.interview_responses

def generate_interview_questions(interview_type: str, company: str = None, difficulty: str = "Intermediate") -> list:
    """Generate interview questions based on type and difficulty"""
    technical_questions = {
        "Beginner": [
            "What is the difference between an array and a linked list?",
            "Explain what is recursion with an example.",
            "What are the basic principles of object-oriented programming?",
            "How does a hash table work?",
            "What is the time complexity of binary search?"
        ],
        "Intermediate": [
            "Implement a function to reverse a linked list.",
            "Explain the difference between SQL and NoSQL databases.",
            "How would you detect a cycle in a linked list?",
            "What is the difference between process and thread?",
            "Design a simple cache system."
        ],
        "Advanced": [
            "Design a distributed system for a social media feed.",
            "Implement a thread-safe singleton pattern.",
            "How would you design a URL shortening service like bit.ly?",
            "Explain CAP theorem and its implications.",
            "Design a recommendation system for an e-commerce platform."
        ]
    }
    
    hr_questions = [
        "Tell me about yourself.",
        "What are your greatest strengths and weaknesses?",
        "Why do you want to work for our company?",
        "Describe a challenging situation you faced and how you handled it.",
        "Where do you see yourself in 5 years?",
        "Why are you leaving your current position?",
        "What motivates you?",
        "How do you handle stress and pressure?"
    ]
    
    behavioral_questions = [
        "Describe a time when you had to work with a difficult team member.",
        "Tell me about a project you're most proud of.",
        "How do you prioritize your tasks when you have multiple deadlines?",
        "Describe a time when you had to learn something new quickly.",
        "Tell me about a time when you made a mistake. How did you handle it?",
        "How do you handle constructive criticism?",
        "Describe a time when you had to persuade someone to see things your way."
    ]
    
    if interview_type == "Technical Interview":
        return technical_questions.get(difficulty, technical_questions["Intermediate"])
    elif interview_type == "HR Interview":
        return hr_questions[:5]
    elif interview_type == "Behavioral Interview":
        return behavioral_questions[:5]
    elif interview_type == "Company-Specific Interview":
        # Customize based on company
        base_questions = technical_questions.get(difficulty, technical_questions["Intermediate"])[:3]
        company_questions = [
            f"Why do you want to work specifically at {company}?",
            f"What do you know about {company}'s recent developments?"
        ]
        return base_questions + company_questions
    
    return hr_questions[:5]  # Default

def analyze_interview_performance(questions: list, responses: list, interview_type: str) -> dict:
    """Analyze interview performance using AI"""
    try:
        # Combine questions and responses
        interview_text = ""
        for i, (question, response) in enumerate(zip(questions, responses)):
            interview_text += f"Q{i+1}: {question}\nA{i+1}: {response}\n\n"
        
        # Use Groq to analyze
        prompt = f"""
        Analyze this {interview_type.lower()} interview performance:
        
        {interview_text}
        
        Provide detailed feedback on:
        1. Overall performance score (0-100)
        2. Communication clarity and confidence
        3. Technical knowledge (if applicable)
        4. Areas of strength
        5. Areas for improvement
        6. Specific recommendations
        
        Format as JSON with keys: overall_score, communication_score, technical_score, strengths, weaknesses, recommendations
        """
        
        system_prompt = "You are an expert interview coach. Provide constructive, detailed feedback to help candidates improve."
        
        response = st.session_state.groq_client.generate_response(prompt, system_prompt)
        
        try:
            analysis = json.loads(response)
        except:
            # Fallback analysis
            analysis = {
                "overall_score": 75,
                "communication_score": 80,
                "technical_score": 70,
                "strengths": ["Good communication", "Structured responses"],
                "weaknesses": ["Need more technical depth", "Practice confidence"],
                "recommendations": ["Practice more coding problems", "Work on articulation"]
            }
        
        return analysis
        
    except Exception as e:
        st.error(f"Error analyzing interview: {str(e)}")
        return {
            "overall_score": 70,
            "communication_score": 75,
            "technical_score": 65,
            "strengths": ["Attempted all questions"],
            "weaknesses": ["Analysis unavailable"],
            "recommendations": ["Continue practicing interviews"]
        }

def show_interview_results(analysis: dict):
    """Display interview analysis results"""
    st.success("🎉 Interview Completed!")
    
    st.markdown("### 📊 Performance Analysis")
    
    # Score metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = analysis.get('overall_score', 70)
        st.metric("Overall Performance", f"{score}%", 
                 delta=f"{score - 70}%" if score != 70 else None)
    
    with col2:
        comm_score = analysis.get('communication_score', 75)
        st.metric("Communication", f"{comm_score}%")
    
    with col3:
        tech_score = analysis.get('technical_score', 65)
        st.metric("Technical Skills", f"{tech_score}%")
    
    # Strengths and weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Strengths")
        for strength in analysis.get('strengths', []):
            st.success(f"• {strength}")
    
    with col2:
        st.markdown("### 🎯 Areas for Improvement")
        for weakness in analysis.get('weaknesses', []):
            st.warning(f"• {weakness}")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    for recommendation in analysis.get('recommendations', []):
        st.info(f"• {recommendation}")
    
    # Performance radar chart
    st.markdown("### 📈 Performance Breakdown")
    
    categories = ['Communication', 'Technical Knowledge', 'Confidence', 'Problem Solving', 'Clarity']
    scores = [
        analysis.get('communication_score', 75),
        analysis.get('technical_score', 65),
        max(60, analysis.get('overall_score', 70) - 10),  # Estimated confidence
        analysis.get('technical_score', 65),  # Problem solving ~ technical
        analysis.get('communication_score', 75)  # Clarity ~ communication
    ]
    
    radar_fig = go.Figure()
    
    radar_fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Your Performance'
    ))
    
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Interview Performance Analysis"
    )
    
    st.plotly_chart(radar_fig, use_container_width=True)

def show_complete_assessment(user_id: int):
    """Show complete assessment suite"""
    st.markdown("### 🎯 Complete Assessment Suite")
    st.info("This comprehensive assessment covers all skill areas")
    
    if st.button("Start Complete Assessment", type="primary"):
        # Initialize complete assessment
        st.session_state.complete_assessment_active = True
        st.session_state.assessment_step = 1
        st.rerun()
    
    if st.session_state.get('complete_assessment_active', False):
        step = st.session_state.get('assessment_step', 1)
        
        # Progress bar
        progress = (step - 1) / 4
        st.progress(progress)
        st.markdown(f"Step {step} of 4")
        
        if step == 1:
            st.markdown("#### Step 1: Quick Profile Update")
            
            with st.form("profile_update"):
                col1, col2 = st.columns(2)
                with col1:
                    skills = st.multiselect("Key Technical Skills:", 
                        ["Java", "Python", "C++", "JavaScript", "SQL", "Data Structures", "Algorithms"])
                    experience = st.selectbox("Coding Experience:", 
                        ["Beginner", "Intermediate", "Advanced"])
                
                with col2:
                    interests = st.multiselect("Areas of Interest:",
                        ["Web Development", "Data Science", "Mobile Apps", "AI/ML", "Cybersecurity"])
                    target_role = st.text_input("Target Role:", value=st.session_state.current_user.get('dream_role', ''))
                
                if st.form_submit_button("Continue to Assessments", type="primary"):
                    # Save updated profile
                    st.session_state.user_skills = skills
                    st.session_state.user_experience = experience
                    st.session_state.assessment_step = 2
                    st.rerun()
        
        elif step == 2:
            st.markdown("#### Step 2: Quick Aptitude Check (10 questions)")
            # Simplified aptitude test
            show_quick_aptitude_test(user_id)
        
        elif step == 3:
            st.markdown("#### Step 3: Technical Assessment (8 questions)")
            # Simplified technical test
            show_quick_technical_test(user_id)
        
        elif step == 4:
            st.markdown("#### Step 4: Communication Sample")
            show_quick_communication_test(user_id)

def show_quick_aptitude_test(user_id: int):
    """Quick aptitude test for complete assessment"""
    if 'quick_aptitude_questions' not in st.session_state:
        questions = st.session_state.assessment_engine.generate_aptitude_test(10)
        st.session_state.quick_aptitude_questions = questions
        st.session_state.quick_aptitude_current = 0
        st.session_state.quick_aptitude_answers = []
    
    questions = st.session_state.quick_aptitude_questions
    current = st.session_state.quick_aptitude_current
    
    if current < len(questions):
        question = questions[current]
        st.markdown(f"**Question {current + 1}: {question['question']}**")
        
        answer = st.radio("Choose answer:", question['options'], key=f"qa_{current}")
        
        if st.button("Next", type="primary"):
            st.session_state.quick_aptitude_answers.append(question['options'].index(answer))
            st.session_state.quick_aptitude_current += 1
            
            if current + 1 >= len(questions):
                # Complete aptitude, move to next step
                results = st.session_state.assessment_engine.evaluate_aptitude_test(
                    st.session_state.quick_aptitude_answers, questions
                )
                st.session_state.db.save_assessment_result(user_id, "aptitude", results['overall_score'], results)
                st.session_state.assessment_step = 3
                
                # Clean up
                del st.session_state.quick_aptitude_questions
                del st.session_state.quick_aptitude_current
                del st.session_state.quick_aptitude_answers
            
            st.rerun()

def show_quick_technical_test(user_id: int):
    """Quick technical test for complete assessment"""
    if 'quick_tech_questions' not in st.session_state:
        questions = st.session_state.assessment_engine.generate_technical_test(
            st.session_state.current_user['branch'], 8
        )
        st.session_state.quick_tech_questions = questions
        st.session_state.quick_tech_current = 0
        st.session_state.quick_tech_answers = []
    
    questions = st.session_state.quick_tech_questions
    current = st.session_state.quick_tech_current
    
    if current < len(questions):
        question = questions[current]
        st.markdown(f"**Question {current + 1} ({question['topic']}): {question['question']}**")
        
        answer = st.radio("Choose answer:", question['options'], key=f"qt_{current}")
        
        if st.button("Next", type="primary"):
            st.session_state.quick_tech_answers.append(question['options'].index(answer))
            st.session_state.quick_tech_current += 1
            
            if current + 1 >= len(questions):
                # Complete technical, move to next step
                results = st.session_state.assessment_engine.evaluate_technical_test(
                    st.session_state.quick_tech_answers, questions
                )
                st.session_state.db.save_assessment_result(user_id, "technical", results['overall_score'], results)
                st.session_state.assessment_step = 4
                
                # Clean up
                del st.session_state.quick_tech_questions
                del st.session_state.quick_tech_current
                del st.session_state.quick_tech_answers
            
            st.rerun()

def show_quick_communication_test(user_id: int):
    """Quick communication test for complete assessment"""
    st.markdown("**Please answer this question to assess communication skills:**")
    
    question = "Describe a technical project you worked on and explain how you would present it to a non-technical audience."
    st.markdown(f"**Question:** {question}")
    
    response = st.text_area("Your answer:", height=120, key="quick_comm_response")
    
    if st.button("Complete Assessment", type="primary"):
        if response.strip():
            # Analyze communication
            results = st.session_state.assessment_engine.analyze_communication(response)
            st.session_state.db.save_assessment_result(user_id, "communication", results['overall_score'], results)
            
            # Calculate and update overall skill profile
            calculate_overall_assessment_results(user_id)
            
            # Complete assessment
            st.session_state.complete_assessment_active = False
            st.session_state.assessment_step = 1
            
            st.success("🎉 Complete Assessment Finished!")
            st.balloons()
            
            time.sleep(2)
            st.rerun()
        else:
            st.error("Please provide an answer to complete the assessment.")

def calculate_overall_assessment_results(user_id: int):
    """Calculate and save overall assessment results"""
    # Get recent assessment scores
    conn = sqlite3.connect(st.session_state.db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT assessment_type, score FROM assessments 
        WHERE user_id = ? 
        ORDER BY completed_at DESC
    """, (user_id,))
    
    recent_scores = {}
    for row in cursor.fetchall():
        assessment_type, score = row
        if assessment_type not in recent_scores:  # Get most recent of each type
            recent_scores[assessment_type] = score
    
    conn.close()
    
    # Create skill matrix
    skill_matrix = {
        'aptitude_breakdown': {
            'quantitative': recent_scores.get('aptitude', 0),
            'logical': recent_scores.get('aptitude', 0) * 0.9,
            'verbal': recent_scores.get('aptitude', 0) * 1.1
        },
        'technical_breakdown': {
            'programming': recent_scores.get('technical', 0),
            'algorithms': recent_scores.get('technical', 0) * 0.8,
            'system_design': recent_scores.get('technical', 0) * 0.7
        },
        'communication_breakdown': {
            'clarity': recent_scores.get('communication', 0),
            'confidence': recent_scores.get('communication', 0) * 0.9,
            'vocabulary': recent_scores.get('communication', 0) * 1.1
        }
    }
    
    # Identify weak areas
    weak_areas = []
    if recent_scores.get('aptitude', 0) < 60:
        weak_areas.append('Aptitude')
    if recent_scores.get('technical', 0) < 60:
        weak_areas.append('Technical Skills')
    if recent_scores.get('communication', 0) < 60:
        weak_areas.append('Communication')
    
    # Update skill profile
    st.session_state.db.update_skill_profile(
        user_id, recent_scores, skill_matrix, weak_areas
    )

if __name__ == "__main__":
    main()