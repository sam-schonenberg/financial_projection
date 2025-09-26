# Investment Loan Configuration

# Investment Loan Configuration

# Loan Scenarios to Analyze
LOAN_SCENARIOS = {
    'no_loan': {
        'amount': 0,
        'interest_rate': 0.0,
        'term_months': 0,
        'description': 'No loan - baseline scenario'
    },
    'actual_loan': {
        'amount': 12000,
        'interest_rate': 0.036,  # 3.6% annual interest
        'term_months': 72,  # 6 years total (72 months)
        'interest_only_months': 12,  # First 12 months interest-only
        'description': '10500€ loan - 1 year interest-only at 3.6%, then 5 years gradual payoff (72 months total)'
    },
    'small_loan': {
        'amount': 10000,
        'interest_rate': 0.0439,
        'term_months': 24,
        'description': '€10k loan over 2 years'
    },
    'medium_loan': {
        'amount': 25000,
        'interest_rate': 0.0439,  # 6.5% annual
        'term_months': 36,
        'description': '€25k loan over 3 years'
    },
    'large_loan': {
        'amount': 50000,
        'interest_rate': 0.0439,  # 7% annual
        'term_months': 48,
        'description': '€50k loan over 4 years'
    },
    'aggressive_loan': {
        'amount': 100000,
        'interest_rate': 0.0439,  # 7.5% annual
        'term_months': 60,
        'description': '€100k loan over 5 years'
    }
}

# How to use loan funds (allocation percentages must sum to 1.0)
LOAN_ALLOCATION_STRATEGIES = {
    'marketing_focused': {
        'description': 'Focus on customer acquisition',
        'marketing_boost': 0.60,
        'team_expansion': 0.15,
        'infrastructure': 0.10,
        'cash_reserve': 0.05,
        'founder_support': 0.10
    },
    'realistic_12k': {
        'description': 'Realistic allocation for €12k loan - gradual deployment',
        'marketing_boost': 0.50,  # €6,000 for marketing over time
        'team_expansion': 0.30,   # €3,600 for team (designer + Vishal support)
        'infrastructure': 0.10,   # €1,200 for better tools
        'cash_reserve': 0.10,     # €1,200 safety buffer
        'founder_support': 0.00   # No direct founder support from loan
    },
    'balanced': {
        'description': 'Balanced growth approach',
        'marketing_boost': 0.40,
        'team_expansion': 0.25,
        'infrastructure': 0.15,
        'cash_reserve': 0.10,
        'founder_support': 0.10
    },
    'team_focused': {
        'description': 'Focus on team building',
        'marketing_boost': 0.25,
        'team_expansion': 0.45,
        'infrastructure': 0.15,
        'cash_reserve': 0.05,
        'founder_support': 0.10
    },
    'conservative': {
        'description': 'Conservative with large cash reserve',
        'marketing_boost': 0.25,
        'team_expansion': 0.20,
        'infrastructure': 0.10,
        'cash_reserve': 0.30,
        'founder_support': 0.15
    }
}

# Marketing boost efficiency (diminishing returns)
# Key: additional monthly marketing spend, Value: efficiency multiplier
MARKETING_BOOST_EFFICIENCY = {
    500: 1.0,      # First €500 extra = 100% efficiency
    1000: 0.9,     # Next €500 (€500-€1000) = 90% efficiency
    2000: 0.8,     # Next €1000 (€1000-€2000) = 80% efficiency
    3000: 0.7,     # Next €1000 (€2000-€3000) = 70% efficiency
    5000: 0.6,     # Next €2000 (€3000-€5000) = 60% efficiency
    10000: 0.5     # Beyond €5000 = 50% efficiency
}

# Team expansion acceleration
TEAM_EXPANSION_BENEFITS = {
    'designer_early_hire': {
        'threshold': 5000,  # If we have €5k+ allocated to team, hire designer 3 months early
        'benefit': 'hire_designer_early',
        'months_accelerated': 3
    },
    'vishal_fulltime_early': {
        'threshold': 10000,  # If we have €10k+ allocated to team, Vishal goes full-time earlier
        'benefit': 'vishal_fulltime_early',
        'profit_threshold_reduction': 0.3  # Reduce threshold by 30%
    },
    'additional_designer': {
        'threshold': 15000,  # If we have €15k+ allocated, can support additional designer capacity
        'benefit': 'additional_designer_capacity',
        'capacity_boost': 0.2  # 20% more capacity per designer
    }
}

# Infrastructure improvements
INFRASTRUCTURE_BENEFITS = {
    'better_tools': {
        'monthly_cost': 200,  # Costs €200/month more
        'productivity_boost': 0.15,  # 15% productivity increase for team
        'customer_satisfaction': 0.05  # 5% lower churn rate
    },
    'premium_infrastructure': {
        'monthly_cost': 500,  # Costs €500/month more
        'productivity_boost': 0.25,  # 25% productivity increase
        'customer_satisfaction': 0.10,  # 10% lower churn rate
        'scaling_efficiency': 0.20  # 20% lower variable costs per customer
    }
}

# Founder support benefits (personal salary/living expenses during growth phase)
FOUNDER_SUPPORT_BENEFITS = {
    'early_salary_start': {
        'threshold': 3000,  # If we have €3k+ allocated to founder support
        'benefit': 'owner_salary_early',
        'salary_threshold_reduction': 0.5  # Start owner salary when monthly profit ≥ €700 instead of €1,400
    },
    'founder_focus': {
        'threshold': 8000,  # If we have €8k+ allocated to founder support
        'benefit': 'founder_focus_time',
        'productivity_boost': 0.20,  # 20% boost to organic customer acquisition
        'strategic_benefits': 0.15  # 15% boost to overall business efficiency
    },
    'founder_cash_buffer': {
        'threshold': 12000,  # If we have €12k+ allocated
        'benefit': 'founder_cash_buffer',
        'months_covered': 6,  # Can focus on business for 6 months without worrying about personal finances
        'risk_reduction': 0.25  # 25% reduction in "forced pivot" scenarios
    }
}

# Loan disbursement timing
LOAN_DISBURSEMENT = {
    'timing': 'month_1',  # When loan is received
    'setup_fee': 0.02,    # 2% setup fee
    'early_repayment_penalty': 0.03  # 3% penalty if paid off early
}