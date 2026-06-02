from langchain_ibm import ChatWatsonx
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain_core.tools import tool
from typing import Dict, Union
from langgraph.prebuilt import create_react_agent
from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
import re


llm = ChatWatsonx(
    model_id="ibm/granite-4-h-small",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="#",
)

llm_ai=ChatOpenAI(model="gpt-4.1-nano")

# response = llm.invoke("What is tool calling in LangChain?")
# print("\nResponse content", response.content)
def add_numbers(inputs:str) -> dict:
    """
    Adds a list of numbers provided in the input dictionary or extracts numbers from a string.

    Parameters:
    - inputs (str): 
    string, it should contain numbers that can be extracted and summed.

    Returns:
    - dict: A dictionary with a single key "result" containing the sum of the numbers.

    Example Input (Dictionary):
    {"numbers": [10, 20, 30]}

    Example Input (String):
    "Add the numbers 10, 20, and 30."


    Example Output:
    {"result": 60}
    """
    numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    result = sum(numbers)
    return {"result": result}


add_numbers("1 2")


add_tool=Tool(
        name="AddTool",
        func=add_numbers,
        description="Adds a list of numbers and returns the result.")


# using the @tool operator
@tool
def add_numbers(inputs:str) -> dict:
    """
    Adds a list of numbers provided in the input string.
    Parameters:
    - inputs (str): 
    string, it should contain numbers that can be extracted and summed.
    Returns:
    - dict: A dictionary with a single key "result" containing the sum of the numbers.
    Example Input:
    "Add the numbers 10, 20, and 30."
    Example Output:
    {"result": 60}
    """
    # Use regular expressions to extract all numbers from the input
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    # numbers = [int(x) for x in inputs.replace(",", "").split() if x.isdigit()]
    
    result = sum(numbers)
    return {"result": result}

# print("Name: \n" , add_numbers.name) 
# print("Description: \n" , add_numbers.description)
# print("Args: \n", add_numbers.args)

# test_input = "10 20 30 a b 40"
# print(add_numbers.invoke(test_input))


print("@tool Decorator Approach:")


# print(f"Has Schema: {hasattr(add_numbers, 'args_schema')}")
# print(f"Args Schema Info: {add_numbers.args}")


@tool
def add_numbers_with_options(numbers: List[float], absolute: bool = False) -> float:
    """
    Adds a list of numbers provided as input.

    Parameters:
    - numbers (List[float]): A list of numbers to be summed.
    - absolute (bool): If True, use the absolute values of the numbers before summing.

    Returns:
    - float: The total sum of the numbers.
    """
    if absolute:
        numbers = [abs(n) for n in numbers]
    return sum(numbers)

# print(f"Has schema info: {add_numbers.args}")
# print(f"Has schema info: {add_numbers_with_options.args}")

@tool
def sum_numbers_with_complex_output(inputs:str) -> Dict[str, Union[float, str]]:
    """ 
    Extracts and sums all integers and decimal numbers from the input string.

    Parameters: 
    - inputs (str) : string that may contain numerical values

    Returns:
    - dict: A dictionary with the key "result". If numbers are found, the value is their sum (float). 
            If no numbers are found or an error occurs, the value is a corresponding message (str).

    Example Input:
    "Add 10, 20.5, and -3."

    Example Output:
    {"result": 27.5}

    """
    matches = re.findall(r'-?\d+(?:\.\d+)?', inputs)
    if not matches:
        return {"result": "No numbers found in input."}
    try:
        numbers = [float(num) for num in matches]
        total = sum(numbers)
        return {"result": total}
    except Exception as e:
        return {"result": f"Error during summation: {str(e)}"}

@tool 
def sum_numbers_from_text(inputs:str) -> float:
    """
    Adds a list of numbers provided in the input string.
    
    Args:
        text: A string containing numbers that should be extracted and summed.
        
    Returns:
        The sum of all numbers found in the input.
    """
    # Use regular expressions to extract all numbers from the input
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    result = sum(numbers)
    return result

# agent = initialize_agent([add_tool], llm, agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True)

# response = agent.run("In 2023, the US GDP was approximately $27.72 trillion, while Canada's was around $2.14 trillion and Mexico's was about $1.79 trillion what is the total.")

# print(response)

# agent2 = initialize_agent(
#     [sum_numbers_from_text], 
#     llm, 
#     agent="structured-chat-zero-shot-react-description", 
#     verbose=True, 
#     handle_parsing_error=True)

# response=agent2.invoke({"input": "Add 10, 20 30, and -30 absolute value "})
# print(response)

# agent_3 = initialize_agent([sum_numbers_with_complex_output], llm_ai, agent="openai-functions", verbose=True, handle_parsing_errors=True)
# response = agent_3.invoke({"input": "Add 10, 20 and 30"})
# print(response)

# agent_openai=initialize_agent(
#     [add_numbers_with_options],
#     llm_ai,
#     agent="openai-functions",
#     verbose=True,
#     handling_parsing_error=True
# )

# response = agent_openai.invoke({
#     "input": "Add -10, -20, and -30 using absolute values."
# })
# print(response)

agent_exec=create_react_agent(model=llm_ai, tools=[sum_numbers_from_text])
msgs = agent_exec.invoke({"messages": [("human", "Add the numbers -10, -20, -30")]})
print(msgs["messages"][-1].content)

