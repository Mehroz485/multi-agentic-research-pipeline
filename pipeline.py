from tools import web_search, scrape_url
import agents


def run_research_pipeline(topic: str) -> dict:
    state = {}

    print("step 1 - search agent is working ...")
    print("=" * 80)

    search_agent = agents.build_search_agent()

    
    searched_result = search_agent.invoke(
        {"messages": [("user", f"Find recent, reliable, and detailed information about: {topic}. "
                               f"You MUST include the raw source URLs in your final response.")] }
    )

    state["search_results"] = searched_result["messages"][-1].content

    print("\n search result \n", state["search_results"])
    print("=" * 80)

    print("\nstep 2 - reader agent is working ...")
    print("=" * 80)

    reader_agent = agents.build_reader_agent()

    
    reader_results = reader_agent.invoke(
        {"messages": [("user",
          f"Scan the following text, find the most relevant source URL, scrape it, and return the deep content.\n"
          f"If no explicit URL is found, use your web_search tool directly to find a source for '{topic}'.\n\n"
          f"Search Results:\n{state['search_results']}")]}
    )

    state['scraped_result'] = reader_results["messages"][-1].content

    print("\n scraped result \n", state['scraped_result'])
    print("=" * 80)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_result']}"
    )

    print("\nstep 3 - writer agent is working ...")
    print("=" * 80)

    state["report"] = agents.writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n final report \n", state["report"])
    print("=" * 80)

    print("\nstep 4 - critic agent is working ...")
    print("=" * 80)

    state["feedback"] = agents.critic_chain.invoke({
        "report": state['report']
    })

    print("\n critic report \n", state['feedback'])
    print("=" * 80)

    return state


if __name__ == "__main__":
    topic = input("Enter the topic: ").strip()

    while not topic:
        print("Topic cannot be empty. Please enter a topic.")
        topic = input("Enter the topic: ").strip()

    result = run_research_pipeline(topic)