# langgraph_agent.py
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, List, Dict, Any
import operator
import config
from datetime import datetime

class AgentState(TypedDict):
    user_input: str
    user_profile: Dict[str, Any]
    assessment_scores: Dict[str, float]
    skill_gaps: List[str]
    recommendations: List[str]
    study_plan: Dict[str, Any]
    current_step: str
    messages: Annotated[List[str], operator.add]

class PreptorAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            api_key=groq_api_key,
            model_name=config.config.GROQ_MODEL,
            temperature=0.7
        )
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_user", self.analyze_user_node)
        workflow.add_node("assess_skills", self.assess_skills_node)
        workflow.add_node("identify_gaps", self.identify_gaps_node)
        workflow.add_node("generate_recommendations", self.generate_recommendations_node)
        workflow.add_node("create_study_plan", self.create_study_plan_node)
        
        # Define edges
        workflow.set_entry_point("analyze_user")
        workflow.add_edge("analyze_user", "assess_skills")
        workflow.add_edge("assess_skills", "identify_gaps")
        workflow.add_edge("identify_gaps", "generate_recommendations")
        workflow.add_edge("generate_recommendations", "create_study_plan")
        workflow.add_edge("create_study_plan", END)
        
        return workflow.compile()
    
    def analyze_user_node(self, state: AgentState) -> AgentState:
        """Analyze user profile and requirements"""
        profile = state["user_profile"]
        
        prompt = f"""
        Analyze this user profile for placement preparation:
        Branch: {profile.get('branch', '')}
        Year: {profile.get('year', '')}
        Target Companies: {profile.get('preferred_companies', [])}
        Dream Role: {profile.get('dream_role', '')}
        
        Provide initial assessment of preparation needs.
        """
        
        response = self.llm.invoke(prompt).content
        
        state["messages"].append(f"User Analysis: {response}")
        state["current_step"] = "User profile analyzed"
        return state
    
    def assess_skills_node(self, state: AgentState) -> AgentState:
        """Assess current skill levels"""
        scores = state["assessment_scores"]
        
        prompt = f"""
        Based on assessment scores:
        Aptitude: {scores.get('aptitude', 0)}/100
        Technical: {scores.get('technical', 0)}/100
        Communication: {scores.get('communication', 0)}/100
        Resume: {scores.get('resume', 0)}/100
        
        Evaluate the student's readiness for placements and identify strengths.
        """
        
        response = self.llm.invoke(prompt).content
        
        state["messages"].append(f"Skill Assessment: {response}")
        state["current_step"] = "Skills assessed"
        return state
    
    def identify_gaps_node(self, state: AgentState) -> AgentState:
        """Identify skill gaps and weaknesses"""
        scores = state["assessment_scores"]
        profile = state["user_profile"]
        
        gaps = []
        if scores.get('aptitude', 0) < 70:
            gaps.append("Quantitative and Logical Reasoning")
        if scores.get('technical', 0) < 70:
            gaps.append("Technical Skills (DSA, DBMS, OS)")
        if scores.get('communication', 0) < 70:
            gaps.append("Communication and Soft Skills")
        if scores.get('resume', 0) < 70:
            gaps.append("Resume Optimization")
        
        prompt = f"""
        For a {profile.get('branch', '')} student targeting {profile.get('preferred_companies', [])},
        with identified gaps in: {gaps}
        
        Provide detailed analysis of each gap and its impact on placement success.
        """
        
        response = self.llm.invoke(prompt).content
        
        state["skill_gaps"] = gaps
        state["messages"].append(f"Gap Analysis: {response}")
        state["current_step"] = "Skill gaps identified"
        return state
    
    def generate_recommendations_node(self, state: AgentState) -> AgentState:
        """Generate learning recommendations"""
        gaps = state["skill_gaps"]
        profile = state["user_profile"]
        
        prompt = f"""
        Generate specific learning recommendations for:
        Student Profile: {profile.get('branch', '')} - Year {profile.get('year', '')}
        Skill Gaps: {gaps}
        Target Companies: {profile.get('preferred_companies', [])}
        
        Recommend:
        1. Specific topics to focus on
        2. Learning resources and platforms
        3. Practice strategies
        4. Timeline for improvement
        """
        
        response = self.llm.invoke(prompt).content
        recommendations = response.split('\n')
        
        state["recommendations"] = recommendations
        state["messages"].append(f"Recommendations: {response}")
        state["current_step"] = "Recommendations generated"
        return state
    
    def create_study_plan_node(self, state: AgentState) -> AgentState:
        """Create detailed study plan"""
        profile = state["user_profile"]
        gaps = state["skill_gaps"]
        recommendations = state["recommendations"]
        
        prompt = f"""
        Create a 4-week intensive study plan:
        
        Student: {profile.get('branch', '')} Year {profile.get('year', '')}
        Focus Areas: {gaps}
        Recommendations: {recommendations[:3]}  # Top 3 recommendations
        
        Create week-by-week breakdown with:
        - Daily study topics (2-3 hours/day)
        - Practice problems count
        - Mock tests schedule
        - Progress checkpoints
        
        Format as structured plan with clear daily goals.
        """
        
        response = self.llm.invoke(prompt).content
        
        # Parse response into structured format
        study_plan = {
            "duration": "4 weeks",
            "daily_hours": "2-3 hours",
            "plan": response,
            "created_at": datetime.now().isoformat()
        }
        
        state["study_plan"] = study_plan
        state["messages"].append(f"Study Plan Created: {response}")
        state["current_step"] = "Study plan ready"
        return state
    
    def run_agent(self, user_input: str, user_profile: Dict[str, Any], 
                  assessment_scores: Dict[str, float]) -> Dict[str, Any]:
        """Run the complete agent workflow"""
        initial_state = AgentState(
            user_input=user_input,
            user_profile=user_profile,
            assessment_scores=assessment_scores,
            skill_gaps=[],
            recommendations=[],
            study_plan={},
            current_step="Starting analysis",
            messages=[]
        )
        
        result = self.graph.invoke(initial_state)
        return result