import psycopg2
from flask import Flask, request, jsonify, render_template
import os
import base64

app = Flask(__name__)

# URL de conexión externo de Render
DATABASE_URL = "postgresql://btu_bim_user:yOs3ITKc3EKTKbF3Yx0gaOypi5g5HvI4@dpg-cu72o123esus73ffd48g-a/btu_bim"

# Conexión a la base de datos
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Ruta principal para servir el formulario HTML
@app.route("/", methods=["GET"])
def home():
    return render_template("formulario.html")  # Sirve el formulario desde /templates

# Ruta para manejar el envío del formulario
@app.route("/submit", methods=["POST"])
def submit_data():
    try:
        # Intentar leer el JSON enviado en la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"error": "Solicitud sin datos o no es JSON válido"}), 400

        # Validar campos requeridos
        required_fields = ["categoria", "elemento", "descripcion", "tipo", "geometria", "terreno", "captacion", "fotografias", "observaciones"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 400

        # Obtener datos
        categoria = data["categoria"]
        elemento = data["elemento"]
        descripcion = data["descripcion"]
        tipo = data["tipo"]
        geometria = data["geometria"]
        terreno = data["terreno"]  # Mantenerlo como lista para TEXT[]
        captacion = data["captacion"]
        fotografias = base64.b64decode(data["fotografias"])  # Convertir Base64 a bytes
        observaciones = data["observaciones"]

        # Usar la conexión global para insertar datos
        cur = conn.cursor()

        # Insertar datos en la tabla
        cur.execute("""
            INSERT INTO datos_btu_bim 
            (categoria, elemento_objeto, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (categoria, elemento, descripcion, tipo, geometria, terreno, captacion, fotografias, observaciones))
        conn.commit()

        cur.close()
        return jsonify({"message": "Datos guardados con éxito"}), 200
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

