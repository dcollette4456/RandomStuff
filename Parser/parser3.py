import pandas as pd
import os

def extract_independent(file_path, output_dir):
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
        return

    if not emails and not urls:
        print("⚠️ No valid data found in file.")
        return

    # Align lengths
    max_len = max(len(emails), len(urls))
    email_list = sorted(emails) + [""] * (max_len - len(emails))
    url_list = sorted(urls) + [""] * (max_len - len(urls))

    df_out = pd.DataFrame({
        "Email_sender": email_list,
        "URL": url_list
    })

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, f"parsed_{base_name}.csv")
    df_out.to_csv(output_path, index=False)

    print(f"✅ Output: {output_path} | 📧 {len(emails)} emails | 🌐 {len(urls)} URLs")

def parse_folder(folder_path):
    output_dir = os.path.abspath(folder_path)
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xlsx"):
                full_path = os.path.join(root, file)
                extract_independent(full_path, output_dir)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 xlsx_per_file_parser.py <folder_path>")
        sys.exit(1)

    target = sys.argv[1]
    if not os.path.isdir(target):
        print("❌ That’s not a folder.")
        sys.exit(1)

    parse_folder(target)
