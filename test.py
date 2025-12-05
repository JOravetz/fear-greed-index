from fear_greed_index import CNNFearAndGreedIndex
import matplotlib.pyplot as plt

cnn_fg = CNNFearAndGreedIndex()

# Print Fear and Greed complete report
print(cnn_fg.get_complete_report())

# Access individual values
print(f"\nCurrent Score: {cnn_fg.get_score()}")
print(f"Current Rating: {cnn_fg.get_rating()}")

# Generate and save charts
fig = cnn_fg.plot_all_charts()
fig.savefig("fear_greed_dashboard.png", dpi=150, bbox_inches='tight')
print("\nSaved chart to fear_greed_dashboard.png")

# Show the chart (comment out if running headless)
plt.show()
