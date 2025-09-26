import pandas as pd
from datetime import timedelta
from config.settings import (
    PROJECT_START, ACTIVE_LOAN_SCENARIO, ACTIVE_LOAN_STRATEGY, MARKETING_COSTS,
    FOUNDER_SUPPORT_CONFIG, REINVESTMENT_CONFIG, WEB_DESIGNER_CONFIG, 
    VISHAL_CONFIG, EMPLOYEE_COSTS, ROLLING_AVERAGE_MONTHS
)

from src.calculations.customers import (
    calculate_new_customers_from_marketing, calculate_organic_customers,
    distribute_customers_by_package, apply_dynamic_churn, apply_package_upgrades,
    calculate_website_customers, get_cac_for_spend
)
from src.calculations.revenue import (
    calculate_monthly_revenue, calculate_revenue_with_cancellations, calculate_cash_flow
)
from src.calculations.costs import (
    calculate_monthly_variable_costs, calculate_monthly_fixed_costs, 
    calculate_marketing_costs
)
from src.calculations.loans import (
    get_loan_details, allocate_loan_funds, calculate_monthly_marketing_boost,
    apply_team_expansion_benefits, apply_infrastructure_benefits, apply_founder_support_benefits,
    calculate_marketing_boost_efficiency, calculate_loan_balance, calculate_monthly_loan_payment
)

def calculate_vishal_compensation_iterative(preliminary_profit_before_vishal, website_revenue, is_fulltime, max_iterations=5):
    """Calculate Vishal's monthly compensation using iterative approach"""
    current_profit_estimate = preliminary_profit_before_vishal
    
    for iteration in range(max_iterations):
        profit_share_eligible = current_profit_estimate > VISHAL_CONFIG['profit_share_threshold']
        
        if is_fulltime:
            fixed_salary = EMPLOYEE_COSTS.get('vishal_fulltime_salary', 1500)
            profit_share = (current_profit_estimate * VISHAL_CONFIG.get('fulltime_profit_share', 0.03)) if profit_share_eligible else 0
            website_share = 0
        else:
            fixed_salary = 0
            profit_share = (current_profit_estimate * VISHAL_CONFIG.get('freelance_profit_share', 0.20)) if profit_share_eligible else 0
            website_share = website_revenue * VISHAL_CONFIG.get('website_revenue_share', 0.20)
        
        compensation = fixed_salary + profit_share + website_share
        new_profit_estimate = preliminary_profit_before_vishal - compensation
        
        if abs(new_profit_estimate - current_profit_estimate) < 1.0:
            return compensation, fixed_salary, profit_share, website_share
        
        current_profit_estimate = new_profit_estimate
    
    return compensation, fixed_salary, profit_share, website_share

def calculate_founder_support(monthly_profit_after_vishal):
    """Calculate founder support payment with proper bounds checking"""
    if monthly_profit_after_vishal < FOUNDER_SUPPORT_CONFIG['min_profit_threshold']:
        return 0
    
    breakpoints = sorted(FOUNDER_SUPPORT_CONFIG['profit_breakpoints'].keys())
    
    for breakpoint in reversed(breakpoints):
        if monthly_profit_after_vishal >= breakpoint:
            calculated_support = FOUNDER_SUPPORT_CONFIG['profit_breakpoints'][breakpoint]
            max_support = FOUNDER_SUPPORT_CONFIG['max_support']
            return min(calculated_support, max_support)
    
    return FOUNDER_SUPPORT_CONFIG['min_support']

def calculate_required_designers(monthly_website_demand):
    """Calculate how many designers are needed with safety buffer"""
    total_workload = 0
    
    for package in ['basic', 'pro', 'enterprise']:
        websites_needed = monthly_website_demand.get(package, 0)
        max_capacity_per_designer = WEB_DESIGNER_CONFIG['capacity_per_month'][package]
        
        if max_capacity_per_designer > 0:
            workload_fraction = websites_needed / max_capacity_per_designer
            total_workload += workload_fraction
    
    buffer = WEB_DESIGNER_CONFIG['capacity_buffer']
    required_designers = max(0, int((total_workload * (1 + buffer)) + 0.99)) if total_workload > 0 else 0
    
    return required_designers, total_workload

