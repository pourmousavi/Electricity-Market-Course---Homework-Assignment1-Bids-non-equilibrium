import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Electricity Market Dashboard", layout="wide")

# Title
st.title("Electricity Market Merit Order Dashboard")
st.markdown("---")

# Initialize session state for storing data
if 'generator_data' not in st.session_state:
    st.session_state.generator_data = []
if 'consumer_data' not in st.session_state:
    st.session_state.consumer_data = []

# Initialize session state for all possible bids
def initialize_session_state():
    """Initialize session state variables for all bids"""
    for i in range(20):  # Max number of participants is 20
        # Generator bids
        if f"gen_{i+1}_price1" not in st.session_state:
            st.session_state[f"gen_{i+1}_price1"] = 20.0 + i*10
            st.session_state[f"gen_{i+1}_qty1"] = 50.0
            st.session_state[f"gen_{i+1}_price2"] = 30.0 + i*10
            st.session_state[f"gen_{i+1}_qty2"] = 75.0
            st.session_state[f"gen_{i+1}_price3"] = 40.0 + i*10
            st.session_state[f"gen_{i+1}_qty3"] = 100.0
        
        # Consumer bids
        if f"con_{i+1}_price1" not in st.session_state:
            st.session_state[f"con_{i+1}_price1"] = 80.0 - i*10
            st.session_state[f"con_{i+1}_qty1"] = 50.0
            st.session_state[f"con_{i+1}_price2"] = 60.0 - i*10
            st.session_state[f"con_{i+1}_qty2"] = 75.0
            st.session_state[f"con_{i+1}_price3"] = 40.0 - i*10
            st.session_state[f"con_{i+1}_qty3"] = 100.0

# Call the initialization function
initialize_session_state()

def update_gen_price(gen_id, bid_num):
    """Update generator price in session state"""
    input_key = f"gen_{gen_id}_price{bid_num}_input"
    state_key = f"gen_{gen_id}_price{bid_num}"
    if input_key in st.session_state:
        st.session_state[state_key] = st.session_state[input_key]

def update_gen_qty(gen_id, bid_num):
    """Update generator quantity in session state"""
    input_key = f"gen_{gen_id}_qty{bid_num}_input"
    state_key = f"gen_{gen_id}_qty{bid_num}"
    if input_key in st.session_state:
        st.session_state[state_key] = st.session_state[input_key]

def update_con_price(con_id, bid_num):
    """Update consumer price in session state"""
    input_key = f"con_{con_id}_price{bid_num}_input"
    state_key = f"con_{con_id}_price{bid_num}"
    if input_key in st.session_state:
        st.session_state[state_key] = st.session_state[input_key]

def update_con_qty(con_id, bid_num):
    """Update consumer quantity in session state"""
    input_key = f"con_{con_id}_qty{bid_num}_input"
    state_key = f"con_{con_id}_qty{bid_num}"
    if input_key in st.session_state:
        st.session_state[state_key] = st.session_state[input_key]

# Move participant number inputs to sidebar
with st.sidebar:
    st.header("Market Participants")
    num_generators = st.number_input("Number of Generators", min_value=1, max_value=20, value=3)
    num_consumers = st.number_input("Number of Consumers", min_value=1, max_value=20, value=3)

# Create tabs for bid inputs in main panel
st.header("Market Participant Bids")
gen_tab, con_tab = st.tabs(["Generator Bids", "Consumer Bids"])

