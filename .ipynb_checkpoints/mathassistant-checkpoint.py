from langchain_ibm import ChatWatsonx
from langchain.agents import AgentType
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool
from langchain_core.tools import tool
from typing import Dict, Union
from langgraph.prebuilt import create_react_agent
from typing import List
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.agents import initialize_agent
import re



# A LLM of your choosing
openai_llm = ChatOpenAI(
    model="gpt-4.1-nano",
    api_key = "your openai api key here",
)

watsonx_llm = ChatWatsonx(
    model_id="ibm/granite-3-2-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id="your project id associated with the API key",
    api_key="your watsonx.ai api key here",
)

# response = llm.invoke("What is tool calling in LangChain?")
# print("\nResponse content", response.content)

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




print("@tool Decorator Approach:")





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


@tool
def subtract_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and performs subtraction sequentially, starting with the first number.

    This function is designed to handle input in string format, where numbers may be separated by spaces, 
    commas, or other delimiters. It parses the input string, extracts numeric values, and calculates 
    the result by subtracting each subsequent number from the first. inputs[0]-inputs[1]-inputs[2]

    Parameters:
    - inputs (str): 
      A string containing numbers to subtract. The string can include spaces, commas, or other 
      delimiters between the numbers.

    Returns:
    - dict: 
      A dictionary containing the key "result" with the calculated difference as its value. 
      If no valid numbers are found in the input string, the result defaults to 0.

    Example Usage:
    - Input: "100, 20, 10"
    - Output: {"result": 70}
        Limitations:
    - The function does not handle cases where numbers are formatted with decimals or other non-integer representations.
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]

    # If no numbers are found, return 0
    if not numbers:
        return {"result": 0}

    # Start with the first number
    result = numbers[0]

    # Subtract all subsequent numbers
    for num in numbers[1:]:
        result -= num

    return {"result": result}


# Multiplication Tool
@tool
def multiply_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and calculates their product.

    Parameters:
    - inputs (str): A string containing numbers separated by spaces, commas, or other delimiters.

    Returns:
    - dict: A dictionary with the key "result" containing the product of the numbers.

    Example Input:
    "2, 3, 4"

    Example Output:
    {"result": 24}

    Notes:
    - If no numbers are found, the result defaults to 1 (neutral element for multiplication).
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]
    print(numbers)

    # If no numbers are found, return 1
    if not numbers:
        return {"result": 1}

    # Calculate the product of the numbers
    result = 1
    for num in numbers:
        result *= num
        print(num)

    return {"result": result}


# Division Tool
@tool
def divide_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and calculates the result of dividing the first number 
    by the subsequent numbers in sequence.

    Parameters:
    - inputs (str): A string containing numbers separated by spaces, commas, or other delimiters.

    Returns:
    - dict: A dictionary with the key "result" containing the quotient.

    Example Input:
    "100, 5, 2"

    Example Output:
    {"result": 10.0}

    Notes:
    - If no numbers are found, the result defaults to 0.
    - Division by zero will raise an error.
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]


    # If no numbers are found, return 0
    if not numbers:
        return {"result": 0}

    # Calculate the result of dividing the first number by subsequent numbers
    result = numbers[0]
    for num in numbers[1:]:
        result /= num

    return {"result": result}

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for factual information about a topic.
    
    Parameters:
    - query (str): The topic or question to search for on Wikipedia
    
    Returns:
    - str: A summary of relevant information from Wikipedia
    """
    wiki = WikipediaAPIWrapper()
    return wiki.run(query)


# # Testing multiply_tool
# multiply_test_input = "2, 3, and four "
# multiply_result = multiply_numbers.invoke(multiply_test_input)
# print("--- Testing MultiplyTool ---")
# print(f"Input: {multiply_test_input}")
# print(f"Output: {multiply_result}")

# # Testing divide_tool
# divide_test_input = "100, 5, two"
# divide_result = divide_numbers.invoke(divide_test_input)
# print("--- Testing DivideTool ---")
# print(f"Input: {divide_test_input}")
# print(f"Output: {divide_result}")

tools=[add_numbers, subtract_numbers, multiply_numbers, divide_numbers, search_wikipedia]

math_agent = create_react_agent(
    model=llm_ai,
    tools=tools,

    prompt="You are a helpful mathematical assistant that can perform various operations. Use the tools precisely and explain your reasoning clearly."
)

# response=math_agent.invoke({
#     "messages": [("human", "What is 25 divided by 4?")]
# })

# final_answer=response["messages"][-1].content
# print(final_answer)


# response2=math_agent.invoke({
#     "messages" : [("human",  "Subtract 100, 20, and 10.")]
# })

# final_answer_2 = response2["messages"][-2].content
# print(final_answer_2)


# print("\n----Testing multiply tool----")
# response3=math_agent.invoke({
#     "messages" : [("human", "Multiply 2, 3, and four.")]
# })

# print("Agent Response:", response3["messages"][-1].content)

# print("\n--- Testing divide tool---")
# response = math_agent.invoke({
#     "messages": [("human", "Divide 100 by 5 and then by 2.")]
# })
# print("Agent Response:", response["messages"][-1].content)

# Test Cases
test_cases = [
    {
        "query": "Subtract 100, 20, and 10.",
        "expected": {"result": 70},
        "description": "Testing subtraction tool with sequential subtraction."
    },
    {
        "query": "Multiply 2, 3, and 4.",
        "expected": {"result": 24},
        "description": "Testing multiplication tool for a list of numbers."
    },
    {
        "query": "Divide 100 by 5 and then by 2.",
        "expected": {"result": 10.0},
        "description": "Testing division tool with sequential division."
    },
    {
        "query": "Subtract 50 from 20.",
        "expected": {"result": -30},
        "description": "Testing subtraction tool with negative results."
    }

]

correct_tasks = []
# Corrected test execution
for index, test in enumerate(test_cases, start=1):
    query = test["query"]
    expected_result = test["expected"]["result"]  # Extract just the value
    
    print(f"\n--- Test Case {index}: {test['description']} ---")
    print(f"Query: {query}")
    
    # Properly format the input
    response = math_agent.invoke({"messages": [("human", query)]})
    
    # Find the tool message in the response
    tool_message = None
    for msg in response["messages"]:
        if hasattr(msg, 'name') and msg.name in ['add_numbers', 'new_subtract_numbers', 'multiply_numbers', 'divide_numbers']:
            tool_message = msg
            break

    if tool_message:
        # Parse the tool result from its content
        import json
        tool_result = json.loads(tool_message.content)["result"]
        print(f"Tool Result: {tool_result}")
        print(f"Expected Result: {expected_result}")
        
        if tool_result == expected_result:
            print(f"✅ Test Passed: {test['description']}")
            correct_tasks.append(test["description"])
        else:
            print(f"❌ Test Failed: {test['description']}")
    else:
        print("❌ No tool was called by the agent")

print("\nCorrectly passed tests:", correct_tasks)
    
print()
print()

query = "What is the population of Canada? Multiply it by 0.75"

response = math_agent.invoke({"messages": [("human", query)]})

print("\nMessage sequence:")
for i, msg in enumerate(response["messages"]):
    print(f"\n--- Message {i+1} ---")
    print(f"Type: {type(msg).__name__}")
    if hasattr(msg, 'content'):
        print(f"Content: {msg.content}")
    if hasattr(msg, 'name'):
        print(f"Name: {msg.name}")
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print(f"Tool calls: {msg.tool_calls}")
