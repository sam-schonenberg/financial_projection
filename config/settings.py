from datetime import datetime, timedelta

# Project Timeline - 2026 ONLY
PROJECT_START = datetime(2026, 1, 1)
PROJECT_END = datetime(2027, 1, 1)

# Owner Configuration
OWNER_SALARY = 1400  # Fixed monthly salary for owner (not used for Einzelunternehmer)

# Organic customer growth from outreach (manual sales, LinkedIn, local visits)
ORGANIC_CUSTOMERS = {
    'january': 1,
    'february': 1,
    'march': 1,
    'april': 2,
    'may': 2,
    'june': 2,
    'july': 2,
    'august': 2,
    'september': 2,
    'october': 2,
    'november': 2,
    'december': 2
}

# Money spent on marketing
MARKETING_COSTS = {
    'january': {'GOOGLE': 0, 'META': 0},
    'february': {'GOOGLE': 0, 'META': 0},
    'march': {'GOOGLE': 500, 'META': 0},
    'april': {'GOOGLE': 500, 'META': 0},
    'may': {'GOOGLE': 500, 'META': 200},
    'june': {'GOOGLE': 1000, 'META': 400},
    'july': {'GOOGLE': 1500, 'META': 600},
    'august': {'GOOGLE': 2000, 'META': 800},
    'september': {'GOOGLE': 2000, 'META': 1000},
    'october': {'GOOGLE': 2000, 'META': 1000},
    'november': {'GOOGLE': 2000, 'META': 1000},
    'december': {'GOOGLE': 2000, 'META': 1000}
}

# Marketing CAC table with diminishing returns (key: money spent, value: customer acquisition cost)
GOOGLE_CAC = {
    '500': 50,
    '1000': 57.5,
    '1500': 65,
    '2000': 72.5
}

META_CAC = {
    '200': 60,
    '400': 64,
    '600': 68,
    '800': 72,
    '1000': 76
}

# customer projected distribution
CUSTOMER_DISTRIBUTION = {
    'basic': 0.55,
    'pro': 0.35,
    'enterprise': 0.1
}

# projected churn rates (dynamic - higher for new customers)
CHURN_PHASES = {
    'early': {'months': 3, 'rates': {'basic': 0.08, 'pro': 0.06, 'enterprise': 0.04}},  # Higher churn for first 3 months
    'late': {'rates': {'basic': 0.04, 'pro': 0.03, 'enterprise': 0.015}}  # Lower loyal customer churn
}

# Customer Packages and Pricing
PACKAGES = {
    'basic': {'price': 29.99},
    'pro': {'price': 99.99},
    'enterprise': {'price': 299.99}
}

# Web Design & SaaS Packages pricing (updated based on your table)
PACKAGES_WITH_WEBSITE = {
    'basic': {'price': 35.99, 'upfront_cost': 250},
    'pro': {'price': 119.99, 'upfront_cost': 500},
    'enterprise': {'price': 259.99, 'upfront_cost': 1000}
}

# Estimated Website Package Interest by SaaS Tier (dynamic conversion rates)
WEBSITE_PACKAGE_CONVERSION_DYNAMIC = {
    'early': {'basic': 0.7, 'pro': 0.7, 'enterprise': 0.4},  # Higher conversion for early outreach clients (months 1-6)
    'late': {'basic': 0.4, 'pro': 0.5, 'enterprise': 0.2}   # Lower conversion for later marketing clients (months 7+)
}

# Employee Costs Configuration
EMPLOYEE_COSTS = {
    'web_designer': 1750,
    'vishal_fulltime_salary': 1500
}

# FIXED: Web Designer Configuration with safety margins
WEB_DESIGNER_CONFIG = {
    'capacity_per_month': {
        'basic': 10,
        'pro': 4,
        'enterprise': 2
    },
    'first_hire_threshold': 0.25,      # Hire first designer at 25% utilization
    'subsequent_hire_threshold': 0.75, # Hire additional at 75% utilization
    'fire_threshold': 0.3,             # Fire if below 30% for 2+ months
    'emergency_hire_threshold': 1.0,   # ADDED: Emergency hiring at 100%+ utilization
    'capacity_buffer': 0.1             # ADDED: 10% buffer for capacity planning
}

# FIXED: Vishal Collaboration Configuration with correct rates
VISHAL_CONFIG = {
    'freelance_profit_share': 0.20,    # 20% of monthly profit when freelance
    'website_revenue_share': 0.20,     # 20% of website revenue when freelance
    'fulltime_profit_share': 0.03,     # CORRECTED: 3% when full-time (was 0.20)
    'fulltime_salary': 1500,           # ADDED: €1,500/month base salary when full-time
    'fulltime_threshold': 8000,        # Switch to full-time at €8k rolling avg profit
    'profit_share_threshold': 2000,    # Only pay profit share if profit > €2k
    'exit_bonus_share': 0.03           # Exit bonus (not used in current model)
}