# Generator Bids Tab
with gen_tab:
    generator_data = []
    
    # Create columns for dropdown and bid inputs
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_gen = st.selectbox(
            "Select Generator",
            options=range(1, num_generators + 1),
            format_func=lambda x: f"Generator {x}"
        )
    
    with col2:
        # Create three columns for the bids
        bid1_col, bid2_col, bid3_col = st.columns(3)
        
        with bid1_col:
            st.write("First Bid")
            price1 = st.number_input(
                "Price ($/MWh)",
                key=f"gen_{selected_gen}_price1_input",
                min_value=0.0,
                value=st.session_state[f"gen_{selected_gen}_price1"],
                help="Minimum price to generate power",
                on_change=update_gen_price,
                args=(selected_gen, 1)
            )
            quantity1 = st.number_input(
                "Quantity (MW)",
                key=f"gen_{selected_gen}_qty1_input",
                min_value=0.0,
                value=st.session_state[f"gen_{selected_gen}_qty1"],
                help="Maximum power that can be generated at this price",
                on_change=update_gen_qty,
                args=(selected_gen, 1)
            )
        
        with bid2_col:
            st.write("Second Bid")
            price2 = st.number_input(
                "Price ($/MWh)",
                key=f"gen_{selected_gen}_price2_input",
                min_value=0.0,
                value=st.session_state[f"gen_{selected_gen}_price2"],
                on_change=update_gen_price,
                args=(selected_gen, 2)
            )
            quantity2 = st.number_input(
                "Quantity (MW)",
                key=f"gen_{selected_gen}_qty2_input",
                min_value=0.0,
                value=st.session_state[f"gen_{selected_gen}_qty2"],
                on_change=update_gen_qty,
                args=(selected_gen, 2)
            )
        
        with bid3_col:
            st.write("Third Bid")
            price3 = st.number_input(
                "Price ($/MWh)",
                key=f"gen_{selected_gen}_price3_input",
                min_value=0.0,
                value=st.session_state[f"gen_{selected_gen}_price3"],
                on_change=update_gen_price,
                args=(selected_gen, 3)
            )
            quantity3 = st.number_input(
                "Quantity (MW)",
                key=f"gen_{selected_gen}_qty3_input",
                min_value=0.0,
                value=st.session_state[f"gen_{selected_gen}_qty3"],
                on_change=update_gen_qty,
                args=(selected_gen, 3)
            )
    
    # Initialize or update generator data
    for i in range(num_generators):
        generator_data.append({
            'id': i+1,
            'price1': st.session_state[f"gen_{i+1}_price1"],
            'quantity1': st.session_state[f"gen_{i+1}_qty1"],
            'price2': st.session_state[f"gen_{i+1}_price2"],
            'quantity2': st.session_state[f"gen_{i+1}_qty2"],
            'price3': st.session_state[f"gen_{i+1}_price3"],
            'quantity3': st.session_state[f"gen_{i+1}_qty3"]
        })

# Consumer Bids Tab
with con_tab:
    consumer_data = []
    
    # Create columns for dropdown and bid inputs
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_con = st.selectbox(
            "Select Consumer",
            options=range(1, num_consumers + 1),
            format_func=lambda x: f"Consumer {x}"
        )
    
    with col2:
        # Create three columns for the bids
        bid1_col, bid2_col, bid3_col = st.columns(3)
        
        with bid1_col:
            st.write("First Bid")
            price1 = st.number_input(
                "Price ($/MWh)",
                key=f"con_{selected_con}_price1_input",
                min_value=0.0,
                value=st.session_state[f"con_{selected_con}_price1"],
                help="Maximum price willing to pay",
                on_change=update_con_price,
                args=(selected_con, 1)
            )
            quantity1 = st.number_input(
                "Quantity (MW)",
                key=f"con_{selected_con}_qty1_input",
                min_value=0.0,
                value=st.session_state[f"con_{selected_con}_qty1"],
                help="Power needed at this price",
                on_change=update_con_qty,
                args=(selected_con, 1)
            )
        
        with bid2_col:
            st.write("Second Bid")
            price2 = st.number_input(
                "Price ($/MWh)",
                key=f"con_{selected_con}_price2_input",
                min_value=0.0,
                value=st.session_state[f"con_{selected_con}_price2"],
                on_change=update_con_price,
                args=(selected_con, 2)
            )
            quantity2 = st.number_input(
                "Quantity (MW)",
                key=f"con_{selected_con}_qty2_input",
                min_value=0.0,
                value=st.session_state[f"con_{selected_con}_qty2"],
                on_change=update_con_qty,
                args=(selected_con, 2)
            )
            
        with bid3_col:
            st.write("Third Bid")
            price3 = st.number_input(
                "Price ($/MWh)",
                key=f"con_{selected_con}_price3_input",
                min_value=0.0,
                value=st.session_state[f"con_{selected_con}_price3"],
                on_change=update_con_price,
                args=(selected_con, 3)
            )
            quantity3 = st.number_input(
                "Quantity (MW)",
                key=f"con_{selected_con}_qty3_input",
                min_value=0.0,
                value=st.session_state[f"con_{selected_con}_qty3"],
                on_change=update_con_qty,
                args=(selected_con, 3)
            )
    
    # Initialize or update consumer data
    for i in range(num_consumers):
        consumer_data.append({
            'id': i+1,
            'price1': st.session_state[f"con_{i+1}_price1"],
            'quantity1': st.session_state[f"con_{i+1}_qty1"],
            'price2': st.session_state[f"con_{i+1}_price2"],
            'quantity2': st.session_state[f"con_{i+1}_qty2"],
            'price3': st.session_state[f"con_{i+1}_price3"],
            'quantity3': st.session_state[f"con_{i+1}_qty3"]
        })

