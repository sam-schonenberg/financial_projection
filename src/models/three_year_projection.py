#!/usr/bin/env python3
"""
Three-Year Financial Projection Module
Extends the existing 2026 projection to cover 2026-2028
"""

import pandas as pd
from datetime import datetime, timedelta
from config.settings import PROJECT_START, ACTIVE_LOAN_SCENARIO, ACTIVE_LOAN_STRATEGY
from src.models.projection import generate_financial_projection
from src.calculations.loans import get_loan_details, calculate_loan_balance, calculate_monthly_loan_payment

def generate_three_year_projection():
    """Generate 3-year financial projection (2026-2028) with loan progression"""
    
    print("🚀 Generating 3-Year Financial Projection (2026-2028)...")
    print("=" * 60)
    
    # Get loan details for multi-year analysis
    loan_details = get_loan_details(ACTIVE_LOAN_SCENARIO)
    
    yearly_projections = {}
    cumulative_data = {
        'customers': 0,
        'revenue': 0,
        'profit': 0,
        'cash_flow': 0,
        'loan_balance': loan_details['amount'],
        'total_loan_payments': 0
    }
    
    # Generate projections for each year
    for year in [2026, 2027, 2028]:
        print(f"\n📊 Processing {year}...")
        
        # Generate single year projection
        if year == 2026:
            # Use existing 2026 projection
            df_year = generate_financial_projection()
        else:
            # For future years, create projected data based on growth patterns
            df_year = project_future_year(year, yearly_projections.get(year-1))
        
        # Calculate year-end metrics
        final_month = df_year.iloc[-1]
        year_metrics = {
            'year': year,
            'final_customers': final_month['total_customers'],
            'final_monthly_revenue': final_month['total_revenue'],
            'final_monthly_profit': final_month['monthly_profit'],
            'annual_revenue': df_year['total_revenue'].sum(),
            'annual_profit': df_year['monthly_profit'].sum(),
            'annual_cash_flow': df_year['net_cash_flow'].sum(),
            'cumulative_cash_flow': final_month['cumulative_cash_flow'],
            'designers_count': final_month['designers_count'],
            'vishal_fulltime': final_month['vishal_fulltime'],
            'marketing_spend': df_year['marketing_spend'].sum(),
            'dataframe': df_year
        }
        
        # Calculate loan metrics for this year
        if loan_details['amount'] > 0:
            annual_loan_payments = df_year['loan_payment'].sum()
            year_end_loan_balance = calculate_loan_balance(
                loan_details['amount'], 
                loan_details['interest_rate'], 
                loan_details['term_months'], 
                year * 12,
                loan_details.get('interest_only_months', 0)
            )
            
            year_metrics.update({
                'annual_loan_payments': annual_loan_payments,
                'year_end_loan_balance': year_end_loan_balance,
                'loan_payment_to_revenue_ratio': (annual_loan_payments / year_metrics['annual_revenue'] * 100) if year_metrics['annual_revenue'] > 0 else 0
            })
            
            cumulative_data['total_loan_payments'] += annual_loan_payments
            cumulative_data['loan_balance'] = year_end_loan_balance
        
        # Update cumulative tracking
        cumulative_data['customers'] = year_metrics['final_customers']
        cumulative_data['revenue'] += year_metrics['annual_revenue']
        cumulative_data['profit'] += year_metrics['annual_profit']
        cumulative_data['cash_flow'] = year_metrics['cumulative_cash_flow']
        
        yearly_projections[year] = year_metrics
        
        print(f"   {year} Final Customers: {year_metrics['final_customers']:,}")
        print(f"   {year} Annual Revenue: €{year_metrics['annual_revenue']:,.2f}")
        print(f"   {year} Annual Profit: €{year_metrics['annual_profit']:,.2f}")
        if loan_details['amount'] > 0:
            print(f"   {year} Loan Payments: €{year_metrics['annual_loan_payments']:,.2f}")
            print(f"   {year} Loan Balance: €{year_metrics['year_end_loan_balance']:,.2f}")
    
    return yearly_projections, cumulative_data

