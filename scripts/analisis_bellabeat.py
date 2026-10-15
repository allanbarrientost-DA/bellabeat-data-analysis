
"""
BellaBeat | Exploratory Data Analysis
=====================================

Purpose:
    Explore daily activity patterns in Fitbit tracker data.

Input:
    data/processed/dailyActivity_consolidado.csv

Outputs:
    results/tables/
    results/generated_charts/

Requirements:
    pandas
    matplotlib

The script does not modify the input dataset.
"""

from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

# This script is stored in the project's scripts/ folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "dailyActivity_consolidado.csv"
)

TABLES_DIR = PROJECT_DIR / "results" / "tables"
CHARTS_DIR = PROJECT_DIR / "results" / "generated_charts"

REQUIRED_COLUMNS = [
    "Id",
    "ActivityDate",
    "TotalSteps",
    "Calories",
    "VeryActiveMinutes",
    "FairlyActiveMinutes",
    "LightlyActiveMinutes",
    "SedentaryMinutes",
]

ACTIVITY_COLUMNS = [
    "VeryActiveMinutes",
    "FairlyActiveMinutes",
    "LightlyActiveMinutes",
]

NUMERIC_COLUMNS = [
    "TotalSteps",
    "TotalDistance",
    "TrackerDistance",
    "VeryActiveDistance",
    "ModeratelyActiveDistance",
    "LightActiveDistance",
    "SedentaryActiveDistance",
    "VeryActiveMinutes",
    "FairlyActiveMinutes",
    "LightlyActiveMinutes",
    "SedentaryMinutes",
    "Calories",
]


# ============================================================
# 2. LOAD AND VALIDATE DATA
# ============================================================

def prepare_output_folders():
    """Create output folders if they do not already exist."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data(file_path):
    """Load the consolidated CSV and validate its structure."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"\nInput file not found:\n{file_path}\n\n"
            "Place your local copy of dailyActivity_consolidado.csv "
            "inside data/processed/."
        )

    data = pd.read_csv(file_path)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    data["ActivityDate"] = pd.to_datetime(
        data["ActivityDate"],
        errors="coerce",
    )

    for column in NUMERIC_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    return data


# ============================================================
# 3. DATA QUALITY AUDIT
# ============================================================

def audit_data(data):
    """Summarize missing values, duplicates and unusual values."""

    print("\n" + "=" * 55)
    print("DATA QUALITY AUDIT")
    print("=" * 55)

    valid_dates = data["ActivityDate"].dropna()

    print(f"Rows: {len(data):,}")
    print(f"Columns: {len(data.columns)}")
    print(f"Unique users: {data['Id'].nunique():,}")

    if not valid_dates.empty:
        print(f"First date: {valid_dates.min().date()}")
        print(f"Last date:  {valid_dates.max().date()}")

    # Missing values and data types
    quality = pd.DataFrame({
        "data_type": data.dtypes.astype(str),
        "missing_values": data.isna().sum(),
    })

    quality.to_csv(TABLES_DIR / "data_quality_summary.csv")

    print("\nMissing values by column:")
    print(quality["missing_values"].to_string())

    # Duplicate checks
    exact_duplicates = data.duplicated().sum()
    key_duplicates = data.duplicated(
        subset=["Id", "ActivityDate"]
    ).sum()

    print(f"\nExact duplicate rows: {exact_duplicates:,}")
    print(f"Duplicate user-date keys: {key_duplicates:,}")

    # Check negative values in activity metrics only
    available_metrics = [
        column
        for column in NUMERIC_COLUMNS
        if column in data.columns
    ]

    negative_counts = (
        data[available_metrics].lt(0).sum()
    )

    print("\nNegative values by metric:")
    print(negative_counts.to_string())

    # Zero-value checks
    zero_summary = {}

    for column in [
        "TotalSteps",
        "TotalDistance",
        "Calories",
    ]:
        if column in data.columns:
            zero_summary[column] = int(
                data[column].eq(0).sum()
            )

    pd.Series(
        zero_summary,
        name="zero_value_records",
    ).to_csv(TABLES_DIR / "zero_value_summary.csv")

    print("\nRecords with zero values:")
    for column, count in zero_summary.items():
        print(f"{column}: {count:,}")

    # Flag zero-step records that still contain activity
    active_minutes = data[ACTIVITY_COLUMNS].fillna(0).sum(axis=1)

    zero_steps_with_activity = (
        data["TotalSteps"].eq(0)
        & active_minutes.gt(0)
    )

    exceptions = data.loc[
        zero_steps_with_activity,
        [
            "Id",
            "ActivityDate",
            "TotalSteps",
            "Calories",
            *ACTIVITY_COLUMNS,
            "SedentaryMinutes",
        ],
    ]

    exceptions.to_csv(
        TABLES_DIR / "zero_steps_with_activity.csv",
        index=False,
    )

    print(
        "\nZero-step records with positive active minutes: "
        f"{len(exceptions):,}"
    )

    print(
        "These records are flagged for review, not "
        "automatically classified as errors."
    )


# ============================================================
# 4. ACTIVITY TYPES
# ============================================================

