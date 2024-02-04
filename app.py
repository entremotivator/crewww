import streamlit as st

# Titles and Headers
st.title("LangChain Streamlit App")
st.header("Setting up LangChain Environment")

# Install requirements
st.subheader("1. Install Requirements")
st.code("pip install Jinja2>=3.1.2 click>=7.0 duckduckgo-search")

# Import Libraries
st.subheader("2. Import Libraries")
st.code("""
from crewai import Agent, Task, Crew, Process
import os
from langchain.tools import DuckDuckGoSearchRun
from langchain.llms import Ollama
""")

# Dynamic Agent and Task Creation
st.subheader("3. Create Agents and Tasks")

agents = []
tasks = []

num_agents = st.number_input("Number of Agents", min_value=1, value=2, step=1)
num_tasks = st.number_input("Number of Tasks", min_value=1, value=3, step=1)

# Choose LLM and Tools for the entire crew
st.subheader("Choose LLM and Tools for the Crew")
selected_llm_crew = st.selectbox("Select LLM for Crew", ["ollama_openhermes", "ollama_solar"])
selected_tool_crew = st.selectbox("Select Tool for Crew", ["DuckDuckGoSearchRun"])

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
    tools=[{selected_tool_crew}, {selected_tool_agent}],
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
st.subheader("4. Create Crew and Process")
st.code(f"""
crew = Crew(
    agents={[f"agent{j + 1}" for j in range(num_agents)]},
    tasks={[f"task{j + 1}" for j in range(num_tasks)]},
    verbose=2,
    process=Process.sequential
)
result = crew.kickoff()
""")

# Output
st.subheader("5. Output")
st.write("Output:", result)
