
from langchain_core.messages import HumanMessage
from app.orchestration.graph import grievance_graph


# First conversation turn
state = {
    "messages": [
        HumanMessage(content="Our school needs three new blackboards.")
    ],
    "department": None,
    "status": "new",
}

result1 = grievance_graph.invoke(state)

print("\n--- TURN 1 ---")
print("Department:", result1.get("department"))
print("Status:", result1.get("status"))
print("Missing fields:", result1.get("missing_fields"))
print("Agent:", result1["messages"][-1].content)


# Second conversation turn
# Preserve the first turn's state and append the citizen's reply.
state2 = {
    **result1,
    "messages": [
        *result1["messages"],
        HumanMessage(content="ZP High School"),
    ],
}

result2 = grievance_graph.invoke(state2)

print("\n--- TURN 2 ---")
print("Department:", result2.get("department"))
print("Status:", result2.get("status"))
print("Missing fields:", result2.get("missing_fields"))
print("Extracted details:", result2.get("extracted_details"))
print("Agent:", result2["messages"][-1].content)



# Third conversation turn
state3 = {
    **result2,
    "messages": [
        *result2["messages"],
        HumanMessage(content="The school is located in Guntur."),
    ],
}

result3 = grievance_graph.invoke(state3)

print("\n--- TURN 3 ---")
print("Department:", result3.get("department"))
print("Status:", result3.get("status"))
print("Missing fields:", result3.get("missing_fields"))
print("Extracted details:", result3.get("extracted_details"))
print("Agent:", result3["messages"][-1].content)


# Fourth conversation turn: Citizen confirms the details
state4 = {
    **result3,
    "messages": [
        *result3["messages"],
        HumanMessage(content="Yes, that is correct."),
    ],
}

result4 = grievance_graph.invoke(state4)

print("\n--- TURN 4 ---")
print("Department:", result4.get("department"))
print("Status:", result4.get("status"))
print("Missing fields:", result4.get("missing_fields"))
print("Confirmed details:", result4.get("extracted_details"))
print("Agent:", result4["messages"][-1].content)