def analyze_activity_types(data):
    """Calculate average daily minutes for each activity type."""

    averages = data[ACTIVITY_COLUMNS].mean()

    averages.index = [
        "Very active",
        "Fairly active",
        "Lightly active",
    ]

    averages.name = "average_minutes_per_day"

    averages.to_csv(
        TABLES_DIR / "average_activity_minutes.csv"
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(averages.index, averages.values)
    ax.bar_label(bars, fmt="%.1f", padding=4)

    ax.set_title("Average Daily Minutes by Activity Type")
    ax.set_xlabel("Activity Type")
    ax.set_ylabel("Average Minutes per Day")

    fig.tight_layout()
    fig.savefig(
        CHARTS_DIR / "activity_types.png",
        dpi=160,
    )
    plt.close(fig)

    print("\n=== AVERAGE DAILY ACTIVITY ===")
    print(averages.round(2).to_string())


# ============================================================
# 5. STEPS AND CALORIES
# ============================================================

def analyze_steps_and_calories(data):
    """Explore the association between steps and recorded calories."""

    valid = data[
        ["TotalSteps", "Calories"]
    ].dropna()

    correlation = valid["TotalSteps"].corr(
        valid["Calories"],
        method="pearson",
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        valid["TotalSteps"],
        valid["Calories"],
        alpha=0.55,
    )

    ax.set_title("Daily Steps and Recorded Calories")
    ax.set_xlabel("Daily Steps")
    ax.set_ylabel("Recorded Calories")

    fig.tight_layout()
    fig.savefig(
        CHARTS_DIR / "steps_vs_calories.png",
        dpi=160,
    )
    plt.close(fig)

    pd.DataFrame([{
        "pearson_correlation": correlation,
        "records_analyzed": len(valid),
    }]).to_csv(
        TABLES_DIR / "steps_calories_correlation.csv",
        index=False,
    )

    print("\n=== STEPS AND CALORIES ===")
    print(f"Pearson correlation: {correlation:.3f}")
    print(f"Records analyzed: {len(valid):,}")


# ============================================================
# 6. WEEKLY ACTIVITY PATTERNS
# ============================================================

def analyze_weekday_patterns(data):
    """Compare average daily steps across weekdays."""

    valid = data.dropna(
        subset=["ActivityDate", "TotalSteps"]
    ).copy()

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    weekday_labels = {
        "Monday": "Monday",
        "Tuesday": "Tuesday",
        "Wednesday": "Wednesday",
        "Thursday": "Thursday",
        "Friday": "Friday",
        "Saturday": "Saturday",
        "Sunday": "Sunday",
    }

    valid["Weekday"] = valid["ActivityDate"].dt.day_name()

    averages = (
        valid.groupby("Weekday")["TotalSteps"]
        .mean()
        .reindex(weekday_order)
    )

    averages.index = [
        weekday_labels[day]
        for day in averages.index
    ]

    averages.name = "average_daily_steps"

    averages.to_csv(
        TABLES_DIR / "average_steps_by_weekday.csv"
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(averages.index, averages.values)
    ax.bar_label(bars, fmt="%.0f", padding=3)

    ax.set_title("Average Daily Steps by Weekday")
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Average Steps")
    ax.tick_params(axis="x", rotation=25)

    fig.tight_layout()
    fig.savefig(
        CHARTS_DIR / "steps_by_weekday.png",
        dpi=160,
    )
    plt.close(fig)

    print("\n=== AVERAGE STEPS BY WEEKDAY ===")
    print(averages.round(0).to_string())


# ============================================================
# 7. USER-LEVEL STEPS AND SEDENTARY TIME
# ============================================================

def analyze_user_activity(data):
    """
    Calculate per-user averages and their Pearson correlation.

    This differs from the daily-record correlation:
    each observation in this comparison represents one user.
    """

    user_summary = (
        data.groupby("Id")
        .agg(
            average_steps=("TotalSteps", "mean"),
            average_sedentary_minutes=(
                "SedentaryMinutes", "mean"
            ),
            recorded_days=("ActivityDate", "count"),
        )
        .dropna(
            subset=[
                "average_steps",
                "average_sedentary_minutes",
            ]
        )
    )

    user_summary.to_csv(
        TABLES_DIR / "user_activity_summary.csv"
    )

    correlation = user_summary[
        "average_steps"
    ].corr(
        user_summary["average_sedentary_minutes"],
        method="pearson",
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        user_summary["average_steps"],
        user_summary["average_sedentary_minutes"],
        alpha=0.75,
    )

    ax.set_title(
        "Average Steps vs. Sedentary Minutes by User"
    )
    ax.set_xlabel("Average Daily Steps per User")
    ax.set_ylabel("Average Daily Sedentary Minutes")

    fig.tight_layout()
    fig.savefig(
        CHARTS_DIR / "user_steps_vs_sedentary_time.png",
        dpi=160,
    )
    plt.close(fig)

    pd.DataFrame([{
        "pearson_correlation": correlation,
        "users_analyzed": len(user_summary),
    }]).to_csv(
        TABLES_DIR / "user_steps_sedentary_correlation.csv",
        index=False,
    )

    print("\n=== USER-LEVEL ACTIVITY ===")
    print(f"Users analyzed: {len(user_summary):,}")
    print(f"Pearson correlation: {correlation:.3f}")
    print(
        "Interpretation: assess the direction and strength "
        "alongside the scatter. Correlation does not imply "
        "causation."
    )


# ============================================================
# 8. MAIN
# ============================================================

def main():
    prepare_output_folders()

    try:
        data = load_data(INPUT_FILE)
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        return 1

    audit_data(data)
    analyze_activity_types(data)
    analyze_steps_and_calories(data)
    analyze_weekday_patterns(data)
    analyze_user_activity(data)

    print("\nAnalysis completed.")
    print(f"Tables saved to: {TABLES_DIR}")
    print(f"Charts saved to: {CHARTS_DIR}")
    print(
        "\nLimitation: results describe this historical sample. "
        "They do not establish causation or guarantee that the "
        "patterns represent BellaBeat customers."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
