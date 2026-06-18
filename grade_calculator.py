import os
import csv


def get_grade(Percentage):
    if Percentage >= 90:
        return 'O'
    elif Percentage >= 80 and Percentage < 90:
        return 'A+'
    elif Percentage >= 70 and Percentage < 80:
        return 'A'
    elif Percentage >= 60 and Percentage < 70:
        return 'B+'
    elif Percentage >= 50 and Percentage < 60:
        return 'B'
    elif Percentage >= 40 and Percentage < 50:
        return 'C'
    elif Percentage >= 33 and Percentage < 40: 
        return 'D'
    else:
        return 'F'
    
def get_grade_description(grade):
    description = {
        "O": "Outstanding",
        "A+": "Excellent",
        "A": "Very Good",
        "B+": "Good",
        "B": "Above Average",
        "C": "Average",
        "D": "Below Average",
        "F": "Fail"
    }
    return description[grade]

def calculate_student_result( student_name, subject_marks, max_marks = 100):
    total_obtained = sum(subject_marks.values())
    total_possible = max_marks * len(subject_marks)
    percentage = (total_obtained / total_possible) * 100
    
    overall_grade = get_grade(percentage)
    
    failed_subjects = []
    subject_results = {}
    
    for subject, marks in subject_marks.items():
        subject_pct = (marks/max_marks) * 100
        subject_grade = get_grade(subject_pct)
        subject_results[subject] = {
            "marks": marks,
            "max_marks": max_marks,
            "percentage": round(subject_pct, 1),
            "grade": subject_grade
        }
        if subject_pct < 33:
            failed_subjects.append(subject)
    
    result = {
        "name": student_name,
        "total_obtained": total_obtained,
        "total_possible": total_possible,
        "percentage": round(percentage, 1),
        "overall_grade": overall_grade,
        "grade_desc": get_grade_description(overall_grade),
        "passed": len(failed_subjects) == 0,
        "failed_subjects": failed_subjects,
        "subjects": subject_results, 
        "rank": None
    }
    
    return result

def process_csv(filepath, max_marks = 100): 
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    results = []
    
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            student_name = row["Student Name"].strip()
            
            subject_marks = {}
            for subject, marks_str in row.items():
                if subject == "Student Name":
                    continue
                marks = float(marks_str.strip())
                subject_marks[subject] = marks
            result = calculate_student_result(student_name, subject_marks, max_marks)
            results.append(result)
    results.sort(key=lambda x: x["percentage"], reverse=True)
    for i, result in enumerate(results):
        result["rank"] = i + 1
    return results