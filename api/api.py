from flask import Flask, request, jsonify
import openai, os, requests, yaml
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv(dotenv_path="../.env")

# Configuration OpenAI API Key with environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configuration Mistral API Key
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
MISTRAL_API_URL = os.getenv('MISTRAL_API_URL')

app = Flask(__name__)

def generate_prompt(text):
    return f"""
    Extract the following details from the given text and format it into a YAML structure:

    1. Name
    2. Phone Numbers
    3. Websites
    4. Emails
    5. Date of Birth
    6. Addresses
    7. Summary
    8. Education
    9. Work Experience
    10. Skills
    11. Certifications

    Text: {text}

    Structure the YAML as follows:

    name: ''
    phoneNumbers:
    - ''
    websites:
    - ''
    emails:
    - ''
    dateOfBirth: ''
    addresses:
    - street: ''
      city: ''
      state: ''
      zip: ''
      country: ''
    summary: ''
    education:
    - school: ''
      degree: ''
      fieldOfStudy: ''
      startDate: ''
      endDate: ''
    workExperience:
    - company: ''
      position: ''
      startDate: ''
      endDate: ''
    skills:
    - name: ''
    certifications:
    - name: ''
    """

def get_structured_yaml(text, model, api_function):
    prompt = generate_prompt(text)
    response = api_function(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    if(model =="open-mistral-7b"):
        return response['choices'][0]['message']['content'].strip()
    return response.choices[0].message['content'].strip()

def get_structured_yaml_gpt(text):
    return get_structured_yaml(text, "gpt-4o", openai.ChatCompletion.create)

def get_structured_yaml_mistral(text):
    def mistral_api_function(model, messages):
        headers = {
            'Authorization': f'Bearer {MISTRAL_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": model,
            "messages": messages
        }

        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        
        return response.json()
         
        
    return get_structured_yaml(text, "open-mistral-7b", mistral_api_function)

def extract_yaml(api_function):
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    try:
        yaml_output = api_function(text)
        return jsonify({'yaml': yaml_output}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract-gpt', methods=['POST'])
def extract_gpt():
    return extract_yaml(get_structured_yaml_gpt)

@app.route('/extract-mistral', methods=['POST'])
def extract_mistral():
    return extract_yaml(get_structured_yaml_mistral)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
