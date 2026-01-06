final_status = {}
# Read entire log file
file= open("log.txt", "r",encoding="utf-8")
data_In_The_File = file.read()
# Split all occurrences of recipient_id
final_status = {}  # dictionary to store data
entries = data_In_The_File.split('"recipient_id":"')
for i in entries[1:]:
    mobile = i.split('"')[0]  # get mobile number
    # Extract status
    status = None
    if '"status":"' in i:
        status = i.split('"status":"')[1].split('"')[0]
    # Extract failed reason (if exists)
    failed_reason = None
    if '"title":"' in i:
        failed_reason = i.split('"title":"')[1].split('"')[0]
    # Store both in the dictionary
    final_status[mobile] = {
        "status": status,
        "failed_reason": failed_reason
    }
# Write all final statuses to a file
file2= open("finalfile.txt", "w")
for mobile, status in final_status.items():
        file2.write(f"{mobile} | {status}\n")

print("Data inserted into the file successfully!")
