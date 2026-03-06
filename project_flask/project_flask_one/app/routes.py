import random
from flask import render_template, request, redirect, url_for
from app import app

# Список шуток для отображения на странице результата
JOKES = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что 31 OCT = 25 DEC! 🎃",
    "Сколько программистов нужно, чтобы поменять лампочку? Ни одного, это проблема аппаратная! 💡",
    "Почему Java и JavaScript — это как автомобиль и ковёр? 🚗🧙",
    "В чём разница между программистом и Богом? Бог не считает себя программистом! 😄",
    "Почему программисты предпочитают тёмную тему? Потому что свет привлекает баги! 🌙",
    "Жизнь программиста: 99 проблем, но код не тот! 💻",
    "Почему программисты не любят природу? Там слишком много багов! 🐛",
    "Что сказал программист, когда увидел красивую девушку? «Хочу посмотреть твой код!» 💕",
]

# Словарь профессий для отображения
PROFESSIONS = {
    "developer": "Разработчик",
    "designer": "Дизайнер",
    "manager": "Менеджер",
    "analyst": "Аналитик",
    "tester": "Тестировщик",
    "devops": "DevOps-инженер",
    "student": "Студент",
    "other": "Другое"
}

# Словарь типов пользователей
USER_TYPES = {
    "newbie": "Новичок",
    "advanced": "Продвинутый",
    "pro": "Профи"
}

# Словарь увлечений
HOBBIES = {
    "books": "книги",
    "sport": "спорт",
    "games": "игры",
    "music": "музыка",
    "travel": "путешествия"
}


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        # Получаем данные из формы
        name = request.form.get("name", "Незнакомец")
        email = request.form.get("email", "")
        color = request.form.get("color", "#3498db")
        profession = request.form.get("profession", "")
        user_type = request.form.get("user_type", "newbie")
        
        # Получаем список увлечений
        hobbies_list = request.form.getlist("hobbies")
        
        # Преобразуем в читаемый вид
        profession_name = PROFESSIONS.get(profession, profession)
        user_type_name = USER_TYPES.get(user_type, user_type)
        hobbies_names = [HOBBIES.get(h, h) for h in hobbies_list]
        
        # Выбираем случайную шутку
        random_joke = random.choice(JOKES)
        
        return render_template(
            "result.html",
            name=name,
            email=email,
            color=color,
            profession=profession_name,
            user_type=user_type_name,
            hobbies=hobbies_names,
            joke=random_joke
        )
    else:
        return redirect(url_for("form"))
