from flask import Flask, request, jsonify, render_template
import psycopg2
import os
import json

app = Flask(__name__)

# URL de conexión externo de Render
DATABASE_URL = "postgresql://btu_bim_user:yOs3ITKc3EKTKbF3Yx0gaOypi5g5HvI4@dpg-cu72o123esus73ffd48g-a/btu_bim"

# Conexión a la base de datos
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Ruta para mantener la app activa (Keep-Alive)
@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200

# Ruta principal para servir el formulario HTML
@app.route("/", methods=["GET"])
def home():
    return render_template("formulario.html")

# Ruta para manejar el envío del formulario
@app.route("/submit", methods=["POST"])
def submit_data():
    try:
        # Leer los datos del formulario
        data = request.get_json()
        if not data:
            return jsonify({"error": "Solicitud vacía o no válida"}), 400

        # Obtener datos del formulario
        modo = data["modo"]
        categoria = data["categoria"]
        elemento = data["elemento"]
        descripcion = data["descripcion"]
        tipo = data["tipo"]
        geometria = data["geometria"]
        terreno = json.dumps(data.get("terreno", []))
        captacion = data["captacion"]
        observaciones = data["observaciones"]

        cur = conn.cursor()

        if modo == "actualizar":
            # Lógica para actualizar un registro existente
            cur.execute("""
                UPDATE datos_btu_bim
                SET categoria=%s, descripcion=%s, tipo=%s, geometria=%s, terreno=%s, captacion=%s, observaciones=%s
                WHERE elemento_objeto=%s
            """, (categoria, descripcion, tipo, geometria, terreno, captacion, observaciones, elemento))
            mensaje = "Registro actualizado con éxito."
        else:
            # Lógica para agregar un nuevo registro
            cur.execute("""
                INSERT INTO datos_btu_bim 
                (categoria, elemento_objeto, descripcion, tipo, geometria, terreno, captacion, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (categoria, elemento, descripcion, tipo, geometria, terreno, captacion, observaciones))
            mensaje = "Nuevo registro agregado con éxito."

        conn.commit()
        cur.close()

        return jsonify({"message": mensaje}), 200
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
