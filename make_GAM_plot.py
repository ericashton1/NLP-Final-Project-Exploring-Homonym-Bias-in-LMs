import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pygam import LinearGAM, s

df = pd.read_csv("results/homonym_minimal_pairs_byword_adjusted_fixed.tsv", sep="\t")
df.columns = df.columns.str.strip()

x_var = "log_freq"
y_var = "surp"
data = df[[x_var, y_var]].dropna()

X = data[[x_var]].values
y = data[y_var].values

gam = LinearGAM(s(0)).fit(X, y)

XX = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)

pred = gam.predict(XX)

conf = gam.confidence_intervals(XX, width=0.95)
lower, upper = conf[:, 0], conf[:, 1]

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(X, y, alpha=0.3, s=30, label="Observed data")

plt.plot(XX, pred, color="red", linewidth=3, label="GAM smooth")

# Confidence band
plt.fill_between(XX.flatten(), lower, upper, color="red", alpha=0.2, label="95% CI")

plt.xlabel(x_var)
plt.ylabel(y_var)
plt.title("GAM Smoothing: Surprisal vs Log Frequency")
plt.legend()
plt.tight_layout()

plt.savefig("gam_plot.png", dpi=300)
plt.show()

print("Saved: gam_plot.png")