def update_designer_count(current_designers, required_designers, current_utilization, months_low_utilization):
    """Update designer count with emergency hiring for over-capacity"""
    if current_designers == 0:
        hire_threshold = WEB_DESIGNER_CONFIG['first_hire_threshold']
    else:
        hire_threshold = WEB_DESIGNER_CONFIG['subsequent_hire_threshold']
    
    fire_threshold = WEB_DESIGNER_CONFIG['fire_threshold']
    emergency_threshold = WEB_DESIGNER_CONFIG['emergency_hire_threshold']
    
    if current_utilization > emergency_threshold:
        needed_designers = max(required_designers, int(current_utilization * current_designers) + 1)
        print(f"⚠️  EMERGENCY HIRING: {current_utilization:.1%} utilization, hiring to {needed_designers} designers")
        return needed_designers, 0
    
    elif current_utilization > hire_threshold and required_designers > current_designers:
        return required_designers, 0
    
    elif current_utilization < fire_threshold and current_designers > 0:
        months_low_utilization += 1
        if months_low_utilization >= 2:
            return max(0, current_designers - 1), 0
        else:
            return current_designers, months_low_utilization
    
    else:
        return current_designers, 0

def update_vishal_status(is_fulltime, rolling_avg_profit):
    """Update Vishal's employment status based on rolling average profit threshold"""
    fulltime_threshold = VISHAL_CONFIG['fulltime_threshold']
    
    if not is_fulltime and rolling_avg_profit >= fulltime_threshold:
        return True
    
    return is_fulltime

def calculate_rolling_average_profit(profit_history):
    """Calculate rolling average profit for the last 3 months"""
    if len(profit_history) < ROLLING_AVERAGE_MONTHS:
        return sum(profit_history) / len(profit_history) if profit_history else 0
    else:
        return sum(profit_history[-ROLLING_AVERAGE_MONTHS:]) / ROLLING_AVERAGE_MONTHS

def calculate_reinvestment_strategy(net_cash_flow, cash_flow_margin, accumulated_personnel_fund):
    """Calculate reinvestment amounts when cash flow margin exceeds 30%"""
    reinvestment = {
        'marketing_boost': 0,
        'personnel_fund_addition': 0,
        'total_reinvested': 0,
        'triggered': False,
        'hire_additional_personnel': False
    }
    
    if cash_flow_margin >= REINVESTMENT_CONFIG['cash_flow_margin_threshold'] and net_cash_flow > 0:
        excess_cash = net_cash_flow * (REINVESTMENT_CONFIG['reinvestment_percentage'])
        
        if excess_cash >= REINVESTMENT_CONFIG['min_monthly_reinvestment']:
            reinvestment['triggered'] = True
            
            marketing_allocation = excess_cash * REINVESTMENT_CONFIG['marketing_allocation']
            reinvestment['marketing_boost'] = min(
                marketing_allocation, 
                REINVESTMENT_CONFIG['max_monthly_marketing_boost']
            )
            
            personnel_allocation = excess_cash * REINVESTMENT_CONFIG['personnel_allocation']
            max_fund = REINVESTMENT_CONFIG['max_personnel_fund']
            
            if accumulated_personnel_fund < max_fund:
                personnel_addition = min(personnel_allocation, max_fund - accumulated_personnel_fund)
                reinvestment['personnel_fund_addition'] = personnel_addition
                
                new_personnel_fund = accumulated_personnel_fund + personnel_addition
                if new_personnel_fund >= REINVESTMENT_CONFIG['personnel_threshold']:
                    reinvestment['hire_additional_personnel'] = True
                    reinvestment['personnel_fund_addition'] -= REINVESTMENT_CONFIG['personnel_threshold']
            
            reinvestment['total_reinvested'] = reinvestment['marketing_boost'] + reinvestment['personnel_fund_addition']
    
    return reinvestment

