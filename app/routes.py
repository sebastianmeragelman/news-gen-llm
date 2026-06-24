# app/routes.py


#----------#
DEFINIMOS LAS RUTAS DE LA APLICACION
#----------#


from flask import Blueprint, request, jsonify
from app.services.news_service import generar_noticia

main = Blueprint("main", __name__)

@main.route("/generar-noticia", methods=["POST"])
def generar():
    data = request.json
    resultado = generar_noticia(data["query"])
    return jsonify(resultado)