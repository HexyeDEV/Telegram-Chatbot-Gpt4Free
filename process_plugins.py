import wolframalpha
from os import getenv

plugins_second_question = {
    "wolframalpha": "Explain the following wolframalpha results in a comprehensive way considering the user input was: <input> \n\nwolframalpha result: <result>. If no result is given, then try to answer the question on your own. After the answer, add the text: [Wolfram]",
}

def process_plugins(result):
    if "[WOLFRAMALPHA" in result:
        return _process_wolframalpha(result)
    else:
        return [False, ""]

def _process_wolframalpha(result):
        query = result.replace(f"[WOLFRAMALPHA ", "").replace(" END]", "")
        wolframalpha_app_id = getenv("WOLFRAMALPHA_APP_ID")
        wf_client = wolframalpha.Client(app_id=wolframalpha_app_id)
        res = wf_client.query(query)
        if res["@success"] == False:
            return [False, ""]
        else:
            w_result = next(res.results).text
            return[True, plugins_second_question["wolframalpha"].replace("<input>", query).replace("<result>", w_result)]