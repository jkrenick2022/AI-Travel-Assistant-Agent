from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_community.tools import DuckDuckGoSearchResults
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Load in environment variables
load_dotenv()

# Initialize instance of our LLM
llm = ChatOpenAI(
    model = "o4-mini",
    temperature = 1.0 # MUST use 1.0 when using o4-mini model
)

# Setup search tool that will allow our Agent to use the internet
tool_search = DuckDuckGoSearchResults()

# Define the shared state that will be passed throughout the graph
class State(TypedDict):
    messages: Annotated[list, add_messages]     # Chat history (all messages both user and AI are stored here)
    valid_input: bool                           # Used for routing - tells if the initial query is valid input

# Node - Validate and Process the user's input
def processing_node(state: State):
    # Get the list of messages from the state
    messages = state.get("messages", [])

    # Ensure that there is user input in the state
    if not messages or not isinstance(messages[-1], HumanMessage):
        return {
            "messages": messages + [AIMessage(content="No user input received.")],
            "valid_input": False
        }

    # Get the last message from the state
    last_message = messages[-1]

    # Make sure the input is valid
    if not last_message.content.strip():
        return {
            "messages": messages + [AIMessage(content="No user input received.")],
            "valid_input": False
        }

    # Pass the user query to the llm for response
    response = llm.invoke([
        SystemMessage(content = (
            "You are a helpful assistant that is great at processing user queries and turning them into a singular search query."
            "You will be given a user query and your job is the turn the users request into a new query that will be passed onto the next node."
            "This new query will be used to search the internet for information relevant to the users original query."
            "Do not bloat the query with unnecessary information, but ensure the context of the original query is preserved."
        )),
        HumanMessage(content = last_message.content)
    ])

    # Append the returned response to the state
    return {
        "messages" : messages + [response],
        "valid_input" : True
    }

# Node - Perform the internet search using DuckDuckGo
def process_search(state: State):
    # Get the list of messages from the state
    messages = state.get("messages", [])

    # Get the search query from the previous llm
    search_query = messages[-1]

    # Make sure the search query is a valid AIMessage
    if not isinstance(search_query, AIMessage):
        return {
            "messages": messages + [AIMessage(content="No search query received.")],
            "valid_input": False
        }

    # Run the search tool using the generated search query
    results = tool_search.run(search_query.content)

    # Append the returned results to the state
    return {
        "messages" : messages + [AIMessage(content=f"Search results: {results}")],
        "valid_input" : True
    }

# Format the search results into a user-friendly structure
def format_output(state: State):
    # Get the list of messages from the state
    messages = state.get("messages", [])

    # Get the results from the search
    search_results = messages[-1]

    # Make sure the results are a valid AIMessage
    if not isinstance(search_results, AIMessage):
        return {
            "messages": messages + [AIMessage(content="No search results received.")],
            "valid_input": False
        }

    # Call the LLM to format the search results
    formatted_results = llm.invoke([
        SystemMessage(content = (
            "You are a helpful assistant that is great at formatting search results into a human readable format."
            "You should receive the results of a search query that was processed in the previous few nodes."
            "The results should contain contents reguarding travel information, such as destinations, cities, countries, etc."
            "Your job is to format the results into the following format:"
            "Topic Sentence (Can be something similar like 'Here are some interesting facts about x' or whatever you feel best fits as an intro sentence.)"
            "3-5 bullet points describing the travel location as a whole"
            "3-5 bullet points naming destinations the user should visit in the travel location"
            "3-5 bullet points naming top things the user should do in the travel location"
            "1-3 bullet points naming any other interesting facts about the travel location the user should know (can put N/A if not applicable)"
            "A List of sources that were used"
            "Stick to this format, and do not bloat the output with unnecessary information."
            "Do not explicitly type metadata such as 'title' or 'source' in the output, just list the contents of the metadata."
            ""
        )),
        HumanMessage(content = search_results.content)
    ])

    # Append the returned response to the state
    return {
        "messages" : messages + [formatted_results],
        "valid_input" : True
    }

# Build the LangGraph workflow
graph_builder = StateGraph(State)

# Register the nodes within the workflow
graph_builder.add_node("process_input", processing_node)
graph_builder.add_node("process_search", process_search)
graph_builder.add_node("format_output", format_output)

# Add edges and conditional logic between nodes
graph_builder.add_edge(START, "process_input")
graph_builder.add_conditional_edges(
    "process_input",
    lambda state: state.get("valid_input", False),
    {
        True: "process_search",
        False: END
    }
)
graph_builder.add_conditional_edges(
    "process_search",
    lambda state: state.get("valid_input", False),
    {
        True: "format_output",
        False: END
    }
)
graph_builder.add_edge("format_output", END)

# Compile the graph
graph = graph_builder.compile()

# Command-line chatbot interface
def chatbot() -> None:
    # Initial state
    state = {
        "messages" : [],
        "valid_input" : False
    }

    # While loop that iterates only when the user does not enter 'q'
    while (user_input := input("Enter your search query ('q' to quit): ")) != "q":
        # Add the user input to the state
        state["messages"] += [HumanMessage(user_input)]

        # Invoke the graph with the updated state
        state = graph.invoke(state)

        # Extract the response from the agent
        response = state["messages"][-1]

        # Check to make sure the workflow processed as intended
        if isinstance(response, AIMessage):
            print(response.content)
        else:
            print("Invalid response received.")

        # FOR DEBUGGING ONLY
        # print("\n\n")
        # print(state["messages"])

# Run the CLI chatbot
chatbot()