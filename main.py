from agent import ask_agent, parse_nl_to_query, ask_agent_parsed

def main():
    # Example 1: Using ask_agent (direct NL query)
    user_query = "Sensors with battery below 20"
    response1 = ask_agent(user_query)
    print("Example 1 - ask_agent response:")
    print(response1)
    print()

    # # Example 2: Parse NL query, then execute
    # nl_query2 = "Get temp and location for sensor 1011"
    # parsed_query2 = parse_nl_to_query(nl_query2)
    # print("Example 2 - parse_nl_to_query output:")
    # print(parsed_query2)
    # response2 = ask_agent_parsed(parsed_query2)
    # print("Example 2 - Executed query result:")
    # print(response2)
    # print()
 #
 #    # Example 3: Query with no sensor_id (all readings)
 #    nl_query3 = "Show me all sensor readings"
 #    parsed_query3 = parse_nl_to_query(nl_query3)
 #    print("Example 3 - parse_nl_to_query (no sensor_id) output:")
 #    print(parsed_query3)
 #    response3 = ask_agent_parsed(parsed_query3)
 #    print("Example 3 - Executed query result:")
 #    print(response3)
 #    print()
 #
 #    # Example 4: Show all active sensors
 #    nl_query4 = "Show me active sensors"
 #    parsed_query4 = parse_nl_to_query(nl_query4)
 #    print("Example 4 - parse_nl_to_query output:")
 #    print(parsed_query4)
 #    response4 = ask_agent_parsed(parsed_query4)
 #    print("Example 4 - Executed query result:")
 #    print(response4)
 #    print()
 #
 # # Example 5: Show all inactive sensors
 #    nl_query5 = "Show me inactivate sensors"
 #    parsed_query5 = parse_nl_to_query(nl_query5)
 #    print("Example 5 - parse_nl_to_query output:")
 #    print(parsed_query5)
 #    response5 = ask_agent_parsed(parsed_query5)
 #    print("Example 5 - Executed query result:")
 #    print(response5)
 #    print()

if __name__ == "__main__":
    main()
