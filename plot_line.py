#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import csv
import sys
import numpy as np

class LinePlotter:
    def __init__(self):
        self.current_x = 12.0  # Start at 12 inches
        self.current_y = 12.0  # Start at 12 inches
        self.points = [(self.current_x, self.current_y)]
        self.scale = 1.0  # 1 inch on paper = 1 foot in drawing
        
    def turn_and_go(self, direction, distance_inches):
        """Move in the specified direction by the given distance in inches."""
        direction = direction.lower()
        
        if direction == 'north':
            self.current_y += distance_inches
        elif direction == 'south':
            self.current_y -= distance_inches
        elif direction == 'east':
            self.current_x += distance_inches
        elif direction == 'west':
            self.current_x -= distance_inches
        else:
            raise ValueError(f"Unknown direction: {direction}")
        
        self.points.append((self.current_x, self.current_y))
        print(f"Moved {direction} {distance_inches}\" to ({self.current_x:.1f}, {self.current_y:.1f})")
    
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
        
        # Extract x and y coordinates
        x_coords = [p[0] for p in self.points]
        y_coords = [p[1] for p in self.points]
        
        # Plot the line
        ax.plot(x_coords, y_coords, 'b-', linewidth=2, marker='o', markersize=4)
        
        # Mark start and end points
        ax.plot(x_coords[0], y_coords[0], 'go', markersize=8, label='Start')
        ax.plot(x_coords[-1], y_coords[-1], 'ro', markersize=8, label='End')
        
        # Add point labels
        for i, (x, y) in enumerate(self.points):
            ax.annotate(f'P{i}', (x, y), xytext=(2, 2), textcoords='offset points', fontsize=8)
        
        # Set axis properties
        ax.set_xlim(0, 8.5 * 12)  # 8.5 inches * 12 (scale factor for feet)
        ax.set_ylim(0, 11 * 12)   # 11 inches * 12 (scale factor for feet)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Labels and title
        ax.set_xlabel('X (inches, East →)')
        ax.set_ylabel('Y (inches, North ↑)')
        ax.set_title('Line Plot (1 inch = 1 foot)')
        ax.legend()
        
        # Add scale note
        ax.text(0.02, 0.98, 'Scale: 1" on paper = 1\' in drawing', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Save to PDF
        with PdfPages(filename) as pdf:
            pdf.savefig(fig, bbox_inches='tight')
        
        plt.close()
        print(f"Plot saved to {filename}")
        
        # Return bounds for logging
        return {
            'min_x': min(x_coords),
            'max_x': max(x_coords),
            'min_y': min(y_coords),
            'max_y': max(y_coords),
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
        # Use test instructions
        print("Using test instructions:")
        test_instructions = [
            ('north', 4),
            ('east', 8),
            ('north', 6)
        ]
        plotter.parse_instructions(test_instructions)
    
    # Generate PDF
    bounds = plotter.plot_to_pdf('line_plot.pdf')
    
    # Print summary
    print("\nSummary:")
    print(f"  Total points: {bounds['points']}")
    print(f"  X range: {bounds['min_x']:.1f}\" to {bounds['max_x']:.1f}\"")
    print(f"  Y range: {bounds['min_y']:.1f}\" to {bounds['max_y']:.1f}\"")

if __name__ == "__main__":
    main()