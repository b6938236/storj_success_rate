#!/usr/bin/env python3
#A StorJ node monitor script: Initial version by turbostorjdsk / KernelPanick, adapted by BrightSilence, original grep statements by Alexey
#Reimplemented in python by b6938236

# Only iterates through the log file once

import sys
import subprocess

if len(sys.argv) == 2: # user provided an argument
    try: # interpret argument as filepath
        with open(sys.argv[1], 'r') as inf:
            log_file = inf.read()
    except: # interpret argument as docker container name
        log_file = subprocess.run(["docker", "logs", sys.argv[1]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
else: # user did not provide argument, use default name of "storagenode"
    log_file = subprocess.run(["docker", "logs", "storagenode"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout

# log_file is a byte array, convert it to a list of strings
log_file = log_file.decode("ascii").split("\n")

audit_success_count = 0
audit_recoverable_failed_count = 0
audit_unrecoverable_failed_count = 0
download_success_count = 0
download_failed_count = 0
upload_success_count = 0
upload_rejected_count = 0
upload_failed_count = 0
repair_download_success_count = 0
repair_download_failed_count = 0
repair_upload_success_count = 0
repair_upload_failed_count = 0
for line in log_file:
    if "GET_AUDIT" in line:
        if "downloaded" in line:
            audit_success_count += 1
        if "failed" in line:
            if "NotFound" in line:
                audit_unrecoverable_failed_count += 1
            else:
                audit_recoverable_failed_count += 1
    elif '"GET"' in line:
        if "downloaded" in line:
            download_success_count += 1
        elif "failed" in line:
            download_failed_count += 1
    elif '"PUT"' in line:
        if "uploaded" in line:
            upload_success_count += 1
        elif "failed" in line:
            upload_failed_count += 1
    elif "rejected" in line:
        if "upload" in line:
            upload_rejected_count += 1
    elif "GET_REPAIR" in line:
        if "downloaded" in line:
            repair_download_success_count += 1
        elif "failed" in line:
            repair_download_failed_count += 1
    elif "PUT_REPAIR" in line:
        if "uploaded" in line:
            repair_upload_success_count += 1
        elif "failed" in line:
            repair_upload_failed_count += 1

# rate calculations and div by 0 checks
if audit_success_count + audit_recoverable_failed_count + audit_unrecoverable_failed_count != 0:
    audit_success_rate_min = audit_success_count / (audit_success_count + audit_recoverable_failed_count + audit_unrecoverable_failed_count)
else:
    audit_success_rate_min = 0
if audit_success_count + audit_unrecoverable_failed_count != 0:
    audit_success_rate_max = audit_success_count / (audit_success_count + audit_unrecoverable_failed_count)
else:
    audit_success_rate_max = 0
if download_success_count + download_failed_count != 0:
    download_success_rate = download_success_count / (download_success_count + download_failed_count)
else:
    download_success_rate = 0
if upload_success_count + upload_rejected_count != 0:
    upload_acceptance_rate = upload_success_count / (upload_success_count + upload_rejected_count)
else:
    upload_acceptance_rate = 0
if upload_success_count + upload_failed_count != 0:
    upload_success_rate = upload_success_count / (upload_success_count + upload_failed_count)
else:
    upload_success_rate = 0
if repair_download_success_count + repair_download_failed_count != 0:
    repair_download_success_rate = repair_download_success_count / (repair_download_success_count + repair_download_failed_count)
else:
    repair_download_success_rate = 0
if repair_upload_success_count + repair_upload_failed_count != 0:
    repair_upload_success_rate = repair_upload_success_count / (repair_upload_success_count + repair_upload_failed_count)
else:
    repair_upload_success_rate = 0

# dump stats to console
print("\033[96m========== AUDIT ============= \033[0m")
print("\033[92mSuccessful:           {0} \033[0m".format(audit_success_count))
print("\033[33mRecoverable failed:   {0} \033[0m".format(audit_recoverable_failed_count))
print("\033[91mUnrecoverable failed: {0} \033[0m".format(audit_unrecoverable_failed_count))
print("Success Rate Min:     {:.3%}".format(audit_success_rate_min))
print("Success Rate Max:     {:.3%}".format(audit_success_rate_max))
print("\033[96m========== DOWNLOAD ========== \033[0m")
print("\033[92mSuccessful:           {0} \033[0m".format(download_success_count))
print("\033[33mFailed:               {0} \033[0m".format(download_failed_count))
print("Success Rate:         {:.3%}".format(download_success_rate))
print("\033[96m========== UPLOAD ============ \033[0m")
print("\033[92mSuccessful:           {0} \033[0m".format(upload_success_count))
print("\033[33mRejected:             {0} \033[0m".format(upload_rejected_count))
print("\033[33mFailed:               {0} \033[0m".format(upload_failed_count))
print("Acceptance Rate:      {:.3%}".format(upload_acceptance_rate))
print("Success Rate:         {:.3%}".format(upload_success_rate))
print("\033[96m========== REPAIR DOWNLOAD === \033[0m")
print("\033[92mSuccessful:           {0} \033[0m".format(repair_download_success_count))
print("\033[33mFailed:               {0} \033[0m".format(repair_download_failed_count))
print("Success Rate:         {:.3%}".format(repair_download_success_rate))
print("\033[96m========== REPAIR UPLOAD ===== \033[0m")
print("\033[92mSuccessful:           {0} \033[0m".format(repair_upload_success_count))
print("\033[33mFailed:               {0} \033[0m".format(repair_upload_failed_count))
print("Success Rate:         {:.3%}".format(repair_upload_success_rate))