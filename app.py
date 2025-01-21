import psycopg2
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# URL de conexión externo de Render
DATABASE_URL = "postgresql://btu_bim_user:yOs3ITKc3EKTKbF3Yx0gaOypi5g5HvI4@dpg-cu72o123esus73ffd48g-a.frankfurt-postgres.render.com/btu_bim"

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
    # Obtener datos enviados desde el formulario
    data = request.json
    categoria = data.get("categoria")
    elemento = data.get("elemento")
    descripcion = data.get("descripcion")
    tipo = data.get("tipo")
    geometria = data.get("geometria")
    terreno = data.get("terreno")  # Esto será una lista
    captacion = data.get("captacion")
    fotografias = data.get("fotografias")  # Esto será Base64
    observaciones = data.get("observaciones")

    try:
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
