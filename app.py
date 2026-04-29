from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

skills = {}

def calculate_score():
    score = 0
    for level in skills.values():
        if level == "Beginner":
            score += 1
        elif level == "Intermediate":
            score += 2
        elif level == "Advanced":
            score += 3
    return score

@app.route("/")
def home():
    return render_template("index.html")

# ✅ Add + Update skill
@app.route("/add", methods=["POST"])
def add():
    data = request.json
    skill = data["skill"].lower()
    level = data["level"]

    if not skill:
        return jsonify({"msg": "⚠️ Enter skill"})

    skills[skill] = level
    return jsonify({"msg": f"✅ {skill} set to {level}"})

@app.route("/view")
def view():
    return jsonify(skills)

@app.route("/delete", methods=["POST"])
def delete():
    data = request.json
    skill = data["skill"].lower()

    if skill in skills:
        del skills[skill]
        return jsonify({"msg": "🗑️ Skill deleted"})
    else:
        return jsonify({"msg": "⚠️ Skill not found"})

# ✅ FULL FIXED RECOMMEND FUNCTION
@app.route("/recommend")
def recommend():
    if not skills:
        return jsonify({"msg": "Add skills first"})

    score = calculate_score()
    roles = []
    gaps = []

    levels = list(skills.values())

    # ✅ FIX: overall level based on highest skill
    if "Advanced" in levels:
        level_msg = "Advanced"
    elif "Intermediate" in levels:
        level_msg = "Intermediate"
    else:
        level_msg = "Beginner"

    skill_set = set(skills.keys())

    # Roles logic
    if {"python", "html", "css", "javascript"}.issubset(skill_set):
        roles.append("Full Stack Developer Intern")
    elif {"python", "sql"}.issubset(skill_set):
        roles.append("Backend Developer Intern")
    elif {"html", "css"}.issubset(skill_set):
        roles.append("Frontend Developer Intern")
    elif "python" in skill_set:
        roles.append("Python Developer Intern")

    # Skill gap
    if "python" in skill_set and "html" in skill_set and "css" not in skill_set:
        gaps.append("Learn CSS for Full Stack")

    return jsonify({
        "score": score,
        "level": level_msg,
        "roles": roles,
        "gaps": gaps
    })

if __name__ == "__main__":
    app.run(debug=True)