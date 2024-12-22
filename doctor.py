import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    data = {
        "model": "codeDoctor",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        try:
            data = json.loads(response_text)
            actual_response = data["response"]
            return f"```{actual_response}```"
        except ValueError as e:
            print("Error:", str(e))
            return "An error occurred while parsing the response."
    else:
        print("Error:", response.text)
        return "An error occurred with the API request."


interface = gr.Interface(
    fn=lambda prompt: f"```java{generate_response(prompt)}```",
    inputs=gr.Textbox(lines=4, placeholder="Enter your Prompt"),
    outputs=gr.Markdown(),
)
interface.launch()