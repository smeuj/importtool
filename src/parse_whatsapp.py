import sys
import re
import json

pat_day       = r"0[1-9]|[1-2][0-9]|3[0-1]|[1-9]"
pat_month     = r"0[1-9]|1[0-2]|[1-9]"
pat_year      = r"\d{2}|\d{4}"
pat_hours     = r"(?:[0-1][0-9])|(?:2[0-4])"
pat_minutes   = r"(?:[0-5][0-9])|60"
pat_date      = f"({pat_month})/({pat_day})/({pat_year})"
pat_time      = f"({pat_hours}):({pat_minutes})"
pat_date_time = f"({pat_date}), ({pat_time})"
pat_name      = r"[^:]+"
pat_message   = f"^{pat_date_time} - ({pat_name}): (.*)$"

def main(in_path, out_path):
    entries = []
    with open(in_path, encoding = "utf-8") as source:
        while True:
            line = source.readline()
            if not line:
                break
            line = line.strip()
            result = re.match(pat_message, line)
            if not result:
                entries[-1]["message"] += f"\n{line}"
            else:
                entries.append({
                    "date":    result.group(1),
                    "time":    result.group(5),
                    "author":  result.group(8),
                    "message": result.group(9)
                })
    with open(out_path, "w", encoding = "utf-8") as dest:
        json.dump(entries, dest, indent = 4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_whatsapp.py <input_path> <output_path>")
    else:
        main(sys.argv[1], sys.argv[2])
