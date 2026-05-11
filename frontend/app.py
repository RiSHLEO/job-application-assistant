import streamlit as st
import httpx
import json

# API URL — points to your FastAPI backend
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Job Application Assistant", page_icon="💼")
st.title("💼 Job Application Assistant")
st.write("Upload your CV and paste a job description to get AI-powered analysis.")

# ============ INPUT SECTION ============

col1, col2 = st.columns(2)

with col1:
    cv_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

with col2:
    st.write("**API Status**")
    try:
        response = httpx.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("API Error")
    except:
        st.error("❌ API Offline — make sure backend is running")

job_description = st.text_area(
    "Paste the job description",
    height=200,
    placeholder="Paste the full job description here..."
)

if st.button("Analyse Application", type="primary"):
    
    if not cv_file:
        st.warning("Please upload your CV")
    elif not job_description.strip():
        st.warning("Please paste a job description")
    elif len(job_description.strip()) < 50:
        st.warning("Job description too short — please paste the full description")
    else:
        with st.spinner("Analysing your application..."):
            try:
                response = httpx.post(
                    f"{API_URL}/analyse",
                    files={"cv": (cv_file.name, cv_file.getvalue(), "application/pdf")},
                    data={"job_description": job_description},
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Match Score
                    st.subheader("📊 Match Analysis")
                    score = result["match_score"]
                    
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        color = "green" if score >= 70 else "orange" if score >= 50 else "red"
                        st.markdown(f"<h1 style='color:{color}'>{score}%</h1>",
                                   unsafe_allow_html=True)
                    with col2:
                        st.write(result["match_summary"])
                    
                    st.progress(score / 100)
                    
                    # Key Strengths
                    st.subheader("✅ Key Strengths")
                    for strength in result["key_strengths"]:
                        st.write(f"• {strength}")
                    
                    # Skill Gaps
                    st.subheader("⚠️ Skill Gaps")
                    for gap in result["skill_gaps"]:
                        importance_color = {
                            "High": "🔴",
                            "Medium": "🟡",
                            "Low": "🟢"
                        }.get(gap["importance"], "⚪")
                        
                        with st.expander(f"{importance_color} {gap['skill']} — {gap['importance']} priority"):
                            st.write(f"**How to address:** {gap['how_to_address']}")
                    
                    # CV Improvements
                    st.subheader("📝 CV Improvements")
                    for improvement in result["cv_improvements"]:
                        with st.expander(f"📄 {improvement['section_name']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Original:**")
                                st.write(improvement["original"])
                            with col2:
                                st.write("**Improved:**")
                                st.write(improvement["rewritten"])
                    
                    # Cover Letter
                    st.subheader("📧 Cover Letter")
                    st.text_area("Copy this cover letter",
                                result["cover_letter"],
                                height=300)
                    
                    # Download
                    st.download_button(
                        label="Download Full Analysis (JSON)",
                        data=json.dumps(result, indent=2),
                        file_name="application_analysis.json",
                        mime="application/json"
                    )
                    
                else:
                    error = response.json()
                    st.error(f"Error: {error.get('detail', 'Unknown error')}")
                    
            except httpx.TimeoutException:
                st.error("Request timed out — please try again.")
            except httpx.ConnectError:
                st.error("Cannot connect to API — make sure the backend is running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")