def project_future_year(year, previous_year_data):
    """Project future year based on growth patterns from previous year"""
    
    # Growth assumptions for future years
    growth_factors = {
        2027: {
            'customer_growth': 0.8,  # 80% growth rate (slower than startup phase)
            'revenue_per_customer_growth': 1.1,  # 10% increase in ARPU
            'cost_efficiency': 0.95,  # 5% cost efficiency improvement
            'churn_improvement': 0.9  # 10% reduction in churn
        },
        2028: {
            'customer_growth': 0.6,  # 60% growth rate (maturing business)
            'revenue_per_customer_growth': 1.08,  # 8% increase in ARPU
            'cost_efficiency': 0.92,  # 8% cost efficiency improvement
            'churn_improvement': 0.85  # 15% reduction in churn
        }
    }
    
    factors = growth_factors.get(year, growth_factors[2028])
    
    # Create month names for the year
    months_total = 12
    month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']
    
    # Base projections on previous year's final month
    if previous_year_data:
        base_customers = int(previous_year_data['final_customers'] * factors['customer_growth'])
        base_monthly_revenue = previous_year_data['final_monthly_revenue'] * factors['revenue_per_customer_growth']
    else:
        # Fallback if no previous data
        base_customers = 200
        base_monthly_revenue = 15000
    
    monthly_data = []
    current_customers = {'basic': int(base_customers * 0.55), 
                        'pro': int(base_customers * 0.35), 
                        'enterprise': int(base_customers * 0.10)}
    cumulative_profit = 0
    cumulative_cash_flow = 0
    current_bank_balance = 50000  # Assume healthy cash position by year 2+
    
    # Get loan details for payment calculations
    loan_details = get_loan_details(ACTIVE_LOAN_SCENARIO)
    
    for month in range(months_total):
        current_date = datetime(year, month + 1, 1)
        month_name = month_names[month]
        
        # Progressive growth throughout the year
        month_multiplier = 1 + (month / 12) * 0.3  # 30% growth over the year
        
        # Customer calculations
        total_customers = sum(current_customers.values())
        total_customers = int(total_customers * month_multiplier)
        
        # Redistribute customers across tiers
        current_customers = {
            'basic': int(total_customers * 0.50),  # Slightly lower basic percentage as business matures
            'pro': int(total_customers * 0.38),    # Higher pro percentage
            'enterprise': int(total_customers * 0.12)  # Higher enterprise percentage
        }
        
        # Revenue calculations (improved ARPU over time)
        saas_revenue = (current_customers['basic'] * 35.99 + 
                       current_customers['pro'] * 119.99 + 
                       current_customers['enterprise'] * 259.99)
        
        # Website revenue (lower conversion in mature years)
        new_websites = int(total_customers * 0.02)  # 2% of customers get new websites monthly
        website_revenue = new_websites * 400  # Average website price
        
        total_revenue = saas_revenue + website_revenue
        
        # Cost calculations (improved efficiency)
        base_costs = total_customers * 0.20  # Variable costs
        marketing_spend = min(total_revenue * 0.15, 5000)  # 15% of revenue, capped
        
        # Team costs (scaled with business)
        designers_count = max(3, int(total_customers / 100))  # 1 designer per 100 customers, minimum 3
        designer_costs = designers_count * 1750
        
        vishal_compensation = total_revenue * 0.03  # 3% of revenue (full-time)
        founder_support = min(total_revenue * 0.05, 2000)  # 5% of revenue, capped
        
        # Infrastructure and fixed costs
        infrastructure_costs = 200 + (total_customers * 0.05)  # Scaling infrastructure
        fixed_costs = 100  # Insurance, etc.
        
        # Loan payments
        monthly_loan_payment = 0
        if loan_details['amount'] > 0:
            interest_only_months = loan_details.get('interest_only_months', 0)
            total_months_elapsed = (year - 2026) * 12 + month + 1
            monthly_loan_payment = calculate_monthly_loan_payment(
                loan_details['amount'], 
                loan_details['interest_rate'], 
                loan_details['term_months'],
                interest_only_months,
                total_months_elapsed
            )
        
        total_costs = (base_costs + marketing_spend + designer_costs + 
                      vishal_compensation + founder_support + infrastructure_costs + 
                      fixed_costs + monthly_loan_payment)
        
        # Apply efficiency improvements
        total_costs *= factors['cost_efficiency']
        
        # Profit and cash flow
        monthly_profit = total_revenue - total_costs
        cumulative_profit += monthly_profit
        
        net_cash_flow = monthly_profit  # Simplified
        cumulative_cash_flow += net_cash_flow
        current_bank_balance += net_cash_flow
        
        # Calculate loan balance
        loan_balance = 0
        if loan_details['amount'] > 0:
            total_months_elapsed = (year - 2026) * 12 + month + 1
            loan_balance = calculate_loan_balance(
                loan_details['amount'], 
                loan_details['interest_rate'], 
                loan_details['term_months'], 
                total_months_elapsed,
                loan_details.get('interest_only_months', 0)
            )
        
        # Store monthly data
        monthly_data.append({
            'month': month + 1,
            'date': current_date.strftime('%Y-%m'),
            'basic_customers': current_customers['basic'],
            'pro_customers': current_customers['pro'],
            'enterprise_customers': current_customers['enterprise'],
            'total_customers': total_customers,
            'new_customers_total': int(total_customers * 0.08),  # 8% growth monthly
            'churned_customers': int(total_customers * 0.02),   # 2% churn monthly
            'total_website_customers': int(total_customers * 0.3),  # 30% have websites
            'new_websites_total': new_websites,
            'designers_count': designers_count,
            'designer_utilization': min(0.85, new_websites / (designers_count * 5)),  # Max 85% utilization
            'vishal_fulltime': 1,  # Assume full-time in future years
            'total_employees': 1 + 1 + designers_count,  # Owner + Vishal + designers
            'saas_revenue': round(saas_revenue, 2),
            'website_revenue': round(website_revenue, 2),
            'total_revenue': round(total_revenue, 2),
            'variable_costs': round(base_costs, 2),
            'marketing_spend': round(marketing_spend, 2),
            'vishal_compensation': round(vishal_compensation, 2),
            'founder_support': round(founder_support, 2),
            'designer_costs': round(designer_costs, 2),
            'total_costs': round(total_costs, 2),
            'monthly_profit': round(monthly_profit, 2),
            'cumulative_profit': round(cumulative_profit, 2),
            'rolling_avg_profit': round(cumulative_profit / (month + 1), 2),
            'net_cash_flow': round(net_cash_flow, 2),
            'cash_flow_margin': round((net_cash_flow / total_revenue * 100), 1) if total_revenue > 0 else 0,
            'cumulative_cash_flow': round(cumulative_cash_flow, 2),
            'bank_balance': round(current_bank_balance, 2),
            'google_spend': round(marketing_spend * 0.6, 2),
            'meta_spend': round(marketing_spend * 0.4, 2),
            'google_customers': int(total_customers * 0.03),
            'meta_customers': int(total_customers * 0.02),
            'organic_customers': int(total_customers * 0.03),
            'loan_balance': round(loan_balance, 2),
            'loan_payment': round(monthly_loan_payment, 2)
        })
    
    return pd.DataFrame(monthly_data)

