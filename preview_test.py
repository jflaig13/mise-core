import requests

ENGINE_URL = "https://payroll-engine-147422626167.us-central1.run.app"

def preview_shift(filepath, filename):
    files = {"audio": open(filepath, "rb")}
    data = {"filename": filename}

    r = requests.post(f"{ENGINE_URL}/parse_only", files=files, data=data)
    r.raise_for_status()
    preview = r.json()
    print("\n=== PARSE PREVIEW ===")
    print(preview)
    return preview


def approve_shift(preview):
    r = requests.post(f"{ENGINE_URL}/commit_shift", json=preview)
    r.raise_for_status()
    print("\n=== COMMIT RESULT ===")
    print(r.json())


if __name__ == "__main__":
    # EXAMPLE USAGE:
    filepath = "/Users/jonathanflaig/Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Papa Staff Resources/Payroll Voice Recordings/030125_PM.wav"
    filename = "030125_PM.wav"

    preview = preview_shift(filepath, filename)

    input("\nApprove? Press Enter to commit...")
    approve_shift(preview)