def create_supply_curve(generator_data):
    """Create supply curve data from generator bids"""
    supply_points = []
    
    for gen in generator_data:
        # Each generator has three price-quantity pairs
        supply_points.append({
            'generator': gen['id'],
            'price': gen['price1'],
            'quantity': gen['quantity1'],
            'cumulative_quantity': 0  # Will be calculated later
        })
        supply_points.append({
            'generator': gen['id'],
            'price': gen['price2'],
            'quantity': gen['quantity2'],
            'cumulative_quantity': 0  # Will be calculated later
        })
        supply_points.append({
            'generator': gen['id'],
            'price': gen['price3'],
            'quantity': gen['quantity3'],
            'cumulative_quantity': 0  # Will be calculated later
        })
    
    # Sort by price (merit order)
    supply_points.sort(key=lambda x: x['price'])
    
    # Calculate cumulative quantities
    cumulative = 0
    for point in supply_points:
        point['cumulative_quantity'] = cumulative + point['quantity']
        cumulative = point['cumulative_quantity']
    
    return supply_points

def create_demand_curve(consumer_data):
    """Create demand curve data from consumer bids"""
    demand_points = []
    
    for con in consumer_data:
        # Each consumer has three price-quantity pairs
        demand_points.append({
            'consumer': con['id'],
            'price': con['price1'],
            'quantity': con['quantity1'],
            'cumulative_quantity': 0  # Will be calculated later
        })
        demand_points.append({
            'consumer': con['id'],
            'price': con['price2'],
            'quantity': con['quantity2'],
            'cumulative_quantity': 0  # Will be calculated later
        })
        demand_points.append({
            'consumer': con['id'],
            'price': con['price3'],
            'quantity': con['quantity3'],
            'cumulative_quantity': 0  # Will be calculated later
        })
    
    # Sort by price (highest to lowest for demand)
    demand_points.sort(key=lambda x: x['price'], reverse=True)
    
    # Calculate cumulative quantities
    cumulative = 0
    for point in demand_points:
        point['cumulative_quantity'] = cumulative + point['quantity']
        cumulative = point['cumulative_quantity']
    
    return demand_points

def find_equilibrium(supply_points, demand_points):
    """Find market equilibrium point where supply and demand curves intersect"""
    # Create arrays of all price points (including vertical segments)
    all_prices = sorted(list(set(
        [p['price'] for p in supply_points] + 
        [p['price'] for p in demand_points]
    )))
    
    # For each price, calculate supply and demand quantities
    supply_curve = []
    demand_curve = []
    
    for price in all_prices:
        # Calculate supply at this price
        supply_qty = 0
        for point in supply_points:
            if point['price'] <= price:
                supply_qty += point['quantity']
        supply_curve.append({'price': price, 'quantity': supply_qty})
        
        # Calculate demand at this price
        demand_qty = 0
        for point in demand_points:
            if point['price'] >= price:
                demand_qty += point['quantity']
        demand_curve.append({'price': price, 'quantity': demand_qty})
    
    # Find intersection
    for i in range(len(all_prices)):
        supply = supply_curve[i]['quantity']
        demand = demand_curve[i]['quantity']
        price = all_prices[i]
        
        # Check if we've found the intersection
        if supply >= demand:
            # If this is the first point where supply >= demand
            if i == 0 or supply_curve[i-1]['quantity'] < demand_curve[i-1]['quantity']:
                return price, min(supply, demand)
            
            # If the previous point also had supply >= demand, 
            # then intersection happened at a vertical segment
            prev_price = all_prices[i-1]
            # Return the price halfway between the two points
            return (price + prev_price) / 2, min(supply, demand)
    
    # If no intersection found, return None or raise exception
    return None, None

