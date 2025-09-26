import math
from config.loan_settings import (
    LOAN_SCENARIOS, LOAN_ALLOCATION_STRATEGIES, MARKETING_BOOST_EFFICIENCY,
    TEAM_EXPANSION_BENEFITS, INFRASTRUCTURE_BENEFITS, FOUNDER_SUPPORT_BENEFITS, 
    LOAN_DISBURSEMENT
)

def calculate_monthly_loan_payment(principal, annual_rate, term_months, interest_only_months=0, current_month=1):
    """Calculate monthly loan payment, handling interest-only periods"""
    if principal == 0 or annual_rate == 0:
        return 0
    
    monthly_rate = annual_rate / 12
    
    # If we're in the interest-only period
    if interest_only_months > 0 and current_month <= interest_only_months:
        return principal * monthly_rate  # Interest-only payment
    
    # If there's an interest-only period, calculate payment for remaining term
    if interest_only_months > 0:
        remaining_term = term_months - interest_only_months
        # Principal remains the same since no principal was paid during interest-only period
        remaining_principal = principal
    else:
        remaining_term = term_months
        remaining_principal = principal
    
    # Standard amortization formula for remaining term
    if remaining_term <= 0:
        return 0
        
    payment = remaining_principal * (monthly_rate * (1 + monthly_rate)**remaining_term) / ((1 + monthly_rate)**remaining_term - 1)
    return payment

def calculate_loan_balance(principal, annual_rate, term_months, months_paid, interest_only_months=0):
    """Calculate remaining loan balance after given number of payments, handling interest-only periods"""
    if principal == 0 or months_paid >= term_months:
        return 0
    
    monthly_rate = annual_rate / 12
    
    # During interest-only period, balance remains the same
    if interest_only_months > 0 and months_paid <= interest_only_months:
        return principal
    
    # After interest-only period
    if interest_only_months > 0 and months_paid > interest_only_months:
        # Calculate remaining balance for the amortizing portion
        remaining_term = term_months - interest_only_months
        months_into_amortization = months_paid - interest_only_months
        
        if months_into_amortization >= remaining_term:
            return 0
            
        monthly_payment = calculate_monthly_loan_payment(principal, annual_rate, term_months, interest_only_months, interest_only_months + 1)
        
        # Calculate remaining balance using amortization formula
        remaining_balance = principal * ((1 + monthly_rate)**(remaining_term - months_into_amortization) - 1) / ((1 + monthly_rate)**remaining_term - 1)
        return remaining_balance
    
    # Standard amortization (no interest-only period)
    monthly_payment = calculate_monthly_loan_payment(principal, annual_rate, term_months)
    remaining_balance = principal * ((1 + monthly_rate)**(term_months - months_paid) - 1) / ((1 + monthly_rate)**term_months - 1)
    return remaining_balance

def get_loan_details(scenario_name):
    """Get loan details for a specific scenario, handling interest-only periods"""
    if scenario_name not in LOAN_SCENARIOS:
        return LOAN_SCENARIOS['no_loan']
    
    scenario = LOAN_SCENARIOS[scenario_name].copy()
    
    if scenario['amount'] > 0:
        interest_only_months = scenario.get('interest_only_months', 0)
        
        # Calculate monthly payment for interest-only period
        if interest_only_months > 0:
            monthly_rate = scenario['interest_rate'] / 12
            interest_only_payment = scenario['amount'] * monthly_rate
            
            # Calculate payment for amortizing period
            remaining_term = scenario['term_months'] - interest_only_months
            if remaining_term > 0:
                amortizing_payment = calculate_monthly_loan_payment(
                    scenario['amount'], scenario['interest_rate'], remaining_term
                )
            else:
                amortizing_payment = 0
                
            scenario['interest_only_payment'] = interest_only_payment
            scenario['amortizing_payment'] = amortizing_payment
            scenario['monthly_payment'] = interest_only_payment  # Default to interest-only for first year
        else:
            # Standard loan
            scenario['monthly_payment'] = calculate_monthly_loan_payment(
                scenario['amount'], scenario['interest_rate'], scenario['term_months']
            )
        
        # Calculate setup fee
        setup_fee = scenario['amount'] * LOAN_DISBURSEMENT.get('setup_fee', 0.02)
        scenario['net_amount'] = scenario['amount'] - setup_fee
        scenario['setup_fee'] = setup_fee
        
        # Calculate total interest over life of loan
        if interest_only_months > 0:
            interest_only_total = interest_only_months * scenario['interest_only_payment']
            remaining_term = scenario['term_months'] - interest_only_months
            if remaining_term > 0:
                amortizing_total = remaining_term * scenario['amortizing_payment']
                total_payments = interest_only_total + amortizing_total
            else:
                total_payments = interest_only_total
        else:
            total_payments = scenario['monthly_payment'] * scenario['term_months']
            
        scenario['total_interest'] = total_payments - scenario['amount']
    else:
        scenario['monthly_payment'] = 0
        scenario['net_amount'] = 0
        scenario['setup_fee'] = 0
        scenario['total_interest'] = 0
    
    return scenario

