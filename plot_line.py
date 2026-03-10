#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import csv
import sys
import numpy as np
import os
from datetime import datetime
import shutil
import math

class LinePlotter:
    def __init__(self):
        # Scale calculation: 32 feet needs to fit in 8.5 inches (with margins)
        # Using 8 inches of usable width (leaving 0.25" margins on each side)
        # Scale: 8 inches / 32 feet = 0.25 inches per foot
        self.scale = 0.25  # 0.25 inches on paper = 1 foot in drawing
        
        # Start 12 feet left of center and 12 feet up from center
        # (4 feet from left edge, 28 feet from bottom)
        # Convert to paper inches: 4 feet * 0.25 = 1 inch from origin
        # With 0.5" margin, this is at 1.5" on paper
        self.current_x = 4.0   # Start at 4 feet from left (real world)
        self.current_y = 28.0  # Start at 28 feet from bottom (real world)
        self.points = [(self.current_x, self.current_y)]
        
        # Track cumulative distances for each direction
        self.cumulative_north = 0.0
        self.cumulative_south = 0.0
        self.cumulative_east = 0.0
        self.cumulative_west = 0.0
        self.step_count = 0
        
    def turn_and_go(self, direction, distance_inches):
        """Move in the specified direction by the given distance in inches."""
        direction = direction.lower()
        
        # Convert inches to feet for internal storage
        distance_feet = distance_inches / 12.0
        
        # Map single-letter abbreviations to full names
        direction_map = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
        if direction in direction_map:
            direction = direction_map[direction]
        
        if direction == 'north':
            self.current_y += distance_feet
        elif direction == 'south':
            self.current_y -= distance_feet
        elif direction == 'east':
            self.current_x += distance_feet
        elif direction == 'west':
            self.current_x -= distance_feet
        else:
            raise ValueError(f"Unknown direction: {direction}")
        
        # Track cumulative distances
        if direction == 'north':
            self.cumulative_north += distance_inches
        elif direction == 'south':
            self.cumulative_south += distance_inches
        elif direction == 'east':
            self.cumulative_east += distance_inches
        elif direction == 'west':
            self.cumulative_west += distance_inches
        
        self.points.append((self.current_x, self.current_y))
        self.step_count += 1
        
        # Calculate net distances
        net_x = (self.cumulative_east - self.cumulative_west) / 12.0
        net_y = (self.cumulative_north - self.cumulative_south) / 12.0
        
        print(f"P{self.step_count-1}→P{self.step_count}: Moved {direction} {distance_inches}\" to ({self.current_x:.1f}', {self.current_y:.1f}')")
        print(f"  Cumulative: N:{self.cumulative_north:.1f}\" S:{self.cumulative_south:.1f}\" E:{self.cumulative_east:.1f}\" W:{self.cumulative_west:.1f}\"")
        print(f"  Net from start: X={net_x:.1f}' Y={net_y:.1f}'")
    
    def parse_instructions(self, instructions):
        """Parse instructions from a list of (direction, distance) tuples."""
        for direction, distance in instructions:
            self.turn_and_go(direction, float(distance))
    
    def parse_csv(self, filename):
        """Parse instructions from a CSV file."""
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            instructions = []
            for row in reader:
                if len(row) >= 2:
                    direction = row[0].strip()
                    distance = row[1].strip()
                    instructions.append((direction, distance))
        return instructions
    
    def plot_to_pdf(self, filename='plot.pdf'):
        """Create the plot and save as PDF."""
        # Archive existing file if it exists
        if os.path.exists(filename):
            # Create timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Get file name and extension
            base_name = os.path.splitext(filename)[0]
            extension = os.path.splitext(filename)[1]
            # Create archive filename
            archive_name = f"{base_name}_archive_{timestamp}{extension}"
            # Move the existing file to archive
            shutil.move(filename, archive_name)
            print(f"Archived existing file to: {archive_name}")
        
        # Create figure with 8.5x11 inch size
        fig, ax = plt.subplots(figsize=(8.5, 11))
        
        # Extract x and y coordinates (in feet) and convert to inches on paper
        x_coords_feet = [p[0] for p in self.points]
        y_coords_feet = [p[1] for p in self.points]
        
        # Convert feet to inches on paper using scale
        x_coords = [x * self.scale for x in x_coords_feet]
        y_coords = [y * self.scale for y in y_coords_feet]
        
        # Plot the line
        ax.plot(x_coords, y_coords, 'b-', linewidth=2, marker='o', markersize=4)
        
        # Mark start and end points
        ax.plot(x_coords[0], y_coords[0], 'go', markersize=8, label='Start')
        ax.plot(x_coords[-1], y_coords[-1], 'ro', markersize=8, label='End')
        
        # Add point labels
        for i, (x_ft, y_ft) in enumerate(self.points):
            x = x_ft * self.scale
            y = y_ft * self.scale
            ax.annotate(f'P{i}', (x, y), xytext=(2, 2), textcoords='offset points', fontsize=8)
        
        # Add segment length annotations
        for i in range(len(self.points) - 1):
            # Get start and end points of segment
            x1_ft, y1_ft = self.points[i]
            x2_ft, y2_ft = self.points[i + 1]
            
            # Calculate segment length
            dx_ft = x2_ft - x1_ft
            dy_ft = y2_ft - y1_ft
            segment_length_ft = math.sqrt(dx_ft**2 + dy_ft**2)
            segment_length_inches = segment_length_ft * 12
            
            # Format as feet and decimal inches (e.g., "6' 3.2"")
            feet_whole = int(segment_length_inches // 12)
            inches_decimal = segment_length_inches % 12
            if feet_whole > 0:
                length_text = f"{feet_whole}' {inches_decimal:.1f}\""
            else:
                length_text = f"{inches_decimal:.1f}\""
            
            # Calculate midpoint for annotation placement
            mid_x = (x1_ft + x2_ft) / 2 * self.scale
            mid_y = (y1_ft + y2_ft) / 2 * self.scale
            
            # Calculate offset perpendicular to segment for better readability
            if dx_ft != 0 or dy_ft != 0:
                # Normalize the perpendicular vector
                length = math.sqrt(dx_ft**2 + dy_ft**2)
                perp_x = -dy_ft / length * 0.15  # Scale down for paper inches
                perp_y = dx_ft / length * 0.15
            else:
                perp_x, perp_y = 0.1, 0.1
            
            # Add the annotation
            ax.annotate(length_text, (mid_x, mid_y), 
                       xytext=(mid_x + perp_x, mid_y + perp_y),
                       fontsize=7, color='red', ha='center',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        # Set axis properties
        # 32 feet * 0.25 = 8 inches, leave 0.25" margins on each side
        ax.set_xlim(0, 8.5)  # Full page width in inches
        ax.set_ylim(0, 11)   # Full page height in inches
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Add grid lines every 4 feet (1 inch on paper)
        ax.set_xticks(np.arange(0, 8.5, 1.0))
        ax.set_yticks(np.arange(0, 11, 1.0))
        
        # Set tick labels to show feet values
        ax.set_xticklabels([f"{i*4}'" for i in range(9)])
        ax.set_yticklabels([f"{i*4}'" for i in range(11)])
        
        # Labels and title
        ax.set_xlabel('X (East →) - feet')
        ax.set_ylabel('Y (North ↑) - feet')
        ax.set_title('Line Plot (32\'×32\' drawing area)')
        ax.legend()
        
        # Add scale note
        ax.text(0.02, 0.98, 'Scale: 1" on paper = 4\' in drawing\nDrawing area: 32\'×32\'', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Save to PDF
        with PdfPages(filename) as pdf:
            pdf.savefig(fig, bbox_inches='tight')
        
        plt.close()
        print(f"Plot saved to {filename}")
        
        # Return bounds for logging (in feet)
        start_point = self.points[0]
        end_point = self.points[-1]
        return {
            'min_x': min(x_coords_feet),
            'max_x': max(x_coords_feet),
            'min_y': min(y_coords_feet),
            'max_y': max(y_coords_feet),
            'points': len(self.points),
            'start': start_point,
            'end': end_point,
            'delta_x': end_point[0] - start_point[0],
            'delta_y': end_point[1] - start_point[1]
        }

def main():
    plotter = LinePlotter()
    
    if len(sys.argv) > 1:
        # Read from CSV file
        csv_file = sys.argv[1]
        print(f"Reading instructions from {csv_file}")
        instructions = plotter.parse_csv(csv_file)
        plotter.parse_instructions(instructions)
    else:
        # Use test instructions (in inches)
        print("Using test instructions:")
        test_instructions = [
            ('north', 48),  # 4 feet = 48 inches
            ('east', 96),   # 8 feet = 96 inches
            ('north', 72)   # 6 feet = 72 inches
        ]
        plotter.parse_instructions(test_instructions)
    
    # Generate PDF
    bounds = plotter.plot_to_pdf('line_plot.pdf')
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    print(f"  Total points: {bounds['points']}")
    print(f"  X range: {bounds['min_x']:.1f}' to {bounds['max_x']:.1f}'")
    print(f"  Y range: {bounds['min_y']:.1f}' to {bounds['max_y']:.1f}'")
    print(f"  Start point: ({bounds['start'][0]:.1f}', {bounds['start'][1]:.1f}')")
    print(f"  End point: ({bounds['end'][0]:.1f}', {bounds['end'][1]:.1f}')")
    print(f"\n  Total distances traveled:")
    print(f"    North: {plotter.cumulative_north:.1f}\" ({plotter.cumulative_north/12:.1f}')")
    print(f"    South: {plotter.cumulative_south:.1f}\" ({plotter.cumulative_south/12:.1f}')")
    print(f"    East: {plotter.cumulative_east:.1f}\" ({plotter.cumulative_east/12:.1f}')")
    print(f"    West: {plotter.cumulative_west:.1f}\" ({plotter.cumulative_west/12:.1f}')")
    print(f"\n  Net displacement from start:")
    print(f"    Delta X: {bounds['delta_x']:.1f}' ({bounds['delta_x']*12:.0f}\")")
    print(f"    Delta Y: {bounds['delta_y']:.1f}' ({bounds['delta_y']*12:.0f}\")")
    import math
    straight_distance = math.sqrt(bounds['delta_x']**2 + bounds['delta_y']**2)
    print(f"    Straight-line distance: {straight_distance:.1f}' ({straight_distance*12:.0f}\")")
    print("="*60)

if __name__ == "__main__":
    main()