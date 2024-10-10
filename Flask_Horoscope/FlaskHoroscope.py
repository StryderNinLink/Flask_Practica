#02 🪐 Horoscope USANDO FLASK
# Desarrolla un programa de horóscopo que:
# - Tenga una lista de signos zodiacales y predicciones
# - Permita al usuario ingresar su signo
# - Muestre una predicción aleatoria para ese signo
# - Guarde un historial de predicciones para cada signo
# - Permita al usuario ver predicciones pasadas para su signo

from flask import Flask, render_template, redirect, url_for, flash, request
import random

app=Flask(__name__)
app.secret_key = 'supersecretkey_horoscope'

saints = ["ARIES", "TAURO", "GÉMINIS", "CÁNCER", "LEO", "VIRGO", "LIBRA", "ESCORPIO", "SAGITARIO", "CAPRICORNIO", "ACUARIO", "PISCIS"]

magic_quote = [
    "Tendras un excelente dia",
    "Comer sano, ayuda mucho",
    "No compres desesperado, mejor espera la oferta",
    "El éxito no es el resultado de la suerte, sino de la preparación.",
    "No temas al fracaso, es una parte del camino hacia el éxito.",
    "El cambio es la única constante en la vida.",
    "El héroe siempre encuentra su camino, aunque el camino esté lleno de enemigos.",
    "Cada nivel superado te acerca más al gran jefe final.",
    "La verdadera experiencia se gana fuera de la zona de confort.",
    "Las decisiones en un juego pueden cambiar el destino del mundo; lo mismo ocurre en la vida.",
    "No subestimes el poder de un buen equipo; juntos, podemos vencer cualquier desafío.",
    "Cada vez que fallas, recuerda: es solo un 'game over', no el final de la partida.",
    "Los mejores loot boxes son las oportunidades disfrazadas de desafíos.",
    "El grind es parte del viaje hacia el nivel máximo.",
    "La historia de tu vida es un RPG; cada elección cuenta.",
    "A veces, la vida te lanza un 'boss fight', pero con estrategia y paciencia, puedes ganar."
]

saveMagic = {saint: [] for saint in saints}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', saints=saints)

@app.route('/magic_prediction', methods=['GET', 'POST'])
def magic_prediction():
    if request.method == 'POST':
        userSaint = request.form['sign'].upper()
        if userSaint in saints:
            quoteM = random.choice(magic_quote)
            saveMagic[userSaint].append(quoteM)
            flash(f"Eres {userSaint}, para ti el universo te dice: '{quoteM}'")
            return redirect(url_for('magic_prediction'))
        else:
            flash("No conozco ese signo... Por favor, repitelo o ve que sea el correcto")
            return render_template('magic_prediction.html', saints=saints)
    return render_template('magic_prediction.html', saints=saints)

@app.route('/past_magic', methods=['GET', 'POST'])
def past_magic():
    if request.method == 'POST':
        userSaint = request.form['sign'].upper()
        if userSaint in saveMagic and saveMagic[userSaint]:
            magic_quote = saveMagic[userSaint]
            return render_template('past_magic.html', userSaint=userSaint, magic_quote=magic_quote, saints=saints)
        return render_template('past_magic.html', userSaint=userSaint, magic_quote=[], saints=saints)
    return render_template('past_magic.html', saints=saints)

if __name__ == "__main__":
    app.run(debug=True)