import csv
import os


def recommend_scholarships(student):

    recommendations = []

    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "dataset", "scholarships.csv")

    with open(file_path, "r") as file:

        reader = csv.DictReader(file)

        for scholarship in reader:

            score = 0

            # Percentage check
            if float(student["percentage"]) >= float(scholarship["Minimum_Percentage"]):
                score += 40

            # Income check
            if float(student["income"]) <= float(scholarship["Maximum_Income"]):
                score += 30

            # Category check
            if scholarship["Category"] == "Any" or scholarship["Category"] == student["category"]:
                score += 15

            # State check
            if scholarship["State"] == "All" or scholarship["State"] == student["state"]:
                score += 10

            # Course check
            if scholarship["Course"] == "Any" or scholarship["Course"] == student["course"]:
                score += 5


            if score >= 50:

                scholarship["Match_Score"] = score

                recommendations.append(scholarship)


    # Highest score first
    recommendations.sort(
        key=lambda x: x["Match_Score"],
        reverse=True
    )

    return recommendations