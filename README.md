# ZFS Disk Mapper & SMART Analyzer


### A Python script that maps ZFS pool hierarchy, analyzes disk SMART attributes, and provides health warnings for TrueNAS systems.

## Features
Pool Visualization: Maps ZFS pool hierarchy showing vdevs and disks

SMART Analysis: Retrieves and parses SMART data for SATA, SAS, and NVMe drives

Health Assessment: Provides warnings based on specified paramaters.

## Alerting Parameters

### SAS

| Condition                          | Drive Type | Threshold     | Severity    |
|------------------------------------|------------|---------------|-------------|
| Uncorrected Read/Write/Verify      | SAS        | >0            | Critical    |
| Corrected Errors                   | SAS        | >1,000,000    | Critical    |
| Corrected Errors                   | SAS        | >100,000      | Performance |
| Corrected Errors                   | SAS        | >10,000       | Caution     |
| Grown Defects                      | SAS        | >0            | Caution     |

### SATA

| Condition              | Drive Type | Threshold | Severity |
|------------------------|------------|-----------|----------|
| Offline Uncorrectable  | SATA       | >0        | Critical |
| Raw Read Error Rate    | SATA       | >0        | Caution  |
| Seek Error Rate        | SATA       | >0        | Caution  |

### NVMe

| Condition       | Drive Type | Threshold | Severity |
|-----------------|------------|-----------|----------|
| Media Errors    | NVMe       | >0        | Critical |
| Error Log Entries | NVMe     | >0        | Caution  |

### Any

| Condition                      | Drive Type | Threshold | Severity |
|--------------------------------|------------|-----------|----------|
| ZFS Read/Write/Checksum Errors | Any        | >0        | Critical |
| Days Since Last Test (On Supported drive)           | Any        | >60       | Caution  |


## Requirements
TrueNAS SCALE/CE
Python 3.x
smartmontools package installed (smartctl command)
Root privileges (for SMART data access)

## Installation
Place the script on your TrueNAS system:
```git clone https://raw.githubusercontent.com/nickf1227/tn-disk-info/main/diskmapper.py```

## Usage
Basic Usage (Console Output)
```sudo python3 diskmapper.py```
Export Results to JSON
```sudo python3 diskmapper.py --json /path/to/output.json```

