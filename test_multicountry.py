import sys
import matplotlib.pyplot as plt
from src.config import CACHE_PATH
from src.data_processor import load_and_preprocess_photos
from src.viz import plot_country_timestamp_report

# Override plt.show to save the figure to disk so it doesn't block evaluation
call_idx = 0


def save_fig(*args, **kwargs):
    global call_idx
    call_idx += 1
    filename = f"multi_country_report_{call_idx}.png"
    plt.savefig(filename)
    print(f"Saved {filename}")


plt.show = save_fig

print("Loading photos...")
df, travel, home = load_and_preprocess_photos()

countries = ["Japan", "Indonesia", "Sri Lanka"]
print(f"Running reports for {countries}...")
plot_country_timestamp_report(travel, countries)
print("Finished!")
