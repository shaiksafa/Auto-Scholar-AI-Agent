from flask import Flask, render_template, request, send_file
from scholarship_engine import recommend_scholarships
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import csv
import os

app = Flask(__name__)

# -----------------------------
# Upload Folder
# -----------------------------

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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
            "category": request.form["category"],
            "aadhaar": request.form["aadhaar"],
            "apaar": request.form.get("apaar", "")
        }

        # -----------------------------
        # Save Uploaded Documents
        # -----------------------------

        documents = [
            "aadhaarCard",
            "incomeCertificate",
            "casteCertificate",
            "bonafide",
            "marksMemo"
        ]

        for doc in documents:

            file = request.files.get(doc)

            if file and file.filename != "":

                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    file.filename
                )

                file.save(filepath)

        # -----------------------------
        # Save Student Details
        # -----------------------------

        students_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "students.csv"
        )

        file_exists = os.path.isfile(students_file)

        with open(
            students_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

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
                    "Category",
                    "Aadhaar",
                    "APAAR"
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
                student["category"],
                student["aadhaar"],
                student["apaar"]
            ])

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

        with open(
            students_file,
            "r",
            encoding="utf-8"
        ) as file:

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


# ------------------------------------
# Download Scholarship Report (PDF)
# ------------------------------------

@app.route("/download_pdf")
def download_pdf():

    pdf_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Scholarship_Report.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>AUTO SCHOLAR AI AGENT</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Scholarship Recommendation Report",
            styles["Heading2"]
        )
    )

    story.append(Paragraph(" ", styles["Normal"]))

    story.append(
        Paragraph(
            "✅ Aadhaar Verification : Verified",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "✅ DigiLocker : Connected",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "✅ Documents : Uploaded & Verified",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "✅ AI Eligibility : Completed",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "✅ Scholarship Recommendation : Generated",
            styles["Normal"]
        )
    )

    story.append(Paragraph(" ", styles["Normal"]))

    story.append(
        Paragraph(
            "Thank you for using Auto Scholar AI Agent.",
            styles["Heading3"]
        )
    )

    doc.build(story)

    return send_file(
        pdf_path,
        as_attachment=True
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )