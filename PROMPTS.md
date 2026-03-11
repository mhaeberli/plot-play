# Project Prompts and Development Log

This file tracks all user prompts and changes throughout the project development.

**Note:** Prompts from Session 1 are reconstructed based on commit messages and code changes, as the actual prompts were not saved. Session 2 prompts are actual verbatim prompts.

## Session 1: March 10, 2026

### Initial Project Creation
**Prompt (reconstructed):** "Create a python program that reads a CSV file with direction and distance columns, and plots the path as a line on a PDF. Start at position 12 inches, 12 inches. Scale should be 1 inch = 1 foot on 8.5x11 paper."
**Commit:** 07f441a - Initial commit: Line plotting program with PDF output
**Changes:**
- Created plot_line.py for plotting lines based on directional instructions
- Supports CSV input format with direction and distance columns
- Outputs to PDF sized for 8.5x11 paper
- Scale: 1 inch on paper = 1 foot in drawing
- Starting point: 12 inches, 12 inches

### Fix Python Environment
**Prompt (reconstructed):** [Error occurred running the program - matplotlib not found]
**Commit:** 39392de - Fix: Install matplotlib for default Python 3.12.5
**Changes:**
- Installed matplotlib for system's default python3
- Program now works with standard 'python3 plot_line.py' command

### Rescale Drawing
**Prompt (reconstructed):** "Can you rescale this to show a 32x32 foot area on the 8.5x11 page? Also change the units from inches to feet and add grid lines."
**Commit:** fa07c9a - Rescale drawing to fit 32x32 foot area on 8.5x11 page
**Changes:**
- New scale: 1 inch on paper = 4 feet in drawing (0.25 inches per foot)
- Starting point moved to center of 32x32 area (16', 16')
- Input units changed from inches to feet
- Added grid lines every 4 feet (1 inch on paper)
- Added feet labels on axes for easier reading

### Change Input Units
**Prompt (reconstructed):** "Actually, let's keep the input in inches instead of feet. The CSV should use inches but the scale should stay the same."
**Commit:** e9e6cb2 - Change input units back to inches while maintaining scale
**Changes:**
- Input distances now in inches (automatically converted to feet internally)
- Scale remains 1 inch on paper = 4 feet in drawing
- CSV files should now specify distances in inches

### Add Direction Abbreviations
**Prompt (reconstructed):** "Can you make it accept single letter abbreviations like n, s, e, w instead of typing out north, south, east, west?"
**Commit:** ea3d70a - Add support for single-letter direction abbreviations
**Changes:**
- Now accepts n/s/e/w as abbreviations for north/south/east/west
- Full direction names still work
- Directions are case-insensitive

### Move Starting Point Left
**Prompt (reconstructed):** "Move the starting point 12 feet to the left"
**Commit:** 2b054e2 - Move starting point 12 feet left
**Changes:**
- Starting point now at (4', 16') instead of (16', 16')
- Drawing starts closer to left edge of the 32x32 foot area
- Allows more room for eastward movement

### Move Starting Point Up
**Prompt (reconstructed):** "Now move it 12 feet up"
**Commit:** cd7f3c2 - Move starting point 12 feet up
**Changes:**
- Starting point now at (4', 28') instead of (4', 16')
- Drawing starts higher up in the 32x32 foot area
- Allows more room for southward movement

### Add Distance Calculations
**Prompt (reconstructed):** "Can you add calculations showing the distance between the start and end points? Show delta X, delta Y, and the straight line distance."
**Commit:** b5fc828 - Add distance calculations between start and end points
**Changes:**
- Shows start and end point coordinates
- Calculates and displays Delta X and Delta Y in feet and inches
- Calculates straight-line distance between start and end
- Helps understand the total displacement after following all instructions

### Add File Archiving
**Prompt (reconstructed):** "Can you make it archive the existing PDF before creating a new one so we don't lose previous plots?"
**Commit:** 66999b0 - Add automatic archiving of existing output files
**Changes:**
- Archives existing line_plot.pdf before creating a new one
- Archive filename includes timestamp (YYYYMMDD_HHMMSS format)
- Prevents accidental overwriting of previous plots
- Shows archive filename in console output