def create_three_year_summary(yearly_projections, cumulative_data):
    """Create a comprehensive 3-year summary report"""
    
    print("\n" + "=" * 80)
    print("THREE-YEAR FINANCIAL PROJECTION SUMMARY (2026-2028)")
    print("=" * 80)
    
    # Year-by-year summary
    print("\nYEAR-BY-YEAR BREAKDOWN:")
    print("-" * 50)
    
    summary_data = []
    for year in [2026, 2027, 2028]:
        data = yearly_projections[year]
        print(f"\n{year}:")
        print(f"  Final Customers: {data['final_customers']:,}")
        print(f"  Annual Revenue: €{data['annual_revenue']:,.2f}")
        print(f"  Annual Profit: €{data['annual_profit']:,.2f}")
        print(f"  Final Monthly Revenue: €{data['final_monthly_revenue']:,.2f}")
        print(f"  Final Monthly Profit: €{data['final_monthly_profit']:,.2f}")
        print(f"  Designers: {data['designers_count']}")
        print(f"  Marketing Spend: €{data['marketing_spend']:,.2f}")
        
        if 'annual_loan_payments' in data:
            print(f"  Loan Payments: €{data['annual_loan_payments']:,.2f}")
            print(f"  Year-end Loan Balance: €{data['year_end_loan_balance']:,.2f}")
            print(f"  Loan/Revenue Ratio: {data['loan_payment_to_revenue_ratio']:.1f}%")
        
        # Calculate growth rates
        if year > 2026:
            prev_data = yearly_projections[year-1]
            customer_growth = ((data['final_customers'] - prev_data['final_customers']) / prev_data['final_customers']) * 100
            revenue_growth = ((data['annual_revenue'] - prev_data['annual_revenue']) / prev_data['annual_revenue']) * 100
            print(f"  Customer Growth: {customer_growth:+.1f}%")
            print(f"  Revenue Growth: {revenue_growth:+.1f}%")
        
        # Store for CSV export
        summary_data.append({
            'year': year,
            'final_customers': data['final_customers'],
            'annual_revenue': data['annual_revenue'],
            'annual_profit': data['annual_profit'],
            'final_monthly_revenue': data['final_monthly_revenue'],
            'final_monthly_profit': data['final_monthly_profit'],
            'designers_count': data['designers_count'],
            'marketing_spend': data['marketing_spend'],
            'cumulative_cash_flow': data['cumulative_cash_flow'],
            'annual_loan_payments': data.get('annual_loan_payments', 0),
            'year_end_loan_balance': data.get('year_end_loan_balance', 0)
        })
    
    # 3-year totals
    print(f"\n3-YEAR CUMULATIVE TOTALS:")
    print(f"Final Customer Base: {cumulative_data['customers']:,}")
    print(f"Total Revenue (3 years): €{cumulative_data['revenue']:,.2f}")
    print(f"Total Profit (3 years): €{cumulative_data['profit']:,.2f}")
    print(f"Final Cash Position: €{cumulative_data['cash_flow']:,.2f}")
    
    if cumulative_data['loan_balance'] >= 0:
        print(f"Total Loan Payments: €{cumulative_data['total_loan_payments']:,.2f}")
        print(f"Remaining Loan Balance: €{cumulative_data['loan_balance']:,.2f}")
        
        # ROI calculation
        if cumulative_data['total_loan_payments'] > 0:
            net_profit_after_loan = cumulative_data['profit'] - cumulative_data['total_loan_payments']
            print(f"Net Profit After Loan: €{net_profit_after_loan:,.2f}")
    
    # Business metrics
    total_revenue = cumulative_data['revenue']
    if total_revenue > 0:
        avg_profit_margin = (cumulative_data['profit'] / total_revenue) * 100
        print(f"Average Profit Margin (3 years): {avg_profit_margin:.1f}%")
    
    # Growth trajectory
    first_year_revenue = yearly_projections[2026]['annual_revenue']
    last_year_revenue = yearly_projections[2028]['annual_revenue']
    if first_year_revenue > 0:
        total_growth = ((last_year_revenue - first_year_revenue) / first_year_revenue) * 100
        cagr = (((last_year_revenue / first_year_revenue) ** (1/2)) - 1) * 100
        print(f"Total Revenue Growth (2026-2028): {total_growth:.1f}%")
        print(f"Compound Annual Growth Rate: {cagr:.1f}%")
    
    return pd.DataFrame(summary_data)

