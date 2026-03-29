from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

model = joblib.load("house_model.pkl")

def generate_floor_plan_svg(length, width, bedrooms, bathrooms, balcony):
    W, H = 760, 540
    margin = 20
    rooms = []

    living_w = int(W * 0.4)
    living_h = int(H * 0.35)
    rooms.append(("Living Room", margin, margin + 40, living_w, living_h, "#E8F4F8"))

    kitchen_w = int(W * 0.3)
    rooms.append(("Kitchen", margin + living_w + 10, margin + 40, kitchen_w, living_h, "#FFF8E7"))

    dining_w = W - living_w - kitchen_w - 30
    rooms.append(("Dining Area", margin + living_w + kitchen_w + 20, margin + 40, dining_w, living_h, "#F0FFF0"))

    bed_w = int(W / max(bedrooms, 1)) - 10
    bed_h = int(H * 0.3)
    for i in range(bedrooms):
        x = margin + i * (bed_w + 10)
        y = margin + 40 + living_h + 20
        rooms.append((f"Bedroom {i+1}", x, y, bed_w, bed_h, "#FFF0F5"))

    bath_w = int(W / max(bathrooms, 1) * 0.45)
    bath_h = int(H * 0.18)
    for i in range(bathrooms):
        x = margin + i * (bath_w + 10)
        y = margin + 40 + living_h + bed_h + 30
        rooms.append((f"Bath {i+1}", x, y, bath_w, bath_h, "#F0F8FF"))

    if balcony > 0:
        rooms.append(("Balcony", W - 160, H - 90, 150, 75, "#F5F5DC"))

    svg = f'<svg viewBox="0 0 800 600" width="800" height="600" xmlns="http://www.w3.org/2000/svg">'
    svg += '<rect width="800" height="600" fill="#FAFAFA"/>'
    svg += '<rect x="5" y="5" width="790" height="590" fill="none" stroke="#222" stroke-width="3"/>'
    svg += f'<text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#222">{bedrooms}BHK Floor Plan — {int(length)}ft x {int(width)}ft</text>'

    for (name, x, y, w, h, color) in rooms:
        svg += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="#444" stroke-width="2"/>'
        cx = x + w // 2
        cy = y + h // 2
        svg += f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" font-size="13" font-weight="bold" fill="#333">{name}</text>'

    svg += '</svg>'
    return svg

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        length = float(request.form.get("length"))
        width  = float(request.form.get("width"))
        area   = length * width

        prediction = model.predict([[length, width, area]])[0]
        bedrooms  = int(prediction[0])
        bathrooms = int(prediction[1])
        balcony   = int(prediction[2])

        svg_plan = generate_floor_plan_svg(length, width, bedrooms, bathrooms, balcony)

        return jsonify({
            "bedrooms":  bedrooms,
            "bathrooms": bathrooms,
            "balcony":   balcony,
            "area":      area,
            "length":    length,
            "width":     width,
            "svg_plan":  svg_plan
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)