### Add Segment Annotations
**Prompt (reconstructed):** "Add length annotations to each line segment on the plot showing the distance in feet and inches"
**Commit:** b84cee2 - Add segment length annotations to plot
**Changes:**
- Each line segment now shows its length in feet and decimal inches
- Format: feet'-inches" (e.g., 12'-6.5")
- Annotations placed at segment midpoints with perpendicular offset
- Red text with white background for visibility

### Fix Axis Labels
**Prompt (reconstructed):** "The axis labels are showing both inches and feet - can you fix it to just show feet?"
**Commit:** 9333e5a - Fix axis labels to show only feet values
**Changes:**
- Removed duplicate axis labels (was showing both inches and feet)
- Now shows only feet values (0', 4', 8', 12', etc.)
- Clarified axis labels with '- feet' suffix

### Update Segment Format
**Prompt (reconstructed):** "Change the segment length format from feet'-inches" to feet' inches" (space instead of hyphen)"
**Commit:** 44419ef - Update segment length format to use space instead of hyphen
**Changes:**
- Changed format from feet'-inches" to feet' inches"
- Example: 6' 3.2" instead of 6'-3.2"
- Cleaner, more standard formatting for measurements

### Remove Verbose Output
**Prompt (reconstructed):** "Can you remove all the verbose diagnostic output? It's too much text. Just keep the summary at the end."
**Commit:** 3aac098 - Remove verbose diagnostic output during plotting
**Changes:**
- Removed per-step movement diagnostics
- Kept comprehensive summary statistics at the end
- Cleaner, less cluttered console output

### Comment Out Diagnostics
**Prompt (reconstructed):** "Actually, instead of removing the diagnostic code, can you just comment it out so we can re-enable it later if needed?"
**Commit:** 51a8227 - Comment out diagnostic output instead of removing
**Changes:**
- Kept diagnostic code but commented out for easy re-enabling
- Clean console output while preserving debugging capability

### Dynamic Output Filenames
**Prompt (reconstructed):** "Make the output PDF filename match the input CSV filename (like BigRoom.csv -> BigRoom.pdf)"
**Commit:** 63b4ea9 - Change output filename to match input CSV filename
**Changes:**
- Output PDF now uses same base name as input CSV file
- xxx.csv → xxx.pdf
- Archival system works with dynamic filenames
- Default line_plot.pdf used when no input file provided

### Organize Archives
**Prompt (reconstructed):** "Add all the CSV files and PDFs to git and organize the archive files into a subfolder"
**Commit:** a03171d - Add all project files and organize archives
**Changes:**
- Added all CSV input files and generated PDFs
- Added text summary files for each plot
- Organized all archive files into line_plot_archives/ subfolder
- Cleaned up Big Room file naming
- Complete project snapshot with all plotting examples

## Session 2: March 11, 2026

### Resume Work
**Prompt:** "resume"
**Response:** Showed project status and recent commits

### Document Prompts
**Prompt:** "please show me all prompts and replies for this project from the start"
**Response:** Created chronological development timeline

### Track Future Prompts
**Prompt (actual):** "in future, please include the literal prompts in the git repo somehow, perhaps in a notes file"
**Response:** Created this PROMPTS.md file to track all user prompts and development

### Track Prompts Globally  
**Prompt (actual):** "please apply this rule globally via CLAUDE.md or whatever is most appropriate"
**Commit:** ebe9141 - Update global CLAUDE.md to track prompts in all projects
**Response:** Updated global CLAUDE.md to include prompt tracking rule for all projects

### Reconstruct Historical Prompts
**Prompt (actual):** "can you try to reconstruct the prompts either from a local file or by whatever means from the git history for this project? even approximately would help"
**Response:** Reconstructed approximate prompts based on commit messages and code changes

---

## Future Prompts

All future prompts and responses will be documented here with the following format:

**Date:** [timestamp]
**Prompt:** [exact user prompt]
**Commit:** [commit hash and message]
**Changes:** [list of changes made]