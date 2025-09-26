import os

def create_organized_csv_reports(df):
    """Create organized CSV reports in separate folder structure - updated with loan investment tracking"""
    # Create reports folder
    reports_folder = 'outputs/financial_reports_2026'
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
    
    # 1. Customer & Growth Metrics
    customer_data = df[['month', 'date', 
                       'basic_customers', 'pro_customers', 'enterprise_customers', 'total_customers',
                       'new_customers_total', 'churned_customers']].copy()
    customer_data.to_csv(f'{reports_folder}/customer_growth.csv', index=False)
    
    # 2. Website Production & Revenue
    website_data = df[['month', 'date',
                      'total_website_customers', 'new_websites_total',
                      'website_revenue']].copy()
    website_data.to_csv(f'{reports_folder}/website_production.csv', index=False)
    
    # 3. Financial Performance
    financial_data = df[['month', 'date',
                        'saas_revenue', 'website_revenue', 'total_revenue',
                        'variable_costs', 'total_costs',
                        'monthly_profit', 'cumulative_profit', 'rolling_avg_profit',
                        'net_cash_flow', 'cash_flow_margin', 'cumulative_cash_flow']].copy()
    financial_data.to_csv(f'{reports_folder}/financial_performance.csv', index=False)
    
    # 4. Team & Operations
    team_data = df[['month', 'date',
                   'designers_count', 'designer_utilization',
                   'vishal_fulltime', 'vishal_compensation', 
                   'founder_support', 'total_employees']].copy()
    team_data['employment_status'] = team_data['vishal_fulltime'].apply(lambda x: 'Full-time' if x == 1 else 'Freelance')
    team_data.to_csv(f'{reports_folder}/team_operations.csv', index=False)
    
    # 5. Marketing & Acquisition
    marketing_data = df[['month', 'date',
                        'marketing_spend', 'google_spend', 'meta_spend',
                        'google_customers', 'meta_customers', 'organic_customers']].copy()
    # Calculate total customers from marketing
    marketing_data['marketing_customers'] = marketing_data['google_customers'] + marketing_data['meta_customers']
    # Calculate CAC if customers were acquired
    marketing_data['cac_marketing'] = marketing_data.apply(
        lambda row: row['marketing_spend'] / row['marketing_customers'] 
        if row['marketing_customers'] > 0 else 0, axis=1
    )
    marketing_data.to_csv(f'{reports_folder}/marketing_acquisition.csv', index=False)
    
    # 6. Cash Flow Analysis
    cashflow_data = df[['month', 'date',
                       'net_cash_flow', 'cash_flow_margin', 'cumulative_cash_flow', 'bank_balance',
                       'total_revenue', 'total_costs']].copy()
    cashflow_data.to_csv(f'{reports_folder}/cash_flow.csv', index=False)
    
    # 7. Reinvestment Analysis (if reinvestment is active)
    if 'reinvestment_active' in df.columns and df['reinvestment_active'].sum() > 0:
        reinvestment_data = df[['month', 'date',
                               'reinvestment_active', 'marketing_reinvestment', 
                               'personnel_fund', 'total_reinvested']].copy()
        # Convert 1/0 to Yes/No for readability in CSV
        reinvestment_data['reinvestment_triggered'] = reinvestment_data['reinvestment_active'].apply(lambda x: 'Yes' if x == 1 else 'No')
        reinvestment_data = reinvestment_data.drop('reinvestment_active', axis=1)
        reinvestment_data.to_csv(f'{reports_folder}/reinvestment_analysis.csv', index=False)
        print(f"  - reinvestment_analysis.csv")
    
    # 8. Loan Analysis (if loan is active) - UPDATED with investment tracking
    if 'loan_balance' in df.columns and df['loan_balance'].iloc[0] > 0:
        loan_data = df[['month', 'date',
                       'loan_balance', 'loan_payment', 'loan_marketing_boost',
                       'monthly_loan_investments', 'total_loan_investments', 
                       'remaining_loan_funds', 'loan_investment_rate']].copy()
        loan_data.to_csv(f'{reports_folder}/loan_impact.csv', index=False)
        print(f"  - loan_impact.csv (with investment tracking)")
        
        # NEW: Dedicated Investment Report
        investment_data = df[['month', 'date', 'monthly_loan_investments', 'total_loan_investments',
                             'loan_marketing_boost', 'marketing_spend', 'remaining_loan_funds', 
                             'loan_investment_rate']].copy()
        # Add investment efficiency metrics
        investment_data['marketing_boost_pct'] = investment_data.apply(
            lambda row: (row['loan_marketing_boost'] / row['marketing_spend'] * 100) 
            if row['marketing_spend'] > 0 else 0, axis=1
        )
        investment_data.to_csv(f'{reports_folder}/loan_investments.csv', index=False)
        print(f"  - loan_investments.csv")
    
    print(f"\nOrganized reports created in '{reports_folder}/' folder:")
    print("  - customer_growth.csv")
    print("  - website_production.csv") 
    print("  - financial_performance.csv")
    print("  - team_operations.csv")
    print("  - marketing_acquisition.csv")
    print("  - cash_flow.csv")
    
    return reports_folder