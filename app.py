import psycopg2
from flask import Flask, request, jsonify, render_template
import json
import base64  # Para manejar datos en formato Base64

app = Flask(__name__)

# URL de conexión externo de Render
DATABASE_URL = "postgresql://btu_bim_user:yOs3ITKc3EKTKbF3Yx0gaOypi5g5HvI4@dpg-cu72o123esus73ffd48g-a/btu_bim"

# Ruta principal para servir el formulario HTML
@app.route("/", methods=["GET"])
def home():
    return render_template("formulario.html")  # Sirve el formulario desde /templates

# Ruta para manejar el envío del formulario
@app.route("/submit", methods=["POST"])
def submit_data():
    try:
        # Obtener datos enviados desde el formulario
        data = request.json
        categoria = data.get("categoria")
        elemento = data.get("elemento")
        descripcion = data.get("descripcion")
        tipo = data.get("tipo")
        geometria = data.get("geometria")

        # Convertir `terreno` a cadena JSON si es una lista
        terreno = data.get("terreno")
        if isinstance(terreno, list):
            terreno = json.dumps(terreno)  # Convertir lista a JSON string

        # Convertir `fotografias` a binario (BYTEA) si viene en Base64
        fotografias = data.get("fotografias")
        if isinstance(fotografias, str):  # Si es una cadena Base64
            fotografias = base64.b64decode(fotografias)

        # Convertir observaciones a cadena (si no es cadena)
        observaciones = data.get("observaciones", "")
        if not isinstance(observaciones, str):
            observaciones = str(observaciones)

        captacion = data.get("captacion")

        # Conexión a la base de datos
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        # Insertar datos en la tabla
        cur.execute("""
            INSERT INTO datos_btu_bim 
            (categoria, elemento_objeto, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (categoria, elemento, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Datos guardados con éxito"}), 200
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return jsonify({"error": f"Error al guardar los datos: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
