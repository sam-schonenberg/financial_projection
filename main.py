#!/usr/bin/env python3
"""
Financial Projection Script for 2026 - UPDATED WITH LOAN INVESTMENT TRACKING
Clean entry point for the financial modeling system with actual loan scenario and investment tracking
"""

import os
from src.models.projection import generate_financial_projection, print_reinvestment_summary, print_loan_investment_summary
from src.models.loan_analysis import generate_loan_recommendation_report, save_loan_analysis_reports, analyze_optimal_loan_scenario
from src.reporting.csv_reports import create_organized_csv_reports
from src.reporting.visualizations import create_visualization
from src.reporting.summaries import (
    print_summary, print_detailed_monthly_data, 
    print_cashflow_analysis, print_website_conversion_analysis
)

def ensure_output_directory():
    """Ensure the outputs directory exists"""
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

def validate_projection_results(df):
    """
    ADDED: Validate projection results to catch calculation errors
    """
    print("\n" + "="*50)
    print("🔍 VALIDATION CHECKS")
    print("="*50)
    
    validation_passed = True
    issues_found = []
    
    # Check founder support never exceeds maximum
    max_founder_support = df['founder_support'].max()
    if max_founder_support > 2000:
        issues_found.append(f"❌ Founder support exceeds €2,000 maximum: €{max_founder_support:.2f}")
        validation_passed = False
    else:
        print(f"✅ Founder support within bounds (max: €{max_founder_support:.2f})")
    
    # Check designer utilization doesn't consistently exceed 100%
    high_utilization_months = len(df[df['designer_utilization'] > 1.0])
    if high_utilization_months > 2:  # Allow occasional spikes
        issues_found.append(f"❌ Designer utilization >100% for {high_utilization_months} months")
        validation_passed = False
    else:
        print(f"✅ Designer utilization manageable ({high_utilization_months} months >100%)")
    
    # Check for reasonable profit progression
    final_profit = df['monthly_profit'].iloc[-1]
    if final_profit < -5000:  # Allow some losses but flag extreme cases
        issues_found.append(f"❌ Final monthly profit is extremely negative: €{final_profit:.2f}")
        validation_passed = False
    else:
        print(f"✅ Final monthly profit reasonable: €{final_profit:.2f}")
    
    # Check cash flow makes sense
    final_cash_flow = df['cumulative_cash_flow'].iloc[-1]
    total_revenue = df['total_revenue'].sum()
    if abs(final_cash_flow) > total_revenue * 1.5:  # Cash flow shouldn't exceed 1.5x total revenue
        issues_found.append(f"❌ Cumulative cash flow seems unrealistic: €{final_cash_flow:.2f}")
        validation_passed = False
    else:
        print(f"✅ Cumulative cash flow reasonable: €{final_cash_flow:.2f}")
    
    # NEW: Check loan investment tracking
    if 'total_loan_investments' in df.columns:
        final_investments = df['total_loan_investments'].iloc[-1]
        investment_rate = df['loan_investment_rate'].iloc[-1]
        remaining_funds = df['remaining_loan_funds'].iloc[-1]
        
        print(f"✅ Loan investments tracked: €{final_investments:.2f} ({investment_rate:.1f}% deployment rate)")
        print(f"✅ Remaining loan funds: €{remaining_funds:.2f}")
        
        # Validate loan fund accounting
        if final_investments + remaining_funds > df['loan_balance'].iloc[0] + df['loan_payment'].sum() * 1.1:
            issues_found.append("❌ Loan fund accounting doesn't balance")
        else:
            print("✅ Loan fund accounting balanced")
    
    # Check reinvestment logic if applicable
    if 'reinvestment_active' in df.columns:
        reinvestment_months = len(df[df['reinvestment_active'] == True])
        total_reinvested = df['total_reinvested'].iloc[-1] if reinvestment_months > 0 else 0
        print(f"✅ Reinvestment strategy: {reinvestment_months} months active, €{total_reinvested:.2f} total")
    
    # Print any issues found
    if issues_found:
        print(f"\n⚠️  VALIDATION ISSUES FOUND:")
        for issue in issues_found:
            print(f"   {issue}")
        print(f"\n❗ Please review calculation logic for the above issues.")
    else:
        print(f"\n🎉 ALL VALIDATION CHECKS PASSED!")
    
    return validation_passed

