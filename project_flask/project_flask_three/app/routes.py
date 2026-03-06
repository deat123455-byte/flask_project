import re
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from app import app


def validate_email(email):
    """Проверка корректности email адреса."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@app.route('/')
def home():
    """Главная страница приложения."""
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime('%A, %B %d, %Y, %H:%M:%S')
    return render_template('index.html', current_date=formatted_date)


@app.route('/about')
def about():
    """Страница 'О нас'."""
    team_members = [
        {'name': 'Alice', 'role': 'Developer'},
        {'name': 'Bob', 'role': 'Designer'},
        {'name': 'Charlie', 'role': 'Project Manager'}
    ]
    return render_template('about.html', team_members=team_members)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Страница контактов с формой обратной связи."""
    contact_info = {
        'department': 'Отдел заботы о клиентах',
        'manager': 'John Smith',
        'email': 'support@example.com',
        'phone': '+1 (555) 123-4567',
        'address': {
            'street': 'ул. Примерная, д. 10, оф. 5',
            'city': 'Москва',
            'postal_code': '101000',
            'country': 'Россия'
        }
    }
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        errors = []

        if not name:
            errors.append('Имя является обязательным полем.')

        if not email:
            errors.append('Email является обязательным полем.')
        elif not validate_email(email):
            errors.append('Некорректный формат email адреса.')

        if not message:
            errors.append('Сообщение является обязательным полем.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('contact.html', name=name, email=email, message=message, contact_info=contact_info)

        flash('Ваше сообщение успешно отправлено!', 'success')
        return redirect(url_for('success'))

    return render_template('contact.html', contact_info=contact_info)


@app.route('/success')
def success():
    """Страница подтверждения успешной отправки формы."""
    return render_template('success.html')
