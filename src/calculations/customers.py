import random
from config.settings import (
    MARKETING_COSTS, GOOGLE_CAC, META_CAC, ORGANIC_CUSTOMERS, 
    CUSTOMER_DISTRIBUTION, CHURN_PHASES, UPGRADE_RATES,
    WEBSITE_PACKAGE_CONVERSION_DYNAMIC
)

def get_cac_for_spend(platform, spend_amount):
    """Get Customer Acquisition Cost based on platform and spend amount"""
    cac_table = GOOGLE_CAC if platform == 'GOOGLE' else META_CAC
    spend_str = str(int(spend_amount))
    
    # Find the appropriate CAC tier
    if spend_str in cac_table:
        return cac_table[spend_str]
    
    # If exact match not found, find closest lower tier
    available_spends = sorted([int(k) for k in cac_table.keys()])
    for spend in reversed(available_spends):
        if spend_amount >= spend:
            return cac_table[str(spend)]
    
    # Fallback to lowest tier
    return cac_table[str(available_spends[0])]

def calculate_new_customers_from_marketing(month_name):
    """Calculate new customers acquired from marketing spend"""
    marketing_data = MARKETING_COSTS.get(month_name, {'GOOGLE': 0, 'META': 0})
    
    total_new_customers = 0
    
    # Calculate customers from Google Ads
    google_spend = marketing_data['GOOGLE']
    if google_spend > 0:
        google_cac = get_cac_for_spend('GOOGLE', google_spend)
        google_customers = int(google_spend / google_cac)
        total_new_customers += google_customers
    
    # Calculate customers from Meta Ads
    meta_spend = marketing_data['META']
    if meta_spend > 0:
        meta_cac = get_cac_for_spend('META', meta_spend)
        meta_customers = int(meta_spend / meta_cac)
        total_new_customers += meta_customers
    
    return total_new_customers

def calculate_organic_customers(month_name):
    """Calculate new organic customers from personal outreach"""
    return ORGANIC_CUSTOMERS.get(month_name, 0)

def distribute_customers_by_package(total_customers):
    """Distribute customers across packages based on CUSTOMER_DISTRIBUTION"""
    return {
        'basic': int(total_customers * CUSTOMER_DISTRIBUTION['basic']),
        'pro': int(total_customers * CUSTOMER_DISTRIBUTION['pro']),
        'enterprise': int(total_customers * CUSTOMER_DISTRIBUTION['enterprise'])
    }

def apply_dynamic_churn(current_customers, customer_ages):
    """Apply dynamic churn rates based on customer age"""
    churned_customers = {}
    remaining_customers = {}
    updated_ages = {}
    
    for package in ['basic', 'pro', 'enterprise']:
        package_customers = current_customers.get(package, 0)
        package_ages = customer_ages.get(package, [])
        
        # Ensure we have age data for all customers
        while len(package_ages) < package_customers:
            package_ages.append(1)  # New customers start at age 1
        
        churned = 0
        new_ages = []
        
        # Apply churn based on customer age
        for i, age in enumerate(package_ages):
            if age <= CHURN_PHASES['early']['months']:
                churn_rate = CHURN_PHASES['early']['rates'][package] / 12  # Convert annual to monthly
            else:
                churn_rate = CHURN_PHASES['late']['rates'][package] / 12
            
            # Check if this customer churns
            if random.random() < churn_rate:
                churned += 1
            else:
                new_ages.append(age + 1)  # Customer stays, age increases
        
        churned_customers[package] = churned
        remaining_customers[package] = max(0, package_customers - churned)
        updated_ages[package] = new_ages
    
    return remaining_customers, churned_customers, updated_ages

def apply_package_upgrades(current_customers, customer_ages):
    """Apply package upgrades (basic->pro, pro->enterprise)"""
    upgraded_customers = current_customers.copy()
    updated_ages = customer_ages.copy()
    
    # Basic to Pro upgrades
    basic_customers = current_customers.get('basic', 0)
    basic_to_pro_upgrades = int(basic_customers * UPGRADE_RATES['basic_to_pro'])
    
    if basic_to_pro_upgrades > 0:
        upgraded_customers['basic'] = max(0, upgraded_customers['basic'] - basic_to_pro_upgrades)
        upgraded_customers['pro'] = upgraded_customers.get('pro', 0) + basic_to_pro_upgrades
        
        # Move customer ages from basic to pro
        if 'basic' in updated_ages and len(updated_ages['basic']) >= basic_to_pro_upgrades:
            moving_ages = updated_ages['basic'][-basic_to_pro_upgrades:]
            updated_ages['basic'] = updated_ages['basic'][:-basic_to_pro_upgrades]
            updated_ages['pro'] = updated_ages.get('pro', []) + moving_ages
    
    # Pro to Enterprise upgrades
    pro_customers = upgraded_customers.get('pro', 0)
    pro_to_enterprise_upgrades = int(pro_customers * UPGRADE_RATES['pro_to_enterprise'])
    
    if pro_to_enterprise_upgrades > 0:
        upgraded_customers['pro'] = max(0, upgraded_customers['pro'] - pro_to_enterprise_upgrades)
        upgraded_customers['enterprise'] = upgraded_customers.get('enterprise', 0) + pro_to_enterprise_upgrades
        
        # Move customer ages from pro to enterprise
        if 'pro' in updated_ages and len(updated_ages['pro']) >= pro_to_enterprise_upgrades:
            moving_ages = updated_ages['pro'][-pro_to_enterprise_upgrades:]
            updated_ages['pro'] = updated_ages['pro'][:-pro_to_enterprise_upgrades]
            updated_ages['enterprise'] = updated_ages.get('enterprise', []) + moving_ages
    
    return upgraded_customers, updated_ages

def get_website_conversion_rates(month_number):
    """Get website conversion rates based on month (early vs late)"""
    if month_number <= 6:
        return WEBSITE_PACKAGE_CONVERSION_DYNAMIC['early']
    else:
        return WEBSITE_PACKAGE_CONVERSION_DYNAMIC['late']

def calculate_website_customers(current_customers, cumulative_website_customers, month_number):
    """Calculate new website package customers based on TOTAL monthly customers with dynamic conversion rates"""
    conversion_rates = get_website_conversion_rates(month_number)
    new_website_customers = {}
    
    for package in ['basic', 'pro', 'enterprise']:
        conversion_rate = conversion_rates.get(package, 0)
        # Apply conversion rate to total customers in each package (not just new ones)
        total_package_customers = current_customers[package]
        # Calculate how many should have websites total
        target_website_customers = round(total_package_customers * conversion_rate)
        # Calculate new website customers (difference from current cumulative)
        current_website_customers = cumulative_website_customers[package]
        new_website_customers[package] = max(0, target_website_customers - current_website_customers)
        cumulative_website_customers[package] += new_website_customers[package]
    
    return new_website_customers, cumulative_website_customers