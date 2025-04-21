import matplotlib.pyplot as plt

def plot_yields_boxplot(signal_yields: dict, decoy_yields: dict, expected_yields: dict):
    """
    Generates a box plot for expected signal and decoy yields (Y_n).

    Args:
        signal_yields (dict): Signal yields from multiple simulations.
        decoy_yields (dict): Decoy yields from multiple simulations.
        expected_yields (dict): Expected yields from multiple simulations.
    """
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "font.size": 12,
        "text.latex.preamble": r"\usepackage{amsmath}"
    })
    
    data = []
    labels = []

    for n in range(1, len(expected_yields) + 1):
        data.append(expected_yields[f'Y_{n}'])
        labels.append(f'$Y_{{{n}}}$')
        data.append(signal_yields[f'Y_{n}'])
        labels.append(f'$Y_{{{n}}}^{{(\\mu)}}$')
        data.append(decoy_yields[f'Y_{n}'])
        labels.append(f'$Y_{{{n}}}^{{(\\nu)}}$')

    # Create box plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Boxes color palette
    colors = ['#8ecae6', '#219ebc', '#023047']
    boxprops = dict(linestyle='-', linewidth=1.5)
    
    # Repeat colors for each group Y_n
    box_colors = []
    for i in range(len(expected_yields)):
        box_colors.extend(colors)
    
    # Create boxplot with personalized colors
    boxplot = ax.boxplot(data, showmeans=True, patch_artist=True)
    
    # Apply colors to boxes
    for patch, color in zip(boxplot['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Style for boxplot elements
    for element in ['whiskers', 'caps', 'medians']:
        for item in boxplot[element]:
            item.set(color='#444444', linewidth=1.5)
    
    for flier in boxplot['fliers']:
        flier.set(marker='o', markerfacecolor='#444444', alpha=0.6, markersize=4)
    
    # Latex notation for axis
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels, rotation=45, fontsize=11)
    ax.set_ylabel(r'\textrm{Yield}', fontsize=14)
    ax.set_title(r'\textrm{Comparison of Expected and Measured Yields}', fontsize=15)
    
    # Plot style
    ax.grid(True, linestyle='--', alpha=0.4, color='gray')
    ax.set_facecolor('#f8f8f8')
    fig.patch.set_facecolor('#ffffff')
    
    # Upgrade ticks
    ax.tick_params(direction='out', length=6, width=1.5)
    
    plt.tight_layout()
    plt.show()