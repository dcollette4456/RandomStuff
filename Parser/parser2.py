import pandas as pd
import os

def extract_independent(file_path):
    print(f"🔍 Parsing: {file_path}")
    emails = set()
    urls = set()
    try:
        excel = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        for sheet_name, sheet in excel.items():
            if not sheet_name.lower().startswith("consolidated"):
                continue
            if "Email_Sender" in sheet.columns and "FE_URL" in sheet.columns:
                emails.update(sheet["Email_Sender"].dropna().unique())
                urls.update(sheet["FE_URL"].dropna().unique())
    except Exception as e:
        print(f"❌ Failed to parse {file_path}: {e}")
    return emails, urls

def parse_folder(path):
    all_emails = set()
    all_urls = set()

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".xlsx"):
                full_path = os.path.join(root, file)
                emails, urls = extract_independent(full_path)
                all_emails.update(emails)
                all_urls.update(urls)

    if not all_emails and not all_urls:
        print("🚫 No valid data found.")
        return

    max_len = max(len(all_emails), len(all_urls))
    emails_list = list(sorted(all_emails))
    urls_list = list(sorted(all_urls))

    # Pad lists to the same length for proper column alignment
    emails_list += [""] * (max_len - len(emails_list))
    urls_list += [""] * (max_len - len(urls_list))

    df_out = pd.DataFrame({
        "Email_sender": emails_list,
        "URL": urls_list
    })

    df_out.to_csv("parsed_watchlist.csv", index=False)
    print(f"\n✅ Done. Saved to: parsed_watchlist.csv")
    print(f"📧 Unique Emails: {len(all_emails)}")
    print(f"🌐 Unique URLs  : {len(all_urls)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 xlsx_unique_parser.py <file_or_folder>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        emails, urls = extract_independent(target)
        emails_list = sorted(emails)
        urls_list = sorted(urls)

        max_len = max(len(emails_list), len(urls_list))
        emails_list += [""] * (max_len - len(emails_list))
        urls_list += [""] * (max_len - len(urls_list))

        df = pd.DataFrame({
            "Email_sender": emails_list,
            "URL": urls_list
        })

        df.to_csv("parsed_watchlist.csv", index=False)
        print(f"✅ Done. Saved to: parsed_watchlist.csv")
    elif os.path.isdir(target):
        parse_folder(target)
    else:
        print("❌ Invalid path.")
