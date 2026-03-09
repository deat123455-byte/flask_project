"""
Секретная база данных агентов разведки
Spy Database Management System
"""
import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret-agent-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Модель агента
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    access_level = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Agent {self.code_name}>'


# Генератор случайных кодовых имен
def generate_code_name():
    adjectives = ['Shadow', 'Black', 'White', 'Red', 'Blue', 'Silent', 'Dark', 'Swift', 'Iron', 'Ghost', 'Night', 'Storm']
    nouns = ['Fox', 'Wolf', 'Eagle', 'Hawk', 'Viper', 'Raven', 'Tiger', 'Falcon', 'Cobra', 'Panther', 'Owl', 'Dragon']
    return f"{random.choice(adjectives)} {random.choice(nouns)}"


# Главная страница - список всех агентов
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    access_filter = request.args.get('access_level', '')
    
    query = Agent.query
    
    if search_query:
        query = query.filter(Agent.code_name.ilike(f'%{search_query}%'))
    
    if access_filter:
        query = query.filter(Agent.access_level == access_filter)
    
    agents = query.order_by(Agent.id).all()
    
    access_levels = ['Секретно', 'Совершенно секретно', 'Абсолютно секретно', 'Особый доступ']
    
    return render_template('index.html', 
                         agents=agents, 
                         search_query=search_query,
                         access_filter=access_filter,
                         access_levels=access_levels)


# Добавление нового агента
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        code_name = request.form.get('code_name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        access_level = request.form.get('access_level', '').strip()
        
        if not all([code_name, phone, email, access_level]):
            flash('Все поля обязательны для заполнения!', 'error')
            return redirect(url_for('add_agent'))
        
        new_agent = Agent(
            code_name=code_name,
            phone=phone,
            email=email,
            access_level=access_level
        )
        
        db.session.add(new_agent)
        db.session.commit()
        
        flash(f'Агент "{code_name}" успешно добавлен в базу!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html', code_names=[])


# Просмотр досье агента
@app.route('/agent/<int:id>')
def view_agent(id):
    agent = Agent.query.get_or_404(id)
    return render_template('agent.html', agent=agent)


# Редактирование данных агента
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)
    
    if request.method == 'POST':
        agent.code_name = request.form.get('code_name', '').strip()
        agent.phone = request.form.get('phone', '').strip()
        agent.email = request.form.get('email', '').strip()
        agent.access_level = request.form.get('access_level', '').strip()
        
        if not all([agent.code_name, agent.phone, agent.email, agent.access_level]):
            flash('Все поля обязательны для заполнения!', 'error')
            return redirect(url_for('edit_agent', id=id))
        
        db.session.commit()
        flash(f'Досье агента "{agent.code_name}" обновлено!', 'success')
        return redirect(url_for('view_agent', id=id))
    
    return render_template('edit.html', agent=agent)


# Удаление агента
@app.route('/delete/<int:id>', methods=['POST'])
def delete_agent(id):
    agent = Agent.query.get_or_404(id)
    code_name = agent.code_name
    
    db.session.delete(agent)
    db.session.commit()
    
    flash(f'Досье агента "{code_name}" уничтожено!', 'warning')
    return redirect(url_for('index'))


# Секретный режим - удаление всех данных
@app.route('/nuke', methods=['POST'])
def nuke_database():
    Agent.query.delete()
    db.session.commit()
    flash('⚠️ ВСЕ ДАННЫЕ УНИЧТОЖЕНЫ! База данных очищена!', 'danger')
    return redirect(url_for('index'))


# Отправка сообщения (имитация)
@app.route('/send-message/<int:id>', methods=['POST'])
def send_message(id):
    agent = Agent.query.get_or_404(id)
    flash(f'📩 Шифрованное сообщение отправлено на {agent.email}', 'info')
    return redirect(url_for('view_agent', id=id))


# Инициализация БД
def init_db():
    with app.app_context():
        db.create_all()
        print("База данных инициализирована!")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
