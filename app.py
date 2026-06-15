from flask import Flask, render_template, request, redirect, session
import random
from quiz_data import paket_kuis

app = Flask(__name__)
app.secret_key = "ryvaquiz"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/roll")
def roll():
    session["paket"] = random.randint(1,5)
    session["nomor"] = 1
    session["skor"] = 0
    return redirect("/question")

@app.route("/question", methods=["GET","POST"])
def question():
    paket = paket_kuis[session["paket"]]
    nomor = session["nomor"]

    if request.method == "POST":
        soal = paket["soal"][nomor]
        j = request.form["jawaban"].strip()

        if isinstance(soal["kunci"], list):
            if j.lower() in soal["kunci"]:
                session["skor"] += 20
        else:
            if j.upper() == soal["kunci"]:
                session["skor"] += 20

        session["nomor"] += 1
        if session["nomor"] > 5:
            return redirect("/result")
        return redirect("/question")

    soal = paket["soal"][nomor]
    return render_template("question.html", paket=paket["nama"], nomor=nomor, soal=soal)

@app.route("/result")
def result():
    return render_template("result.html", skor=session.get("skor",0))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
