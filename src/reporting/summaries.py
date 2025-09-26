from config.settings import PROJECT_START, PROJECT_END

def print_summary(df):
    """Print summary statistics - updated for cleaned master table"""
    print("=" * 60)
    print("FINANCIAL PROJECTION SUMMARY - 2026")
    print("=" * 60)
    
    # Project overview
    print(f"Project Duration: {PROJECT_START.strftime('%Y-%m-%d')} to {PROJECT_END.strftime('%Y-%m-%d')}")
    print(f"Total Months: {len(df)}")
    print()
    
    # Final numbers
    final_month = df.iloc[-1]
    print("FINAL PROJECTIONS (End of 2026):")
    print(f"Total SaaS Customers: {final_month['total_customers']:,}")
    print(f"  - Basic: {final_month['basic_customers']:,}")
    print(f"  - Pro: {final_month['pro_customers']:,}")
    print(f"  - Enterprise: {final_month['enterprise_customers']:,}")
    print()
    
    print(f"Total Website Customers: {final_month['total_website_customers']:,}")
    print()
    
    print(f"Web Designers Employed: {final_month['designers_count']}")
    print(f"Vishal Status: {'Full-time' if final_month['vishal_fulltime'] else 'Freelance'}")
    print(f"Designer Utilization: {final_month['designer_utilization']:.1%}")
    print()
    
    # Revenue breakdown
    print(f"Final Monthly SaaS Revenue: €{final_month['saas_revenue']:,.2f}")
    print(f"Final Monthly Website Revenue: €{final_month['website_revenue']:,.2f}")
    print(f"Final Monthly Total Revenue: €{final_month['total_revenue']:,.2f}")
    print(f"Final Monthly Costs: €{final_month['total_costs']:,.2f}")
    print(f"  - Vishal Compensation: €{final_month['vishal_compensation']:,.2f}")
    print(f"  - Founder Support: €{final_month['founder_support']:,.2f}")
    print(f"  - Designer Costs: €{final_month['designer_costs']:,.2f}")
    print(f"  - Marketing Spend: €{final_month['marketing_spend']:,.2f}")
    print(f"Final Monthly Profit: €{final_month['monthly_profit']:,.2f}")
    print(f"Final Cash Flow Margin: {final_month['cash_flow_margin']:.1f}%")
    print()
    
    # Total revenue streams
    total_saas_revenue = df['saas_revenue'].sum()
    total_website_revenue = df['website_revenue'].sum()
    total_vishal_compensation = df['vishal_compensation'].sum()
    total_founder_support = df['founder_support'].sum()
    total_designer_costs = df['designer_costs'].sum()
    
    print(f"CUMULATIVE REVENUE (2026):")
    print(f"Total SaaS Revenue: €{total_saas_revenue:,.2f}")
    print(f"Total Website Revenue: €{total_website_revenue:,.2f}")
    print(f"Total Combined Revenue: €{total_saas_revenue + total_website_revenue:,.2f}")
    print()
    
    print(f"CUMULATIVE COSTS (2026):")
    print(f"Total Founder Support: €{total_founder_support:,.2f}")
    print(f"Total Designer Costs: €{total_designer_costs:,.2f}")
    print(f"Total Vishal Compensation: €{total_vishal_compensation:,.2f}")
    print(f"Total Marketing Spend: €{df['marketing_spend'].sum():,.2f}")
    print()
    
    print(f"CUMULATIVE NET PROFIT: €{final_month['cumulative_profit']:,.2f}")
    print(f"CUMULATIVE CASH FLOW: €{final_month['cumulative_cash_flow']:,.2f}")
    print()
    
    # Marketing efficiency
    total_marketing_spend = df['marketing_spend'].sum()
    total_customers_acquired_marketing = df['google_customers'].sum() + df['meta_customers'].sum()
    total_customers_acquired_organic = df['organic_customers'].sum()
    total_customers_acquired = df['new_customers_total'].sum()
    avg_cac = total_marketing_spend / total_customers_acquired_marketing if total_customers_acquired_marketing > 0 else 0
    print(f"MARKETING SUMMARY:")
    print(f"Total Marketing Spend: €{total_marketing_spend:,.2f}")
    print(f"Customers from Marketing: {total_customers_acquired_marketing:,}")
    print(f"Customers from Organic: {total_customers_acquired_organic:,}")
    print(f"Total Customers Acquired: {total_customers_acquired:,}")
    print(f"Average CAC (Marketing only): €{avg_cac:.2f}")
    print()
    
    # Website production summary
    total_websites = df['new_websites_total'].sum()
    print(f"WEBSITE PRODUCTION SUMMARY:")
    print(f"Total Websites Created: {total_websites:,}")
    print(f"Average Designers per Month: {df['designers_count'].mean():.1f}")
    print(f"Peak Designers: {df['designers_count'].max()}")
    print()
    
    # Cash flow summary
    positive_cash_months = len(df[df['net_cash_flow'] > 0])
    negative_cash_months = len(df[df['net_cash_flow'] <= 0])
    max_negative_cash = df['cumulative_cash_flow'].min()
    avg_cash_flow_margin = df[df['total_revenue'] > 0]['cash_flow_margin'].mean()
    print(f"CASH FLOW SUMMARY:")
    print(f"Months with Positive Cash Flow: {positive_cash_months}")
    print(f"Months with Negative Cash Flow: {negative_cash_months}")
    print(f"Lowest Cumulative Cash Position: €{max_negative_cash:,.2f}")
    print(f"Final Cash Position: €{final_month['cumulative_cash_flow']:,.2f}")
    print(f"Average Cash Flow Margin: {avg_cash_flow_margin:.1f}%")
    print()
    
    # Vishal compensation summary
    months_freelance = len(df[df['vishal_fulltime'] == 0])
    months_fulltime = len(df[df['vishal_fulltime'] == 1])
    fulltime_transition_month = None
    for idx, row in df.iterrows():
        if row['vishal_fulltime'] == 1:
            fulltime_transition_month = row['month']
            break
    
    print(f"VISHAL COLLABORATION SUMMARY:")
    print(f"Months as Freelance: {months_freelance}")
    print(f"Months as Full-time: {months_fulltime}")
    if fulltime_transition_month:
        print(f"Transition to Full-time: Month {fulltime_transition_month} ({df.iloc[fulltime_transition_month-1]['date']})")
    print(f"Total Compensation Paid: €{total_vishal_compensation:,.2f}")
    print()
    
    # Founder support summary
    months_with_founder_support = len(df[df['founder_support'] > 0])
    avg_founder_support = df[df['founder_support'] > 0]['founder_support'].mean() if months_with_founder_support > 0 else 0
    
    print(f"FOUNDER SUPPORT SUMMARY:")
    print(f"Total Founder Support Paid: €{total_founder_support:,.2f}")
    print(f"Months with Support: {months_with_founder_support}")
    print(f"Average Monthly Support: €{avg_founder_support:,.2f}")
    print()
    
    # Reinvestment summary (if applicable)
    if 'reinvestment_active' in df.columns:
        reinvestment_months = len(df[df['reinvestment_active'] == 1])
        total_marketing_reinvested = df['marketing_reinvestment'].sum()
        
        print(f"REINVESTMENT SUMMARY (30% Margin Threshold):")
        print(f"Months with Reinvestment Active: {reinvestment_months}")
        print(f"Total Marketing Reinvestment: €{total_marketing_reinvested:,.2f}")
        print(f"Total Reinvested: €{df['total_reinvested'].iloc[-1]:,.2f}")
        print()
    
    # Break-even analysis
    break_even_month = None
    cash_flow_positive_month = None
    founder_support_start_month = None
    
    for idx, row in df.iterrows():
        if row['cumulative_profit'] > 0 and break_even_month is None:
            break_even_month = row['month']
        if row['cumulative_cash_flow'] > 0 and cash_flow_positive_month is None:
            cash_flow_positive_month = row['month']
        if row['founder_support'] > 0 and founder_support_start_month is None:
            founder_support_start_month = row['month']
    
    if break_even_month:
        print(f"Break-even (Profit) Month: {break_even_month} ({df.iloc[break_even_month-1]['date']})")
    else:
        print("Break-even (Profit): Not achieved within 2026")
        
    if founder_support_start_month:
        print(f"Founder Support Starts: Month {founder_support_start_month} ({df.iloc[founder_support_start_month-1]['date']})")
    else:
        print("Founder Support: Not started (monthly profit never reached €2,000)")
        
    if cash_flow_positive_month:
        print(f"Cash Flow Positive Month: {cash_flow_positive_month} ({df.iloc[cash_flow_positive_month-1]['date']})")
    else:
        print("Cash Flow Positive: Not achieved within 2026")

def print_detailed_monthly_data(df):
    """Display key monthly data for verification - updated for cleaned master table"""
    print("\nKey Monthly Metrics:")
    preview_columns = ['month', 'date', 'total_customers', 'new_customers_total', 'designers_count', 
                      'founder_support', 'vishal_compensation', 'total_revenue', 
                      'total_costs', 'monthly_profit', 'net_cash_flow', 'cumulative_cash_flow', 'bank_balance']
    print(df[preview_columns].to_string(index=False))

def print_cashflow_analysis(df):
    """Show cash flow analysis with percentages - updated for cleaned master table"""
    print("\nCash Flow Analysis (First 6 months):")
    cashflow_columns = ['month', 'cash_flow_margin', 'net_cash_flow', 'cumulative_cash_flow', 
                       'bank_balance', 'reinvestment_active', 'marketing_reinvestment']
    print(df[cashflow_columns].head(6).to_string(index=False))

def print_website_conversion_analysis(df):
    """Show website conversion analysis - updated for cleaned master table"""
    print("\nWebsite Production Analysis:")
    website_columns = ['month', 'basic_customers', 'pro_customers', 'enterprise_customers',
                      'new_websites_total', 'total_website_customers', 'designers_count']
    print(df[website_columns].to_string(index=False))