import matplotlib.pyplot as plt

def create_visualization(df):
    """Create financial projection charts - updated for cleaned master table"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Revenue streams vs costs and cash flow with margin
    ax1.plot(df['month'], df['saas_revenue'], label='SaaS Revenue', linewidth=2)
    ax1.plot(df['month'], df['website_revenue'], label='Website Revenue', linewidth=2)
    ax1.plot(df['month'], df['total_revenue'], label='Total Revenue', linewidth=2, linestyle='--')
    ax1.plot(df['month'], df['total_costs'], label='Total Costs', linewidth=2)
    ax1.plot(df['month'], df['net_cash_flow'], label='Net Cash Flow', linewidth=2, alpha=0.7)
    
    # Add cash flow margin on secondary y-axis
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['month'], df['cash_flow_margin'], color='orange', linestyle=':', linewidth=2, alpha=0.8, label='Cash Flow Margin %')
    ax1_twin.set_ylabel('Cash Flow Margin (%)', color='orange')
    ax1_twin.tick_params(axis='y', labelcolor='orange')
    ax1_twin.axhline(y=0, color='orange', linestyle=':', alpha=0.3)
    
    ax1.set_title('Monthly Revenue vs Costs vs Cash Flow & Margin')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Amount (€)')
    ax1.legend(loc='upper left')
    ax1_twin.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Customer growth and designer scaling
    ax2.plot(df['month'], df['total_customers'], label='Total SaaS Customers', linewidth=2)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(df['month'], df['designers_count'], color='red', marker='o', linewidth=2, label='Designers')
    ax2.set_title('Customer Growth vs Designer Scaling')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('SaaS Customers', color='blue')
    ax2_twin.set_ylabel('Designers', color='red')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left')
    ax2_twin.legend(loc='upper right')
    
    # Cumulative profit vs cumulative cash flow
    ax3.plot(df['month'], df['cumulative_profit'], label='Cumulative Profit', linewidth=3, color='green')
    ax3.plot(df['month'], df['cumulative_cash_flow'], label='Cumulative Cash Flow', linewidth=3, color='blue')
    ax3.set_title('Cumulative Profit vs Cumulative Cash Flow')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Amount (€)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    # Team compensation breakdown (updated for cleaned master table)
    ax4.plot(df['month'], df['founder_support'], linewidth=2, color='blue', label='Founder Support')
    ax4.plot(df['month'], df['vishal_compensation'], linewidth=2, color='purple', label='Vishal Total')
    ax4.plot(df['month'], df['designer_costs'], linewidth=2, color='orange', label='Designer Costs')
    total_team_costs = df['founder_support'] + df['vishal_compensation'] + df['designer_costs']
    ax4.plot(df['month'], total_team_costs, linewidth=3, color='red', linestyle='--', label='Total Team Costs')
    ax4.set_title('Monthly Team Compensation Breakdown')
    ax4.set_xlabel('Month')
    ax4.set_ylabel('Amount (€)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the plot as an image
    output_path = 'outputs/financial_projection_2026_charts.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Charts saved as '{output_path}'")
    
    plt.show()
    return output_path

def create_advanced_visualization(df):
    """Create additional advanced charts for reinvestment analysis"""
    if 'reinvestment_active' not in df.columns:
        return
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Cash Flow Margin & Reinvestment Trigger
    ax1.plot(df['month'], df['cash_flow_margin'], linewidth=3, color='blue', label='Cash Flow Margin')
    ax1.axhline(y=30, color='red', linestyle='--', alpha=0.7, label='30% Trigger Threshold')
    
    # Highlight reinvestment months
    reinvestment_months = df[df['reinvestment_active'] == True]
    if not reinvestment_months.empty:
        ax1.scatter(reinvestment_months['month'], reinvestment_months['cash_flow_margin'], 
                   color='red', s=100, alpha=0.7, label='Reinvestment Active', zorder=5)
    
    ax1.set_title('Cash Flow Margin & Reinvestment Trigger Points')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Cash Flow Margin (%)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Marketing Spend Breakdown
    ax2.plot(df['month'], df['google_spend'], label='Google Ads', linewidth=2)
    ax2.plot(df['month'], df['meta_spend'], label='Meta Ads', linewidth=2)
    ax2.plot(df['month'], df['marketing_reinvestment'], label='Reinvestment Boost', linewidth=2, linestyle=':', alpha=0.8)
    ax2.plot(df['month'], df['marketing_spend'], label='Total Marketing', linewidth=3, linestyle='--', alpha=0.7)
    ax2.set_title('Marketing Spend Breakdown & Reinvestment')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Amount (€)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Customer Acquisition Channels
    ax3.bar(df['month'], df['google_customers'], label='Google Customers', alpha=0.7)
    ax3.bar(df['month'], df['meta_customers'], bottom=df['google_customers'], label='Meta Customers', alpha=0.7)
    ax3.bar(df['month'], df['organic_customers'], 
           bottom=df['google_customers'] + df['meta_customers'], label='Organic Customers', alpha=0.7)
    ax3.set_title('Monthly Customer Acquisition by Channel')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('New Customers')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Reinvestment Fund Accumulation
    ax4.plot(df['month'], df['total_reinvested'], linewidth=3, color='green', label='Cumulative Reinvested')
    ax4.plot(df['month'], df['personnel_fund'], linewidth=2, color='orange', label='Personnel Fund')
    ax4_twin = ax4.twinx()
    ax4_twin.plot(df['month'], df['designers_count'], color='red', marker='s', linewidth=2, label='Designers Count')
    
    ax4.set_title('Reinvestment Fund Accumulation & Team Growth')
    ax4.set_xlabel('Month')
    ax4.set_ylabel('Amount (€)', color='green')
    ax4_twin.set_ylabel('Designers Count', color='red')
    ax4.legend(loc='upper left')
    ax4_twin.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the advanced plot
    output_path = 'outputs/reinvestment_analysis_2026_charts.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Advanced reinvestment charts saved as '{output_path}'")
    
    plt.show()
    return output_path