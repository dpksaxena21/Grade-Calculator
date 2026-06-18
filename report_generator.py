import csv
import os
from datetime import datetime


def save_csv_report(results, output_path):
    subject_names = list(results[0]["subjects"].keys())
    
    fieldnames = ["Rank", "Student Name"] 
    for subject in subject_names:
        fieldnames.append(f"{subject} (Marks)")
        fieldnames.append(f"{subject} (Grade)")
    fieldnames += ["Total", "Max Total", "Percentage", "Overall Grade", "Result"]
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            row = {
                "Rank": r["rank"],
                "Student Name": r["name"],
                "Total": r["total_obtained"],
                "Max Total": r["total_possible"],
                "Percentage": f"{r['percentage']}%",
                "Overall Grade": r["overall_grade"],
                "Result": "PASS" if r["passed"] else "FAIL",
            }
            for subject in subject_names:
                s = r["subjects"][subject]
                row[f"{subject} (Marks)"] = s["marks"]
                row[f"{subject} (Grade)"]= s["grade"]
                
            writer.writerow(row)
    print(f"CSV report saved: {output_path}")
    
def save_text_report( results, output_path):
    
    generated_at = datetime.now().strftime("%d %B %Y, %I:%M %p")
    total_students = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total_students - passed
    class_avg = sum(r["percentage"] for r in results) / total_students
    topper = results[0]
    
    with open(output_path, "w", encoding = "utf-8") as f:
        f.write("="*60 + "\n")
        f.write("           STUDENT GRADE REPORT\n")
        f.write(f"Total Students : {total_students}\n")
        f.write(f"Passed :         {passed}\n")
        f.write(f"Failed :         {failed}\n")
        f.write(f"Class Average :  {class_avg:.1f}%\n")
        f.write(f"Pass Rate : {(passed/total_students)*100:.1f}%\n")
        f.write(f"Class Topper : {topper['name']} ({topper['percentage']}%)\n")
        f.write(f"\n" + "="*60 + "\n\n")
        
        for r in results:
            f.write(f"Rank #{r['rank']}: {r['name']}\n")
            f.write("-" * 40 + "\n")
            
            for subject, data in r["subjects"].items():
                f.write(
                    f"  {subject:<20} {data['marks']:>5} / {data['max_marks']}   ({data['percentage']}%)   {data['grade']}\n"
                )
            
            f.write("-" * 40 + "\n")
            f.write(f"  {'Total':<20} {r['total_obtained']:>5} / {r['total_possible']} ({r['percentage']}%)\n")
            f.write(f"  Overall Grade   : {r['overall_grade']}: {r['grade_desc']}\n")
            f.write(f"  Result          : {'PASS' if r['passed'] else 'FAIL'}\n")
            
            if r["failed_subjects"]:
                f.write(f"  Failed in      : {', '.join(r['failed_subjects'])}\n")
                
            f.write("\n")
            
    print(f"Text report saved: {output_path}")