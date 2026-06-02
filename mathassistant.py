from langchain_ibm import ChatWatsonx
from langchain_agents import AgentType
import re


llm = ChatWatsonx(
    model_id="ibm/granite-4-h-small",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="skills-network",
)

response = llm.invoke("What is tool calling in LangChain?")
print("\nResponse content", response.content)