def allocate_loan_funds(net_amount, strategy_name):
    """Allocate loan funds according to strategy"""
    if strategy_name not in LOAN_ALLOCATION_STRATEGIES:
        strategy_name = 'balanced'
    
    strategy = LOAN_ALLOCATION_STRATEGIES[strategy_name]
    
    allocation = {}
    allocation['marketing_boost'] = net_amount * strategy['marketing_boost']
    allocation['team_expansion'] = net_amount * strategy['team_expansion']
    allocation['infrastructure'] = net_amount * strategy['infrastructure']
    allocation['cash_reserve'] = net_amount * strategy['cash_reserve']
    allocation['founder_support'] = net_amount * strategy['founder_support']
    allocation['strategy_description'] = strategy['description']
    
    return allocation

def calculate_marketing_boost_efficiency(additional_monthly_spend):
    """Calculate efficiency multiplier for additional marketing spend"""
    if additional_monthly_spend <= 0:
        return 0
    
    total_efficiency = 0
    remaining_spend = additional_monthly_spend
    
    spend_tiers = sorted(MARKETING_BOOST_EFFICIENCY.keys())
    previous_tier = 0
    
    for tier in spend_tiers:
        if remaining_spend <= 0:
            break
            
        tier_spend = min(remaining_spend, tier - previous_tier)
        efficiency = MARKETING_BOOST_EFFICIENCY[tier]
        total_efficiency += tier_spend * efficiency
        
        remaining_spend -= tier_spend
        previous_tier = tier
    
    # Any spend beyond highest tier uses the lowest efficiency
    if remaining_spend > 0:
        lowest_efficiency = min(MARKETING_BOOST_EFFICIENCY.values())
        total_efficiency += remaining_spend * lowest_efficiency
    
    return total_efficiency / additional_monthly_spend if additional_monthly_spend > 0 else 0

def calculate_monthly_marketing_boost(allocation, month_number, total_months=12):
    """Calculate how much extra marketing spend per month from loan allocation"""
    marketing_fund = allocation['marketing_boost']
    
    # Spread marketing boost over 12 months (or remaining months if loan taken mid-year)
    months_remaining = total_months - (month_number - 1)
    if months_remaining <= 0:
        return 0
    
    # Distribute remaining marketing funds over remaining months
    monthly_boost = marketing_fund / months_remaining
    
    # Update allocation to reflect spending
    allocation['marketing_boost'] -= monthly_boost
    
    return monthly_boost

def apply_team_expansion_benefits(allocation, current_designers, vishal_is_fulltime, vishal_profit_threshold):
    """Apply team expansion benefits based on allocation"""
    benefits = {
        'hire_designer_early': False,
        'vishal_fulltime_early': False,
        'additional_designer_capacity': False,
        'months_accelerated': 0,
        'profit_threshold_multiplier': 1.0,
        'capacity_boost': 0
    }
    
    team_fund = allocation['team_expansion']
    
    # Check each benefit threshold
    for benefit_name, config in TEAM_EXPANSION_BENEFITS.items():
        if team_fund >= config['threshold']:
            if config['benefit'] == 'hire_designer_early':
                benefits['hire_designer_early'] = True
                benefits['months_accelerated'] = config['months_accelerated']
            
            elif config['benefit'] == 'vishal_fulltime_early':
                benefits['vishal_fulltime_early'] = True
                benefits['profit_threshold_multiplier'] = 1 - config['profit_threshold_reduction']
            
            elif config['benefit'] == 'additional_designer_capacity':
                benefits['additional_designer_capacity'] = True
                benefits['capacity_boost'] = config['capacity_boost']
    
    return benefits

