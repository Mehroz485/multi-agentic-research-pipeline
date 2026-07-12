#streamlit app
import streamlit as st
import os


from pipeline import run_research_pipeline


st.set_page_config(
    page_title="AI Research Agent Pipeline",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    .agent-card {
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


st.title("⚡ Autonomous Multi-Agent Research System")
st.markdown("Enter a topic below. A team of specialized agents will search the web, scrape deep content, draft a structured report, and critically evaluate the quality.")

st.divider()


topic = st.text_input(
    "Research Topic / Query",
    placeholder="e.g., Impact of Quantum Computing on Modern Cryptography...",
    help="Provide a clear, detailed topic for the agent swarm to investigate."
)


if st.button("🚀 Launch Agent Swarm", type="primary", use_container_width=True):
    if not topic.strip():
        st.error("⚠️ Topic cannot be empty. Please enter a valid research topic.")
    else:
        
        status_container = st.container()
        
        with status_container:
            st.subheader("⚙️ Live Agent Execution Stream")
            
            
            with st.status("🔍 Step 1: Deploying Search Agent...", expanded=True) as status_search:
                st.write("Configuring Tavily/Search environment variables...")
                
                st.write("Scanning global indexes for relevant matching documents and source links...")
                
                
                try:
                    with st.spinner("Agents are thinking and collaborating..."):
                        pipeline_data = run_research_pipeline(topic.strip())
                    status_search.update(label="✅ Step 1: Search Complete! Extracted source URLs.", state="complete", expanded=False)
                except Exception as e:
                    status_search.update(label="❌ Pipeline Failed", state="error")
                    st.error(f"An error occurred during execution: {str(e)}")
                    st.stop()

            
            with st.status("📖 Step 2: Deploying Reader Agent (Web Scraper)...", expanded=False) as status_reader:
                st.write("Parsing deep payload strings extracted from step 1...")
                st.write("Bypassing document layout trees to retrieve core factual data panels...")
                st.code(pipeline_data.get("scraped_result", ""), language="text")
                status_reader.update(label="✅ Step 2: Content Scraped Successfully.", state="complete")

            
            with st.status("✍️ Step 3: Deploying Writer Agent...", expanded=False) as status_writer:
                st.write("Synthesizing raw data and formatting Markdown trees...")
                status_writer.update(label="✅ Step 3: Report Drafted.", state="complete")

            
            with st.status("⚖️ Step 4: Deploying Critic Agent...", expanded=False) as status_critic:
                st.write("Evaluating analytical alignment, structural gaps, and source references...")
                status_critic.update(label="✅ Step 4: Quality Review Finalized.", state="complete")

        st.success("🎉 Research Pipeline execution finished successfully!")
        st.divider()

        
        report_tab, evaluation_tab, logs_tab = st.tabs([
            "📄 Generated Research Report", 
            "📊 Critic Evaluation & Quality", 
            "👁️ Raw Agent Telemetry Logs"
        ])

        with report_tab:
            st.subheader("Final Research Output")
            # Render the beautiful markdown output directly
            st.markdown(pipeline_data.get("report", "No report generated."))
            
            
            st.divider()
            st.download_button(
                label="📥 Download Report as Markdown (.md)",
                data=pipeline_data.get("report", ""),
                file_name=f"research_{topic.lower().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with evaluation_tab:
            st.subheader("Critic Performance Matrix")
            
            
            feedback_text = pipeline_data.get("feedback", "")
            score = "N/A"
            for word in feedback_text.split():
                if "/10" in word:
                    score = word
                    break
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric(label="Quality Score Assessment", value=score)
            with col2:
                st.markdown("### Feedback Overview")
                st.write(feedback_text)

        with logs_tab:
            st.subheader("Telemetry & State Payloads")
            
            st.markdown("#### **Search Agent Output Snippet**")
            st.info(pipeline_data.get("search_results", "Empty"))
            
            st.markdown("#### **Reader Agent Deep Content**")
            st.text_area("Scraped Text Data", value=pipeline_data.get("scraped_result", ""), height=200, disabled=True)
