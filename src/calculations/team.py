from config.settings import WEB_DESIGNER_CONFIG, VISHAL_CONFIG, EMPLOYEE_COSTS, ROLLING_AVERAGE_MONTHS

def calculate_required_designers(monthly_website_demand):
    """
    FIXED: Calculate how many designers are needed based on monthly website demand with safety buffer
    """
    total_workload = 0
    
    # Calculate total monthly workload as a fraction of designer capacity
    for package in ['basic', 'pro', 'enterprise']:
        websites_needed = monthly_website_demand.get(package, 0)
        max_capacity_per_designer = WEB_DESIGNER_CONFIG['capacity_per_month'][package]
        
        # Calculate workload as fraction of one designer's time
        # Example: 5 basic sites / 10 max basic sites = 0.5 (50% of designer's time)
        workload_fraction = websites_needed / max_capacity_per_designer if max_capacity_per_designer > 0 else 0
        total_workload += workload_fraction
    
    # Calculate required designers with buffer to avoid constant over-utilization
    # Add 10% buffer for capacity planning
    buffer = WEB_DESIGNER_CONFIG.get('capacity_buffer', 0.1)  # 10% buffer
    required_designers = max(0, int((total_workload * (1 + buffer)) + 0.99)) if total_workload > 0 else 0
    
    return required_designers, total_workload

def update_designer_count(current_designers, required_designers, current_utilization, months_low_utilization):
    """
    FIXED: Update designer count based on demand and utilization thresholds with emergency hiring
    """
    # Different thresholds for first hire vs subsequent hires
    if current_designers == 0:
        hire_threshold = WEB_DESIGNER_CONFIG['first_hire_threshold']  # 25% for first hire
    else:
        hire_threshold = WEB_DESIGNER_CONFIG['subsequent_hire_threshold']  # 75% for additional hires
    
    fire_threshold = WEB_DESIGNER_CONFIG['fire_threshold']  # 30%
    emergency_threshold = WEB_DESIGNER_CONFIG.get('emergency_hire_threshold', 1.0)  # 100%
    
    # CRITICAL FIX: Handle over-utilization properly
    if current_utilization > emergency_threshold:  # Over 100% utilization
        # Emergency hiring - we're severely understaffed
        needed_designers = max(required_designers, int(current_utilization * current_designers) + 1)
        print(f"⚠️  EMERGENCY HIRING: {current_utilization:.1%} utilization, hiring to {needed_designers} designers")
        return needed_designers, 0  # Reset low utilization counter
    
    # Standard hiring logic: if utilization is above threshold, hire more
    elif current_utilization > hire_threshold and required_designers > current_designers:
        return required_designers, 0  # Reset low utilization counter
    
    # Firing logic: if utilization is below threshold for 2+ months, reduce designers
    elif current_utilization < fire_threshold and current_designers > 0:
        months_low_utilization += 1
        if months_low_utilization >= 2:
            return max(0, current_designers - 1), 0  # Can go down to 0 designers
        else:
            return current_designers, months_low_utilization
    
    else:
        return current_designers, 0  # Reset low utilization counter

def calculate_vishal_compensation_iterative(preliminary_profit_before_vishal, website_revenue, is_fulltime, max_iterations=5):
    """
    FIXED: Calculate Vishal's monthly compensation using iterative approach to handle circular dependency
    Since his compensation depends on profit, but profit calculation includes his compensation
    """
    
    # Start with initial estimate (no Vishal compensation)
    current_profit_estimate = preliminary_profit_before_vishal
    
    for iteration in range(max_iterations):
        # Check if profit exceeds threshold for profit sharing
        profit_share_eligible = current_profit_estimate > VISHAL_CONFIG['profit_share_threshold']
        
        if is_fulltime:
            # Full-time: Fixed salary + 3% profit share (only if profit > threshold) + NO website share
            fixed_salary = EMPLOYEE_COSTS['vishal_fulltime_salary']  # €1,500 - FIXED: Use EMPLOYEE_COSTS
            
            # CORRECTED: Use 3% not 20% for full-time profit share
            profit_share = (current_profit_estimate * VISHAL_CONFIG['fulltime_profit_share']) if profit_share_eligible else 0  # 3%
            website_share = 0  # No website revenue share when full-time
            
        else:
            # Freelance: 20% profit share (only if profit > threshold) + 20% website revenue share (no fixed salary)
            fixed_salary = 0
            profit_share = (current_profit_estimate * VISHAL_CONFIG['freelance_profit_share']) if profit_share_eligible else 0  # 20%
            website_share = website_revenue * VISHAL_CONFIG['website_revenue_share']  # 20%
        
        compensation = fixed_salary + profit_share + website_share
        
        # Calculate new profit estimate after this compensation
        new_profit_estimate = preliminary_profit_before_vishal - compensation
        
        # Check for convergence (difference < €1)
        if abs(new_profit_estimate - current_profit_estimate) < 1.0:
            return compensation, fixed_salary, profit_share, website_share
        
        current_profit_estimate = new_profit_estimate
    
    # If we didn't converge, use the last calculation
    print(f"⚠️  Vishal compensation calculation didn't fully converge after {max_iterations} iterations")
    return compensation, fixed_salary, profit_share, website_share

def calculate_vishal_compensation(monthly_profit, website_revenue, is_fulltime):
    """
    LEGACY: Calculate Vishal's monthly compensation based on the collaboration agreement
    This is the old function kept for compatibility - use calculate_vishal_compensation_iterative instead
    """
    # Check if profit exceeds threshold for profit sharing
    profit_share_eligible = monthly_profit > VISHAL_CONFIG['profit_share_threshold']
    
    if is_fulltime:
        # Full-time: Fixed salary + 3% profit share (only if profit > threshold) + NO website share
        fixed_salary = EMPLOYEE_COSTS['vishal_fulltime_salary']
        profit_share = (monthly_profit * VISHAL_CONFIG['fulltime_profit_share']) if profit_share_eligible else 0
        website_share = 0  # No website revenue share when full-time
        return fixed_salary + profit_share + website_share, fixed_salary, profit_share, website_share
    else:
        # Freelance: 20% profit share (only if profit > threshold) + 20% website revenue share (no fixed salary)
        profit_share = (monthly_profit * VISHAL_CONFIG['freelance_profit_share']) if profit_share_eligible else 0
        website_share = website_revenue * VISHAL_CONFIG['website_revenue_share']
        return profit_share + website_share, 0, profit_share, website_share

def update_vishal_status(is_fulltime, rolling_avg_profit):
    """Update Vishal's employment status based on rolling average profit threshold"""
    fulltime_threshold = VISHAL_CONFIG['fulltime_threshold']
    
    # Switch to full-time when rolling average profit reaches €8k
    if not is_fulltime and rolling_avg_profit >= fulltime_threshold:
        return True
    
    return is_fulltime

def calculate_rolling_average_profit(profit_history):
    """Calculate rolling average profit for the last N months"""
    if len(profit_history) < ROLLING_AVERAGE_MONTHS:
        return sum(profit_history) / len(profit_history) if profit_history else 0
    else:
        return sum(profit_history[-ROLLING_AVERAGE_MONTHS:]) / ROLLING_AVERAGE_MONTHS