import json
from collections import Counter

with open("blocked_groups.json", "r") as file:
        blocked_groups = json.load(file)

all_ids = []
unique_group_ids = []
bot_ids = blocked_groups.keys()

for id in bot_ids:
    for group_info in blocked_groups[id]['groups']:
          all_ids.append(group_info['group_id'])

value_counts = Counter(all_ids)
for value, count in value_counts.items():
    print(f"{value}: {count}")