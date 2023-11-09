from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections
import requests
from unidecode import unidecode

app = Flask(__name__)

nltk.data.path.append('C:\\Users\\thoma\\OneDrive\\Escritorio\\Proyecto_lab\\punkt_y_wordnet')

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/question', methods=['GET'])
def question():
    chatbot = Chat(pares, reflections)
    usuario_input = request.args.get('text')
    if usuario_input.lower() == 'salir':
        return jsonify({'translation': "Chatbot: ¡Hasta luego!"})
    elif usuario_input[:14].lower() == 'traduce esto: ':
        translation = translate(usuario_input[14:])
        return jsonify({'translation': ("Chatbot: " + translation)})
    elif usuario_input[:9].lower() == 'traduce: ':
        translation = translate(usuario_input[9:])
        return jsonify({'translation': ("Chatbot: " + translation)})
    else:
        respuesta = chatbot.respond(unidecode(usuario_input))
        if respuesta is None:
            return jsonify({'translation': "Chatbot: Lo siento, no puedo responder a tu pregunta"})
        else:
            return jsonify({'translation': ("Chatbot: " + respuesta)})



def translate(texto):
    api_token = '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'
    model_name = 'Helsinki-NLP/opus-mt-en-es'

    api_url = f'https://api-inference.huggingface.co/models/{model_name}'
    text = texto

    headers = {'Authorization': f'Bearer {api_token}'}

    try:
        response = requests.post(api_url, headers=headers, json={'inputs': text})

        # Analizar la respuesta JSON
        response_json = response.json()

        # Extraer la traducción
        if response_json:
            translation = response_json[0].get('translation_text')
        else:
            translation = "Lo siento, ocurió un error al intentar traducir el texto. Por favor intenta de nuevo mas tarde."

        # Imprimir la traducción
        return translation
    except:
        translation = "Lo siento, ocurió un error al intentar traducir el texto. Por favor intenta de nuevo mas tarde."
        return translation
#preguntas y respuestas
pares = [
    ['Hola', ['¡Hola!', '¡Hola!, ¿en qué puedo ayudarte?']],
    ['Ok', ['¡Hola! ¿Cómo puedo ayudarte hoy?']],
    ['Sos real?', ['No! soy un programa creado por Thomas, Eric, Matias y Franco.']],
    ['Que eres?', ['Soy un programa creado por Thomas, Eric, Matias y Franco.']],
    ['Quien eres?', ['Soy un programa creado por Thomas, Eric, Matias y Franco.']],
    ['Que es Python?', ['Python es un lenguaje de programación de alto nivel ampliamente utilizado para desarrollo de software.']],
    ['Que es la programacion?', ['La programación es el proceso de crear un conjunto de instrucciones o código que una computadora o sistema informático puede entender y ejecutar.']],
    ['Como puedo aprender a programar?', ['Para aprender a programar, elige un lenguaje, utiliza recursos en línea, practica regularmente y trabaja en proyectos personales.']],
    ['Es necesario ir a la universidad para conseguir trabajo como programador?', ['No! se puede conseguir trabajo siendo autodidacta, pero un titulo muchas veces ayuda']],
    ['Que dia es hoy?', ['Hoy es viernes 10 de octubre, un poco soleado.']],
    ['Los chicos aprobaran con este proyecto?', ['Esperemos que si! :)']],
    ['Adios', ['¡Adiós!', 'Hasta luego, que tengas un buen día.']],
]

if __name__ == '__main__':
    app.run(port=5000)