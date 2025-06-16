class Plugin:
    def __init__(self, name, prompt, has_followup=False, followup_prompt=None):
        self.name = name
        self.prompt = prompt
        if has_followup and followup_prompt is None:
            raise ValueError("If has_followup is True, followup_prompt must be provided.")
        self.has_followup = has_followup
        self.followup_prompt = followup_prompt

plugins = [
    Plugin(
        name="wolframalpha",
        prompt="Wolframalpha plugin lets you perform math operations. If appropriate to use it, answer exactly with: \"[WOLFRAMALPHA <query> END]\" where query is the operation you need to solve. Examples: Input: Solve for x: 2x+3=5 Output: [WOLFRAMALPHA solve (2x+3=5) for x END] Input: A*2=B solve for B Output: [WOLFRAMALPHA solve (A*2=B) for B END]. Even if you got the input in a different language, always use english in the wolframalpha query.",
        has_followup=True,
        followup_prompt="Explain the following wolframalpha results in a comprehensive way considering the user input was: <input> \n\nwolframalpha result: <result>. If no result is given, then try to answer the question on your own. After the answer, add the text: [Wolfram]"
    )
]