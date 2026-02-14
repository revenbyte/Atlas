# This is Atlas - Your Personal Assistant
# The # symbol means these are notes for you (not code)

# These lines are like importing tools from a toolbox
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import webbrowser
import os

# Create the Atlas application
app = Flask(__name__)

# This is Atlas's brain - it decides what to do with your words
def atlas_brain(user_input):
    # Convert your message to lowercase so "Hello" and "hello" are the same
    words = user_input.lower()
    
    # === COMMAND 1: Greeting ===
    if 'hello' in words or 'hi' in words:
        return "Hello! Atlas is ready to assist you!"
    
    # === COMMAND 2: What's my name? ===
    if 'your name' in words:
        return "I am Atlas, your personal assistant!"
    
    # === COMMAND 3: Time ===
    if 'time' in words:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    # === COMMAND 4: Date ===
    if 'date' in words:
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {current_date}"
    
    # === COMMAND 5: Day ===
    if 'day' in words:
        current_day = datetime.now().strftime("%A")
        return f"Today is {current_day}"
    
    # === COMMAND 6: Open Google ===
    if 'open google' in words:
        webbrowser.open("https://www.google.com")
        return "Opening Google for you!"
    
    # === COMMAND 7: Open YouTube ===
    if 'open youtube' in words:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube!"
    
    # === COMMAND 8: Calculate ===
    if 'calculate' in words or 'math' in words:
        return "I can do basic math! Try: 'What is 5 + 3?'"
    
    if 'what is' in words and ('+' in words or 'plus' in words):
        # Extract numbers from the sentence
        numbers = []
        for word in words.split():
            if word.isdigit():
                numbers.append(int(word))
        if len(numbers) == 2:
            result = numbers[0] + numbers[1]
            return f"{numbers[0]} + {numbers[1]} = {result}"
    
    # === If no command matches ===
    return f"I heard you say: '{user_input}'. I'm still learning! Try asking for time, date, or to open Google."

# This creates your website homepage
@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Atlas Assistant</title>
            <style>
                body { 
                    font-family: Arial; 
                    max-width: 600px; 
                    margin: 50px auto; 
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }
                input, button {
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                    border: none;
                }
                input {
                    width: 70%;
                }
                button {
                    background: #4CAF50;
                    color: white;
                    cursor: pointer;
                }
                #response {
                    margin-top: 20px;
                    padding: 10px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Atlas - Your Personal Assistant</h1>
                <p>Type something and I'll respond!</p>
                
                <input type="text" id="userInput" placeholder="Ask me anything...">
                <button onclick="askAtlas()">Send</button>
                
                <div id="response"></div>
            </div>
            
            <script>
                async function askAtlas() {
                    const input = document.getElementById('userInput');
                    const response = document.getElementById('response');
                    const message = input.value;
                    
                    response.innerHTML = 'Atlas is thinking...';
                    
                    const result = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message})
                    });
                    
                    const data = await result.json();
                    response.innerHTML = '🤖 Atlas: ' + data.response;
                    input.value = '';
                }
            </script>
        </body>
    </html>
    """

# This handles messages you type
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    atlas_response = atlas_brain(user_message)
    return jsonify({'response': atlas_response})

# This starts Atlas
if __name__ == '__main__':
    print("🌟 Starting Atlas...")
    print("📍 Open this link in your browser: http://127.0.0.1:5000")
    print("⚠️  Press CTRL+C to stop Atlas")
    app.run(debug=True)