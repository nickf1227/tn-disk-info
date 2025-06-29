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


## Alerting Parameters...cont

### If there are fields that are missing or thresholds that should be modified, PRs and dicussion are welcome. 

### A Bit more on Corrected Errors:
#### These thresholds are somewhat arbitrary. My polstulation is based on these assumptions.

*When the drive has to correct errors, it may take extra time to read or write the data. This can lead to increased latency and reduced throughput. In a ZFS vdev (which is typically a group of drives working together), a single slow drive can slow down the entire vdev because ZFS waits for all drives to complete the operation. This may be especially painful or obvious during a scrub.*

#### However this Dell document, Last Modified: 01 May 2025 contraindicates that assumption, so I will welcome any feedback. I have seen evidence, real and anecdotal, that support both of these positions. 

*The SMART specification allows vendors to provide these counters, such as the ones shown in the above example, for informational purposes. The counters are not necessarily a count of soft or hard faults within the ECC logic. This allows each drive vendor flexibility as to what is displayed in the available SMART fields. For some vendors, no error data is in the ECC read or verify categories. In the example above, the vendor has chosen to use the counters for monitoring the ECC functionality. The values which are presented do not represent an error-rate. Similarly, a higher rate of events on some disks in comparison to others does not indicate that a performance problem exists.*

#### https://www.dell.com/support/kbdoc/en-us/000147878/excessive-smart-error-rates-logged-for-read-and-verify-ecc-errors-on-certain-enterprise-hard-drives

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