def apply_founder_support_benefits(allocation):
    """Apply founder support benefits based on allocation"""
    benefits = {
        'owner_salary_early': False,
        'founder_focus': False,
        'founder_cash_buffer': False,
        'salary_threshold_multiplier': 1.0,
        'organic_boost': 0,
        'productivity_boost': 0,
        'risk_reduction': 0,
        'description': 'No founder support'
    }
    
    founder_fund = allocation['founder_support']
    
    # Check each benefit threshold (from highest to lowest)
    if founder_fund >= FOUNDER_SUPPORT_BENEFITS['founder_cash_buffer']['threshold']:
        config = FOUNDER_SUPPORT_BENEFITS['founder_cash_buffer']
        benefits.update({
            'founder_cash_buffer': True,
            'risk_reduction': config['risk_reduction'],
            'description': 'Founder cash buffer (6 months security)'
        })
        # Also include lower tier benefits
        benefits.update({
            'founder_focus': True,
            'organic_boost': FOUNDER_SUPPORT_BENEFITS['founder_focus']['productivity_boost'],
            'productivity_boost': FOUNDER_SUPPORT_BENEFITS['founder_focus']['strategic_benefits'],
            'owner_salary_early': True,
            'salary_threshold_multiplier': 1 - FOUNDER_SUPPORT_BENEFITS['early_salary_start']['salary_threshold_reduction']
        })
        
    elif founder_fund >= FOUNDER_SUPPORT_BENEFITS['founder_focus']['threshold']:
        config = FOUNDER_SUPPORT_BENEFITS['founder_focus']
        benefits.update({
            'founder_focus': True,
            'organic_boost': config['productivity_boost'],
            'productivity_boost': config['strategic_benefits'],
            'description': 'Founder focus time (productivity boost)'
        })
        # Also include lower tier benefits
        benefits.update({
            'owner_salary_early': True,
            'salary_threshold_multiplier': 1 - FOUNDER_SUPPORT_BENEFITS['early_salary_start']['salary_threshold_reduction']
        })
        
    elif founder_fund >= FOUNDER_SUPPORT_BENEFITS['early_salary_start']['threshold']:
        config = FOUNDER_SUPPORT_BENEFITS['early_salary_start']
        benefits.update({
            'owner_salary_early': True,
            'salary_threshold_multiplier': config['salary_threshold_reduction'],
            'description': 'Early owner salary start'
        })
    
    return benefits

def apply_infrastructure_benefits(allocation):
    """Apply infrastructure benefits based on allocation"""
    benefits = {
        'monthly_cost_increase': 0,
        'productivity_boost': 0,
        'churn_reduction': 0,
        'variable_cost_reduction': 0,
        'description': 'No infrastructure improvements'
    }
    
    infrastructure_fund = allocation['infrastructure']
    
    # Determine infrastructure level based on allocation
    if infrastructure_fund >= 10000:  # €10k+ for premium
        config = INFRASTRUCTURE_BENEFITS['premium_infrastructure']
        benefits.update({
            'monthly_cost_increase': config['monthly_cost'],
            'productivity_boost': config['productivity_boost'],
            'churn_reduction': config['customer_satisfaction'],
            'variable_cost_reduction': config['scaling_efficiency'],
            'description': 'Premium infrastructure upgrade'
        })
        # Deduct cost from allocation
        allocation['infrastructure'] -= 10000
        
    elif infrastructure_fund >= 5000:  # €5k+ for better tools
        config = INFRASTRUCTURE_BENEFITS['better_tools']
        benefits.update({
            'monthly_cost_increase': config['monthly_cost'],
            'productivity_boost': config['productivity_boost'],
            'churn_reduction': config['customer_satisfaction'],
            'description': 'Better tools upgrade'
        })
        # Deduct cost from allocation
        allocation['infrastructure'] -= 5000
    
    return benefits

def calculate_loan_impact_summary(scenario_name, strategy_name):
    """Calculate overall impact summary of loan scenario"""
    loan_details = get_loan_details(scenario_name)
    
    if loan_details['amount'] == 0:
        return {
            'loan_amount': 0,
            'monthly_payment': 0,
            'total_interest': 0,
            'strategy': 'No loan',
            'roi_breakeven_months': 0
        }
    
    allocation = allocate_loan_funds(loan_details['net_amount'], strategy_name)
    
    # Estimate potential monthly revenue increase
    marketing_monthly = allocation['marketing_boost'] / 12
    marketing_efficiency = calculate_marketing_boost_efficiency(marketing_monthly)
    estimated_monthly_customers = (marketing_monthly * marketing_efficiency) / 60  # Assume €60 CAC
    estimated_monthly_revenue_increase = estimated_monthly_customers * 70  # Assume €70 avg revenue per customer
    
    # Simple ROI calculation
    monthly_benefit = estimated_monthly_revenue_increase
    monthly_cost = loan_details['monthly_payment']
    
    roi_breakeven_months = loan_details['amount'] / max(monthly_benefit - monthly_cost, 1) if monthly_benefit > monthly_cost else float('inf')
    
    return {
        'loan_amount': loan_details['amount'],
        'net_amount': loan_details['net_amount'],
        'monthly_payment': loan_details['monthly_payment'],
        'total_interest': loan_details['total_interest'],
        'strategy': allocation['strategy_description'],
        'estimated_monthly_revenue_increase': estimated_monthly_revenue_increase,
        'estimated_monthly_customers': estimated_monthly_customers,
        'roi_breakeven_months': roi_breakeven_months,
        'allocation': allocation,
        'interest_only_months': loan_details.get('interest_only_months', 0),
        'interest_only_payment': loan_details.get('interest_only_payment', 0),
        'amortizing_payment': loan_details.get('amortizing_payment', 0)
    }