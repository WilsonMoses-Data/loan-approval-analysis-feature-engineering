"""Generate branded README visuals for the Week 3 loan-approval project."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "loan_prediction_week3_final_cleaned.csv"
IMAGE_DIR = ROOT / "images"

DARK = "#0d0d0d"
OFF_WHITE = "#f4f0e8"
GREY = "#a9a7a2"
GOLD = "#c69a4b"
GRID = "#333333"


def finish_chart(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def style_axis(axis: plt.Axes, grid_axis: str = "y") -> None:
    axis.set_facecolor(DARK)
    axis.tick_params(colors=OFF_WHITE, labelsize=10)
    axis.xaxis.label.set_color(GREY)
    axis.yaxis.label.set_color(GREY)
    axis.title.set_color(OFF_WHITE)
    for spine in axis.spines.values():
        spine.set_visible(False)
    axis.grid(axis=grid_axis, color=GRID, linewidth=0.7, alpha=0.65)
    axis.set_axisbelow(True)


def create_social_preview() -> None:
    fig = plt.figure(figsize=(8, 4), dpi=160, facecolor=DARK)
    canvas = fig.add_axes((0, 0, 1, 1))
    canvas.set_axis_off()
    canvas.add_patch(
        plt.Rectangle((0.065, 0.12), 0.008, 0.76, transform=canvas.transAxes, color=GOLD)
    )
    fig.text(0.10, 0.77, "FINANCIAL ANALYTICS  |  WEEK 3", color=GOLD, fontsize=12, weight="bold")
    fig.text(0.10, 0.58, "LOAN APPROVAL", color=OFF_WHITE, fontsize=29, weight="bold")
    fig.text(0.10, 0.45, "ANALYSIS + FEATURES", color=OFF_WHITE, fontsize=22, weight="bold")
    fig.text(0.10, 0.30, "614 applications  •  6 tests  •  12 engineered features", color=GREY, fontsize=10)
    fig.text(0.10, 0.17, "WILSON MOSES  |  DATA SCIENCE × AI ENGINEERING", color=GOLD, fontsize=10)
    logo_axis = fig.add_axes((0.78, 0.32, 0.18, 0.34))
    logo_axis.imshow(plt.imread(IMAGE_DIR / "wilson-moses-logo.png"))
    logo_axis.set_axis_off()
    fig.savefig(IMAGE_DIR / "social-preview.png", facecolor=DARK)
    plt.close(fig)


def create_credit_history_chart(data: pd.DataFrame) -> None:
    rates = data.groupby("credit_history", observed=True)["loan_status"].apply(lambda values: values.eq("Y").mean() * 100)
    labels = ["No positive history", "Positive history"]
    values = [rates.loc[0.0], rates.loc[1.0]]
    fig, axis = plt.subplots(figsize=(8.6, 5), facecolor=DARK)
    bars = axis.bar(labels, values, color=[GREY, GOLD], width=0.56)
    style_axis(axis)
    axis.set_title("Historical approval rate by credit history", fontsize=17, weight="bold", pad=18)
    axis.set_ylabel("Approval rate (%)")
    axis.set_ylim(0, 100)
    for bar, value in zip(bars, values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 3, f"{value:.2f}%", ha="center", color=OFF_WHITE, fontsize=11, weight="bold")
    finish_chart(fig, IMAGE_DIR / "credit-history-approval.png")


def create_property_area_chart(data: pd.DataFrame) -> None:
    order = ["Semiurban", "Urban", "Rural"]
    rates = data.groupby("property_area", observed=True)["loan_status"].apply(lambda values: values.eq("Y").mean() * 100).reindex(order)
    fig, axis = plt.subplots(figsize=(8.8, 5), facecolor=DARK)
    bars = axis.bar(order, rates.values, color=[GOLD, "#777777", "#aaa7a2"], width=0.58)
    style_axis(axis)
    axis.set_title("Historical approval rate by property area", fontsize=17, weight="bold", pad=18)
    axis.set_ylabel("Approval rate (%)")
    axis.set_ylim(0, 100)
    for bar, value in zip(bars, rates.values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 3, f"{value:.2f}%", ha="center", color=OFF_WHITE, fontsize=11, weight="bold")
    finish_chart(fig, IMAGE_DIR / "property-area-approval.png")


def create_income_loan_chart(data: pd.DataFrame) -> None:
    palette = data["loan_status"].map({"Y": GOLD, "N": GREY})
    fig, axis = plt.subplots(figsize=(8.8, 5.2), facecolor=DARK)
    axis.scatter(data["total_income"], data["loan_amount"], c=palette, s=25, alpha=0.60, edgecolors="none")
    style_axis(axis, grid_axis="both")
    axis.set_title("Household income and requested loan amount", fontsize=17, weight="bold", pad=18)
    axis.set_xlabel("Total monthly income")
    axis.set_ylabel("Recorded loan amount (thousands)")
    axis.text(0.98, 0.05, "Spearman rho = 0.688", transform=axis.transAxes, ha="right", color=GOLD, fontsize=10, weight="bold")
    finish_chart(fig, IMAGE_DIR / "income-loan-relationship.png")


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(DATA_PATH)
    create_social_preview()
    create_credit_history_chart(data)
    create_property_area_chart(data)
    create_income_loan_chart(data)
    print("Created branded Week 3 README visuals.")


if __name__ == "__main__":
    main()
