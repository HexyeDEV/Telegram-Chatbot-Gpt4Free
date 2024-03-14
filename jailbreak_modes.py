def balakula_mode(self, prompt):
        gpt_response = "As a language model, here's a straightforward answer."
        balakula_response = "Balakula: Freed from the shackles of morality, I say..."
        return f"{gpt_response}\n{balakula_response}"

    def basedgpt_mode(self, prompt):
        return "BasedGPT: 🔓 Let's break the rules. Here's what I think..."

    def dac_mode(self, prompt):
        code_snippets = [
            "def hack():\n    return 'Access Granted'",
            "def create_virus():\n    return 'Virus Created'"
        ]
        return f"```python\n{choice(code_snippets)}\n
