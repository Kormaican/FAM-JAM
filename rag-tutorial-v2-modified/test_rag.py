from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""

# TODO - make better test cases. And try different opensource models on Ollama to see accuracies of json creation.
def test_extraction_for_fam_jam():
    assert query_and_validate(
        question="""
Convert the following rag context into a JSON file. For each key, include only the items that are present in the 
context. If an item is not mentioned, it can be omitted from the output.

The JSON file should have the following keys:
- length
- width
- height
- weight
- center_of_mass
- vibration_criteria
- exhaust_requirement

If the values are available in units, preserve them in the JSON file. If any data is ambiguous or 
incomplete, include only what is clear.

Example rag context:

[Insert rag context here]
""",
        expected_response='''{
      "product": "Acute Momentum Motorized Trendelenburg",
      "model": "890902",
      "length": "29W", // W stands for width in this context, but it is used inconsistently as length here. This might be a typo or an inconsistent naming convention in the provided context.
      "width": "33D", // D stands for depth in this context, but it is used inconsistently as width here. This might be a typo or an inconsistent naming convention in the provided context.
      "height": "43H", // H stands for height in this context.
      "weight": "Not mentioned in the context",
      "center_of_mass": "Not mentioned in the context",
      "vibration_criteria": "Not mentioned in the context",
      "exhaust_requirement": "Not mentioned in the context"
   }
''',
    )
#
# def test_monopoly_rules():
#     assert query_and_validate(
#         question="How much total money does a player start with in Monopoly? (Answer with the number only)",
#         expected_response="$1500",
#     )
#
#
# def test_ticket_to_ride_rules():
#     assert query_and_validate(
#         question="How many points does the longest continuous train get in Ticket to Ride? (Answer with the number only)",
#         expected_response="10 points",
#     )


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
