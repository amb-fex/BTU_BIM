from flask import Flask, request, jsonify, render_template
import psycopg2
import os
import json

app = Flask(__name__)

# URL de conexión a la base de datos (Render)
DATABASE_URL = "postgresql://btu_bim_user:yOs3ITKc3EKTKbF3Yx0gaOypi5g5HvI4@dpg-cu72o123esus73ffd48g-a/btu_bim"

# Conexión global a la base de datos
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    conn = None  # Asegurarnos de manejar esto en caso de error


# Ruta principal para servir el formulario HTML
@app.route("/", methods=["GET"])
def home():
    return render_template("formulario.html")


# Ruta para manejar el envío del formulario
@app.route("/submit", methods=["POST"])
def submit_data():
    try:
        # Leer los datos enviados desde el formulario
        data = request.get_json()
        if not data:
            return jsonify({"error": "Solicitud vacía o no válida"}), 400

        # Validar campos obligatorios
        required_fields = ["modo", "categoria", "elemento", "tipo", "geometria"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}), 400

        # Validar que la categoría sea válida
        categorias_validas = [
            "Mapa Base", "Curvas de Nivel", "Límites Administrativos",
            "Red Hidrográfica", "Red Vial", "Edificaciones", "Uso del Suelo",
            "Cobertura Vegetal", "Infraestructura de Servicios", "Puntos de Interés"
        ]
        if data["categoria"] not in categorias_validas:
            return jsonify({"error": "Categoría no válida"}), 400

        # Obtener datos
        modo = data["modo"]
        categoria = data["categoria"]
        elemento = data["elemento"]
        descripcion = data.get("descripcion", "")
        tipo = data["tipo"]
        geometria = data["geometria"]
        terreno = json.dumps(data.get("terreno", []))  # Convertir lista de terreno a JSON
        captacion = data.get("captacion", "")
        observaciones = data.get("observaciones", "")

        cur = conn.cursor()

        if modo == "actualizar":
            # Actualizar registro existente
            cur.execute("""
                UPDATE datos_btu_bim
                SET categoria=%s, descripcion=%s, tipo=%s, geometria=%s, terreno=%s, captacion=%s, observaciones=%s
                WHERE elemento_objeto=%s
            """, (categoria, descripcion, tipo, geometria, terreno, captacion, observaciones, elemento))
            mensaje = "Registro actualizado con éxito."
        else:
            # Agregar un nuevo registro
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


# Mantener viva la app (Keep-Alive)
@app.route("/keep-alive", methods=["GET"])
def keep_alive():
    return jsonify({"message": "La app está activa"}), 200


if __name__ == "__main__":
    # Puerto dinámico para Render
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