# LLM Costs Configuration (threshold-based)
LLM_COSTS = {
    'loss_making': {
        'cost': 43,  # ChatGPT Plus + Claude Pro (€20 + €23 = €43)
        'description': 'ChatGPT Plus + Claude Pro for personal use'
    },
    'profitable': {
        'cost': 110,  # Claude Max for higher usage
        'threshold': 0,  # Switch when monthly profit > €0
        'description': 'Claude Max for increased usage'
    },
    'team_expansion': {
        'cost': 150,  # Claude Team (5 users minimum at €30/user)
        'threshold': 5000,  # Switch when monthly profit > €5k
        'description': 'Claude Team (5 users) for collaborative work'
    },
    'scale_up': {
        'cost': 300,  # Claude Team (10 users at €30/user)
        'threshold': 15000,  # Switch when monthly profit > €15k
        'description': 'Claude Team (10 users) for full team access'
    }
}

# Fixed Monthly Costs (excluding per-employee costs)
FIXED_COSTS = {
    'adobe_license': 0,
    'business_insurance': 35
}

# Per-Employee Costs
PER_EMPLOYEE_COSTS = {
    'google_workspace': 10.20  # €10.20 per employee per month
}

# One-time Legal & Compliance Costs (spread across specific months)
LEGAL_COMPLIANCE_COSTS = {
    'privacy_policy_terms': {
        'month': 1,
        'cost': 1000
    },
    'freelancer_contracts': {
        'month': 1,
        'cost': 300
    },
    'data_protection_audit': {
        'month': 1,
        'cost': 800
    }
}

# Domain: €15/year → bundled into Pro/Enterprise tiers
# Variable Costs (per customer)
VARIABLE_COSTS = {
    'basic': {'month': 0.18, 'year': 0},
    'pro': {'month': 0.45, 'year': 15.00},
    'enterprise': {'month': 1.20, 'year': 75.00}
}

# Package Upgrade Rates (customers upgrading between tiers)
UPGRADE_RATES = {
    'basic_to_pro': 0.01,      # 1% of basic customers upgrade to pro each month
    'pro_to_enterprise': 0.005  # 0.5% of pro customers upgrade to enterprise each month
}

# Website Project Settings
WEBSITE_CANCELLATION_RATE = 0.05  # 5% of website projects get cancelled/refunded

# Rolling Average Settings
ROLLING_AVERAGE_MONTHS = 3  # Use 3-month rolling average for stability-sensitive decisions

# Server scaling costs based on total customer count
SERVER_UPGRADES = {
    '10': 10,
    '50': 20,
    '100': 40,
    '200': 70,
    '500': 120
}

# FIXED: Founder support configuration with explicit bounds - MOVED HERE for easy modification
FOUNDER_SUPPORT_CONFIG = {
    'min_profit_threshold': 2500,        # Start founder support when monthly profit > €2k
    'min_support': 500,                  # Minimum €500/month
    'max_support': 20000,               
    'profit_breakpoints': {
        2000: 500,  
        5000: 1000,  
        8000: 2000,  
        12000: 3400, 
        15000: 4800 
    }
}

# FIXED: Reinvestment configuration with validation - MOVED HERE for easy modification
REINVESTMENT_CONFIG = {
    'cash_flow_margin_threshold': 30.0,  # 30% margin threshold - CHANGE THIS to adjust trigger
    'reinvestment_percentage': 0.6,      # Reinvest 60% of excess cash flow
    'marketing_allocation': 0.5,         # 50% of reinvestment goes to marketing
    'personnel_allocation': 0.5,         # 50% of reinvestment goes to personnel
    'min_monthly_reinvestment': 500,     # Minimum €500/month to trigger reinvestment
    'max_monthly_marketing_boost': 3000, # Cap marketing boost at €3k/month
    'personnel_threshold': 2000,         # Need €2k+ accumulated to hire additional personnel
    'max_personnel_fund': 10000          # Cap personnel fund accumulation
}

# ADDED: Validation limits to prevent calculation errors
VALIDATION_LIMITS = {
    'max_founder_support': 20000,        # Hard cap on founder support (should match FOUNDER_SUPPORT_CONFIG['max_support'])
    'max_utilization_before_hire': 1.0, # Trigger emergency hiring above 100%
    'min_monthly_profit': -20000,      # Flag extreme negative profits
    'max_marketing_spend_per_month': 10000,  # Sanity check on marketing
    'max_designers': 50                 # Reasonable upper limit on team size
}

# Loan Configuration
ACTIVE_LOAN_SCENARIO = 'actual_loan'  # Change this to test different loan scenarios
ACTIVE_LOAN_STRATEGY = 'realistic_12k'  # Change this to test different allocation strategies