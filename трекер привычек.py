import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import date, timedelta

DATA_FILE = "habits.json"


class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱  Трекер привычек")
        self.root.geometry("480x550")
        self.root.configure(bg="#f4f6f8")

        self.habits = self.load_data()

        # Заголовок
        title = tk.Label(
            root, text="Мои привычки",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f6f8", fg="#2c3e50"
        )
        title.pack(pady=15)

        # Список привычек
        self.frame = tk.Frame(root, bg="#f4f6f8")
        self.frame.pack(fill="both", expand=True, padx=20)

        # Кнопки
        btn_frame = tk.Frame(root, bg="#f4f6f8")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="➕ Добавить", command=self.add_habit,
            bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", padx=15, pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame, text="💾  Сохранить", command=self.save_data,
            bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", padx=15, pady=8
        ).pack(side="left", padx=5)

        self.refresh()

    # ---------- Данные ----------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.habits, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Сохранено", "Данные успешно сохранены!")

    # ---------- Логика ----------
    def today_str(self):
        return date.today().isoformat()

    def calc_streak(self, habit):
        """Считаем текущую серию подряд идущих дней."""
        streak = 0
        day = date.today()
        while day.isoformat() in habit["done"]:
            streak += 1
            day -= timedelta(days=1)
        return streak

    def add_habit(self):
        name = simpledialog.askstring("Новая привычка", "Название:")
        if name and name.strip():
            self.habits.append({"name": name.strip(), "done": []})
            self.refresh()
            self.save_data()

    def remove_habit(self, habit):
        if messagebox.askyesno("Удалить", f"Удалить «{habit['name']}»?"):
            self.habits.remove(habit)
            self.refresh()
            self.save_data()

    def toggle_today(self, habit):
        today = self.today_str()
        if today in habit["done"]:
            habit["done"].remove(today)
        else:
            habit["done"].append(today)
        self.refresh()
        self.save_data()

    # ---------- Отрисовка ----------
    def refresh(self):
        for w in self.frame.winfo_children():
            w.destroy()

        today = self.today_str()

        if not self.habits:
            tk.Label(
                self.frame, text="Пока нет привычек.\nДобавьте первую!",
                font=("Segoe UI", 11), bg="#f4f6f8", fg="#7f8c8d"
            ).pack(pady=30)
            return

        for habit in self.habits:
            done_today = today in habit["done"]
            streak = self.calc_streak(habit)

            card = tk.Frame(self.frame, bg="white", bd=0, relief="flat")
            card.pack(fill="x", pady=6, ipady=8)

            # Кнопка-чекбокс
            mark = "✔" if done_today else "○"
            btn = tk.Button(
                card, text=mark, width=3,
                font=("Segoe UI", 14, "bold"),
                bg="#27ae60" if done_today else "#ecf0f1",
                fg="white" if done_today else "#7f8c8d",
                relief="flat",
                command=lambda h=habit: self.toggle_today(h)
            )
            btn.pack(side="left", padx=10)

            # Название и серия
            info = tk.Frame(card, bg="white")
            info.pack(side="left", fill="x", expand=True)
            tk.Label(
                info, text=habit["name"], font=("Segoe UI", 12, "bold"),
                bg="white", fg="#2c3e50", anchor="w"
            ).pack(anchor="w")
            tk.Label(
                info, text=f"🔥  Серия: {streak} дн.   |   Всего: {len(habit['done'])}",
                font=("Segoe UI", 9), bg="white", fg="#7f8c8d", anchor="w"
            ).pack(anchor="w")

            # Удалить
            tk.Button(
                card, text="✕", font=("Segoe UI", 11),
                bg="white", fg="#e74c3c", relief="flat",
                command=lambda h=habit: self.remove_habit(h)
            ).pack(side="right", padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()