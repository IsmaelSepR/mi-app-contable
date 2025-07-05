from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from mi_app import db
from mi_app.models import Transaction
from mi_app.forms import TransactionForm
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(owner=current_user).order_by(Transaction.date.desc()).all()
    
    balance = 0
    ingresos = 0
    gastos = 0
    for t in transactions:
        if t.type == 'ingreso':
            balance += t.amount
            ingresos += t.amount
        else:
            balance -= t.amount
            gastos += t.amount

    return render_template('dashboard.html', title='Dashboard', transactions=transactions, balance=balance, ingresos=ingresos, gastos=gastos)

@main_bp.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            description=form.description.data,
            amount=form.amount.data,
            date=form.date.data,
            type=form.type.data,
            owner=current_user
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaccion anadida con exito.', 'success')
        return redirect(url_for('main.dashboard'))
    
    if not form.date.data:
        form.date.data = datetime.utcnow().date()
        
    return render_template('transaction_form.html', title='Anadir Transaccion', form=form, legend='Nueva Transaccion')

@main_bp.route('/transaction/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.owner != current_user:
        abort(403)
    
    form = TransactionForm(obj=transaction)
    if form.validate_on_submit():
        form.populate_obj(transaction)
        db.session.commit()
        flash('Transaccion actualizada con exito.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('transaction_form.html', title='Editar Transaccion', form=form, legend='Editar Transaccion')

@main_bp.route('/transaction/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.owner != current_user:
        abort(403)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaccion eliminada con exito.', 'info')
    return redirect(url_for('main.dashboard'))