def calculate_welfare(generator_data, consumer_data, market_price, equilibrium_quantity):
    """Calculate welfare for generators and consumers"""
    supply_points = create_supply_curve(generator_data)
    demand_points = create_demand_curve(consumer_data)
    
    results = {'generators': [], 'consumers': []}
    
    # Generator welfare
    remaining_quantity = equilibrium_quantity  # Track remaining quantity to be allocated
    
    # Sort supply points by price (merit order)
    supply_points_sorted = sorted(supply_points, key=lambda x: (x['price'], x['generator']))
    
    # Track allocated quantity per generator
    gen_quantities = {gen['id']: 0 for gen in generator_data}
    gen_costs = {gen['id']: 0 for gen in generator_data}
    
    # Allocate quantity to generators based on merit order
    for point in supply_points_sorted:
        if remaining_quantity > 0:
            gen_id = point['generator']
            qty_from_segment = min(point['quantity'], remaining_quantity)
            gen_quantities[gen_id] += qty_from_segment
            gen_costs[gen_id] += qty_from_segment * point['price']
            remaining_quantity -= qty_from_segment
    
    # Calculate welfare for each generator
    for gen in generator_data:
        gen_quantity_sold = gen_quantities[gen['id']]
        gen_cost = gen_costs[gen['id']]
        gen_revenue = market_price * gen_quantity_sold
        producer_surplus = gen_revenue - gen_cost
        
        results['generators'].append({
            'Generator': f'Gen {gen["id"]}',
            'Quantity (MW)': gen_quantity_sold,
            'Revenue ($K)': gen_revenue / 1000,
            'Cost ($K)': gen_cost / 1000,
            'Producer Surplus ($K)': producer_surplus / 1000
        })
    
    # Consumer welfare
    remaining_quantity = equilibrium_quantity  # Reset remaining quantity for consumers
    
    # Sort demand points by price (highest to lowest)
    demand_points_sorted = sorted(demand_points, key=lambda x: (-x['price'], x['consumer']))
    
    # Track allocated quantity per consumer
    con_quantities = {con['id']: 0 for con in consumer_data}
    con_utilities = {con['id']: 0 for con in consumer_data}
    
    # Allocate quantity to consumers based on willingness to pay
    for point in demand_points_sorted:
        if remaining_quantity > 0:
            con_id = point['consumer']
            qty_from_segment = min(point['quantity'], remaining_quantity)
            con_quantities[con_id] += qty_from_segment
            con_utilities[con_id] += qty_from_segment * point['price']
            remaining_quantity -= qty_from_segment
    
    # Calculate welfare for each consumer
    for con in consumer_data:
        con_quantity_bought = con_quantities[con['id']]
        con_utility = con_utilities[con['id']]
        con_cost = market_price * con_quantity_bought
        consumer_surplus = con_utility - con_cost
        
        results['consumers'].append({
            'Consumer': f'Con {con["id"]}',
            'Quantity (MW)': con_quantity_bought,
            'Utility ($K)': con_utility / 1000,
            'Cost ($K)': con_cost / 1000,
            'Consumer Surplus ($K)': consumer_surplus / 1000
        })
    
    return results

def calculate_supply_at_price(supply_points, price):
    """Calculate total quantity supplied at a given price"""
    total_quantity = 0
    for point in supply_points:
        if point['price'] <= price:
            total_quantity += point['quantity']
    return total_quantity