def generate_financial_projection():
    """Generate financial projection with all fixes applied and loan investment tracking"""
    
    months_total = 12
    month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']
    
    # Initialize loan scenario
    loan_details = get_loan_details(ACTIVE_LOAN_SCENARIO)
    loan_allocation = allocate_loan_funds(loan_details['net_amount'], ACTIVE_LOAN_STRATEGY)
    team_benefits = apply_team_expansion_benefits(loan_allocation, 0, False, 8000)
    infrastructure_benefits = apply_infrastructure_benefits(loan_allocation)
    founder_benefits = apply_founder_support_benefits(loan_allocation)
    
    # Calculate infrastructure setup costs
    infrastructure_setup_cost = 0
    if infrastructure_benefits['monthly_cost_increase'] == 200:
        infrastructure_setup_cost = 5000
    elif infrastructure_benefits['monthly_cost_increase'] == 500:
        infrastructure_setup_cost = 10000
    
    # Initialize tracking variables
    current_customers = {'basic': 0, 'pro': 0, 'enterprise': 0}
    customer_ages = {'basic': [], 'pro': [], 'enterprise': []}
    cumulative_website_customers = {'basic': 0, 'pro': 0, 'enterprise': 0}
    
    current_designers = 0
    months_low_utilization = 0
    vishal_is_fulltime = False
    profit_history = []
    
    current_loan_balance = loan_details['amount']
    remaining_loan_funds = loan_details['net_amount']
    current_bank_balance = loan_details['net_amount']
    
    accumulated_personnel_fund = 0
    additional_designers_from_reinvestment = 0
    total_reinvested = 0
    total_loan_investments = 0
    
    monthly_data = []
    cumulative_profit = 0
    cumulative_cash_flow = 0
    
    for month in range(months_total):
        # Basic month info
        current_date = PROJECT_START + timedelta(days=30*month)
        month_name = month_names[month]
        
        # Loan calculations
        interest_only_months = loan_details.get('interest_only_months', 0)
        monthly_loan_payment = calculate_monthly_loan_payment(
            loan_details['amount'], 
            loan_details['interest_rate'], 
            loan_details['term_months'],
            interest_only_months,
            month + 1
        )
        
        if month > 0:
            current_loan_balance = calculate_loan_balance(
                loan_details['amount'], loan_details['interest_rate'], 
                loan_details['term_months'], month, interest_only_months
            )
        
        # Customer management
        current_customers, churned_customers, customer_ages = apply_dynamic_churn(current_customers, customer_ages)
        if infrastructure_benefits['churn_reduction'] > 0:
            for package in churned_customers:
                reduction = int(churned_customers[package] * infrastructure_benefits['churn_reduction'])
                churned_customers[package] = max(0, churned_customers[package] - reduction)
                current_customers[package] += reduction
        
        current_customers, customer_ages = apply_package_upgrades(current_customers, customer_ages)
        
        # Marketing calculations
        base_marketing_spend = calculate_marketing_costs(month_name)
        marketing_boost_from_loan = calculate_monthly_marketing_boost(loan_allocation, month + 1, months_total)
        
        # Reinvestment calculations
        marketing_boost_from_reinvestment = 0
        reinvestment = {'triggered': False, 'personnel_fund_addition': 0}
        if month > 0:
            prev_month_data = monthly_data[-1]
            reinvestment = calculate_reinvestment_strategy(
                prev_month_data['net_cash_flow'], 
                prev_month_data['cash_flow_margin'],
                accumulated_personnel_fund
            )
            
            if reinvestment['triggered']:
                marketing_boost_from_reinvestment = reinvestment['marketing_boost']
                accumulated_personnel_fund += reinvestment['personnel_fund_addition']
                total_reinvested += reinvestment['total_reinvested']
                
                if reinvestment['hire_additional_personnel']:
                    additional_designers_from_reinvestment += 1
                    accumulated_personnel_fund = max(0, accumulated_personnel_fund - REINVESTMENT_CONFIG['personnel_threshold'])
        
        # Marketing spend breakdown
        marketing_data = MARKETING_COSTS.get(month_name, {'GOOGLE': 0, 'META': 0})
        base_google_spend = marketing_data['GOOGLE']
        base_meta_spend = marketing_data['META']
        
        total_marketing_boost = marketing_boost_from_loan + marketing_boost_from_reinvestment
        google_boost = total_marketing_boost * 0.6
        meta_boost = total_marketing_boost * 0.4
        
        total_google_spend = base_google_spend + google_boost
        total_meta_spend = base_meta_spend + meta_boost
        total_marketing_spend = total_google_spend + total_meta_spend
        
        # Customer acquisition
        google_customers = 0
        meta_customers = 0
        
        if total_google_spend > 0:
            google_cac = get_cac_for_spend('GOOGLE', total_google_spend)
            google_customers = int(total_google_spend / google_cac)
        
        if total_meta_spend > 0:
            meta_cac = get_cac_for_spend('META', total_meta_spend)
            meta_customers = int(total_meta_spend / meta_cac)
        
        new_customers_from_marketing = google_customers + meta_customers
        
        organic_customers = calculate_organic_customers(month_name)
        if founder_benefits['organic_boost'] > 0:
            organic_boost = int(organic_customers * founder_benefits['organic_boost'])
            organic_customers += organic_boost
        
        new_customers_by_package = distribute_customers_by_package(new_customers_from_marketing)
        new_customers_by_package['basic'] += organic_customers
        
        new_customers_total = new_customers_from_marketing + organic_customers
        
        # Add new customers to current base
        for package in ['basic', 'pro', 'enterprise']:
            new_count = new_customers_by_package[package]
            current_customers[package] += new_count
            customer_ages[package] = customer_ages.get(package, []) + [1] * new_count
        
        total_customers = sum(current_customers.values())
        
        # Website customers
        new_website_customers = {'basic': 0, 'pro': 0, 'enterprise': 0}
        
        if month + 1 <= 6:
            conversion_rates = {'basic': 0.7, 'pro': 0.7, 'enterprise': 0.4}
        else:
            conversion_rates = {'basic': 0.4, 'pro': 0.5, 'enterprise': 0.2}
        
        for package in ['basic', 'pro', 'enterprise']:
            new_customers_this_package = new_customers_by_package[package]
            new_website_customers[package] = round(new_customers_this_package * conversion_rates[package])
            cumulative_website_customers[package] += new_website_customers[package]
        
        # Designer calculations
        required_designers, designer_utilization = calculate_required_designers(new_website_customers)
        total_designers_available = current_designers + additional_designers_from_reinvestment
        
        if total_designers_available > 0:
            current_utilization = designer_utilization / total_designers_available
        else:
            current_utilization = designer_utilization
        
        current_designers, months_low_utilization = update_designer_count(
            total_designers_available, required_designers, current_utilization, months_low_utilization
        )
        
        total_designers_available = current_designers + additional_designers_from_reinvestment
        
        # Revenue calculations
        saas_revenue, website_revenue_gross = calculate_monthly_revenue(current_customers, new_website_customers)
        total_revenue, website_revenue, cancellation_amount = calculate_revenue_with_cancellations(
            saas_revenue, website_revenue_gross
        )
        
        # Variable costs
        monthly_variable_costs = calculate_monthly_variable_costs(current_customers, total_customers)
        if infrastructure_benefits['variable_cost_reduction'] > 0:
            monthly_variable_costs *= (1 - infrastructure_benefits['variable_cost_reduction'])
        
        # Preliminary calculations for Vishal compensation
        preliminary_rolling_avg = calculate_rolling_average_profit(profit_history) if profit_history else 0
        total_designers_cost = current_designers * 1750
        basic_fixed_costs = (35 + total_marketing_spend + total_designers_cost + infrastructure_benefits['monthly_cost_increase'])
        
        preliminary_profit_before_vishal = total_revenue - monthly_variable_costs - basic_fixed_costs - monthly_loan_payment
        
        # Update Vishal status and calculate compensation
        vishal_threshold_multiplier = team_benefits['profit_threshold_multiplier']
        vishal_is_fulltime = update_vishal_status(vishal_is_fulltime, preliminary_rolling_avg)
        
        vishal_compensation, vishal_salary, vishal_profit_share, vishal_website_share = calculate_vishal_compensation_iterative(
            preliminary_profit_before_vishal, website_revenue, vishal_is_fulltime
        )
        
        # Calculate founder support
        final_preliminary_profit = preliminary_profit_before_vishal - vishal_compensation
        founder_support_payment = calculate_founder_support(final_preliminary_profit)
        founder_support_payment = min(founder_support_payment, FOUNDER_SUPPORT_CONFIG['max_support'])
        
        # Final calculations
        profit_after_all_compensation = final_preliminary_profit - founder_support_payment
        profit_history.append(profit_after_all_compensation)
        rolling_avg_profit = calculate_rolling_average_profit(profit_history)
        
        monthly_fixed_costs, llm_cost, llm_description, per_employee_costs = calculate_monthly_fixed_costs(
            month_name, current_designers, month + 1, vishal_compensation + founder_support_payment, 
            rolling_avg_profit, vishal_is_fulltime, 0
        )
        
        total_monthly_costs = monthly_variable_costs + monthly_fixed_costs + monthly_loan_payment
        monthly_profit = total_revenue - total_monthly_costs
        cumulative_profit += monthly_profit
        
        cash_flow_in, cash_flow_out, net_cash_flow, cash_flow_margin, cost_ratio = calculate_cash_flow(
            total_revenue, total_monthly_costs
        )
        cumulative_cash_flow += net_cash_flow
        current_bank_balance += net_cash_flow
        
        # NOW calculate loan investments - assume you start with €0, so early expenses are loan-funded
        monthly_loan_investments = 0
        
        # In month 1, you start with €0, so most expenses are loan-funded
        if month == 0:
            # Legal/compliance costs that you couldn't afford without loan
            legal_costs = 0
            for cost_type, details in {'privacy_policy_terms': {'cost': 1000}, 
                                     'freelancer_contracts': {'cost': 300}, 
                                     'data_protection_audit': {'cost': 800}}.items():
                legal_costs += details['cost']
            
            if legal_costs > 0:
                monthly_loan_investments += legal_costs
                remaining_loan_funds -= legal_costs
                print(f"💰 Loan funding legal/compliance setup: €{legal_costs:,.2f}")
            
            # Infrastructure setup costs 
            if infrastructure_setup_cost > 0:
                monthly_loan_investments += infrastructure_setup_cost
                remaining_loan_funds -= infrastructure_setup_cost
                print(f"💰 Loan funding infrastructure setup: €{infrastructure_setup_cost:,.2f}")
            
            # First month's essential costs that exceed revenue
            essential_month1_costs = (35 +  # business insurance
                                    total_marketing_spend +  # all marketing is loan-funded initially
                                    total_designers_cost +  # designer costs
                                    vishal_compensation +  # Vishal compensation
                                    infrastructure_benefits['monthly_cost_increase'])  # ongoing infrastructure
            
            # If revenue doesn't cover essential costs, the difference is loan-funded
            month1_deficit = max(0, essential_month1_costs - total_revenue)
            if month1_deficit > 0:
                monthly_loan_investments += month1_deficit
                remaining_loan_funds -= month1_deficit
                print(f"💰 Loan covering month 1 operating deficit: €{month1_deficit:,.2f}")
        
        # Marketing boost from loan (ongoing investment)
        if marketing_boost_from_loan > 0:
            monthly_loan_investments += marketing_boost_from_loan
            remaining_loan_funds -= marketing_boost_from_loan
        
        # Track if we're operating at a loss and need loan funding
        if net_cash_flow < 0 and remaining_loan_funds > 0:
            # If we're losing money, that loss is effectively funded by loan
            cash_flow_support = min(abs(net_cash_flow), remaining_loan_funds)
            monthly_loan_investments += cash_flow_support
            remaining_loan_funds -= cash_flow_support
            if month < 6:  # Only show this message for first 6 months to avoid spam
                print(f"💰 Loan covering cash flow deficit: €{cash_flow_support:,.2f}")
        
        # Track any founder support as loan investment (since you start with €0)
        if founder_support_payment > 0:
            monthly_loan_investments += founder_support_payment
            remaining_loan_funds -= founder_support_payment
            if month < 3:  # Only show for first few months
                print(f"💰 Loan funding founder support: €{founder_support_payment:,.2f}")
        
        total_loan_investments += monthly_loan_investments
        
        # Validation checks
        validation_errors = []
        
        if founder_support_payment > FOUNDER_SUPPORT_CONFIG['max_support']:
            validation_errors.append(f"Month {month + 1}: Founder support €{founder_support_payment} exceeds maximum €{FOUNDER_SUPPORT_CONFIG['max_support']}")
        
        if current_utilization > 1.0:
            validation_errors.append(f"Month {month + 1}: Designer utilization {current_utilization:.1%} exceeds 100%")
        
        if monthly_profit < -10000:
            validation_errors.append(f"Month {month + 1}: Monthly profit €{monthly_profit} is extremely negative")
        
        if validation_errors:
            print("⚠️  VALIDATION WARNINGS:")
            for error in validation_errors:
                print(f"   {error}")
        
        # Debug output for high-utilization or high-profit months
        if current_utilization > 0.9 or monthly_profit > 10000:
            print(f"\n🔍 DEBUG Month {month + 1}:")
            print(f"   Designers: {current_designers} (utilization: {current_utilization:.1%})")
            print(f"   Website demand: {sum(new_website_customers.values())} websites")
            print(f"   Profit before Vishal: €{preliminary_profit_before_vishal:.2f}")
            print(f"   Vishal compensation: €{vishal_compensation:.2f}")
            print(f"   Founder support: €{founder_support_payment:.2f}")
            print(f"   Final profit: €{monthly_profit:.2f}")
            print(f"   Cash flow margin: {cash_flow_margin:.1f}%")
        
        # Store monthly data
        monthly_data.append({
            # Time tracking
            'month': month + 1,
            'date': current_date.strftime('%Y-%m'),
            
            # Customer metrics
            'basic_customers': current_customers['basic'],
            'pro_customers': current_customers['pro'],
            'enterprise_customers': current_customers['enterprise'],
            'total_customers': total_customers,
            'new_customers_total': new_customers_total,
            'churned_customers': sum(churned_customers.values()),
            
            # Website metrics
            'total_website_customers': sum(cumulative_website_customers.values()),
            'new_websites_total': sum(new_website_customers.values()),
            
            # Team metrics
            'designers_count': current_designers,
            'designer_utilization': round(current_utilization, 2),
            'vishal_fulltime': 1 if vishal_is_fulltime else 0,
            'total_employees': 1 + (1 if vishal_is_fulltime else 0) + current_designers,
            
            # Revenue metrics
            'saas_revenue': round(saas_revenue, 2),
            'website_revenue': round(website_revenue, 2),
            'total_revenue': round(total_revenue, 2),
            
            # Cost metrics
            'variable_costs': round(monthly_variable_costs, 2),
            'marketing_spend': round(total_marketing_spend, 2),
            'vishal_compensation': round(vishal_compensation, 2),
            'founder_support': round(founder_support_payment, 2),
            'designer_costs': round(total_designers_cost, 2),
            'total_costs': round(total_monthly_costs, 2),
            
            # Profitability
            'monthly_profit': round(monthly_profit, 2),
            'cumulative_profit': round(cumulative_profit, 2),
            'rolling_avg_profit': round(rolling_avg_profit, 2),
            
            # Cash flow & bank balance
            'net_cash_flow': round(net_cash_flow, 2),
            'cash_flow_margin': round(cash_flow_margin, 1),
            'cumulative_cash_flow': round(cumulative_cash_flow, 2),
            'bank_balance': round(current_bank_balance, 2),
            
            # Marketing breakdown
            'google_spend': round(total_google_spend, 2),
            'meta_spend': round(total_meta_spend, 2),
            'google_customers': google_customers,
            'meta_customers': meta_customers,
            'organic_customers': organic_customers,
            
            # Reinvestment tracking
            'reinvestment_active': 1 if (month > 0 and cash_flow_margin >= REINVESTMENT_CONFIG['cash_flow_margin_threshold']) else 0,
            'marketing_reinvestment': round(marketing_boost_from_reinvestment, 2),
            'personnel_fund': round(accumulated_personnel_fund, 2),
            'total_reinvested': round(total_reinvested, 2),
            
            # Loan tracking
            'loan_balance': round(current_loan_balance, 2),
            'loan_payment': round(monthly_loan_payment, 2),
            'loan_marketing_boost': round(marketing_boost_from_loan, 2),
            
            # Investment tracking
            'monthly_loan_investments': round(monthly_loan_investments, 2),
            'total_loan_investments': round(total_loan_investments, 2),
            'remaining_loan_funds': round(remaining_loan_funds, 2),
            'loan_investment_rate': round((total_loan_investments / loan_details['net_amount'] * 100), 1) if loan_details['net_amount'] > 0 else 0,
        })
    
    return pd.DataFrame(monthly_data)

