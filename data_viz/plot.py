import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (update filename if needed)
dir = "../scrape/out/" # TODO iterate through all files in this directory

# get working directory
import os
wdir = os.getcwd()
file = wdir + "/scrape/out/2025-03-01_11-38-19_parking_data.csv" # dynamically updates working directory based on who is running it

df = pd.read_csv(file, header=None, names=["timestamp", "garage", "fullness_percentage"])

# Convert timestamp to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["day_of_week"] = df["timestamp"].dt.day_name()  # Extract day of the week
df["hour"] = df["timestamp"].dt.hour  # Extract hour of the day
df["date"] = df["timestamp"].dt.date  # Extract date

# Sorting for consistency
df = df.sort_values(by=["date", "hour", "garage"])

# Define color palette for consistency
palette = sns.color_palette("tab10")

### Plot 1: Parking Fullness Over Time ###
plt.figure(figsize=(12, 6))
sns.lineplot(x=df["timestamp"], y=df["fullness_percentage"], hue=df["garage"], palette=palette)
plt.title("Parking Fullness Over Time")
plt.xlabel("Time")
plt.ylabel("Fullness (%)")
plt.xticks(rotation=45)
plt.legend(title="Garage")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

### Plot 2: Average Parking Fullness Per Garage ###
plt.figure(figsize=(10, 5))
sns.barplot(x=df["garage"], y=df["fullness_percentage"], ci=None, palette=palette)
plt.title("Average Parking Fullness Per Garage")
plt.xlabel("Garage")
plt.ylabel("Average Fullness (%)")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

### Plot 3: Heatmap of Parking Fullness by Hour and Garage ###
df_pivot = df.pivot_table(index="hour", columns="garage", values="fullness_percentage", aggfunc="mean")
plt.figure(figsize=(10, 6))
sns.heatmap(df_pivot, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5)
plt.title("Heatmap of Parking Fullness by Hour and Garage")
plt.xlabel("Garage")
plt.ylabel("Hour of the Day")
plt.show()

### Plot 4: Parking Trends by Day of the Week ###
plt.figure(figsize=(12, 6))
sns.boxplot(x="day_of_week", y="fullness_percentage", hue="garage", data=df, order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], palette=palette)
plt.title("Parking Fullness Trends by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Fullness (%)")
plt.xticks(rotation=45)
plt.legend(title="Garage")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
