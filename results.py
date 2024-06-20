import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from sklearn.metrics import mean_squared_error, r2_score

_predictions = pd.read_csv("ochem_pred.csv")
_truth = pd.read_csv("ochem_test.csv")
data = pd.DataFrame(
    {
        "truth": _truth["logS"],
        "prediction": _predictions["task_0"],
    }
)

# Create the plot
fig, ax = plt.subplots(figsize=(5, 4), constrained_layout=True)
ax: Axes
ax.grid(True, which="major", axis="both")
ax.set_axisbelow(True)
hb = ax.hexbin(x=data["truth"], y=data["prediction"], gridsize=70, cmap="viridis", mincnt=1)

cb = fig.colorbar(hb, ax=ax)
cb.set_label("Number of compounds")
ax.plot([-12, 2], [-12, 2], "r", linewidth=1)
ax.plot([-12, 2], [-11, 3], "r--", linewidth=0.5)
ax.plot([-12, 2], [-13, 1], "r--", linewidth=0.5)
ax.set_title(r"$\tt{fastsolv}$")
ax.set_xlabel("Solubility (LogS)")
ax.set_ylabel("cLogS")
ax.set_xlim(-12, 2)
ax.set_ylim(-12, 2)

# Text box for R2 and MSE
textstr = "\n".join(
    (
        f"$\\bf{{R2}}:$ {r2_score(data['truth'], data['prediction']):.2f}",
        f"$\\bf{{MSE}}:$ {mean_squared_error(data['truth'], data['prediction']):.2f}",
    )
)
ax.text(
    -8.55,
    -2.1,
    textstr,
    transform=ax.transData,
    fontsize=10,
    verticalalignment="top",
    horizontalalignment="right",
)

# Pie chart
_frac_wn_1 = np.count_nonzero(np.abs(data["truth"] - data["prediction"]) < 1.0) / len(data)
sizes = [1 - _frac_wn_1, _frac_wn_1]
ax_inset = ax.inset_axes([-12, -2, 4, 4], transform=ax.transData)
ax_inset.pie(
    sizes,
    colors=["#ae2b27", "#4073b2"],
    startangle=360 * (_frac_wn_1 - 0.5) / 2,
    wedgeprops={"edgecolor": "black"},
    autopct="%1.f%%",
    textprops=dict(color="w"),
)
ax_inset.axis("equal")

plt.show()
