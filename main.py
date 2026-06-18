import os
from grade_calculator import process_csv
from report_generator import save_csv_report, save_text_report

INPUT_FILE = "data/marks.csv"
OUTPUT_CSV = "output/results.csv"
OUTPUT_TEXT = "output/report.txt"
MAX_MARKS = 100

def print_separator():
    print("-"* 55)
    
def print_results_table(results):
    print(f"\n{'Rank': <6} {'Name':<25} {'%':>6}  {'Grade':<4}  {'Result'}")
    print_separator()
    
    for r in results:
        result_str = "PASS" if r["passed"] else "FAIL"
        print(f"{r['rank']:<6} {r['name']:<25} {r['percentage']:.1f}%  {r['overall_grade']:<4}  {result_str}")
        
    print_separator()
    
def main():
        print("\n" + "=" * 55)
        print("        STUDENT GRADE CALCULATOR")
        print("=" * 55)
        
        if not os.path.exists(INPUT_FILE):
            print(f"\nError: {INPUT_FILE} not found")
            return
        
        print(f"\nReading from: {INPUT_FILE}")
        
        results = process_csv(INPUT_FILE, max_marks=MAX_MARKS)
        
        print_results_table(results)
        
        passed = sum(1 for r in results if r["passed"])
        failed = len(results) - passed
        class_avg = sum(r["percentage"] for r in results) / len(results)
        
        print(f"\nClass Average : {class_avg:.1f}%")
        print(f"Passed          : {passed} / {len(results)}")
        print(f"Failed          : {failed} / {len(results)}")
        print(f"Topper        : {results[0]['name']} ({results[0]['percentage']}%)")
        
        os.makedirs("output", exist_ok=True)
        print()
        save_csv_report(results, OUTPUT_CSV)
        save_text_report(results, OUTPUT_TEXT)
        
        print("\nDone! Check the output/ folder.")
        
if __name__ == "__main__":
    main()
        