def calculate_demand_at_price(demand_points, price):
    """Calculate total quantity demanded at a given price"""
    total_quantity = 0
    for point in sorted(demand_points, key=lambda x: x['price'], reverse=True):
        if point['price'] >= price:
            total_quantity += point['quantity']
    return total_quantity

def distribute_quantity_equally(points, available_quantity):
    """Distribute available quantity equally among points with equal prices"""
    # Group points by price
    price_groups = {}
    for point in points:
        price = point['price']
        if price not in price_groups:
            price_groups[price] = []
        price_groups[price].append(point)
    
    # Distribute quantity within each price group
    allocated_quantities = {(p['generator'] if 'generator' in p else p['consumer']): 0 for p in points}
    remaining_quantity = available_quantity
    
    for price in sorted(price_groups.keys()):
        group = price_groups[price]
        total_requested = sum(p['quantity'] for p in group)
        
        if total_requested <= remaining_quantity:
            # Can fulfill all requests at this price
            for point in group:
                participant_id = point['generator'] if 'generator' in point else point['consumer']
                allocated_quantities[participant_id] += point['quantity']
            remaining_quantity -= total_requested
        else:
            # Must distribute remaining quantity equally
            equal_share = remaining_quantity / len(group)
            for point in group:
                participant_id = point['generator'] if 'generator' in point else point['consumer']
                allocated_quantity = min(point['quantity'], equal_share)
                allocated_quantities[participant_id] += allocated_quantity
            remaining_quantity = 0
        
        if remaining_quantity <= 0:
            break
    
    return allocated_quantities

def calculate_welfare_at_alternative_price(generator_data, consumer_data, market_price, eq_price):
    """Calculate welfare for generators and consumers at non-equilibrium price"""
    supply_points = create_supply_curve(generator_data)
    demand_points = create_demand_curve(consumer_data)
    
    # Calculate quantity based on price comparison with equilibrium
    if market_price > eq_price:
        available_quantity = calculate_demand_at_price(demand_points, market_price)
    else:
        available_quantity = calculate_supply_at_price(supply_points, market_price)
    
    results = {'generators': [], 'consumers': [], 'total_quantity': available_quantity}
    
    # Generator welfare
    if market_price > eq_price:
        # Get all generators willing to supply at this price
        eligible_points = [p for p in supply_points if p['price'] <= market_price]
        allocated_quantities = distribute_quantity_equally(eligible_points, available_quantity)
        
        for gen in generator_data:
            gen_points = sorted([p for p in supply_points if p['generator'] == gen['id']], 
                              key=lambda x: x['price'])
            
            gen_quantity_sold = allocated_quantities.get(gen['id'], 0)
            gen_cost = 0
            remaining_qty = gen_quantity_sold
            
            # Calculate cost using merit order
            for point in gen_points:
                if remaining_qty > 0:
                    qty_from_segment = min(point['quantity'], remaining_qty)
                    gen_cost += point['price'] * qty_from_segment
                    remaining_qty -= qty_from_segment
            
            gen_revenue = market_price * gen_quantity_sold
            producer_surplus = gen_revenue - gen_cost
            
            results['generators'].append({
                'Generator': f'Gen {gen["id"]}',
                'Quantity (MW)': gen_quantity_sold,
                'Revenue ($K)': gen_revenue / 1000,
                'Cost ($K)': gen_cost / 1000,
                'Producer Surplus ($K)': producer_surplus / 1000
            })
    else:
        # For prices below equilibrium
        eligible_points = [p for p in supply_points if p['price'] <= market_price]
        allocated_quantities = distribute_quantity_equally(eligible_points, available_quantity)
        
        for gen in generator_data:
            gen_points = sorted([p for p in supply_points if p['generator'] == gen['id']], 
                              key=lambda x: x['price'])
            
            gen_quantity_sold = allocated_quantities.get(gen['id'], 0)
            gen_cost = 0
            remaining_qty = gen_quantity_sold
            
            # Calculate cost using merit order
            for point in gen_points:
                if remaining_qty > 0 and point['price'] <= market_price:
                    qty_from_segment = min(point['quantity'], remaining_qty)
                    gen_cost += point['price'] * qty_from_segment
                    remaining_qty -= qty_from_segment
            
            gen_revenue = market_price * gen_quantity_sold
            producer_surplus = gen_revenue - gen_cost
            
            results['generators'].append({
                'Generator': f'Gen {gen["id"]}',
                'Quantity (MW)': gen_quantity_sold,
                'Revenue ($K)': gen_revenue / 1000,
                'Cost ($K)': gen_cost / 1000,
                'Producer Surplus ($K)': producer_surplus / 1000
            })

    # Consumer welfare
    eligible_points = [p for p in demand_points if p['price'] >= market_price]
    allocated_quantities = distribute_quantity_equally(eligible_points, available_quantity)
    
    for con in consumer_data:
        con_points = sorted([p for p in demand_points if p['consumer'] == con['id']], 
                          key=lambda x: x['price'], reverse=True)
        
        con_quantity_bought = allocated_quantities.get(con['id'], 0)
        con_utility = 0
        remaining_qty = con_quantity_bought
        
        # Calculate utility using merit order
        for point in con_points:
            if remaining_qty > 0:
                qty_from_segment = min(point['quantity'], remaining_qty)
                con_utility += point['price'] * qty_from_segment
                remaining_qty -= qty_from_segment
        
        con_cost = market_price * con_quantity_bought
        consumer_surplus = con_utility - con_cost
        
        results['consumers'].append({
            'Consumer': f'Con {con["id"]}',
            'Quantity (MW)': con_quantity_bought,
            'Utility ($K)': con_utility / 1000,
            'Cost ($K)': con_cost / 1000,
            'Consumer Surplus ($K)': consumer_surplus / 1000
        })
    
    return results

