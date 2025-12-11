#!/usr/bin/env python3
"""
Simple script to display the KDE plot image
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def display_kde_plot():
    """Display the generated KDE plot"""
    
    # Load and display the image
    img_path = '/workspaces/cas-uzh/module-2/day6/restaurant_price_kde_comparison.png'
    
    try:
        img = mpimg.imread(img_path)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(img)
        ax.axis('off')  # Hide axes
        plt.title('Restaurant Price Distribution KDE Comparison', fontsize=16, pad=20)
        plt.tight_layout()
        plt.show()
        
        print("KDE plot displayed successfully!")
        
    except FileNotFoundError:
        print(f"Image file not found: {img_path}")
    except Exception as e:
        print(f"Error displaying image: {e}")

if __name__ == "__main__":
    display_kde_plot()