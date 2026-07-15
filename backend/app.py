from flask import Flask, render_template, request
from scholarship_engine import recommend_scholarships
import csv
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "gender": request.form["gender"],
            "state": request.form["state"],
            "college": request.form["college"],
            "course": request.form["course"],
            "percentage": request.form["percentage"],
            "income": request.form["income"],
            "category": request.form["category"]
        }

        # Save student details to students.csv
        students_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "students.csv"
        )

        file_exists = os.path.isfile(students_file)

        with open(students_file, "a", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Name",
                    "Email",
                    "Phone",
                    "Gender",
                    "State",
                    "College",
                    "Course",
                    "Percentage",
                    "Income",
                    "Category"
                ])

            writer.writerow([
                student["name"],
                student["email"],
                student["phone"],
                student["gender"],
                student["state"],
                student["college"],
                student["course"],
                student["percentage"],
                student["income"],
                student["category"]
            ])

        # Get scholarship recommendations
        scholarships = recommend_scholarships(student)

        return render_template(
            "result.html",
            student=student,
            scholarships=scholarships
        )

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    students = []

    students_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "students.csv"
    )

    if os.path.exists(students_file):

        with open(students_file, "r", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:
                students.append(row)

    return render_template(
        "dashboard.html",
        students=students
    )


@app.route("/result")
def result():
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)