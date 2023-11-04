from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html', translate = translate)

@app.route('/translate', methods=['GET'])
def translate():
    api_token = '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'
    model_name = 'Helsinki-NLP/opus-mt-en-es'

    api_url = f'https://api-inference.huggingface.co/models/{model_name}'
    text = request.args.get('text')

    headers = {'Authorization': f'Bearer {api_token}'}
    response = requests.post(api_url, headers=headers, json={'inputs': text})

    # Analizar la respuesta JSON
    response_json = response.json()

    # Extraer la traducción
    translation = response_json[0]['translation_text']

    return jsonify({'translation': translation})
if __name__ == '__main__':
    app.run(port=8000, debug=True)