"""
Loan scenario comparison and analysis module
"""

import pandas as pd
from config.settings import ACTIVE_LOAN_SCENARIO, ACTIVE_LOAN_STRATEGY
from config.loan_settings import LOAN_SCENARIOS, LOAN_ALLOCATION_STRATEGIES
from src.calculations.loans import calculate_loan_impact_summary
from src.models.projection import generate_financial_projection

def compare_all_loan_scenarios():
    """Generate projections for all loan scenarios and compare results"""
    
    # Store original settings
    original_scenario = ACTIVE_LOAN_SCENARIO
    original_strategy = ACTIVE_LOAN_STRATEGY
    
    comparison_results = []
    
    print("Analyzing all loan scenarios...")
    
    for scenario_name in LOAN_SCENARIOS.keys():
        for strategy_name in LOAN_ALLOCATION_STRATEGIES.keys():
            print(f"  - Running {scenario_name} with {strategy_name} strategy...")
            
            # Temporarily update settings for this scenario
            import config.settings
            config.settings.ACTIVE_LOAN_SCENARIO = scenario_name
            config.settings.ACTIVE_LOAN_STRATEGY = strategy_name
            
            # Generate projection
            df = generate_financial_projection()
            
            # Calculate summary metrics
            final_month = df.iloc[-1]
            total_revenue = df['total_revenue'].sum()
            total_profit = df['monthly_profit'].sum()
            total_loan_payments = df['monthly_loan_payment'].sum()
            final_cash_flow = final_month['cumulative_cash_flow']
            final_customers = final_month['total_customers']
            
            # Break-even analysis
            break_even_month = None
            for idx, row in df.iterrows():
                if row['cumulative_profit'] > 0:
                    break_even_month = row['month']
                    break
            
            # ROI calculation
            loan_amount = LOAN_SCENARIOS[scenario_name]['amount']
            net_roi = (total_profit - total_loan_payments) if loan_amount > 0 else total_profit
            roi_percentage = ((net_roi / loan_amount) * 100) if loan_amount > 0 else 0
            
            comparison_results.append({
                'scenario': scenario_name,
                'strategy': strategy_name,
                'loan_amount': loan_amount,
                'total_revenue': total_revenue,
                'total_profit': total_profit,
                'total_loan_payments': total_loan_payments,
                'net_profit_after_loan': total_profit - total_loan_payments,
                'final_cash_flow': final_cash_flow,
                'final_customers': final_customers,
                'break_even_month': break_even_month or 'Not achieved',
                'roi_percentage': roi_percentage,
                'loan_description': LOAN_SCENARIOS[scenario_name]['description'],
                'strategy_description': LOAN_ALLOCATION_STRATEGIES[strategy_name]['description']
            })
    
    # Restore original settings
    config.settings.ACTIVE_LOAN_SCENARIO = original_scenario
    config.settings.ACTIVE_LOAN_STRATEGY = original_strategy
    
    return pd.DataFrame(comparison_results)

def analyze_optimal_loan_scenario():
    """Analyze and recommend the optimal loan scenario"""
    
    comparison_df = compare_all_loan_scenarios()
    
    # Sort by different metrics to find optimal scenarios
    best_roi = comparison_df.loc[comparison_df['roi_percentage'].idxmax()]
    best_cash_flow = comparison_df.loc[comparison_df['final_cash_flow'].idxmax()]
    best_growth = comparison_df.loc[comparison_df['final_customers'].idxmax()]
    best_profit = comparison_df.loc[comparison_df['net_profit_after_loan'].idxmax()]
    
    # Conservative option (lowest loan amount with positive ROI)
    positive_roi_scenarios = comparison_df[comparison_df['roi_percentage'] > 0]
    conservative = positive_roi_scenarios.loc[positive_roi_scenarios['loan_amount'].idxmin()] if not positive_roi_scenarios.empty else None
    
    analysis = {
        'best_roi': best_roi.to_dict(),
        'best_cash_flow': best_cash_flow.to_dict(),
        'best_growth': best_growth.to_dict(),
        'best_profit': best_profit.to_dict(),
        'conservative_option': conservative.to_dict() if conservative is not None else None,
        'comparison_table': comparison_df
    }
    
    return analysis

