---
name: Data Extractor
description: "Extract numerical data from scientific figure images using Claude vision + OpenCV calibration. Supports 26+ plot types including bar charts, scatter plots, forest plots, Kaplan-Meier curves, box plots, and more."
category: scientific-writing
tags: figure, data-extraction, plot, visualization, OCR, digitize, image-analysis
source: custom
---

# Data Extractor

## Use this skill when

- Extracting numerical data from published figure images
- Digitizing plots from PDF papers for meta-analysis
- Re-creating figures from old publications without source data
- Validating reported values against their visual representations
- Converting raster figures to data tables for re-analysis

## Instructions

### Supported Plot Types

| Plot Type | Extraction Method | Output |
|-----------|------------------|--------|
| Bar chart | Height measurement + axis calibration | Category → value table |
| Scatter plot | Point detection + coordinate mapping | (x, y) pairs |
| Line chart | Curve tracing + sampling | (x, y) series |
| Box plot | Median, Q1, Q3, whisker detection | Summary statistics |
| Forest plot | Point estimate + CI extraction | Effect size ± CI |
| Kaplan-Meier | Survival curve digitization | Time → survival table |
| Heatmap | Color → value mapping | Matrix of values |
| Violin plot | Distribution envelope → kernel density | Density estimates |
| ROC curve | Curve tracing | (FPR, TPR) pairs |
| Volcano plot | Point detection with labels | (logFC, -log10p) pairs |

### Workflow

```python
import cv2
import numpy as np

def extract_data_from_figure(image_path: str, plot_type: str = "scatter"):
    """
    Semi-automated data extraction workflow:
    
    1. Load and preprocess image
    2. Detect axes and scale bars
    3. Calibrate coordinate system
    4. Extract data points
    5. Map pixel coordinates to data values
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Step 1: Detect axes
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100,
                            minLineLength=100, maxLineGap=10)
    
    # Step 2: Use OCR for axis labels and tick marks
    # (requires pytesseract or Claude vision)
    
    # Step 3: Map pixel → data coordinates
    # px_to_data = lambda px: (px - origin_px) * scale + data_min
    
    return data_points

# For Claude Vision: describe the figure and ask for data extraction
VISION_PROMPT = """
Analyze this scientific figure and extract all numerical data:

1. Identify the plot type (bar, scatter, line, etc.)
2. Read axis labels and units
3. Extract all data points with their values
4. Note any error bars, confidence intervals, or annotations
5. Return as a structured table

Format the output as CSV:
x_label, y_label, value, error_lower, error_upper, group
"""
```

### Best Practices

- **Always cross-validate** extracted values against reported text
- **Report extraction uncertainty** (±pixel resolution mapped to data units)
- **Document the source** figure, panel, and page number
- **Use vector figures** (PDF/SVG) when available for higher accuracy
