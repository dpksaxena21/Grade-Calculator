import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from grade_calculator import process_csv
from report_generator import save_csv_report, save_text_report

# ── App settings ─────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GradeCalculatorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Grade Calculator")
        self.geometry("900x650")
        self.resizable(False, False)
        self.csv_path = None

        self._build_ui()

    def _build_ui(self):

        # ── Title ─────────────────────────────────────────────────────────
        title = ctk.CTkLabel(self, text="Grade Calculator",
                             font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(30, 4))

        subtitle = ctk.CTkLabel(self, text="Load a CSV of student marks → get instant results",
                                font=ctk.CTkFont(size=13),
                                text_color="gray")
        subtitle.pack(pady=(0, 20))

        # ── Top controls ──────────────────────────────────────────────────
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=40, pady=(0, 10))

        self.file_label = ctk.CTkLabel(controls, text="No file selected",
                                       font=ctk.CTkFont(size=12),
                                       text_color="gray")
        self.file_label.pack(side="left", padx=(0, 12))

        browse_btn = ctk.CTkButton(controls, text="Browse CSV",
                                   width=120, command=self._browse_file)
        browse_btn.pack(side="left", padx=(0, 8))

        self.max_marks_label = ctk.CTkLabel(controls, text="Max marks:",
                                            font=ctk.CTkFont(size=12))
        self.max_marks_label.pack(side="left", padx=(16, 6))

        self.max_marks_entry = ctk.CTkEntry(controls, width=60,
                                            placeholder_text="100")
        self.max_marks_entry.pack(side="left", padx=(0, 8))
        self.max_marks_entry.insert(0, "100")

        self.run_btn = ctk.CTkButton(controls, text="Calculate Grades",
                                     width=150, state="disabled",
                                     command=self._run)
        self.run_btn.pack(side="left", padx=(8, 0))

        # ── Results table ─────────────────────────────────────────────────
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 10))

        headers = ["Rank", "Student Name", "Total", "Percentage", "Grade", "Result"]
        widths  = [60, 220, 100, 110, 80, 80]

        header_row = ctk.CTkFrame(table_frame, fg_color="#1a1a2e")
        header_row.pack(fill="x", padx=10, pady=(10, 0))

        for h, w in zip(headers, widths):
            ctk.CTkLabel(header_row, text=h, width=w,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#6366F1").pack(side="left", padx=4, pady=8)

        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.row_widths = widths

        # ── Stats bar ─────────────────────────────────────────────────────
        self.stats_frame = ctk.CTkFrame(self, fg_color="#1a1a2e", height=50)
        self.stats_frame.pack(fill="x", padx=40, pady=(0, 10))

        self.stat_labels = {}
        for key in ["Students", "Passed", "Failed", "Average", "Topper"]:
            box = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
            box.pack(side="left", expand=True, padx=10, pady=8)
            ctk.CTkLabel(box, text=key,
                         font=ctk.CTkFont(size=10),
                         text_color="gray").pack()
            lbl = ctk.CTkLabel(box, text="—",
                               font=ctk.CTkFont(size=14, weight="bold"))
            lbl.pack()
            self.stat_labels[key] = lbl

        # ── Export buttons ────────────────────────────────────────────────
        export_frame = ctk.CTkFrame(self, fg_color="transparent")
        export_frame.pack(pady=(0, 20))

        ctk.CTkButton(export_frame, text="Export CSV",
                      width=140, command=self._export_csv).pack(side="left", padx=8)
        ctk.CTkButton(export_frame, text="Export Text Report",
                      width=160, command=self._export_text).pack(side="left", padx=8)

        self.results = None

    # ── Actions ───────────────────────────────────────────────────────────────

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select marks CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        if path:
            self.csv_path = path
            self.file_label.configure(text=os.path.basename(path), text_color="white")
            self.run_btn.configure(state="normal")

    def _run(self):
        if not self.csv_path:
            return
        try:
            max_marks = int(self.max_marks_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Max marks must be a number.")
            return

        self.run_btn.configure(state="disabled", text="Calculating...")
        threading.Thread(target=self._process, args=(max_marks,), daemon=True).start()

    def _process(self, max_marks):
        try:
            self.results = process_csv(self.csv_path, max_marks=max_marks)
            self.after(0, self._display_results)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, lambda: self.run_btn.configure(state="normal", text="Calculate Grades"))

    def _display_results(self):
        # Clear old rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        widths = self.row_widths

        for r in self.results:
            color = "#0f2027" if r["rank"] % 2 == 0 else "transparent"
            row = ctk.CTkFrame(self.scroll_frame, fg_color=color)
            row.pack(fill="x", pady=1)

            result_color = "#22C55E" if r["passed"] else "#EF4444"
            grade_colors = {
                "O": "#818CF8", "A+": "#34D399", "A": "#34D399",
                "B+": "#FCD34D", "B": "#FCD34D", "C": "#FB923C",
                "D": "#F87171", "F": "#EF4444"
            }
            grade_color = grade_colors.get(r["overall_grade"], "white")

            values = [
                (str(r["rank"]),               "white"),
                (r["name"],                    "white"),
                (f"{r['total_obtained']} / {r['total_possible']}", "gray"),
                (f"{r['percentage']}%",        "white"),
                (r["overall_grade"],           grade_color),
                ("PASS" if r["passed"] else "FAIL", result_color),
            ]

            for (val, col), w in zip(values, widths):
                ctk.CTkLabel(row, text=val, width=w,
                             font=ctk.CTkFont(size=12),
                             text_color=col).pack(side="left", padx=4, pady=6)

        # Update stats
        passed    = sum(1 for r in self.results if r["passed"])
        failed    = len(self.results) - passed
        class_avg = sum(r["percentage"] for r in self.results) / len(self.results)
        topper    = self.results[0]["name"].split()[0]

        self.stat_labels["Students"].configure(text=str(len(self.results)))
        self.stat_labels["Passed"].configure(text=str(passed), text_color="#22C55E")
        self.stat_labels["Failed"].configure(text=str(failed), text_color="#EF4444")
        self.stat_labels["Average"].configure(text=f"{class_avg:.1f}%")
        self.stat_labels["Topper"].configure(text=topper, text_color="#818CF8")

        self.run_btn.configure(state="normal", text="Calculate Grades")

    def _export_csv(self):
        if not self.results:
            messagebox.showwarning("No data", "Calculate grades first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV", "*.csv")],
                                            initialfile="results.csv")
        if path:
            save_csv_report(self.results, path)
            messagebox.showinfo("Saved", f"CSV saved to:\n{path}")

    def _export_text(self):
        if not self.results:
            messagebox.showwarning("No data", "Calculate grades first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text", "*.txt")],
                                            initialfile="report.txt")
        if path:
            save_text_report(self.results, path)
            messagebox.showinfo("Saved", f"Report saved to:\n{path}")


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = GradeCalculatorApp()
    app.mainloop()