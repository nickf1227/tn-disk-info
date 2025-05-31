#!/usr/bin/env python3
import subprocess
import json
import math
import re
import argparse
import os
from collections import defaultdict
from datetime import datetime

# Initialize JSON output structure
json_output = {
    "pools": [],
    "timestamp": datetime.now().isoformat()
}

def convert_size(size_bytes):
    """Convert bytes to human-readable format"""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_smart_data(device):
    """Retrieve SMART data for a device using smartctl"""
    try:
        result = subprocess.run(
            ["sudo", "smartctl", "-a", f"/dev/{device}"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"

def parse_smart_data(smart_output):
    """Parse SMART output with separate paths for SATA, SAS, and NVMe"""
    results = defaultdict(lambda: "N/A")
    
    # Determine drive type
    drive_type = "SATA"  # Default to SATA
    if "NVMe" in smart_output or "Namespace" in smart_output:
        drive_type = "NVMe"
    elif "SAS" in smart_output or "SCSI" in smart_output:
        drive_type = "SAS"
    results['drive_type'] = drive_type
    
    # Extract health status based on drive type
    if drive_type == "SAS":
        # SAS-specific health status
        health_match = re.search(r"SMART Health Status:\s*(\w+)", smart_output)
        health_status = health_match.group(1) if health_match else "UNKNOWN"
        # Convert "OK" to "PASSED" for consistency
        results['health_status'] = "PASSED" if health_status == "OK" else health_status
    else:
        # Standard health status for other drives
        health_match = re.search(
            r"SMART overall-health self-assessment test result:\s*(\w+)", 
            smart_output
        )
        results['health_status'] = health_match.group(1) if health_match else "UNKNOWN"
    
    # Extract Power_On_Hours using SMART ID 9 for all drive types
    hours_match = re.search(r"9\s+Power_On_Hours\s+.*?-\s+(\d+)", smart_output)
    if hours_match:
        results['power_on_hours'] = int(hours_match.group(1))
    else:
        # Fallback to other patterns
        hours_match = re.search(r"Power_?On_?Hours[:\s]*([\d,]+)", smart_output, re.IGNORECASE)
        if hours_match:
            hours_str = hours_match.group(1).replace(',', '')
            results['power_on_hours'] = int(hours_str)
        else:
            # Try alternative pattern for current power on hours
            hours_match = re.search(r"Accumulated power on time.*?(\d+):\d+", smart_output, re.IGNORECASE)
            if hours_match:
                results['power_on_hours'] = int(hours_match.group(1))
            else:
                results['power_on_hours'] = "N/A"
    
    # Drive type specific parsing
    if drive_type == "NVMe":
        # NVMe-specific patterns
        media_errors_match = re.search(r"Media and Data Integrity Errors:\s*(\d+)", smart_output)
        error_log_match = re.search(r"Error Information Log Entries:\s*(\d+)", smart_output)
        
        results['media_errors'] = int(media_errors_match.group(1)) if media_errors_match else 0
        results['error_log_entries'] = int(error_log_match.group(1)) if error_log_match else 0
        
    elif drive_type == "SAS":
        # SAS-specific patterns
        read_match = re.search(r"read:\s+.*?\s+(\d+)$", smart_output, re.MULTILINE)
        write_match = re.search(r"write:\s+.*?\s+(\d+)$", smart_output, re.MULTILINE)
        verify_match = re.search(r"verify:\s+.*?\s+(\d+)$", smart_output, re.MULTILINE)
        
        # Improved grown defects detection with fallback
        grown_defects_match = re.search(r"Elements in grown defect list:\s*(\d+)", smart_output)
        if not grown_defects_match:
            # Alternative pattern for some SAS drives
            grown_defects_match = re.search(r"grown defect list:\s*(\d+)", smart_output)
        results['grown_defects'] = int(grown_defects_match.group(1)) if grown_defects_match else 0
        
        # Parse corrected errors
        read_corrected = re.search(r"read:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", smart_output)
        write_corrected = re.search(r"write:\s+(\极d+)\s+(\d+)\s+(\d+)\s+(\d+)", smart_output)
        verify_corrected = re.search(r"verify:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", smart_output)
        
        results['read_corrected'] = int(read_corrected.group(4)) if read_corrected else 0
        results['write_corrected'] = int(write_corrected.group(4)) if write_corrected else 0
        results['verify_corrected'] = int(verify_corrected.group(4)) if verify_corrected else 0
        
        results['read_errors'] = int(read_match.group(1)) if read_match else 0
        results['write_errors'] = int(write_match.group(1)) if write_match else 0
        results['verify_errors'] = int(verify_match.group(1)) if verify_match else 0
        
    else:  # SATA
        # SATA-specific patterns using SMART IDs
        patterns = {
            'raw_read_error_rate': r"1\s+Raw_Read_Error_Rate.*?\s+\d+\s+\d+\s+\d+\s+\S+\s+\S+\s+-\s+(\d+)",
            'seek_error_rate': r"7\s+Seek_Error_Rate.*?\s+\d+\s+\d+\s+\d+\s+\S+\s+\S+\s+-\s+(\d+)",
            'offline_uncorrectable': r"198\s+Offline_Uncorrectable.*?\s+\d+\s+\d+\s+\d+\s+\S+\s+\S+\s+-\s+(\d+)",
            'udma_crc_error_count': r"199\s+UDMA_CRC_Error_Count.*?\s+\d+\s+\d+\s+\d+\s+\S+\s+\S+\s+-\s+(\d+)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, smart_output)
            results[key] = int(match.group(1)) if match else 0
    
    # Improved test log parsing for all drive types
    test_log_match = re.search(
        r"#\s*1\s+([\w\s]+?)\s+(\w+(?:\s+\w+)?)\s+.*?(\d+)\s",
        smart_output,
        re.MULTILINE
    )
    
    if test_log_match:
        results['last_test'] = {
            'description': test_log_match.group(1).strip(),
            'status': test_log_match.group(2).strip(),
            'lifetime_hours': int(test_log_match.group(3))
        }
    else:
        # Try alternative pattern for test logs with different formats
        alt_test_match = re.search(
            r"#\s*1\s+([\w\s]+?)\s+(\w+).*?(\d+)\s",
            smart_output,
            re.MULTILINE
        )
        if alt_test_match:
            results['last_test'] = {
                'description': alt_test_match.group(1).strip(),
                'status': alt_test_match.group(2).strip(),
                'lifetime_hours': int(alt_test_match.group(3))
            }
        else:
            # Fallback to NVMe pattern
            nvme_test_match = re.search(
                r"Self-test execution status:\s+\(\s*\d+\)\s+(.*?)\n",
                smart_output
            )
            if nvme_test_match:
                results['last_test'] = {
                    'description': "Self-test",
                    'status': nvme_test_match.group(1).strip(),
                    'lifetime_hours': results.get('power_on_hours', 'N/A')
                }
            else:
                results['last极test'] = {
                    'description': 'N/A',
                    'status': 'N/A',
                    'lifetime_hours': 'N/A'
                }
    
    return dict(results)

def format_time_ago(current_hours, test_hours):
    """Format time since last test"""
    if current_hours == "N/A" or test_hours == "N/A":
        return "N/A"
    
    hours_ago = current_hours - test_hours
    if hours_ago < 24:
        return f"{hours_ago} hours ago"
    
    days_ago = hours_ago // 24
    return f"{days_ago} days ago"

def calculate_days_since(current_hours, test_hours):
    """Calculate days since last test"""
    if current_hours == "N/A" or test_hours == "N/A" or not isinstance(current_hours, int) or not isinstance(test_hours, int):
        return "N/A"
    
    hours_ago = current_hours - test_hours
    if hours_ago < 0:
        return "N/A"
    
    return hours_ago / 24

def main():
    parser = argparse.ArgumentParser(description='Disk Mapper with JSON export')
    parser.add_argument('--json', type=str, help='Path to output JSON file')
    args = parser.parse_args()
    
    # Fetch pool and disk data
    try:
        pool_data = json.loads(subprocess.check_output(["midclt", "call", "pool.query"]))
        disk_data = json.loads(subprocess.check_output(["midclt", "call", "disk.query"]))
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error fetching data: {str(e)}")
        return

    # Create disk lookup tables
    guid_to_disk = {}
    devname_to_disk = {}
    for disk in disk_data:
        if disk.get('zfs_guid'):
            guid_to_disk[str(disk['zfs_guid'])] = disk
        if disk.get('devname'):
            devname_to_disk[disk['devname']] = disk
        # Also index by gptid if available
        if disk.get('name') and disk['name'].startswith('gptid/'):
            devname_to_disk[disk['name'][6:]] = disk

    # Process each pool
    for pool in pool_data:
        pool_name = pool.get('name', 'UNKNOWN')
        print(f"\n\033[1;36m{' POOL: ' + pool_name + ' ':=^80}\033[0m")
        
        # Create pool entry for JSON
        pool_entry = {
            "name": pool_name,
            "vdevs": []
        }
        json_output["pools"].append(pool_entry)
        
        # Process topology sections
        topology = pool.get('topology', {})
        for vdev_type, vdev_list in topology.items():
            for vdev in vdev_list:
                process_vdev(vdev, vdev_type, guid_to_disk, devname_to_disk, pool_entry)

    # Save JSON output if requested
    if args.json:
        try:
            with open(args.json, 'w') as f:
                json.dump(json_output, f, indent=4)
            print(f"\n\033[1;32mJSON output saved to {args.json}\033[0m")
        except Exception as e:
            print(f"\n\033[1;31mError saving JSON: {str(e)}\033[0m")

def process_vdev(vdev, vdev_type, guid_to_disk, devname_to_disk, pool_entry, indent=1):
    # Print VDEV header
    vdev_name = vdev.get('name', 'UNKNOWN')
    indent_str = "  " * indent
    print(f"\n{indent_str}\033[1;33mVDEV: {vdev_name} ({vdev_type.upper()})\033[0m")
    print(f"{indent_str}{'-' * 60}")
    
    # Create vdev entry for JSON
    vdev_entry = {
        "name": vdev_name,
        "type": vdev_type,
        "children": []
    }
    pool_entry["vdevs"].append(vdev_entry)
    
    # Process children
    for child in vdev.get('children', []):
        if child.get('type') == 'DISK':
            disk_entry = print_disk(child, guid_to_disk, devname_to_disk, indent + 1)
            vdev_entry["children"].append(disk_entry)
        else:
            # Recursive call for nested vdevs
            process_vdev(child, child.get('type', 'UNKNOWN'), guid_to_disk, devname_to_disk, 
                         vdev_entry, indent + 1)
    
    # Add separator after vdev
    print(f"{indent_str}{'#' * 60}")

def print_disk(disk_child, guid_to_disk, devname_to_disk, indent):
    # Get basic disk info
    part_device = disk_child.get('device', 'UNKNOWN')
    whole_disk = disk_child.get('disk', 'UNKNOWN')
    zfs_guid = disk_child.get('guid', '')
    
    # Find matching disk info
    disk_info = guid_to_disk.get(str(zfs_guid)) or devname_to_disk.get(whole_disk) or {}
    
    # Get stats and errors
    stats = disk_child.get('stats', {})
    read_errors = stats.get('read_errors', 0)
    write_errors = stats.get('write_errors', 0)
    checksum_errors = stats.get('checksum_errors', 0)
    
    errors = f"ZFS Read: \033[1;31m{read_errors}\033[0m, " \
             f"ZFS Write: \033[1;31m{write_errors}\033[0m, " \
             f"ZFS Checksum: \033[1;31m{checksum_errors}\033[0m"
    
    # Format size
    raw_size = disk_info.get('size', 0)
    size_human = convert_size(raw_size) if raw_size else "UNKNOWN"
    
    # Get GPTID
    gptid = "N/A"
    if 'name' in disk_child and disk_child['name']:
        gptid = f"/dev/gptid/{disk_child['name']}"
    elif 'path' in disk_child and 'gptid' in disk_child['path']:
        gptid = disk_child['path']
    
    # Print disk information
    indent_str = "  " * indent
    print(f"{indent_str}\033[1;32mPool Device: /dev/{part_device}\033[0m")
    print(f"{indent_str}├─ ZFS GUID: \033[1;35m{zfs_guid}\033[0m")
    print(f"{indent_str}├─ Physical Disk: /dev/{whole_disk}")
    print(f"{indent_str}├─ Errors: {errors}")
    print(f"{indent_str}├─ Serial: \033[1;34m{disk_info.get('serial', 'UNKNOWN')}\033[0m")
    print(f"{indent_str}├─ Model: {disk_info.get('model', 'UNKNOWN')}")
    print(f"{indent_str}├─ Size: {size_human} ({raw_size} bytes)")
    print(f"{indent_str}└─ GPTID: \033[1;35m{gptid}\033[0m")
    
    # Create disk entry for JSON
    disk_entry = {
        "partition": part_device,
        "disk": whole_disk,
        "zfs_guid": zfs_guid,
        "errors": {
            "read": read_errors,
            "write": write_errors,
            "checksum": checksum_errors
        },
        "serial": disk_info.get('serial', 'UNKNOWN'),
        "model": disk_info.get('model', 'UNKNOWN'),
        "size_bytes": raw_size,
        "size_human": size_human,
        "gptid": gptid,
        "smart_data": None
    }
    
    # Get and parse SMART data
    print(f"{indent_str}{'-' * 60}")
    print(f"{indent_str}\033[1;34mSMART DATA FOR /dev/{whole_disk}:\033[0m")
    
    smart_output = get_smart_data(whole_disk)
    smart_data = parse_smart_data(smart_output) if not smart_output.startswith("Error") else {}
    
    if smart_data:
        # Health status with color coding
        health_status = smart_data.get('health_status', 'UNKNOWN')
        status_color = "\033[1;32m" if health_status == "PASSED" else "\033[1;31m"
        drive_type = smart_data.get('drive_type', 'UNKNOWN')
        power_on_hours = smart_data.get('power_on_hours', 'N/A')
        
        print(f"{indent_str}├─ Drive Type: {drive_type}")
        print(f"{indent_str}├─ Health Status: {status_color}{health_status}\033[0m")
        print(f"{indent_str}├─ Power On Hours: \033[1;33m{power_on_hours}\033[0m")
        
        # Handle different drive types
        if drive_type == "NVMe":
            media_errors = smart_data.get('media_errors', 0)
            error_log_entries = smart_data.get('error_log_entries', 0)
            print(f"{indent_str}├─ Media Integrity Errors: \033[1;31m{media_errors}\033[0m")
            print(f"{indent_str}├─ Error Log Entries: \033[1;31m{error_log_entries}\033[0m")
            
            # Add to JSON
            disk_entry["smart_data"] = {
                "drive_type": drive_type,
                "health_status": health_status,
                "power_on_hours": power_on_hours,
                "media_errors": media_errors,
                "error_log_entries": error_log_entries
            }
            
        elif drive_type == "SAS":
            print(f"{indent_str}├─ Uncorrected Errors:")
            print(f"{indent_str}│  ├─ Read: \033[1;31m{smart_data.get('read_errors', 0)}\033[0m")
            print(f"{indent_str}│  ├─ Write: \033[1;31m{smart_data.get('write_errors', 0)}\033[0m")
            print(f"{indent_str}│  └─ Verify: \033[1;31m{smart_data.get('verify_errors', 0)}\033[0m")
            print(f"{indent_str}├─ Grown Defects: \033[1;31m{smart_data.get('grown_defects', 0)}\033[0m")
            
            # Show corrected errors for SAS drives
            print(f"{indent_str}├─ Corrected Errors:")
            print(f"{indent_str}│  ├─ Read: \033[1;33m{smart_data.get('read_corrected', 0)}\033[0m")
            print(f"{indent_str}│  ├─ Write: \033[1;33m{smart_data.get('write_corrected', 0)}\033[0m")
            print(f"{indent_str}│  └─ Verify: \033[1;33m{smart_data.get('verify_corrected', 0)}\033[0m")
            
            # Add to JSON
            disk_entry["smart_data"] = {
                "drive_type": drive_type,
                "health_status": health_status,
                "power_on_hours": power_on_hours,
                "uncorrected_errors": {
                    "read": smart_data.get('read_errors', 0),
                    "write": smart_data.get('write_errors', 0),
                    "verify": smart_data.get('verify_errors', 0)
                },
                "grown_defects": smart_data.get('grown_defects', 0),
                "corrected_errors": {
                    "read": smart_data.get('read_corrected', 0),
                    "write": smart_data.get('write_corrected', 0),
                    "verify": smart_data.get('verify_corrected', 0)
                }
            }
            
        else:  # SATA
            print(f"{indent_str}├─ SMART Attributes:")
            print(f"{indent_str}│  ├─ Raw Read Error Rate: \033[1;31m{smart_data.get('raw_read_error_rate', 0)}\033[0m")
            print(f"{indent_str}│  ├─ Seek Error Rate: \033[1;31m{smart_data.get('seek_error_rate', 0)}\033[0m")
            print(f"{indent_str}│  ├─ Offline Uncorrectable: \033[1;31m{smart_data.get('offline_uncorrectable', 0)}\033[0m")
            print(f"{indent_str}│  └─ UDMA CRC Error Count: \033[1;31m{smart_data.get('udma_crc_error_count', 0)}\033[0m")
            
            # Add to JSON
            disk_entry["smart_data"] = {
                "drive_type": drive_type,
                "health_status": health_status,
                "power_on_hours": power_on_hours,
                "raw_read_error_rate": smart_data.get('raw_read_error_rate', 0),
                "seek_error_rate": smart_data.get('seek_error_rate', 0),
                "offline_uncorrectable": smart_data.get('offline_uncorrectable', 0),
                "udma_crc_error_count": smart_data.get('udma_crc_error_count', 0)
            }
        
        # Last test information with time ago
        last_test = smart_data.get('last_test', {})
        test_description = last_test.get('description', 'N/A')
        test_status = last_test.get('status', 'N/A')
        test_hours = last_test.get('lifetime_hours', 'N/A')
        
        # Calculate time since test if possible
        time_since = "N/A"
        if power_on_hours != "极N/A" and test_hours != "N/A" and isinstance(power_on_hours, int) and isinstance(test_hours, int):
            time_since = format_time_ago(power_on_hours, test_hours)
        
        print(f"{indent_str}└─ Last Test: \033[1;35m{test_description}\033[0m")
        print(f"{indent_str}   ├─ Status: {test_status}")
        print(f"{indent_str}   ├─ Lifetime Hours: {test_hours}")
        print(f"{indent_str}   └─ Time Since: {time_since}")
        
        # Add last test to JSON
        if disk_entry["smart_data"]:
            disk_entry["smart_data"]["last_test"] = {
                "description": test_description,
                "status": test_status,
                "lifetime_hours": test_hours,
                "time_since": time_since
            }
    else:
        print(f"{indent_str}\033[1;31mSMART data unavailable: {smart_output[:200]}{'...' if len(smart_output) > 200 else ''}\033[0m")
        disk_entry["smart_data"] = {
            "error": smart_output[:200] + ('...' if len(smart_output) > 200 else '')
        }
    
    # Initialize warning variables
    critical_reasons = []
    caution_reasons = []
    slowdown_reasons = []
    test_warning = False
    
    # Check critical conditions (immediate replacement)
    if read_errors > 0 or write_errors > 0 or checksum_errors > 0:
        if read_errors > 0:
            critical_reasons.append(f"ZFS Read errors: {read_errors}")
        if write_errors > 0:
            critical_reasons.append(f"ZFS Write errors: {write_errors}")
        if checksum_errors > 0:
            critical_reasons.append(f"ZFS Checksum errors: {checksum_errors}")
    
    # Check drive-specific critical conditions
    if smart_data:
        drive_type = smart_data.get('drive_type', 'UNKNOWN')
        
        if drive_type == "NVMe":
            media_errors = smart_data.get('media_errors', 0)
            if media_errors > 0:
                critical_reasons.append(f"Media Integrity Errors: {media_errors}")
                
        elif drive_type == "SAS":
            # SAS-specific critical errors
            sas_read_errors = smart_data.get('read_errors', 0)
            sas_write_errors = smart_data.get('write_errors', 0)
            sas_verify_errors = smart_data.get('verify_errors', 0)
            
            if sas_read_errors > 0:
                critical_reasons.append(f"SAS Read Errors: {sas_read_errors}")
            if sas_write_errors > 0:
                critical_reasons.append(f"SAS Write Errors: {sas_write_errors}")
            if sas_verify_errors > 0:
                critical_reasons.append(f"SAS Verify Errors: {sas_verify_errors}")
                
            # Check for critical corrected errors
            read_corrected = smart_data.get('read_corrected', 0)
            write_corrected = smart_data.get('write_corrected', 0)
            verify_corrected = smart_data.get('verify_corrected', 0)
            
            # Critical threshold (>1,000,000)
            if read_corrected > 1000000:
                critical_reasons.append(f"Critical corrected read errors: {read_corrected}")
            if write_corrected > 1000000:
                critical_reasons.append(f"Critical corrected write errors: {write_corrected}")
            if verify_corrected > 1000000:
                critical_reasons.append(f"Critical corrected verify errors: {verify_corrected}")
                
            # Performance threshold (>100,000)
            if read_corrected > 100000:
                slowdown_reasons.append(f"Corrected read errors: {read_corrected}")
            if write_corrected > 100000:
                slowdown_reasons.append(f"Corrected write errors: {write_corrected}")
            if verify_corrected > 100000:
                slowdown_reasons.append(f"Corrected verify errors: {verify_corrected}")
                
            # Caution threshold (>10,000)
            if 10000 < read_corrected <= 100000:
                caution_reasons.append(f"Corrected read errors: {read_corrected}")
            if 10000 < write_corrected <= 100000:
                caution_reasons.append(f"Corrected write errors: {write_corrected}")
            if 10000 < verify_corrected <= 100000:
                caution_reasons.append(f"Corrected verify errors: {verify_corrected}")
                
            # Grown defects as caution
            grown_defects = smart_data.get('grown_defects', 0)
            if grown_defects > 0:
                caution_reasons.append(f"Grown Defects: {grown_defects}")
                
        else:  # SATA
            # SATA-specific critical errors
            offline_uncorrect = smart_data.get('offline_uncorrectable', 0)
            if offline_uncorrect > 0:
                critical_reasons.append(f"Offline Uncorrectable: {offline_uncorrect}")
            
            # Check caution conditions for the other attributes
            raw_read = smart_data.get('raw_read_error_rate', 0)
            seek = smart_data.get('seek_error_rate', 0)
            udma = smart_data.get('udma_crc_error_count', 0)
            
            if raw_read > 0 and not critical_reasons:
                caution_reasons.append(f"Raw Read Error Rate: {raw_read}")
            if seek > 0 and not critical_reasons:
                caution_reasons.append(f"Seek Error Rate: {seek}")
            if udma > 0 and not critical_reasons:
                caution_reasons.append(f"UDMA CRC Error Count: {udma}")
    
    # Check caution conditions (monitor closely)
    if smart_data:
        drive_type = smart_data.get('drive_type', 'UNKNOWN')
        
        if drive_type == "NVMe":
            error_log_entries = smart_data.get('error_log_entries', 0)
            if error_log_entries > 0 and not critical_reasons:
                caution_reasons.append(f"Error Log Entries: {error_log_entries}")
                
        elif drive_type == "SAS":
            # Already handled above
            pass
                
        else:  # SATA
            # SATA-specific caution conditions
            sata_read_errors = smart_data.get('read_errors', 0)
            sata_write_errors = smart_data.get('write_errors', 0)
            sata_verify_errors = smart_data.get('verify_errors', 0)
            
            if (0 < sata_read_errors <= 10) and not critical_reasons:
                caution_reasons.append(f"SATA Read Errors: {sata_read_errors}")
            if (0 < sata_write_errors <= 10) and not critical_reasons:
                caution_reasons.append(f"SATA Write Errors: {sata_write_errors}")
            if (0 < sata_verify_errors <= 10) and not critical_reasons:
                caution_reasons.append(f"SATA Verify Errors: {sata_verify_errors}")
    
    # Check for old SMART test (for all drive types)
    if smart_data and not critical_reasons:
        last_test = smart_data.get('last_test', {})
        test_status = last_test.get('status', '')
        test_hours = last_test.get('lifetime_hours', 'N/A')
        power_on_hours = smart_data.get('power_on_hours', 'N/A')
        
        # Only proceed if test completed successfully
        if test_status and ('completed' in test_status.lower() or 'success' in test_status.lower()):
            days_since = calculate_days_since(power_on_hours, test_hours)
            if isinstance(days_since, float) and days_since > 60:
                test_warning = True
                caution_reasons.append(f"Last SMART test was {int(days_since)} days ago - recommend running a new test")
    
    # Add warnings to JSON
    disk_entry["warnings"] = {
        "critical": critical_reasons,
        "caution": caution_reasons,
        "slowdown": slowdown_reasons,
        "test_warning": test_warning
    }
    
    # Print warnings if needed
    if critical_reasons:
        warning_box = [
            "************************************************************",
            "\033[1;31mCRITICAL WARNING: THIS DISK SHOULD BE REPLACED IMMEDIATELY!\033[0m",
            "Reasons:"
        ]
        warning_box.extend([f"  • {reason}" for reason in critical_reasons])
        warning_box.append("************************************************************")
        
        print(f"\n{indent_str}")
        for line in warning_box:
            print(f"{indent_str}{line}")
    
    elif caution_reasons:
        warning_box = [
            "------------------------------------------------------------",
            "\033[1;33mCAUTION: MONITOR THIS DRIVE CLOSELY\033[0m",
            "The disk shows some errors but doesn't appear to be failing yet:"
        ]
        warning_box.extend([f"  • {reason}" for reason in caution_reasons])
        warning_box.append("Recommendations:")
        warning_box.append("  • Monitor SMART attributes regularly")
        if test_warning:
            warning_box.append("  • Run a new SMART short test")
        warning_box.append("------------------------------------------------------------")
        
        print(f"\n{indent_str}")
        for line in warning_box:
            print(f"{indent_str}{line}")
    
    # Print slowdown warnings for SAS with new format
    if slowdown_reasons:
        slowdown_box = [
            "------------------------------------------------------------",
            "\033[1;33mPERFORMANCE WARNING: DRIVE MAY BE SLOWING DOWN ITS VDEV\033[0m",
            "High error correction rates may be impacting performance:",
            "For some drive models and firmwares, higher numbers may be part of \"normal\" operation. ",
        ]
        slowdown_box.extend([f"  • {reason}" for reason in slowdown_reasons])
        slowdown_box.append("Recommendations:")
        slowdown_box.append("  • Consider replacing this drive")
        slowdown_box.append("  • Monitor vdev performance metrics")
        slowdown_box.append("------------------------------------------------------------")
        
        print(f"\n{indent_str}")
        for line in slowdown_box:
            print(f"{indent_str}{line}")
    
    # Add separator
    print(f"{indent_str}{'.' * 60}")
    
    return disk_entry

if __name__ == "__main__":
    main()
