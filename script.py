import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI


async def main():
    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
    )

    # Define the task for the agent
    task = "Find a list of all U.S. presidents"

    # Create the agent with the specified task and language model
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=True,  # Enable vision capabilities if needed
        save_conversation_path="logs/conversation.json"  # Path to save the conversation history
    )

    # Run the agent
    history = await agent.run()

    # Access and print useful information from the agent's history
    print("Visited URLs:", history.urls())
    print("Extracted Content:", history.extracted_content())

# Execute the main function
if __name__ == "__main__":
    asyncio.run(main())