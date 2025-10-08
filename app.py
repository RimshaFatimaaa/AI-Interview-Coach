"""
AI-Powered Job Interview Coach - NLP Demo App
Simple Streamlit app to display NLP processing results from the notebook
"""

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from Streamlit secrets
try:
    openai_key = st.secrets["OPENAI_API_KEY"]
    # Set the environment variable for other modules
    os.environ['OPENAI_API_KEY'] = openai_key
except KeyError:
    st.error("⚠️ OPENAI_API_KEY not found. Please set it in Streamlit Cloud secrets.")
    st.stop()
from ai_modules.nlp_processor import process_interview_response, NLPProcessor
from ai_modules.llm_processor_simple import SimpleLLMProcessor, QuestionType, DifficultyLevel
from ai_modules.langchain_processor import LangChainInterviewProcessor
from ai_modules.auth import check_auth_status, init_session_state
from ai_modules.auth_ui import show_auth_page, show_logout_button, show_header_logout
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="AI Interview Coach - Advanced Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1.5rem;
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-icon {
        font-size: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 3rem;
        height: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .logo-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .logout-btn {
        background: #ffffff;
        color: #6c757d;
        border: 1px solid #dee2e6;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .logout-btn:hover {
        background: #f8f9fa;
        border-color: #adb5bd;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Input section styling */
    .input-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e9ecef;
    }
    
    .mode-selector {
        margin-bottom: 2rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
    
    /* Button styling */
    .stButton > button {
        background: #6c757d;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background: #5a6268;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: #f8f9fa;
        border-radius: 12px;
        border: 1px solid #e9ecef;
    }
    
    .footer h4 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .footer p {
        color: #6c757d;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    init_session_state()
    
    # Check authentication
    is_authenticated = check_auth_status()
    if not is_authenticated:
        show_auth_page()
        return
    
    # Custom header with logo
    st.markdown("""
    <div class="header-container">
        <div class="logo-section">
            <div class="logo-icon">🎯</div>
            <div>
                <h1 class="logo-text">AI Interview Coach</h1>
                <p style="color: #6c757d; margin: 0; font-size: 0.85rem; font-weight: 400;">Smart Analysis • AI-Powered</p>
            </div>
        </div>
        <div>
            <button class="logout-btn" onclick="window.location.href='?logout=true'">Logout</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    st.markdown('<h1 class="main-header">✨ Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # Mode selection - Simplified to only Interview Simulation
    st.markdown('<div class="mode-selector">', unsafe_allow_html=True)
    analysis_mode = "Interview Simulation"  # Fixed mode
    st.info("🎭 **Interview Simulation Mode** - Generate questions and evaluate responses")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interview Simulation Mode - Simplified
    st.markdown("### 🎭 Interview Simulation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        question_type = st.selectbox(
            "Question Type:",
            ["hr_behavioral", "technical"],
            help="Select the type of question"
        )
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty Level:",
            ["easy", "medium", "hard"],
            help="Choose the difficulty level"
        )
    
    # Generate question for simulation
    if st.button("🎯 Generate Question", type="primary"):
        with st.spinner("Generating question..."):
            try:
                # Use LangChain processor
                langchain_processor = LangChainInterviewProcessor(use_openai=True)
                question_result = langchain_processor.generate_question_langchain(
                    round_type=question_type,
                    context=f"Software Engineer with {difficulty} level experience"
                )
                
                # Create a simple question object for compatibility
                class SimpleQuestion:
                    def __init__(self, question_text, question_type, difficulty):
                        self.question_text = question_text
                        self.question_type = type('obj', (object,), {'value': question_type})
                        self.difficulty = type('obj', (object,), {'value': difficulty})
                
                question = SimpleQuestion(
                    question_text=question_result["question"],
                    question_type=question_type,
                    difficulty=difficulty
                )
                
                st.session_state['current_question'] = question
                st.session_state['langchain_processor'] = langchain_processor
            except Exception as e:
                st.error(f"Error generating question: {str(e)}")
                # Fallback to simple processor
                try:
                    llm_processor = SimpleLLMProcessor(use_openai=False)
                    question = llm_processor.generate_question(
                        QuestionType(question_type),
                        "Software Engineer",
                        DifficultyLevel(difficulty)
                    )
                    st.session_state['current_question'] = question
                    st.session_state['llm_processor'] = llm_processor
                except Exception as e2:
                    st.error(f"Fallback also failed: {str(e2)}")
    
    # Display current question
    if 'current_question' in st.session_state:
        question = st.session_state['current_question']
        st.markdown(f"**Question:** {question.question_text}")
        st.markdown(f"**Type:** {question.question_type.value}")
        st.markdown(f"**Difficulty:** {question.difficulty.value}")
        system_question = question.question_text
    
    # Response input section - Always show for Interview Simulation
    st.markdown("### 💬 Response Input")
    
    # Simple text area for user input
    user_response = st.text_area(
        "Enter candidate response:",
        value="",
        height=100,
        placeholder="Type or paste the candidate's response here...",
        help="Enter the candidate's response to analyze"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close input section
    
    # Process button - Simplified for Interview Simulation only
    if st.button("🔍 Analyze Response", type="primary"):
        if not user_response.strip():
            st.error("Please enter a response to analyze.")
        else:
            with st.spinner("🤖 Analyzing response..."):
                try:
                    # First run NLP preprocessing
                    nlp_processor = NLPProcessor()
                    cleaned_data = nlp_processor.preprocess_text(user_response)
                    features = nlp_processor.extract_features(user_response, cleaned_data)
                    
                    # Use direct OpenAI evaluation for consistent high-quality scoring
                    try:
                        from notebooks.LLMs_test import evaluate_answer
                        
                        # Use the main evaluate_answer function which handles OpenAI properly
                        evaluation_result = evaluate_answer(system_question, user_response)
                        
                        # Display results using LangChain format for consistency
                        display_langchain_evaluation(evaluation_result, system_question)
                        
                        # Show session summary
                        st.markdown("### 📊 Session Summary")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Questions Asked", "1")
                        with col2:
                            eval_data = evaluation_result.get("evaluation", {})
                            overall_score = (eval_data.get("relevance", 0) + eval_data.get("completeness", 0) + eval_data.get("clarity", 0)) / 3 * 100
                            st.metric("Average Score", f"{overall_score:.1f}/100")
                        with col3:
                            st.metric("Current Difficulty", "Medium")
                        
                    except Exception as e:
                        st.error(f"OpenAI evaluation failed: {str(e)}")
                        import traceback
                        st.error(f"Full error: {traceback.format_exc()}")
                        # Fallback to simple processor
                        if 'llm_processor' in st.session_state:
                            llm_processor = st.session_state['llm_processor']
                        else:
                            llm_processor = SimpleLLMProcessor(use_openai=False)
                            st.session_state['llm_processor'] = llm_processor
                        
                        evaluation = llm_processor.evaluate_answer(
                            question=system_question,
                            candidate_answer=user_response,
                            cleaned_answer=' '.join(cleaned_data['no_stopwords'])
                        )
                        
                        # Display results
                        display_llm_evaluation(evaluation, system_question)
                        
                        # Show session summary
                        session_summary = llm_processor.get_session_summary()
                        display_session_summary(session_summary)
                        
                        # Adjust difficulty for next question
                        llm_processor.adjust_difficulty(evaluation.overall_score)
                        
                except Exception as e:
                    st.error(f"Error analyzing response: {str(e)}")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h4>🤖 AI-Powered Job Interview Coach</h4>
        <p>Powered by Advanced NLP & LLM Technology | Step 2: Dynamic Question Generation & Answer Evaluation</p>
        <p>Built with ❤️ using Streamlit, Transformers, and LangChain</p>
    </div>
    """, unsafe_allow_html=True)


def display_session_summary(session_summary):
    """Display interview session summary"""
    st.markdown("### 📊 Session Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Questions Asked",
            value=session_summary["total_questions"]
        )
    
    with col2:
        st.metric(
            label="Average Score",
            value=f"{session_summary['average_score']:.1f}/100"
        )
    
    with col3:
        st.metric(
            label="Current Difficulty",
            value=session_summary["current_difficulty"].title()
        )

def display_llm_evaluation(evaluation, question):
    """Display simplified LLM evaluation results"""
    st.markdown('<h2 class="section-header">🤖 LLM Evaluation Results</h2>', unsafe_allow_html=True)
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Overall Score",
            value=f"{evaluation.overall_score:.1f}/100",
            delta=f"{evaluation.overall_score - 50:.1f}",
            help="Overall performance score"
        )
    
    with col2:
        st.metric(
            label="Relevance",
            value=f"{evaluation.relevance_score:.1f}/100",
            help="How well the answer addresses the question"
        )
    
    with col3:
        st.metric(
            label="Clarity",
            value=f"{evaluation.clarity_score:.1f}/100",
            help="How clear and well-structured the answer is"
        )
    
    with col4:
        st.metric(
            label="Correctness",
            value=f"{evaluation.correctness_score:.1f}/100",
            help="Technical accuracy and correctness"
        )
    
    # Feedback
    st.markdown("#### 💬 Feedback")
    st.info(evaluation.feedback)
    
    # Suggestions
    st.markdown("#### 💡 Suggestions")
    for i, suggestion in enumerate(evaluation.suggestions, 1):
        st.markdown(f"{i}. {suggestion}")


def convert_langchain_evaluation(evaluation_result):
    """Convert LangChain evaluation result to expected format"""
    eval_data = evaluation_result.get("evaluation", {})
    
    # Create a simple object with the expected attributes
    class EvaluationResult:
        def __init__(self, eval_data):
            self.overall_score = (eval_data.get("relevance", 0) + 
                                eval_data.get("completeness", 0) + 
                                eval_data.get("clarity", 0)) / 3 * 100
            self.relevance_score = eval_data.get("relevance", 0) * 100
            self.clarity_score = eval_data.get("clarity", 0) * 100
            self.correctness_score = eval_data.get("completeness", 0) * 100
            self.feedback = eval_data.get("feedback", "No feedback available")
            self.suggestions = eval_data.get("suggestions", "No suggestions available")
            if isinstance(self.suggestions, str):
                self.suggestions = [self.suggestions]
    
    return EvaluationResult(eval_data)


def display_langchain_evaluation(evaluation_result, question):
    """Display LangChain evaluation results"""
    st.markdown('<h2 class="section-header">🤖 LangChain Evaluation Results</h2>', unsafe_allow_html=True)
    
    eval_data = evaluation_result.get("evaluation", {})
    similarity = evaluation_result.get("similarity", 0)
    matched_canonical = evaluation_result.get("matched_canonical", {})
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Calculate overall score with minimum threshold for very poor answers
        relevance = eval_data.get("relevance", 0)
        completeness = eval_data.get("completeness", 0)
        clarity = eval_data.get("clarity", 0)
        
        # Apply minimum score logic for very poor answers
        raw_score = (relevance + completeness + clarity) / 3 * 100
        
        # If all scores are very low (indicating a very poor answer), cap the overall score
        if relevance < 0.1 and completeness < 0.1 and clarity < 0.2:
            overall_score = min(raw_score, 15.0)  # Cap at 15 for very poor answers
        else:
            overall_score = raw_score
            
        st.metric(
            label="Overall Score",
            value=f"{overall_score:.1f}/100",
            delta=f"{overall_score - 50:.1f}",
            help="Overall performance score"
        )
    
    with col2:
        relevance_score = eval_data.get("relevance", 0) * 100
        st.metric(
            label="Relevance",
            value=f"{relevance_score:.1f}/100",
            help="How well the answer addresses the question"
        )
    
    with col3:
        clarity_score = eval_data.get("clarity", 0) * 100
        st.metric(
            label="Clarity",
            value=f"{clarity_score:.1f}/100",
            help="How clear and well-structured the answer is"
        )
    
    with col4:
        completeness_score = eval_data.get("completeness", 0) * 100
        st.metric(
            label="Completeness",
            value=f"{completeness_score:.1f}/100",
            help="How complete and thorough the answer is"
        )
    
    # Additional metrics
    col5, col6 = st.columns(2)
    
    with col5:
        st.metric(
            label="Similarity Score",
            value=f"{similarity:.3f}",
            help="Similarity to canonical answer (0-1)"
        )
    
    with col6:
        st.metric(
            label="Matched Canonical ID",
            value=matched_canonical.get("id", "N/A"),
            help="ID of the best matching canonical answer"
        )
    
    # Feedback
    st.markdown("#### 💬 Feedback")
    feedback = eval_data.get("feedback", "No feedback available")
    st.info(feedback)
    
    # Suggestions
    st.markdown("#### 💡 Suggestions")
    suggestions = eval_data.get("suggestions", "No suggestions available")
    if isinstance(suggestions, str):
        suggestions = [suggestions]
    for i, suggestion in enumerate(suggestions, 1):
        st.markdown(f"{i}. {suggestion}")
    
    # Show matched canonical answer for reference
    if matched_canonical.get("answer"):
        st.markdown("#### 📚 Matched Canonical Answer (Reference)")
        st.text_area(
            "Reference Answer:",
            value=matched_canonical["answer"],
            height=100,
            disabled=True,
            help="This is the canonical answer that was most similar to the candidate's response"
        )


def display_langchain_session_summary(session_summary):
    """Display LangChain session summary"""
    st.markdown("### 📊 LangChain Session Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Messages",
            value=session_summary.get("total_messages", 0)
        )
    
    with col2:
        st.metric(
            label="Conversation Rounds",
            value=session_summary.get("conversation_rounds", 0)
        )
    
    with col3:
        st.metric(
            label="Memory Status",
            value="✅ Active" if session_summary.get("memory_available", False) else "❌ Inactive"
        )

if __name__ == "__main__":
    main()