# Main dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Merit Order Curve")
    
    # Create supply and demand curves
    supply_points = create_supply_curve(generator_data)
    demand_points = create_demand_curve(consumer_data)
    
    # Find equilibrium
    eq_price, eq_quantity = find_equilibrium(supply_points, demand_points)
    
    # Create the plot
    fig = go.Figure()
    
    # Colors for different participants
    gen_colors = px.colors.qualitative.Set1[:len(generator_data)]
    con_colors = px.colors.qualitative.Set2[:len(consumer_data)]

    # Plot supply curve segments with connecting vertical lines
    # First, create a list of all generator points and sort by price
    all_generator_points = []
    for i, gen in enumerate(generator_data):
        points = [p for p in supply_points if p['generator'] == gen['id']]
        for point in points:
            point['color'] = gen_colors[i]  # Assign color based on generator
        all_generator_points.extend(points)
    
    # Sort all generator points by price in ascending order (merit order)
    all_generator_points = sorted(all_generator_points, key=lambda x: x['price'])
    
    # Plot generator points
    cumulative = 0
    shown_generators = set()  # Track which generators have been shown in legend
    for i, point in enumerate(all_generator_points):
        # Find generator index for color
        gen_id = point['generator']
        color = gen_colors[gen_id - 1]
        
        # Horizontal line
        fig.add_trace(go.Scatter(
            x=[cumulative, cumulative + point['quantity']],
            y=[point['price'], point['price']],
            mode='lines',
            name=f'Gen {gen_id}',
            line=dict(color=color, width=2),
            showlegend=(gen_id not in shown_generators)  # Show in legend if not shown yet
        ))
        shown_generators.add(gen_id)  # Mark this generator as shown
        
        # Vertical connecting line if not the last point
        if i < len(all_generator_points) - 1:
            next_point = all_generator_points[i + 1]
            fig.add_trace(go.Scatter(
                x=[cumulative + point['quantity'], cumulative + point['quantity']],
                y=[point['price'], next_point['price']],
                mode='lines',
                name=f'Gen {gen_id}',  # Add name for tooltip
                line=dict(color=color, width=2),
                showlegend=False
            ))
        
        cumulative += point['quantity']

    # Plot demand curve segments with connecting vertical lines
    # First, create a list of all consumer points and sort by price
    all_consumer_points = []
    for i, con in enumerate(consumer_data):
        points = [p for p in demand_points if p['consumer'] == con['id']]
        for point in points:
            point['color'] = con_colors[i]  # Assign color based on consumer
        all_consumer_points.extend(points)
    
    # Sort all consumer points by price in descending order
    all_consumer_points = sorted(all_consumer_points, key=lambda x: x['price'], reverse=True)
    
    # Plot consumer points
    cumulative = 0
    shown_consumers = set()  # Track which consumers have been shown in legend
    for i, point in enumerate(all_consumer_points):
        # Find consumer index for color
        con_id = point['consumer']
        color = con_colors[con_id - 1]
        
        # Horizontal line
        fig.add_trace(go.Scatter(
            x=[cumulative, cumulative + point['quantity']],
            y=[point['price'], point['price']],
            mode='lines',
            name=f'Con {con_id}',
            line=dict(color=color, width=2),
            showlegend=(con_id not in shown_consumers)  # Show in legend if not shown yet
        ))
        shown_consumers.add(con_id)  # Mark this consumer as shown
        
        # Vertical connecting line if not the last point
        if i < len(all_consumer_points) - 1:
            next_point = all_consumer_points[i + 1]
            fig.add_trace(go.Scatter(
                x=[cumulative + point['quantity'], cumulative + point['quantity']],
                y=[point['price'], next_point['price']],
                mode='lines',
                name=f'Con {con_id}',  # Add name for tooltip
                line=dict(color=color, width=2),
                showlegend=False
            ))
        
        cumulative += point['quantity']

    # Plot equilibrium point
    fig.add_trace(go.Scatter(
        x=[eq_quantity],
        y=[eq_price],
        mode='markers',
        name='Equilibrium',
        marker=dict(color='black', size=10, symbol='star')
    ))
    
    # Add equilibrium lines
    fig.add_hline(y=eq_price, line_dash="dot", line_color="gray", 
                  annotation_text=f"Equilibrium Price: ${eq_price:.2f}/MWh")
    fig.add_vline(x=eq_quantity, line_dash="dot", line_color="gray",
                  annotation_text=f"Equilibrium Quantity: {eq_quantity:.1f} MW")
    
    fig.update_layout(
        title="Electricity Market Merit Order",
        xaxis_title="Quantity (MW)",
        yaxis_title="Price ($/MWh)",
        height=600,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Market Summary")
    st.metric("Equilibrium Price", f"${eq_price:.2f}/MWh")
    st.metric("Equilibrium Quantity", f"{eq_quantity:.1f} MW")

# Welfare Analysis
st.header("Welfare Analysis")

# Calculate welfare at equilibrium
welfare_eq = calculate_welfare(generator_data, consumer_data, eq_price, eq_quantity)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Generator Welfare (Equilibrium)")
    df_gen_eq = pd.DataFrame(welfare_eq['generators'])
    st.dataframe(df_gen_eq, use_container_width=True)
    
    total_producer_surplus = df_gen_eq['Producer Surplus ($K)'].sum()
    st.metric("Total Producer Surplus", f"${total_producer_surplus:.1f}K")

with col2:
    st.subheader("Consumer Welfare (Equilibrium)")
    df_con_eq = pd.DataFrame(welfare_eq['consumers'])
    st.dataframe(df_con_eq, use_container_width=True)
    
    total_consumer_surplus = df_con_eq['Consumer Surplus ($K)'].sum()
    st.metric("Total Consumer Surplus", f"${total_consumer_surplus:.1f}K")

# Total welfare
total_welfare = total_producer_surplus + total_consumer_surplus
st.metric("Total Market Welfare", f"${total_welfare:.1f}K")

# Alternative Price Analysis
st.header("Alternative Price Scenario")

alternative_price = st.number_input(
    "Enter Alternative Market Price ($/MWh)", 
    value=eq_price, 
    min_value=0.0,
    help="Enter a price different from equilibrium to see welfare changes"
)

if alternative_price != eq_price:
    # Calculate welfare at alternative price
    welfare_alt = calculate_welfare_at_alternative_price(
        generator_data, 
        consumer_data, 
        alternative_price,
        eq_price  # Add the missing equilibrium price parameter
    )
    
    st.subheader(f"Welfare Comparison: Alternative Price ${alternative_price:.2f}/MWh")
    
    # Generator comparison
    df_gen_alt = pd.DataFrame(welfare_alt['generators'])
    df_gen_alt['Surplus Change ($K)'] = df_gen_alt['Producer Surplus ($K)'] - df_gen_eq['Producer Surplus ($K)']
    df_gen_alt['% Change'] = (df_gen_alt['Surplus Change ($K)'] / df_gen_eq['Producer Surplus ($K)'] * 100).round(1)
    
    # Select and reorder columns for generator display
    df_gen_display = df_gen_alt[['Generator', 'Quantity (MW)', 
                                'Revenue ($K)', 'Cost ($K)', 
                                'Producer Surplus ($K)', 
                                'Surplus Change ($K)', '% Change']]
    
    st.subheader("Generator Welfare at Alternative Price")
    st.dataframe(df_gen_display, use_container_width=True)
    
    # Consumer comparison
    df_con_alt = pd.DataFrame(welfare_alt['consumers'])
    df_con_alt['Surplus Change ($K)'] = df_con_alt['Consumer Surplus ($K)'] - df_con_eq['Consumer Surplus ($K)']
    df_con_alt['% Change'] = (df_con_alt['Surplus Change ($K)'] / df_con_eq['Consumer Surplus ($K)'] * 100).round(1)
    
    # Select and reorder columns for consumer display
    df_con_display = df_con_alt[['Consumer', 'Quantity (MW)', 
                                'Utility ($K)', 'Cost ($K)', 
                                'Consumer Surplus ($K)', 
                                'Surplus Change ($K)', '% Change']]
    
    st.subheader("Consumer Welfare at Alternative Price")
    st.dataframe(df_con_display, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    total_producer_surplus_alt = df_gen_alt['Producer Surplus ($K)'].sum()
    total_consumer_surplus_alt = df_con_alt['Consumer Surplus ($K)'].sum()
    total_welfare_alt = total_producer_surplus_alt + total_consumer_surplus_alt
    
    producer_surplus_change = total_producer_surplus_alt - total_producer_surplus
    consumer_surplus_change = total_consumer_surplus_alt - total_consumer_surplus
    total_welfare_change = total_welfare_alt - total_welfare
    
    producer_pct_change = (producer_surplus_change / total_producer_surplus * 100).round(1)
    consumer_pct_change = (consumer_surplus_change / total_consumer_surplus * 100).round(1)
    welfare_pct_change = (total_welfare_change / total_welfare * 100).round(1)
    
    with col1:
        st.metric(
            "Producer Surplus Change", 
            f"${producer_surplus_change:.1f}K",
            f"{producer_pct_change}%"
        )
    
    with col2:
        st.metric(
            "Consumer Surplus Change", 
            f"${consumer_surplus_change:.1f}K",
            f"{consumer_pct_change}%"
        )
    
    with col3:
        st.metric(
            "Total Welfare Change", 
            f"${total_welfare_change:.1f}K",
            f"{welfare_pct_change}%"
        )

# Instructions
with st.expander("How to Use This Dashboard"):
    st.markdown("""
    ### Instructions:
    1. **Set Market Participants**: Use the sidebar to set the number of generators and consumers
    2. **Enter Bids**: For each generator and consumer, enter three price-quantity pairs
    3. **View Merit Order**: The main chart shows the supply and demand curves with equilibrium
    4. **Analyze Welfare**: Review the welfare calculations for each participant
    5. **Test Alternative Prices**: Enter a different market price to see how welfare changes
    
    ### Key Concepts:
    - **Supply Curve**: Generators ordered from cheapest to most expensive
    - **Demand Curve**: Consumers ordered from highest to lowest willingness to pay
    - **Equilibrium**: Where supply meets demand
    - **Producer Surplus**: Revenue minus cost for generators
    - **Consumer Surplus**: Utility minus cost for consumers
    - **Market Welfare**: Total of producer and consumer surplus
    """)