def generate_loan_recommendation_report():
    """Generate a comprehensive loan recommendation report"""
    
    analysis = analyze_optimal_loan_scenario()
    
    print("\n" + "="*80)
    print("LOAN SCENARIO ANALYSIS & RECOMMENDATIONS")
    print("="*80)
    
    print("\nSCENARIO COMPARISON SUMMARY:")
    print("-" * 40)
    
    # Display top scenarios by different metrics
    scenarios = [
        ("Best ROI", analysis['best_roi']),
        ("Best Cash Flow", analysis['best_cash_flow']),
        ("Best Growth", analysis['best_growth']),
        ("Best Total Profit", analysis['best_profit'])
    ]
    
    if analysis['conservative_option']:
        scenarios.append(("Conservative Option", analysis['conservative_option']))
    
    for metric_name, scenario in scenarios:
        print(f"\n{metric_name}:")
        print(f"  Loan: {scenario['loan_description']}")
        print(f"  Strategy: {scenario['strategy_description']}")
        print(f"  Amount: €{scenario['loan_amount']:,}")
        print(f"  Final Customers: {scenario['final_customers']:,}")
        print(f"  Total Revenue: €{scenario['total_revenue']:,.2f}")
        print(f"  Net Profit After Loan: €{scenario['net_profit_after_loan']:,.2f}")
        print(f"  Final Cash Flow: €{scenario['final_cash_flow']:,.2f}")
        print(f"  ROI: {scenario['roi_percentage']:.1f}%")
        print(f"  Break-even: {scenario['break_even_month']}")
    
    print("\n" + "="*80)
    print("DETAILED COMPARISON TABLE:")
    print("="*80)
    
    # Display comparison table
    display_columns = ['scenario', 'strategy', 'loan_amount', 'final_customers', 
                      'total_revenue', 'net_profit_after_loan', 'final_cash_flow', 
                      'roi_percentage', 'break_even_month']
    
    print(analysis['comparison_table'][display_columns].to_string(index=False, float_format='%.2f'))
    
    # Recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS:")
    print("="*80)
    
    best_overall = analysis['best_roi']
    print(f"\nRecommended Scenario: {best_overall['loan_description']}")
    print(f"Recommended Strategy: {best_overall['strategy_description']}")
    print(f"\nReasoning:")
    print(f"- Provides {best_overall['roi_percentage']:.1f}% ROI")
    print(f"- Achieves {best_overall['final_customers']:,} customers by end of 2026")
    print(f"- Generates €{best_overall['net_profit_after_loan']:,.2f} net profit after loan payments")
    print(f"- Break-even achieved in month {best_overall['break_even_month']}")
    
    if analysis['conservative_option']:
        conservative = analysis['conservative_option']
        print(f"\nConservative Alternative: {conservative['loan_description']}")
        print(f"- Lower risk with €{conservative['loan_amount']:,} loan amount")
        print(f"- Still provides {conservative['roi_percentage']:.1f}% ROI")
        print(f"- Final cash flow: €{conservative['final_cash_flow']:,.2f}")
    
    return analysis

def save_loan_analysis_reports(analysis):
    """Save loan analysis to CSV files"""
    import os
    
    reports_folder = 'outputs/loan_analysis_2026'
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
    
    # Save comparison table
    analysis['comparison_table'].to_csv(f'{reports_folder}/loan_scenario_comparison.csv', index=False)
    
    # Save detailed projections for top scenarios
    top_scenarios = [
        ('best_roi', analysis['best_roi']),
        ('best_cash_flow', analysis['best_cash_flow']),
        ('best_growth', analysis['best_growth'])
    ]
    
    for scenario_type, scenario_data in top_scenarios:
        # Generate detailed projection for this scenario
        import config.settings
        config.settings.ACTIVE_LOAN_SCENARIO = scenario_data['scenario']
        config.settings.ACTIVE_LOAN_STRATEGY = scenario_data['strategy']
        
        df = generate_financial_projection()
        df.to_csv(f'{reports_folder}/{scenario_type}_detailed_projection.csv', index=False)
    
    print(f"\nLoan analysis reports saved to '{reports_folder}/' folder")
    return reports_folder