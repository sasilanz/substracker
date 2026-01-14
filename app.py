from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Subscription
from datetime import datetime
import os

app = Flask(__name__)

# Konfiguration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscriptions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Datenbankinitialisierung
db.init_app(app)

@app.before_request
def create_tables():
    """Erstelle Tabellen falls nicht vorhanden"""
    db.create_all()

@app.route('/')
def index():
    """Dashboard mit allen Subscriptions, sortiert nach Fälligkeitsdatum"""
    subscriptions = Subscription.query.order_by(Subscription.due_date).all()
    
    # Berechne Gesamtbudget und nächste Zahlungen
    total_monthly = sum(s.amount for s in subscriptions if s.cycle == 'monthly')
    total_yearly = sum(s.amount for s in subscriptions if s.cycle == 'yearly')
    
    return render_template('index.html', 
                         subscriptions=subscriptions,
                         total_monthly=total_monthly,
                         total_yearly=total_yearly)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Neue Subscription hinzufügen"""
    if request.method == 'POST':
        try:
            subscription = Subscription(
                name=request.form['name'],
                amount=float(request.form['amount']),
                cycle=request.form['cycle'],
                due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date(),
                login=request.form.get('login', ''),
                password=request.form.get('password', ''),
                notes=request.form.get('notes', '')
            )
            db.session.add(subscription)
            db.session.commit()
            flash(f'Subscription "{subscription.name}" erfolgreich hinzugefügt!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Fehler: {str(e)}', 'error')
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Subscription bearbeiten"""
    subscription = Subscription.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            subscription.name = request.form['name']
            subscription.amount = float(request.form['amount'])
            subscription.cycle = request.form['cycle']
            subscription.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
            subscription.login = request.form.get('login', '')
            subscription.password = request.form.get('password', '')
            subscription.notes = request.form.get('notes', '')
            
            db.session.commit()
            flash(f'Subscription "{subscription.name}" erfolgreich aktualisiert!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Fehler: {str(e)}', 'error')
    
    return render_template('edit.html', subscription=subscription)

@app.route('/delete/<int:id>')
def delete(id):
    """Subscription löschen"""
    subscription = Subscription.query.get_or_404(id)
    name = subscription.name
    
    try:
        db.session.delete(subscription)
        db.session.commit()
        flash(f'Subscription "{name}" erfolgreich gelöscht!', 'success')
    except Exception as e:
        flash(f'Fehler: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