# Summary function for reinvestment analysis
def print_reinvestment_summary(df):
    """Print summary of reinvestment strategy results"""
    
    print("\n" + "="*60)
    print("REINVESTMENT STRATEGY ANALYSIS - 30% MARGIN THRESHOLD")
    print("="*60)
    
    reinvestment_months = df[df['reinvestment_active'] == 1]
    
    if len(reinvestment_months) == 0:
        print("Reinvestment strategy was never triggered (30% cash flow margin not reached)")
        return
    
    first_trigger_month = reinvestment_months.iloc[0]['month']
    total_marketing_reinvested = df['marketing_reinvestment'].sum()
    total_personnel_fund = df['personnel_fund'].iloc[-1]
    
    print(f"First trigger month: {first_trigger_month}")
    print(f"Months with reinvestment active: {len(reinvestment_months)}")
    print(f"Total marketing reinvestment: €{total_marketing_reinvested:,.2f}")
    print(f"Final personnel fund: €{total_personnel_fund:,.2f}")
    print(f"Total reinvested: €{df['total_reinvested'].iloc[-1]:,.2f}")
    
    total_founder_support = df['founder_support'].sum()
    months_with_support = len(df[df['founder_support'] > 0])
    avg_monthly_support = df[df['founder_support'] > 0]['founder_support'].mean() if months_with_support > 0 else 0
    
    print(f"\nFOUNDER SUPPORT SUMMARY:")
    print(f"Total founder support paid: €{total_founder_support:,.2f}")
    print(f"Months with founder support: {months_with_support}")
    print(f"Average monthly support: €{avg_monthly_support:,.2f}")
    print(f"Maximum monthly support: €{df['founder_support'].max():,.2f}")
    
    final_customers_with = df['total_customers'].iloc[-1]
    
    print(f"\nGROWTH IMPACT:")
    print(f"Final customer count with reinvestment: {final_customers_with:,}")
    print(f"Additional marketing spend generated: €{total_marketing_reinvested:,.2f}")
    print(f"Estimated additional customers from reinvestment: {total_marketing_reinvested / 60:.0f}")
    
    if len(reinvestment_months) > 0:
        print(f"\nMONTHLY REINVESTMENT BREAKDOWN:")
        reinvestment_columns = ['month', 'cash_flow_margin', 'net_cash_flow', 
                               'marketing_reinvestment', 'personnel_fund']
        print(reinvestment_months[reinvestment_columns].to_string(index=False))

