from config.settings import PACKAGES_WITH_WEBSITE, WEBSITE_CANCELLATION_RATE

def calculate_monthly_revenue(customers_dict, website_customers_dict):
    """Calculate total monthly revenue from SaaS and website packages"""
    # SaaS recurring revenue
    saas_revenue = 0
    for package in ['basic', 'pro', 'enterprise']:
        customer_count = customers_dict.get(package, 0)
        price = PACKAGES_WITH_WEBSITE[package]['price']  # Use website package pricing
        saas_revenue += customer_count * price
    
    # Website package one-time revenue (only for new website customers this month)
    website_revenue = 0
    for package in ['basic', 'pro', 'enterprise']:
        new_website_customers = website_customers_dict.get(package, 0)
        upfront_cost = PACKAGES_WITH_WEBSITE[package]['upfront_cost']
        website_revenue += new_website_customers * upfront_cost
    
    return saas_revenue, website_revenue

def calculate_revenue_with_cancellations(saas_revenue, website_revenue_gross):
    """Apply website cancellation rate to revenue"""
    website_revenue = website_revenue_gross * (1 - WEBSITE_CANCELLATION_RATE)
    total_revenue = saas_revenue + website_revenue
    cancellation_amount = website_revenue_gross * WEBSITE_CANCELLATION_RATE
    
    return total_revenue, website_revenue, cancellation_amount

def calculate_cash_flow(total_revenue, total_costs):
    """Calculate monthly cash flow (in vs out) with percentage metrics"""
    cash_flow_in = total_revenue  # All revenue comes in as cash
    cash_flow_out = total_costs   # All costs go out as cash
    net_cash_flow = cash_flow_in - cash_flow_out
    
    # Calculate cash flow margin (net cash flow as % of revenue)
    cash_flow_margin = (net_cash_flow / cash_flow_in * 100) if cash_flow_in > 0 else 0
    
    # Calculate cost ratio (costs as % of revenue)
    cost_ratio = (cash_flow_out / cash_flow_in * 100) if cash_flow_in > 0 else 0
    
    return cash_flow_in, cash_flow_out, net_cash_flow, cash_flow_margin, cost_ratio