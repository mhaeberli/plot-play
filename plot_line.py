#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import csv
import sys
import numpy as np

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
        
        self.points.append((self.current_x, self.current_y))
        print(f"Moved {direction} {distance_inches}\" to ({self.current_x:.1f}', {self.current_y:.1f}')")
    
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
        
        # Set axis properties
        # 32 feet * 0.25 = 8 inches, leave 0.25" margins on each side
        ax.set_xlim(0, 8.5)  # Full page width in inches
        ax.set_ylim(0, 11)   # Full page height in inches
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Add grid lines every 4 feet (1 inch on paper)
        ax.set_xticks(np.arange(0, 8.5, 1.0))
        ax.set_yticks(np.arange(0, 11, 1.0))
        
        # Labels and title
        ax.set_xlabel('X (East →)')
        ax.set_ylabel('Y (North ↑)')
        ax.set_title('Line Plot (32\'×32\' drawing area)')
        ax.legend()
        
        # Add scale note
        ax.text(0.02, 0.98, 'Scale: 1" on paper = 4\' in drawing\nDrawing area: 32\'×32\'', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Add feet labels on secondary axes
        for i in range(0, 9):
            ax.text(i, -0.15, f'{i*4}\'', ha='center', fontsize=8)
        for i in range(0, 11):
            ax.text(-0.15, i, f'{i*4}\'', ha='right', fontsize=8)
        
        # Save to PDF
        with PdfPages(filename) as pdf:
            pdf.savefig(fig, bbox_inches='tight')
        
        plt.close()
        print(f"Plot saved to {filename}")
        
        # Return bounds for logging (in feet)
        return {
            'min_x': min(x_coords_feet),
            'max_x': max(x_coords_feet),
            'min_y': min(y_coords_feet),
            'max_y': max(y_coords_feet),
            'points': len(self.points)
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
    print("\nSummary:")
    print(f"  Total points: {bounds['points']}")
    print(f"  X range: {bounds['min_x']:.1f}' to {bounds['max_x']:.1f}'")
    print(f"  Y range: {bounds['min_y']:.1f}' to {bounds['max_y']:.1f}'")

if __name__ == "__main__":
    main()