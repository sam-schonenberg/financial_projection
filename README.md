# Financial Projection System

A comprehensive Python-based financial modeling tool for SaaS businesses with website development services. Designed for realistic business projections, loan analysis, and bank presentations.

## 🎯 Project Overview

This system generates detailed financial projections for a hybrid SaaS + web development business model, including:
- Monthly customer acquisition and churn modeling
- Revenue projections from subscription and project-based services
- Team scaling and cost management
- Loan scenario analysis and investment tracking
- Cash flow management and reinvestment strategies

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pandas
- matplotlib

### Installation
```bash
git clone https://github.com/yourusername/financial-projection.git
cd financial-projection
pip install -r requirements.txt
```

### Basic Usage
```bash
# Run main projection with actual loan scenario
python main.py

# Run simplified realistic projection for IHK presentation
python realistic_projection.py
```

## 📊 Key Features

### Business Model Support
- **SaaS Subscriptions**: Basic (€35.99), Pro (€119.99), Enterprise (€259.99)
- **Website Development**: Project-based revenue with freelancer capacity management
- **Customer Acquisition**: Marketing-driven + organic growth modeling
- **Realistic Churn**: Dynamic churn rates based on customer age and tier

### Financial Analysis
- **Multi-scenario Loan Analysis**: Compare different loan amounts and strategies
- **Cash Flow Management**: Always-positive cash flow with safety thresholds
- **Team Scaling**: Automated hiring/firing based on demand and revenue
- **Reinvestment Strategy**: Automatic reinvestment when margins exceed 30%

### Reporting & Visualization
- **Organized CSV Reports**: Customer growth, financial performance, team operations
- **Interactive Charts**: Revenue trends, cash flow analysis, team scaling
- **Bank-Ready Summaries**: Professional reports for loan applications

## 🏗️ Project Structure

```
financial-projection/
├── config/                    # Configuration files
│   ├── settings.py           # Main business parameters
│   └── loan_settings.py      # Loan scenarios and strategies
├── src/
│   ├── calculations/         # Core calculation modules
│   │   ├── customers.py      # Customer acquisition and churn
│   │   ├── revenue.py        # Revenue calculations
│   │   ├── costs.py          # Cost management
│   │   ├── team.py           # Team scaling logic
│   │   └── loans.py          # Loan analysis
│   ├── models/               # Financial models
│   │   ├── projection.py     # Main projection engine
│   │   ├── loan_analysis.py  # Loan scenario comparison
│   │   └── three_year_projection.py
│   └── reporting/            # Report generation
│       ├── csv_reports.py    # CSV export functions
│       ├── summaries.py      # Text summaries
│       └── visualizations.py # Chart generation
├── main.py                   # Main application entry point
├── realistic_projection.py   # Simplified IHK/bank version
└── requirements.txt
```

## 🔧 Configuration

### Business Parameters (`config/settings.py`)
- Customer acquisition costs and conversion rates
- Subscription pricing and customer distribution
- Team costs and hiring thresholds
- Marketing spend schedules

### Loan Scenarios (`config/loan_settings.py`)
- Multiple loan amounts and terms
- Investment allocation strategies
- Infrastructure and team expansion benefits

## 💼 Use Cases

### For Business Planning
- Monthly financial projections
- Team scaling decisions
- Cash flow management
- Growth strategy validation

### For Bank Presentations
- Realistic revenue projections
- Loan repayment capacity analysis
- Risk assessment and mitigation
- Job creation potential

### For Investor Relations
- Multi-year growth trajectories
- ROI analysis and break-even points
- Scenario comparison and sensitivity analysis

## 📈 Sample Output

### Key Metrics (End of 2026)
- **Customers**: 150-200 total
- **Monthly Revenue**: €12,000-15,000
- **Monthly Profit**: €2,000-3,000
- **Team Size**: 3-4 people
- **Cash Flow**: Always positive

### Generated Reports
- `customer_growth.csv` - Customer acquisition and churn tracking
- `financial_performance.csv` - Revenue, costs, and profitability
- `team_operations.csv` - Staffing and utilization metrics
- `loan_impact.csv` - Loan deployment and repayment tracking

## 🎨 Visualization Examples

The system generates professional charts including:
- Revenue streams vs costs over time
- Customer growth and team scaling correlation
- Cumulative profit and cash flow trends
- Marketing spend efficiency analysis

## ⚙️ Customization

### Adjusting Business Model
```python
# config/settings.py
PACKAGES_WITH_WEBSITE = {
    'basic': {'price': 35.99, 'upfront_cost': 250},
    'pro': {'price': 119.99, 'upfront_cost': 500},
    'enterprise': {'price': 259.99, 'upfront_cost': 1000}
}
```

### Loan Scenarios
```python
# config/loan_settings.py
LOAN_SCENARIOS = {
    'conservative': {'amount': 10000, 'interest_rate': 0.036, 'term_months': 36},
    'aggressive': {'amount': 50000, 'interest_rate': 0.055, 'term_months': 60}
}
```

## 🧪 Validation & Testing

The system includes built-in validation checks:
- Founder support limits
- Designer utilization thresholds
- Cash flow reasonableness
- Loan fund accounting accuracy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Roadmap

- [ ] Integration with accounting software APIs
- [ ] Web-based dashboard interface
- [ ] Advanced Monte Carlo simulation
- [ ] Multi-currency support
- [ ] Real-time data integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions or support:
- Create an issue in this repository
- Review the configuration examples in `/config/`
- Check the validation output for calculation errors

## 🏆 Acknowledgments

- Built for realistic business planning and bank presentations
- Designed with conservative growth assumptions
- Validated against real-world SaaS metrics and cost structures