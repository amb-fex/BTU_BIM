import psycopg2
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Configuración de PostgreSQL
DB_HOST = "localhost"
DB_NAME = "btu_bim"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_PORT = "5432"

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
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
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
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

