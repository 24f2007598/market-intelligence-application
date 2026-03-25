# import json

# def extract_structured_data(llm, query, rag_output):
#     prompt = f"""
#     The user asked: "{query}"

#     Based on this query, extract ONLY relevant structured insights.

#     Return ONLY valid JSON list:
#     [
#       {{
#         "company": "",
#         "page_type": "",
#         "change_type": "",
#         "feature": "",
#         "old_value": "",
#         "new_value": "",
#         "price": "",
#         "summary": "",
#         "importance_score": ""
#       }}
#     ]

#     If nothing relevant, return [].

#     Text:
#     {rag_output}
#     """

#     response = llm.invoke(prompt)

#     try:
#         return json.loads(response)
#     except:
#         return []