def print_loan_investment_summary(df):
    """Print summary of loan fund investments"""
    
    print("\n" + "="*60)
    print("LOAN INVESTMENT ANALYSIS")
    print("="*60)
    
    final_month = df.iloc[-1]
    loan_amount = df['loan_balance'].iloc[0] + df['loan_payment'].sum()
    
    if loan_amount == 0:
        print("No loan scenario active")
        return
    
    total_investments = final_month['total_loan_investments']
    remaining_funds = final_month['remaining_loan_funds']
    investment_rate = final_month['loan_investment_rate']
    
    print(f"Original Loan Amount: €{loan_amount:,.2f}")
    print(f"Total Loan Investments (2026): €{total_investments:,.2f}")
    print(f"Remaining Loan Funds: €{remaining_funds:,.2f}")
    print(f"Investment Rate: {investment_rate:.1f}% of loan funds deployed")
    
    investment_months = df[df['monthly_loan_investments'] > 0]
    if len(investment_months) > 0:
        print(f"\nMONTHLY INVESTMENT BREAKDOWN:")
        investment_columns = ['month', 'monthly_loan_investments', 'loan_marketing_boost', 'total_loan_investments']
        print(investment_months[investment_columns].to_string(index=False))
    
    total_loan_payments = df['loan_payment'].sum()
    print(f"\nLOAN SERVICING (2026):")
    print(f"Total Loan Payments: €{total_loan_payments:,.2f}")
    print(f"Average Monthly Payment: €{total_loan_payments/12:,.2f}")
    print(f"Final Loan Balance: €{final_month['loan_balance']:,.2f}")
    
    # ROI Analysis
    revenue_impact = df['total_revenue'].sum()
    print(f"\nROI ANALYSIS:")
    print(f"Total Revenue Generated (2026): €{revenue_impact:,.2f}")
    print(f"Investment to Revenue Ratio: {(total_investments / revenue_impact * 100):.1f}%" if revenue_impact > 0 else "N/A")
    print(f"Loan Cost to Revenue Ratio: {(total_loan_payments / revenue_impact * 100):.1f}%" if revenue_impact > 0 else "N/A")