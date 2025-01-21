import psycopg2
from flask import Flask, request, jsonify, render_template

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
    data = request.json
    try:
        categoria = data.get("categoria")
        elemento = data.get("elemento")
        descripcion = data.get("descripcion")
        tipo = data.get("tipo")
        geometria = data.get("geometria")
        terreno = ','.join(data.get("terreno", []))  # Convierte lista a cadena
        captacion = data.get("captacion")
        fotografias = data.get("fotografias")
        observaciones = data.get("observaciones")
    except KeyError as e:
        return jsonify({"error": f"Faltan datos requeridos: {e}"}), 400

    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
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
        return jsonify({"error": f"Error al guardar los datos: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)


