from datetime import datetime
import os
import random
import sqlite3
import time
import flet as ft


def get_db_path():
    return "math_practice.db"


def init_db():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            mode TEXT,
            question TEXT,
            user_ans TEXT,
            correct_ans TEXT,
            status TEXT,
            time REAL,
            comment TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def save_to_db(record):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO history (date, mode, question, user_ans, correct_ans, status, time, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            record["date"],
            record["mode"],
            record["question"],
            record["user_ans"],
            record["correct_ans"],
            record["status"],
            record["time"],
            record["comment"],
        ),
    )
    conn.commit()
    conn.close()


def fetch_from_db():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, mode, question, user_ans, correct_ans, status, time, comment FROM history ORDER BY id DESC"
    )
    rows = cursor.fetchall()
    conn.close()

    history_list = []
    for row in rows:
        history_list.append(
            {
                "date": row[0],
                "mode": row[1],
                "question": row[2],
                "user_ans": row[3],
                "correct_ans": row[4],
                "status": row[5],
                "time": row[6],
                "comment": row[7],
            }
        )
    return history_list


def clear_db():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()


def main(page: ft.Page):
    init_db()
    page.title = "Math Practice Pro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F7FA"

    state = {
        "mode": None,
        "num1": 0,
        "num2": 0,
        "correct_quotient": 0,
        "correct_remainder": 0,
        "correct_answer": 0,
        "score": 0,
        "start_time": 0,
    }

    def generate_problem():
        if state["mode"] == "multiplication":
            state["num1"] = random.randint(1000, 99999)
            digit_choice = random.choice([2, 3])
            if digit_choice == 2:
                state["num2"] = random.randint(10, 99)
            else:
                state["num2"] = random.randint(100, 999)

            state["correct_answer"] = state["num1"] * state["num2"]
        elif state["mode"] == "division":
            state["num2"] = random.randint(2, 99)
            state["num1"] = random.randint(100, 99999)
            state["correct_quotient"] = state["num1"] // state["num2"]
            state["correct_remainder"] = state["num1"] % state["num2"]

    def show_home(e=None):
        state["mode"] = None
        state["score"] = 0
        page.clean()

        header = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.CALCULATE, size=50, color="#3F51B5"),
                    ft.Text(
                        "Math Practice Pro",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1A237E",
                    ),

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
        )

        btn_mul = ft.Button(
            content=ft.Text("Multiplication"),
            on_click=lambda _: start_practice("multiplication"),
            width=260,
            height=50,
        )

        btn_div = ft.Button(
            content=ft.Text("Division"),
            on_click=lambda _: start_practice("division"),
            width=260,
            height=50,
        )

        btn_report = ft.OutlinedButton(
            content=ft.Text("View Performance Report"),
            on_click=lambda _: show_report(),
            width=260,
            height=50,
        )

        page.add(
            ft.Column(
                [header, btn_mul, btn_div, btn_report],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                expand=True,
            )
        )
        page.update()

    def start_practice(mode):
        state["mode"] = mode
        generate_problem()
        show_quiz_screen()

    def show_quiz_screen():
        page.clean()
        state["start_time"] = time.time()

        op_symbol = "×" if state["mode"] == "multiplication" else "÷"
        q_str = f"{state['num1']} {op_symbol} {state['num2']}"

        question_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"{q_str} = ?",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="#0D47A1",
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=20,
                alignment=ft.Alignment(0, 0),
            ),
            elevation=5,
        )

        if state["mode"] == "division":
            quotient_input = ft.TextField(
                label="Vagfol (Quotient)",
                keyboard_type=ft.KeyboardType.NUMBER,
                width=240,
                text_align=ft.TextAlign.CENTER,
                text_size=18,
                border_radius=10,
            )
            remainder_input = ft.TextField(
                label="Vagsesh (Remainder)",
                keyboard_type=ft.KeyboardType.NUMBER,
                width=240,
                text_align=ft.TextAlign.CENTER,
                text_size=18,
                border_radius=10,
            )
            input_controls = [quotient_input, remainder_input]
        else:
            answer_input = ft.TextField(
                label="Tomar answer likho",
                keyboard_type=ft.KeyboardType.NUMBER,
                width=240,
                text_align=ft.TextAlign.CENTER,
                text_size=20,
                border_radius=10,
            )
            input_controls = [answer_input]

        def submit_answer(e):
            end_time = time.time()
            time_taken = round(end_time - state["start_time"], 2)
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                if state["mode"] == "division":
                    if not quotient_input.value or not remainder_input.value:
                        return
                    user_q = int(quotient_input.value)
                    user_r = int(remainder_input.value)

                    is_correct = (user_q == state["correct_quotient"]) and (
                        user_r == state["correct_remainder"]
                    )
                    status = "Correct" if is_correct else "Incorrect"

                    user_ans_str = f"Vagfol: {user_q}, Vagsesh: {user_r}"
                    correct_ans_str = f"Vagfol: {state['correct_quotient']}, Vagsesh: {state['correct_remainder']}"
                else:
                    if not answer_input.value:
                        return
                    user_ans = float(answer_input.value)
                    is_correct = user_ans == state["correct_answer"]
                    status = "Correct" if is_correct else "Incorrect"

                    user_ans_str = str(user_ans)
                    correct_ans_str = str(state["correct_answer"])

                time_comment = ""
                if is_correct:
                    state["score"] += 1
                    if time_taken <= 180:
                        time_comment = "Lightning Fast"
                    elif time_taken <= 240:
                        time_comment = "Great speed"
                    elif time_taken <= 300:
                        time_comment = "Good job"
                    else:
                        time_comment = "You are slow"
                else:
                    time_comment = "You should practice more"

                record = {
                    "date": current_date,
                    "mode": state["mode"],
                    "question": q_str,
                    "user_ans": user_ans_str,
                    "correct_ans": correct_ans_str,
                    "status": status,
                    "time": time_taken,
                    "comment": time_comment,
                }
                save_to_db(record)

                show_next_screen(status, time_taken, correct_ans_str, time_comment)

            except ValueError:
                pass

        submit_btn = ft.Button(
            content=ft.Text("Submit Answer"),
            on_click=submit_answer,
            width=240,
            height=45,
        )

        back_btn = ft.TextButton(
            content=ft.Text("<- Back to Home"), on_click=show_home
        )

        page.add(
            ft.Column(
                [
                    ft.Text(
                        f"Mode: {state['mode'].capitalize()}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#263238",
                    ),
                    question_card,
                    *input_controls,
                    submit_btn,
                    back_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                expand=True,
            )
        )
        page.update()

    def show_next_screen(status, time_taken, correct_ans_str, time_comment):
        page.clean()
        result_color = "#2E7D32" if status == "Correct" else "#C62828"

        summary_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Answer Recorded!",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=result_color,
                        ),
                        ft.Text(
                            f"Result: {time_comment}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#3F51B5",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            f"Sothik Uttar: {correct_ans_str}",
                            color="#37474F",
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            f"Time Taken: {time_taken} seconds",
                            color="#263238",
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text(
                            f"Current Score: {state['score']}",
                            color="#263238",
                            weight=ft.FontWeight.W_500,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=20,
            )
        )

        btn_next = ft.Button(
            content=ft.Text("Next Problem"),
            on_click=lambda _: (generate_problem(), show_quiz_screen()),
            width=240,
            height=45,
        )

        btn_home = ft.OutlinedButton(
            content=ft.Text("Home"), on_click=show_home, width=240, height=45
        )

        page.add(
            ft.Column(
                [summary_card, btn_next, btn_home],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                expand=True,
            )
        )
        page.update()

    def show_report():
        page.clean()
        history_data = fetch_from_db()

        title = ft.Text(
            "Performance Report (Average)",
            size=20,
            weight=ft.FontWeight.BOLD,
            color="#1A237E",
            text_align=ft.TextAlign.CENTER,
        )

        report_list = ft.ListView(expand=1, spacing=10, padding=10, height=320)

        if not history_data:
            report_list.controls.append(
                ft.Text("Kono practice record nei!", italic=True, color="#37474F")
            )
        else:
            total_attempts = len(history_data)
            total_time = sum([item["time"] for item in history_data])
            avg_time = round(total_time / total_attempts, 2)
            correct_count = sum(
                1 for item in history_data if item["status"] == "Correct"
            )

            summary_header = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"Total Solved: {total_attempts}",
                            weight=ft.FontWeight.BOLD,
                            color="#1A237E",
                        ),
                        ft.Text(
                            f"Total Correct: {correct_count} / {total_attempts}",
                            weight=ft.FontWeight.BOLD,
                            color="#2E7D32",
                        ),
                        ft.Text(
                            f"Average Time: {avg_time} sec/problem",
                            weight=ft.FontWeight.BOLD,
                            color="#3F51B5",
                        ),
                    ]
                ),
                padding=10,
                bgcolor="#E8EAF6",
                border_radius=8,
            )
            report_list.controls.append(summary_header)

            for item in history_data:
                report_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                item["date"],
                                                size=11,
                                                color="#546E7A",
                                            ),
                                            ft.Text(
                                                item["status"],
                                                color="#2E7D32"
                                                if item["status"] == "Correct"
                                                else "#C62828",
                                                weight=ft.FontWeight.BOLD,
                                                size=12,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    ft.Text(
                                        f"Q: {item['question']}",
                                        weight=ft.FontWeight.BOLD,
                                        color="#263238",
                                    ),
                                    ft.Text(
                                        f"Your Ans: {item['user_ans']} | Correct: {item['correct_ans']}",
                                        size=12,
                                        color="#37474F",
                                    ),
                                    ft.Text(
                                        f"Comment: {item.get('comment', '')}",
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color="#0D47A1",
                                    ),
                                ],
                                spacing=4,
                            ),
                            padding=10,
                        )
                    )
                )

        def clear_report_click(e):
            clear_db()
            show_report()

        clear_btn = ft.OutlinedButton(
            content=ft.Text("Clear Report", color="#C62828"),
            on_click=clear_report_click,
            width=240,
        )

        back_btn = ft.Button(content=ft.Text("<- Home"), on_click=show_home, width=240)

        page.add(
            ft.Column(
                [title, report_list, clear_btn, back_btn],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True,
            )
        )
        page.update()

    show_home()


ft.run(main)