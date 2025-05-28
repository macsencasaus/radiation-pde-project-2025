import os

import numpy as np
from flask import Flask, Response, jsonify, request, send_from_directory

from src.fixed_point import source_iteration
from src.input_data import InputData
from src.mesh import Mesh

app = Flask(__name__, static_folder="../frontend/dist")

@app.route("/", methods=["GET"])
def home() -> Response:
    return send_from_directory(str(app.static_folder), "index.html")

@app.route("/<path:filename>")
def serve_file(filename) -> Response:
    return send_from_directory(str(app.static_folder), filename)


@app.route("/api/solve", methods=["POST"])
def solve() -> Response:
    data = request.get_json()

    if data is None:
        return Response({"error": "Invalid JSON"}, 400)

    try:
        input_data = InputData(**data)
        mesh = Mesh(input_data)

        n_angles = data["n_angles"]
        tol = data["tol"]
        max_iter = data["max_iter"]

        start_phi = np.zeros(mesh.n_points)

        phi = source_iteration(
            start_phi=start_phi,
            n_angles=n_angles,
            mesh=mesh,
            data=input_data,
            tol=tol,
            max_iter=max_iter,
        )

        return jsonify({"phi": list(phi), "gridpoints": list(mesh.gridpoints)})
        
    except Exception as e:
        return Response({"error": e}, 500)


if __name__ == "__main__":
    port = os.environ.get("PORT")

    if port:
        port = int(port)
    else:
        port = 8080

    app.run(port=port)