def main():
    """Main execution function"""
    print("Financial Projection System for 2026 - WITH ACTUAL LOAN SCENARIO")
    print("="*70)
    print("🏦 Actual Loan Configuration:")
    print("   • €12,000 loan amount")
    print("   • 3.6% annual interest rate")
    print("   • 72 months total term (6 years)")
    print("   • First 12 months: Interest-only (€36/month)")
    print("   • Investment tracking enabled")
    print("="*70)
    
    # Ask user what they want to run
    print("\nOptions:")
    print("1. Run projection with actual loan scenario")
    print("2. Analyze all loan scenarios and get recommendations")
    print("3. Run both actual loan projection and scenario analysis")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    # Ensure output directory exists
    ensure_output_directory()
    
    if choice in ['1', '3']:
        print("\n🚀 Generating financial projection with actual loan scenario...")
        run_actual_loan_projection()
    
    if choice in ['2', '3']:
        print("\n📊 Analyzing loan scenarios...")
        run_loan_analysis()
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("All reports and charts have been generated in the 'outputs/' folder")
    print("🏦 Actual loan projections show:")
    print("   • Minimal 2026 loan costs (€36/month interest-only)")
    print("   • Investment deployment tracking")
    print("   • Enhanced growth potential analysis")
    print("   • Loan fund utilization metrics")

def run_actual_loan_projection():
    """Run the financial projection with actual loan scenario and investment tracking"""
    try:
        # Generate projections
        print("📊 Running projection calculations with actual loan...")
        df = generate_financial_projection()
        
        # ADDED: Validate results before proceeding
        validation_passed = validate_projection_results(df)
        
        if not validation_passed:
            print("\n⚠️  Some validation issues were found. Proceeding with analysis but please review the calculations.")
        
        # Print summary analysis
        print_summary(df)
        
        # Print reinvestment analysis if applicable
        if 'reinvestment_active' in df.columns:
            print_reinvestment_summary(df)
        
        # NEW: Print loan investment analysis
        if 'total_loan_investments' in df.columns:
            print_loan_investment_summary(df)
        
        # Create organized CSV reports
        print("\n📋 Creating organized CSV reports...")
        create_organized_csv_reports(df)
        
        # Create visualizations
        print("\n📈 Generating charts...")
        create_visualization(df)
        
        # Save master CSV for further analysis
        master_csv_path = 'outputs/financial_projection_2026_actual_loan_master.csv'
        df.to_csv(master_csv_path, index=False)
        print(f"\n💾 Master projection saved to '{master_csv_path}'")
        
        # Save transposed master CSV
        master_csv_transposed_path = 'outputs/financial_projection_2026_actual_loan_master_transposed.csv'
        df_transposed = df.transpose()
        df_transposed.to_csv(master_csv_transposed_path)
        print(f"💾 Transposed master projection saved to '{master_csv_transposed_path}'")
        
        # Display detailed analysis
        print_detailed_monthly_data(df)
        print_cashflow_analysis(df)
        print_website_conversion_analysis(df)
        
        # UPDATED: Summary of key metrics with loan investment tracking
        print("\n" + "="*50)
        print("📈 KEY PERFORMANCE INDICATORS")
        print("="*50)
        final_month = df.iloc[-1]
        print(f"Final Monthly Revenue: €{final_month['total_revenue']:,.2f}")
        print(f"Final Monthly Profit: €{final_month['monthly_profit']:,.2f}")
        print(f"Final Cash Flow Margin: {final_month['cash_flow_margin']:.1f}%")
        print(f"Total Customers: {final_month['total_customers']:,}")
        print(f"Designers Employed: {final_month['designers_count']}")
        print(f"Designer Utilization: {final_month['designer_utilization']:.1%}")
        print(f"Cumulative Profit: €{final_month['cumulative_profit']:,.2f}")
        print(f"Cumulative Cash Flow: €{final_month['cumulative_cash_flow']:,.2f}")
        print(f"Final Bank Balance: €{final_month['bank_balance']:,.2f}")
        
        # Loan investment summary
        if 'total_loan_investments' in df.columns:
            print(f"\n🏦 LOAN INVESTMENT SUMMARY:")
            print(f"Total Loan Investments: €{final_month['total_loan_investments']:,.2f}")
            print(f"Investment Deployment Rate: {final_month['loan_investment_rate']:.1f}%")
            print(f"Remaining Loan Funds: €{final_month['remaining_loan_funds']:,.2f}")
            print(f"Total Loan Payments (2026): €{df['loan_payment'].sum():,.2f}")
        
        # Reinvestment summary
        if final_month.get('reinvestment_active', False):
            reinvestment_months = len(df[df['reinvestment_active'] == True])
            total_reinvested = final_month.get('total_reinvested', 0)
            print(f"Reinvestment Strategy: Active for {reinvestment_months} months")
            print(f"Total Reinvested: €{total_reinvested:,.2f}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error during projection calculation: {str(e)}")
        print("Please check your configuration and calculation files.")
        raise

def run_loan_analysis():
    """Run comprehensive loan analysis"""
    try:
        # Generate loan analysis and recommendations
        analysis = generate_loan_recommendation_report()
        
        # Save detailed analysis reports
        save_loan_analysis_reports(analysis)
        
    except Exception as e:
        print(f"❌ Error during loan analysis: {str(e)}")
        print("Please check your loan configuration files.")
        raise

if __name__ == "__main__":
    main()