def save_three_year_reports(yearly_projections, summary_df):
    """Save comprehensive 3-year reports"""
    
    import os
    reports_folder = 'outputs/three_year_projection_2026_2028'
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
    
    # Save 3-year summary
    summary_df.to_csv(f'{reports_folder}/three_year_summary.csv', index=False)
    print(f"\n💾 3-year summary saved to '{reports_folder}/three_year_summary.csv'")
    
    # Save individual year projections
    for year in [2026, 2027, 2028]:
        df = yearly_projections[year]['dataframe']
        df.to_csv(f'{reports_folder}/projection_{year}.csv', index=False)
        print(f"💾 {year} projection saved to '{reports_folder}/projection_{year}.csv'")
    
    # Create combined master file with all years
    combined_data = []
    for year in [2026, 2027, 2028]:
        df = yearly_projections[year]['dataframe'].copy()
        df['year'] = year
        combined_data.append(df)
    
    master_df = pd.concat(combined_data, ignore_index=True)
    master_df.to_csv(f'{reports_folder}/master_three_year_projection.csv', index=False)
    print(f"💾 Master 3-year file saved to '{reports_folder}/master_three_year_projection.csv'")
    
    return reports_folder

def main():
    """Main function to run 3-year projection"""
    print("🚀 Three-Year Financial Projection Tool")
    print("=" * 50)
    
    try:
        # Generate 3-year projections
        yearly_projections, cumulative_data = generate_three_year_projection()
        
        # Create summary
        summary_df = create_three_year_summary(yearly_projections, cumulative_data)
        
        # Save reports
        reports_folder = save_three_year_reports(yearly_projections, summary_df)
        
        print(f"\n🎉 3-Year projection complete!")
        print(f"📁 All reports saved in '{reports_folder}/'")
        
        return yearly_projections, summary_df
        
    except Exception as e:
        print(f"❌ Error generating 3-year projection: {str(e)}")
        raise

if __name__ == "__main__":
    main()