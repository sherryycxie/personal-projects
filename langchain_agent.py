import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure necessary API keys are set
if not os.getenv("TAVILY_API_KEY") or not os.getenv("LANGCHAIN_API_KEY"):
    raise ValueError("Missing necessary API keys. Please check your .env file.")

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor

# Initialize search tool
search = TavilySearchResults()

# Load documents
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(docs)

# Create vector store
vector = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vector.as_retriever()

# Create retriever tool
retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)

tools = [search, retriever_tool]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Load prompt
prompt = hub.pull("hwchase17/openai-functions-agent")

# Create agent
agent = create_openai_functions_agent(llm, tools, prompt)

# Create agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run agent
while True:
    user_input = input("Enter your query (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    response = agent_executor.invoke({"input": user_input})
    print(response)

