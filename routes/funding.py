# Funding & Investor Relations Routes for 9-Table Database Architecture
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.funding_service import FundingService
from services.startup_service import StartupService

funding_bp = Blueprint('funding', __name__)

# ----------------------------------------------------
# Funding Rounds
# ----------------------------------------------------
@funding_bp.route('/')
@funding_bp.route('/rounds')
def rounds_list():
    """Lists all funding rounds across portfolio startups."""
    rounds = FundingService.get_funding_rounds()
    return render_template('funding/rounds_list.html', rounds=rounds)

@funding_bp.route('/rounds/create', methods=['GET', 'POST'])
def round_create():
    """Opens a new funding round for a startup."""
    if 'user_id' not in session:
        flash('Please login to create a funding round.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        startup_id = request.form.get('startup_id')
        round_type = request.form.get('round_type', 'Seed').strip()
        target_amount = request.form.get('target_amount', 0)
        status = request.form.get('status', 'open')
        
        if not startup_id or not round_type:
            flash('Please select a startup and specify round type.', 'danger')
            return redirect(url_for('funding.round_create'))

        FundingService.create_funding_round(startup_id, round_type, target_amount, status)
        flash('Funding round created successfully!', 'success')
        return redirect(url_for('funding.rounds_list'))
        
    startups = StartupService.get_all_startups()
    return render_template('funding/round_create.html', startups=startups)

@funding_bp.route('/rounds/<int:round_id>')
def round_detail(round_id):
    """Views round progress, investors participating, and allocation tickets."""
    round_data = FundingService.get_funding_round_by_id(round_id)
    if not round_data:
        flash('Funding round not found.', 'danger')
        return redirect(url_for('funding.rounds_list'))

    investments = FundingService.get_round_investments(round_id)
    investors = FundingService.get_investors()
    return render_template('funding/round_detail.html', round=round_data, investments=investments, investors=investors)

@funding_bp.route('/rounds/<int:round_id>/close', methods=['POST'])
def round_close(round_id):
    """Closes an active funding round."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    FundingService.close_round(round_id)
    flash('Funding round marked as closed.', 'info')
    return redirect(url_for('funding.round_detail', round_id=round_id))

# ----------------------------------------------------
# Investments (Transactions)
# ----------------------------------------------------
@funding_bp.route('/rounds/<int:round_id>/invest', methods=['POST'])
def add_investment(round_id):
    """Records an investment ticket into INVESTMENTS table."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    investor_id = request.form.get('investor_id')
    amount = request.form.get('amount')
    
    if not investor_id or not amount:
        flash('Please select an investor and enter an investment amount.', 'danger')
        return redirect(url_for('funding.round_detail', round_id=round_id))
        
    try:
        FundingService.add_investment_transaction(round_id, investor_id, amount)
        flash(f'Successfully recorded investment of ${float(amount):,.2f}!', 'success')
    except Exception as e:
        flash(f'Error recording investment: {e}', 'danger')
        
    return redirect(url_for('funding.round_detail', round_id=round_id))

# ----------------------------------------------------
# Investors
# ----------------------------------------------------
@funding_bp.route('/investors')
def investors_list():
    """Lists investor directory with total capital deployed."""
    investors = FundingService.get_investors()
    return render_template('funding/investors_list.html', investors=investors)

@funding_bp.route('/investors/create', methods=['GET', 'POST'])
def investor_create():
    """Registers a new accredited investor."""
    if 'user_id' not in session:
        flash('Please login to register an investor.', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        firm_name = request.form.get('firm_name', '').strip()
        
        if not name or not email:
            flash('Investor name and email are required.', 'danger')
            return redirect(url_for('funding.investor_create'))

        FundingService.create_investor(name, email, phone, firm_name)
        flash(f'Investor "{name}" registered successfully!', 'success')
        return redirect(url_for('funding.investors_list'))
        
    return render_template('funding/investor_create.html')
