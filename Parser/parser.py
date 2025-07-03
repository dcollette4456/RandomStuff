import pandas as pd
import os

def extract_fixed_columns(file_path):
    print(f"🔍 Parsing: {file_path}")
    try:
        df = pd.read_excel(file_path, sheet_name="Consolidated (1036)", engine='openpyxl')
        if all(col in df.columns for col in ["Email_Sender", "FE_URL"]):
            df_clean = df[["Email_Sender", "FE_URL"]].dropna()
            df_clean.columns = ["Email_sender", "URL"]  # Normalize for Sentinel
            return df_clean
        else:
            print(f"⚠️  Missing expected columns in: {file_path}")
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
    return pd.DataFrame(columns=["Email_sender", "URL"])

def parse_folder(path):
    all_data = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".xlsx"):
                full_path = os.path.join(root, file)
                df = extract_fixed_columns(full_path)
                if not df.empty:
                    all_data.append(df)
    if not all_data:
        print("🚫 No valid data found.")
        return
    result = pd.concat(all_data, ignore_index=True).drop_duplicates()
    result.to_csv("parsed_watchlist.csv", index=False)
    print(f"\n✅ Done. Saved: parsed_watchlist.csv")
    print(f"📊 Rows exported: {len(result)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 xlsx_fixed_parser.py <file_or_folder_path>")
        exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        df = extract_fixed_columns(target)
        if not df.empty:
            df.drop_duplicates().to_csv("parsed_watchlist.csv", index=False)
            print(f"✅ Done. Saved: parsed_watchlist.csv")
        else:
            print("🚫 No valid data extracted.")
    elif os.path.isdir(target):
        parse_folder(target)
    else:
        print("❌ Path does not exist.")
