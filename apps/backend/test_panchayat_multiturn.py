
from langchain_core.messages import HumanMessage
from app.orchestration.graph import grievance_graph


# TURN 1: Citizen reports a village concern
state1 = {
    "messages": [
        HumanMessage(
            content="The streetlight in Pedakakani village is not working."
        )
    ],
    "department": None,
    "status": "new",
}

result1 = grievance_graph.invoke(state1)

print("\n--- TURN 1 ---")
print("Department:", result1.get("department"))
print("Status:", result1.get("status"))
print("Missing fields:", result1.get("missing_fields"))
print("Agent:", result1["messages"][-1].content)


# TURN 2: Citizen provides the location
state2 = {
    **result1,
    "messages": [
        *result1["messages"],
        HumanMessage(content="Near the village school."),
    ],
}

result2 = grievance_graph.invoke(state2)

print("\n--- TURN 2 ---")
print("Department:", result2.get("department"))
print("Status:", result2.get("status"))
print("Missing fields:", result2.get("missing_fields"))
print("Extracted details:", result2.get("extracted_details"))
print("Agent:", result2["messages"][-1].content)


# TURN 3: Citizen confirms the information
state3 = {
    **result2,
    "messages": [
        *result2["messages"],
        HumanMessage(content="Yes, that is correct."),
    ],
}

result3 = grievance_graph.invoke(state3)

print("\n--- TURN 3 ---")
print("Department:", result3.get("department"))
print("Status:", result3.get("status"))
print("Confirmed details:", result3.get("extracted_details"))
print("Agent:", result3["messages"][-1].content)

