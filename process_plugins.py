import wolframalpha
from os import getenv
from plugins import plugins as plugins_list

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
            second_question = None
            for plugin in plugins_list:
                if plugin.name == "wolframalpha" and plugin.has_followup:
                    second_question = plugin.followup_prompt
                    break
                if not second_question:
                     raise ValueError("No follow-up question found for wolframalpha plugin.")
            return[True, second_question.replace("<input>", query).replace("<result>", w_result)]