## Screenshot
![image](https://github.com/user-attachments/assets/da1b0758-7a65-4a09-8355-ed3aa0abe3d3)


## Example Output (SAS)
```
================================== POOL: ice ===================================

  VDEV: raidz2-0 (DATA)
  ------------------------------------------------------------
    Pool Device: /dev/sdm1
    ├─ ZFS GUID: 5227492984876952151
    ├─ Physical Disk: /dev/sdm
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDPS6L
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/d1a41189-604a-44ec-9faf-88d10e8e7eea
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdm:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 37363
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 37227
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdl1
    ├─ ZFS GUID: 1890505091264157917
    ├─ Physical Disk: /dev/sdl
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHD4V0L
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/fbce79d0-6db2-41ea-b83d-d86090d62814
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdl:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41889
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 2
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdac1
    ├─ ZFS GUID: 15641419920947187991
    ├─ Physical Disk: /dev/sdac
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHE35SL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/ab738ba2-7291-4e9b-beb3-6cbca0917f60
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdac:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 4
    │  ├─ Write: 1
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41623
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdf1
    ├─ ZFS GUID: 7980293907302437342
    ├─ Physical Disk: /dev/sdf
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHD06XL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/920d1d04-8f3f-452b-87c2-8e4d9f71c5aa
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdf:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41887
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 41
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41751
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdai1
    ├─ ZFS GUID: 9631990446359566766
    ├─ Physical Disk: /dev/sdai
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHBHYGL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/77429595-9454-4152-9ba5-5fecbd8af598
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdai:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 1082
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41622
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdo1
    ├─ ZFS GUID: 9383799614074970413
    ├─ Physical Disk: /dev/sdo
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDRYYL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/cf4ede22-0b39-4ad1-a0be-51e974a96be7
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdo:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41888
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 1
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41752
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdal1
    ├─ ZFS GUID: 480631239828802416
    ├─ Physical Disk: /dev/sdal
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDBDXL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/4bf26bfe-3e20-4d24-add0-f367ae74e3f9
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdal:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 3
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41622
       └─ Time Since: 5 days ago
    ............................................................
  ############################################################
```

## Example Output SATA

```
root@truenas[/home/truenas_admin]# python3 diskmap.py

================================= POOL: vault ==================================

  VDEV: raidz1-0 (DATA)
  ------------------------------------------------------------
    Pool Device: /dev/sda1
    ├─ ZFS GUID: 11807597651784319308
    ├─ Physical Disk: /dev/sda
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: JEKX0SPZ
    ├─ Model: WDC_WD100EMAZ-00WJTA0
    ├─ Size: 9.1 TiB (10000831348736 bytes)
    └─ GPTID: /dev/gptid/55eee86c-6b90-49c8-99b9-f2d81613b629
    ------------------------------------------------------------
    SMART DATA FOR /dev/sda:
    ├─ Drive Type: SATA
    ├─ Health Status: PASSED
    ├─ Power On Hours: 32886
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 30950
       └─ Time Since: 80 days ago


    ------------------------------------------------------------
    CAUTION: MONITOR THIS DRIVE CLOSELY
he disk shows some errors but doesn't appear to be failing yet:
      • Last SMART test was 80 days ago - recommend running a new test
    Recommendations:
      • Monitor SMART attributes regularly
      • Run a new SMART short test
    ------------------------------------------------------------
    ............................................................
    Pool Device: /dev/sdb1
    ├─ ZFS GUID: 12912970852056213168
    ├─ Physical Disk: /dev/sdb
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: 7JJ9BZKC
    ├─ Model: WDC_WD101KRYZ-01JPDB1
    ├─ Size: 9.1 TiB (10000831348736 bytes)
    └─ GPTID: /dev/gptid/4002c52e-5860-4897-a242-e65157f05864
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdb:
    ├─ Drive Type: SATA
    ├─ Health Status: PASSED
    ├─ Power On Hours: 53487
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 51883
       └─ Time Since: 66 days ago


    ------------------------------------------------------------
    CAUTION: MONITOR THIS DRIVE CLOSELY
he disk shows some errors but doesn't appear to be failing yet:
      • Last SMART test was 66 days ago - recommend running a new test
    Recommendations:
      • Monitor SMART attributes regularly
      • Run a new SMART short test
    ------------------------------------------------------------
    ............................................................
    Pool Device: /dev/sdc1
    ├─ ZFS GUID: 6061726270598089927
    ├─ Physical Disk: /dev/sdc
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: 7JJD9B7C
    ├─ Model: WDC_WD101KRYZ-01JPDB1
    ├─ Size: 9.1 TiB (10000831348736 bytes)
    └─ GPTID: /dev/gptid/a006ac63-3545-4252-8a5f-14f8a0b5d27a
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdc:
    ├─ Drive Type: SATA
    ├─ Health Status: PASSED
    ├─ Power On Hours: 53312
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 51708
       └─ Time Since: 66 days ago


    ------------------------------------------------------------
    CAUTION: MONITOR THIS DRIVE CLOSELY
he disk shows some errors but doesn't appear to be failing yet:
      • Last SMART test was 66 days ago - recommend running a new test
    Recommendations:
      • Monitor SMART attributes regularly
      • Run a new SMART short test
    ------------------------------------------------------------
    ............................................................
    Pool Device: /dev/sdd1
    ├─ ZFS GUID: 9113497765191841136
    ├─ Physical Disk: /dev/sdd
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: 7JJAP2NC
    ├─ Model: WDC_WD101KRYZ-01JPDB1
    ├─ Size: 9.1 TiB (10000831348736 bytes)
    └─ GPTID: /dev/gptid/529885d0-aed6-4287-9e37-77172dbb514c
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdd:
    ├─ Drive Type: SATA
    ├─ Health Status: PASSED
    ├─ Power On Hours: 50971
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 46577
       └─ Time Since: 183 days ago


    ------------------------------------------------------------
    CAUTION: MONITOR THIS DRIVE CLOSELY
he disk shows some errors but doesn't appear to be failing yet:
      • Last SMART test was 183 days ago - recommend running a new test
    Recommendations:
      • Monitor SMART attributes regularly
      • Run a new SMART short test
    ------------------------------------------------------------
    ............................................................
  ############################################################
```

## Example Output NVME


```
root@prod:~# python3 diskmaps.py

================================ POOL: inferno =================================

  VDEV: raidz1-0 (DATA)
  ------------------------------------------------------------
    Pool Device: /dev/nvme0n1p1
    ├─ ZFS GUID: 212601209224793468
    ├─ Physical Disk: /dev/nvme0n1
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: PHM29081000X960CGN
    ├─ Model: INTEL SSDPE21D960GA
    ├─ Size: 894.25 GiB (960197124096 bytes)
    └─ GPTID: /dev/gptid/312852f6-50ed-4365-adda-ef6316578b66
    ------------------------------------------------------------
    SMART DATA FOR /dev/nvme0n1:
    ├─ Drive Type: NVMe
    ├─ Health Status: PASSED
    ├─ Power On Hours: N/A
    ├─ Media Integrity Errors: 0
    ├─ Error Log Entries: 0
    └─ Last Test: N/A
       ├─ Status: N极/A
       ├─ Lifetime Hours: N/A
       └─ Time Since: N/A
    ............................................................
    Pool Device: /dev/nvme5n1p1
    ├─ ZFS GUID: 10743034860780890768
    ├─ Physical Disk: /dev/nvme5n1
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: PHM2908101QG960CGN
    ├─ Model: INTEL SSDPE21D960GA
    ├─ Size: 894.25 GiB (960197124096 bytes)
    └─ GPTID: /dev/gptid/0072df54-2228-4138-a18b-b3989174a72c
    ------------------------------------------------------------
    SMART DATA FOR /dev/nvme5n1:
    ├─ Drive Type: NVMe
    ├─ Health Status: PASSED
    ├─ Power On Hours: N/A
    ├─ Media Integrity Errors: 0
    ├─ Error Log Entries: 0
    └─ Last Test: N/A
       ├─ Status: N极/A
       ├─ Lifetime Hours: N/A
       └─ Time Since: N/A
    ............................................................
    Pool Device: /dev/nvme2n1p1
    ├─ ZFS GUID: 11750420763846093416
    ├─ Physical Disk: /dev/nvme2n1
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: PHM2913000DC960CGN
    ├─ Model: INTEL SSDPE21D960GA
    ├─ Size: 894.25 GiB (960197124096 bytes)
    └─ GPTID: /dev/gptid/a4d0b29d-d652-4dd4-a030-3d3a534dc066
    ------------------------------------------------------------
    SMART DATA FOR /dev/nvme2n1:
    ├─ Drive Type: NVMe
    ├─ Health Status: PASSED
    ├─ Power On Hours: N/A
    ├─ Media Integrity Errors: 0
    ├─ Error Log Entries: 0
    └─ Last Test: N/A
       ├─ Status: N极/A
       ├─ Lifetime Hours: N/A
       └─ Time Since: N/A
    ............................................................
    Pool Device: /dev/nvme3n1p1
    ├─ ZFS GUID: 16221756077833732578
    ├─ Physical Disk: /dev/nvme3n1
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: PHM2913000QM960CGN
    ├─ Model: INTEL SSDPE21D960GA
    ├─ Size: 894.25 GiB (960197124096 bytes)
    └─ GPTID: /dev/gptid/0ff1c64b-cacf-4c86-be99-124426875d75
    ------------------------------------------------------------
    SMART DATA FOR /dev/nvme3n1:
    ├─ Drive Type: NVMe
    ├─ Health Status: PASSED
    ├─ Power On Hours: N/A
    ├─ Media Integrity Errors: 0
    ├─ Error Log Entries: 5
    └─ Last Test: N/A
       ├─ Status: N极/A
       ├─ Lifetime Hours: N/A
       └─ Time Since: N/A


    ------------------------------------------------------------
    CAUTION: MONITOR THIS DRIVE CLOSELY
    The disk shows some errors but doesn't appear to be failing yet:
      • Error Log Entries: 5
    Recommendations:
      • Monitor SMART attributes regularly
    ------------------------------------------------------------
    ............................................................
    Pool Device: /dev/nvme1n1p1
    ├─ ZFS GUID: 8625327235819249102
    ├─ Physical Disk: /dev/nvme1n1
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: PHM2913000YF960CGN
    ├─ Model: INTEL SSDPE21D960GA
    ├─ Size: 894.25 GiB (960197124096 bytes)
    └─ GPTID: /dev/gptid/8ede0d57-adbb-49a2-9715-6255b2eb8e88
    ------------------------------------------------------------
    SMART DATA FOR /dev/nvme1n1:
    ├─ Drive Type: NVMe
    ├─ Health Status: PASSED
    ├─ Power On Hours: N/A
    ├─ Media Integrity Errors: 0
    ├─ Error Log Entries: 0
    └─ Last Test: N/A
       ├─ Status: N极/A
       ├─ Lifetime Hours: N/A
       └─ Time Since: N/A
    ............................................................
  ############################################################
```
