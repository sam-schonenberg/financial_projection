from config.settings import (
    VARIABLE_COSTS, SERVER_UPGRADES, FIXED_COSTS, MARKETING_COSTS,
    PER_EMPLOYEE_COSTS, LLM_COSTS, LEGAL_COMPLIANCE_COSTS, OWNER_SALARY
)

def calculate_monthly_variable_costs(customers_dict, total_customers):
    """Calculate total monthly variable costs including server scaling"""
    # Per-customer variable costs
    monthly_costs = 0
    yearly_costs = 0
    
    for package in ['basic', 'pro', 'enterprise']:
        customer_count = customers_dict.get(package, 0)
        monthly_cost_per_customer = VARIABLE_COSTS[package]['month']
        yearly_cost_per_customer = VARIABLE_COSTS[package]['year']
        
        monthly_costs += customer_count * monthly_cost_per_customer
        yearly_costs += customer_count * yearly_cost_per_customer
    
    # Server scaling costs
    server_costs = 0
    server_tiers = sorted([int(k) for k in SERVER_UPGRADES.keys()])
    
    for tier in reversed(server_tiers):
        if total_customers >= tier:
            server_costs = SERVER_UPGRADES[str(tier)]
            break
    
    return monthly_costs + (yearly_costs / 12) + server_costs

def calculate_marketing_costs(month_name):
    """Calculate total marketing spend for the month"""
    marketing_data = MARKETING_COSTS.get(month_name, {'GOOGLE': 0, 'META': 0})
    return marketing_data['GOOGLE'] + marketing_data['META']

def calculate_per_employee_costs(total_employees):
    """Calculate costs that scale with number of employees"""
    return total_employees * PER_EMPLOYEE_COSTS['google_workspace']

def calculate_llm_costs(rolling_avg_profit):
    """Calculate LLM costs based on rolling average profit thresholds"""
    # Check thresholds from highest to lowest
    if rolling_avg_profit > LLM_COSTS['scale_up']['threshold']:
        return LLM_COSTS['scale_up']['cost'], LLM_COSTS['scale_up']['description']
    elif rolling_avg_profit > LLM_COSTS['team_expansion']['threshold']:
        return LLM_COSTS['team_expansion']['cost'], LLM_COSTS['team_expansion']['description']
    elif rolling_avg_profit > LLM_COSTS['profitable']['threshold']:
        return LLM_COSTS['profitable']['cost'], LLM_COSTS['profitable']['description']
    else:
        return LLM_COSTS['loss_making']['cost'], LLM_COSTS['loss_making']['description']

def calculate_legal_costs(month_number):
    """Calculate one-time legal/compliance costs for specific months"""
    legal_costs = 0
    for cost_type, details in LEGAL_COMPLIANCE_COSTS.items():
        if month_number == details['month']:
            legal_costs += details['cost']
    return legal_costs

def calculate_owner_salary(monthly_profit):
    """Calculate owner's monthly salary - only starts when monthly profit reaches €1,400"""
    if monthly_profit >= 1400:
        return OWNER_SALARY
    else:
        return 0

def calculate_monthly_fixed_costs(month_name, designer_count, month_number, vishal_compensation, 
                                rolling_avg_profit, vishal_is_fulltime, owner_salary):
    """Calculate total monthly fixed costs including marketing, designers, Vishal's compensation, 
    owner salary, LLM costs, and legal costs"""
    base_fixed = sum(FIXED_COSTS.values())
    marketing_spend = calculate_marketing_costs(month_name)
    designer_costs = designer_count * 1750  # EMPLOYEE_COSTS['web_designer']
    
    # Calculate total employees (you + Vishal + designers)
    total_employees = 1 + (1 if vishal_is_fulltime else 0) + designer_count
    per_employee_costs = calculate_per_employee_costs(total_employees)
    
    # Calculate dynamic LLM costs based on rolling average profit
    llm_cost, llm_description = calculate_llm_costs(rolling_avg_profit)
    
    # Add one-time legal/compliance costs in specific months
    legal_costs = calculate_legal_costs(month_number)
    
    total_fixed = (base_fixed + marketing_spend + designer_costs + vishal_compensation + 
                   owner_salary + llm_cost + per_employee_costs + legal_costs)
    
    return total_fixed, llm_cost, llm_description, per_employee_costs