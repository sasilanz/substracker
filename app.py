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
    """Dashboard mit allen Subscriptions, sortiert nach Vertragsende"""
    subscriptions = Subscription.query.order_by(Subscription.contract_end.asc().nullslast(), Subscription.name).all()
    
    # Berechne Gesamtbudget nach Währung gruppiert
    totals = {}
    for sub in subscriptions:
        currency = sub.currency
        if currency not in totals:
            totals[currency] = {'monthly': 0, 'yearly': 0}
        
        if sub.cycle == 'monthly':
            totals[currency]['monthly'] += sub.amount
            totals[currency]['yearly'] += sub.amount * 12
        elif sub.cycle == 'quarterly':
            totals[currency]['monthly'] += sub.amount / 3
            totals[currency]['yearly'] += sub.amount * 4
        elif sub.cycle == 'semi-annually':
            totals[currency]['monthly'] += sub.amount / 6
            totals[currency]['yearly'] += sub.amount * 2
        elif sub.cycle == 'yearly':
            totals[currency]['monthly'] += sub.amount / 12
            totals[currency]['yearly'] += sub.amount
        elif sub.cycle == 'biennial':
            totals[currency]['monthly'] += sub.amount / 24
            totals[currency]['yearly'] += sub.amount / 2
    
    return render_template('index.html', 
                         subscriptions=subscriptions,
                         totals=totals)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Neue Subscription hinzufügen"""
    if request.method == 'POST':
        try:
            payment_day = request.form.get('payment_day')
            contract_end = request.form.get('contract_end')
            subscription = Subscription(
                name=request.form['name'],
                amount=float(request.form['amount']),
                currency=request.form.get('currency', 'CHF'),
                cycle=request.form['cycle'],
                payment_day=int(payment_day) if payment_day else None,
                cancellation_period=request.form.get('cancellation_period', ''),
                contract_end=datetime.strptime(contract_end, '%Y-%m-%d').date() if contract_end else None,
                website=request.form.get('website', ''),
                login=request.form.get('login', ''),
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
            payment_day = request.form.get('payment_day')
            contract_end = request.form.get('contract_end')
            subscription.name = request.form['name']
            subscription.amount = float(request.form['amount'])
            subscription.currency = request.form.get('currency', 'CHF')
            subscription.cycle = request.form['cycle']
            subscription.payment_day = int(payment_day) if payment_day else None
            subscription.cancellation_period = request.form.get('cancellation_period', '')
            subscription.contract_end = datetime.strptime(contract_end, '%Y-%m-%d').date() if contract_end else None
            subscription.website = request.form.get('website', '')
            subscription.login = request.form.get('login', '')
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
    app.run(debug=True, host='0.0.0.0', port=4999)
