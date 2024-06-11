from flask import Flask, request, render_template, jsonify
from rich.console import Console
import ollama

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

console = Console()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    # Get the uploaded file
    file = request.files['file']
    # Get the prompt text
    prompt = request.form['prompt']

    # Read the file content (assuming it's a text file)
    file_content = file.read().decode('utf-8')

    # Combine file content and prompt
    combined_input = f"File Content:\n{file_content}\n\nPrompt:\n{prompt}"

    try:
        # Stream the chat response from the LLaMA model
        stream = ollama.chat(
            model="Llama3",
            messages=[{"role": "user", "content": combined_input}],
            stream=True
        )

        response = ""
        for chunk in stream:
            response += chunk['message']['content']

        # Return the response as JSON
        return jsonify({"response": response})

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return jsonify({"response": f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
