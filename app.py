import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain.llms import Ollama
from langchain.tools import DuckDuckGoSearchRun

# Install required libraries
# Run these commands in the terminal
# pip install crewai
# pip install langchain
# pip install duckduckgo-search
# ollama pull openhermes

# Initialize Ollama and DuckDuckGoSearchRun
ollama_llm = Ollama(model="openhermes")
search_tool = DuckDuckGoSearchRun()

# Main Streamlit app
def main():
    st.title("Agent Building Platform")

    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Add Agent", "Edit Agent"])

    if page == "Home":
        home_page()
    elif page == "Add Agent":
        add_agent_page()
    elif page == "Edit Agent":
        edit_agent_page()

# Home page with agent creation and kickoff
def home_page():
    st.header("Home - Create and Kickoff Agents")

    # Dynamic Agent and Task Creation
    num_agents = st.number_input("Number of Agents", min_value=1, value=2, step=1)
    num_tasks = st.number_input("Number of Tasks", min_value=1, value=3, step=1)

    # Choose LLM and Tools for the entire crew
    st.subheader("Choose LLM and Tools for the Crew")
    selected_llm_crew = st.selectbox("Select LLM for Crew", ["ollama_openhermes", "ollama_solar"])
    selected_tool_crew = st.selectbox("Select Tool for Crew", ["DuckDuckGoSearchRun"])

    agents = []
    tasks = []

    # Loop to create agents
    for i in range(num_agents):
        st.write(f"Agent {i + 1}")
        role = st.text_input(f"Role {i + 1}", f"Agent{i + 1}")
        goal = st.text_area(f"Goal {i + 1}", f"Agent{i + 1} goal")
        backstory = st.text_area(f"Backstory {i + 1}", f"You are an AI {role}")
        verbose = st.checkbox(f"Verbose {i + 1}", True)
        allow_delegation = st.checkbox(f"Allow Delegation {i + 1}", False)

        # Choose LLM and Tools for individual agents
        st.subheader(f"Choose LLM and Tools for Agent {i + 1}")
        selected_llm_agent = st.selectbox(f"Select LLM for Agent {i + 1}", ["ollama_openhermes", "ollama_solar"])
        selected_tool_agent = st.selectbox(f"Select Tool for Agent {i + 1}", ["DuckDuckGoSearchRun"])

        agent_code = f"""
agent{i + 1} = Agent(
    role='{role}',
    goal='{goal}',
    backstory='{backstory}',
    tools=['{selected_tool_crew}', '{selected_tool_agent}'],
    verbose={verbose},
    llm='{selected_llm_crew}' if i == 0 else '{selected_llm_agent}',
    allow_delegation={allow_delegation}
)
"""
        agents.append(agent_code)

    for i in range(num_tasks):
        st.write(f"Task {i + 1}")
        description = st.text_input(f"Description {i + 1}", f"Task{i + 1} description")
        assigned_agent = st.selectbox(f"Assign to Agent {i + 1}", [f"agent{j + 1}" for j in range(num_agents)])

        task_code = f"""
task{i + 1} = Task(description='{description}', agent={assigned_agent})
"""
        tasks.append(task_code)

    # Crew and Process
    st.subheader("Create Crew and Process")
    crew_code = f"""
crew = Crew(
    agents={[f"agent{j + 1}" for j in range(num_agents)]},
    tasks={[f"task{j + 1}" for j in range(num_tasks)]},
    verbose=2,
    process=Process.sequential
)
result = crew.kickoff()
"""
    st.code(crew_code)

    # Output
    st.subheader("Output")
    st.write("Output:", result)

# Add agent page
def add_agent_page():
    st.header("Add New Agent")

    role = st.text_input("Role", "New Agent")
    goal = st.text_area("Goal", "New Agent goal")
    backstory = st.text_area("Backstory", "You are an AI")
    verbose = st.checkbox("Verbose", True)
    allow_delegation = st.checkbox("Allow Delegation", False)

    # Choose LLM and Tools for the new agent
    st.subheader("Choose LLM and Tools for the New Agent")
    selected_llm_agent = st.selectbox("Select LLM for New Agent", ["ollama_openhermes", "ollama_solar"])
    selected_tool_agent = st.selectbox("Select Tool for New Agent", ["DuckDuckGoSearchRun"])

    new_agent_code = f"""
new_agent = Agent(
    role='{role}',
    goal='{goal}',
    backstory='{backstory}',
    tools=['{selected_tool_agent}'],
    verbose={verbose},
    llm='{selected_llm_agent}',
    allow_delegation={allow_delegation}
)
"""
    st.code(new_agent_code)

# Edit agent page
def edit_agent_page():
    st.header("Edit Agent")

    agent_to_edit = st.selectbox("Select Agent to Edit", ["Researcher", "Technical Content Creator", "New Agent"])

    if agent_to_edit == "Researcher":
        st.write("Editing Researcher Agent")
        researcher.role = st.text_input("Role", researcher.role)
        researcher.goal = st.text_area("Goal", researcher.goal)
        researcher.backstory = st.text_area("Backstory", researcher.backstory)
        researcher.verbose = st.checkbox("Verbose", researcher.verbose)
        researcher.allow_delegation = st.checkbox("Allow Delegation", researcher.allow_delegation)

    elif agent_to_edit == "Technical Content Creator":
        st.write("Editing Technical Content Creator Agent")
        writer.role = st.text_input("Role", writer.role)
        writer.goal = st.text_area("Goal", writer.goal)
        writer.backstory = st.text_area("Backstory", writer.backstory)
        writer.verbose = st.checkbox("Verbose", writer.verbose)
        writer.allow_delegation = st.checkbox("Allow Delegation", writer.allow_delegation)

    elif agent_to_edit == "New Agent":
        st.write("Editing New Agent")

# Run the Streamlit app
if __name__ == "__main__":
    main()
