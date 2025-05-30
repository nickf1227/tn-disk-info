# ZFS Disk Mapper & SMART Analyzer


### A Python script that maps ZFS pool hierarchy, analyzes disk SMART attributes, and provides health warnings for TrueNAS systems.

## Features
Pool Visualization: Maps ZFS pool hierarchy showing vdevs and disks

SMART Analysis: Retrieves and parses SMART data for SATA, SAS, and NVMe drives

Health Assessment: Provides warnings based on specified paramaters.

## Alerting Parameters

| Condition                          | Drive Type | Threshold     | Severity      |
|------------------------------------|------------|---------------|---------------|
| Offline Uncorrectable              | SATA       | >0            | Critical      |
| Media Errors                       | NVMe       | >0            | Critical      |
| Uncorrected Read/Write/Verify      | SAS        | >0            | Critical      |
| ZFS Read/Write/Checksum Errors     | Any        | >0            | Critical      |
| Corrected Errors                   | SAS        | >1,000,000    | Critical      |
| Corrected Errors                   | SAS        | >100,000      | Performance   |
| Raw Read Error Rate                | SATA       | >0            | Caution       |
| Seek Error Rate                    | SATA       | >0            | Caution       |
| Error Log Entries                  | NVMe       | >0            | Caution       |
| Grown Defects                      | SAS        | >0            | Caution       |
| Days Since Last Test               | Any        | >60           | Caution       |

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

  VDEV: raidz2-1 (DATA)
  ------------------------------------------------------------
    Pool Device: /dev/sds1
    ├─ ZFS GUID: 12468174715504800729
    ├─ Physical Disk: /dev/sds
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDXDVL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/b12c53b4-a32a-4cde-a835-dce039199fa3
    ------------------------------------------------------------
    SMART DATA FOR /dev/sds:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 38
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdz1
    ├─ ZFS GUID: 12575810268036164475
    ├─ Physical Disk: /dev/sdz
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHE4BDL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/8fb5d904-dd5c-494a-9d75-e8fe155a89bc
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdz:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41760
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 380
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41623
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdi1
    ├─ ZFS GUID: 8709587202117841210
    ├─ Physical Disk: /dev/sdi
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDRZEL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/2f8b9428-915a-4109-826f-0dd2c039b7bd
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdi:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41888
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 5
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41751
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdag1
    ├─ ZFS GUID: 12420098536708636925
    ├─ Physical Disk: /dev/sdag
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHE4AEL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/e28b0363-8d27-4d75-8eff-d73054f6b4e8
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdag:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41760
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 13
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41624
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdaf1
    ├─ ZFS GUID: 6248787858642409255
    ├─ Physical Disk: /dev/sdaf
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHAHSEL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/c81992e2-3315-47ce-b839-cabef787a5c2
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdaf:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
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
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdah1
    ├─ ZFS GUID: 7064277241025105086
    ├─ Physical Disk: /dev/sdah
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH0LL4L
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/03d3709f-43d5-4d43-aada-c49dda1246e8
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdah:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 5
    │  ├─ Write: 2
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41623
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdu1
    ├─ ZFS GUID: 8435778198864465328
    ├─ Physical Disk: /dev/sdu
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAGU6KLL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/8acc8ce0-99d0-4e1d-b2a3-8f55d45fc963
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdu:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
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
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
  ############################################################

  VDEV: raidz2-2 (DATA)
  ------------------------------------------------------------
    Pool Device: /dev/sdak1
    ├─ ZFS GUID: 15395414914633738779
    ├─ Physical Disk: /dev/sdak
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH4T4TL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/af36fe9c-18c8-4c01-b9e4-991d13f8bfb4
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdak:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 17
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41622
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdw1
    ├─ ZFS GUID: 241834966907461809
    ├─ Physical Disk: /dev/sdw
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH7T9BL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/374f6b0c-cbea-4597-b44d-5b91a3410e15
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdw:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 34
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdaa1
    ├─ ZFS GUID: 3357271669658868424
    ├─ Physical Disk: /dev/sdaa
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH7B0EL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/5eaa2d45-3fb7-42d6-af1b-8a561ca56169
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdaa:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 77
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41623
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdr1
    ├─ ZFS GUID: 663480060468884393
    ├─ Physical Disk: /dev/sdr
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHD99LL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/127afe09-e10d-4884-aed3-eeac99f82be0
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdr:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
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
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdae1
    ├─ ZFS GUID: 12084474217870916236
    ├─ Physical Disk: /dev/sdae
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHD4UXL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/044cfd82-3ab0-4378-abff-d4952e0515f9
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdae:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 10
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41623
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdd1
    ├─ ZFS GUID: 2415210037473635969
    ├─ Physical Disk: /dev/sdd
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH7XX5L
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/57ebb7ea-e7f3-43dd-9445-bca31a60cb4d
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdd:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41888
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
       ├─ Lifetime Hours: 41751
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdad1
    ├─ ZFS GUID: 2321010819975352589
    ├─ Physical Disk: /dev/sdad
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH73TVL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/3aff0510-28d5-4e78-bf7c-c675941217ad
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdad:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
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
       ├─ Lifetime Hours: 41622
       └─ Time Since: 5 days ago
    ............................................................
  ############################################################

  VDEV: raidz2-3 (DATA)
  ------------------------------------------------------------
    Pool Device: /dev/sdv1
    ├─ ZFS GUID: 6447577595542961760
    ├─ Physical Disk: /dev/sdv
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHD4XTL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/ddf9473c-48ff-4f5a-9af9-f367ca80c182
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdv:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 6
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdaj1
    ├─ ZFS GUID: 10666041267281724571
    ├─ Physical Disk: /dev/sdaj
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHE7BGL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/60f1dc27-041d-46de-9970-c8d0906edeb2
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdaj:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41759
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 14
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41623
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sde1
    ├─ ZFS GUID: 6453720879157404243
    ├─ Physical Disk: /dev/sde
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDPGUL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/bba518e0-1c32-422d-ac9e-1d2a4275c9ea
    ------------------------------------------------------------
    SMART DATA FOR /dev/sde:
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
       ├─ Lifetime Hours: 41751
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdq1
    ├─ ZFS GUID: 4320819603845537000
    ├─ Physical Disk: /dev/sdq
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAGEAVDL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/d645a548-b228-4470-99e5-fed51aff3d4b
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdq:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41888
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
       ├─ Lifetime Hours: 41752
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdx1
    ├─ ZFS GUID: 2629839678881986450
    ├─ Physical Disk: /dev/sdx
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHD4ZUL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/be798ef3-bb11-4546-b0b0-109e044f3188
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdx:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 31
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdab1
    ├─ ZFS GUID: 11464489017973229028
    ├─ Physical Disk: /dev/sdab
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHE4AJL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/cfe17d9e-3db9-4863-a979-a3ba7ddc7425
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdab:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
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
    Pool Device: /dev/sdg1
    ├─ ZFS GUID: 2650944322410844617
    ├─ Physical Disk: /dev/sdg
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH5W6PL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/c2dfee62-4936-4c5f-a957-66994b075454
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdg:
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
       ├─ Lifetime Hours: 41752
       └─ Time Since: 5 days ago
    ............................................................
  ############################################################

  VDEV: raidz2-4 (DATA)
  ------------------------------------------------------------
    Pool Device: /dev/sdt1
    ├─ ZFS GUID: 12194731234089258709
    ├─ Physical Disk: /dev/sdt
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAH751XL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/a0823ea8-1a73-4d18-907b-3f0d97d5dccb
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdt:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 127
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41754
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdj1
    ├─ ZFS GUID: 16530722200458359384
    ├─ Physical Disk: /dev/sdj
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHE1J1L
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/25b6416c-1e6f-4949-9066-2ce1f5105a5a
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdj:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41888
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 5
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41752
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdy1
    ├─ ZFS GUID: 10368835707209052527
    ├─ Physical Disk: /dev/sdy
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: 2TGU89UD
    ├─ Model: HUH721010AL42C0
    ├─ Size: 9.1 TiB (10000831348736 bytes)
    └─ GPTID: /dev/gptid/2c279d59-6b1b-47cd-a3a2-2e1f694035ac
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdy:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 48228
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 1122
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: N/A
       ├─ Status: N极/A
       ├─ Lifetime Hours: N/A
       └─ Time Since: N/A
    ............................................................
    Pool Device: /dev/sdp1
    ├─ ZFS GUID: 2813416134184314367
    ├─ Physical Disk: /dev/sdp
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDHLVL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/a6a003a5-dcbd-4693-a990-d94e2627dbe3
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdp:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41889
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
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdn1
    ├─ ZFS GUID: 4070674839367337299
    ├─ Physical Disk: /dev/sdn
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDEEEL
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/34cfb707-8d83-461b-86e1-4689ca42440e
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdn:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41890
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
       ├─ Lifetime Hours: 41753
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdk1
    ├─ ZFS GUID: 13388807557241155624
    ├─ Physical Disk: /dev/sdk
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHDX95L
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/b5a166f7-2478-4487-a80c-aaf23dafd031
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdk:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41888
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 12
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41751
       └─ Time Since: 5 days ago
    ............................................................
    Pool Device: /dev/sdc1
    ├─ ZFS GUID: 14718135334986108667
    ├─ Physical Disk: /dev/sdc
    ├─ Errors: ZFS Read: 0, ZFS Write: 0, ZFS Checksum: 0
    ├─ Serial: VAHEE12L
    ├─ Model: HUS728T8TAL4204
    ├─ Size: 7.28 TiB (8001563222016 bytes)
    └─ GPTID: /dev/gptid/1a2f31ae-c25d-428a-9f5e-839ebcc53b19
    ------------------------------------------------------------
    SMART DATA FOR /dev/sdc:
    ├─ Drive Type: SAS
    ├─ Health Status: PASSED
    ├─ Power On Hours: 41888
    ├─ Uncorrected Errors:
    │  ├─ Read: 0
    │  ├─ Write: 0
    │  └─ Verify: 0
    ├─ Grown Defects: 0
    ├─ Corrected Errors:
    │  ├─ Read: 9
    │  ├─ Write: 0
    │  └─ Verify: 0
    └─ Last Test: Background
       ├─ Status: short  Completed
       ├─ Lifetime Hours: 41751
       └─ Time Since: 5 days ago
    ............................................................
  ############################################################

  VDEV: ad3c9bc5-89e0-48a1-becb-4c7667cd485e (CACHE)
  ------------------------------------------------------------
  ############################################################

  VDEV: 84d26063-594f-44ef-ab77-f0b4573e702e (CACHE)
  ------------------------------------------------------------
  ############################################################
```

Example Output SATA

```
root@truenas[/home/truenas_admin]# python3 diskmapper.py

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
    ├─ Power On Hours: 0
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 30950
       └─ Time Since: -30950 hours ago
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
    ├─ Power On Hours: 0
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 51883
       └─ Time Since: -51883 hours ago
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
    ├─ Power On Hours: 0
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 51708
       └─ Time Since: -51708 hours ago
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
    ├─ Power On Hours: 0
    ├─ SMART Attributes:
    │  ├─ Raw Read Error Rate: 0
    │  ├─ Seek Error Rate: 0
    │  ├─ Offline Uncorrectable: 0
    │  └─ UDMA CRC Error Count: 0
    └─ Last Test: Short
       ├─ Status: offline       Completed
       ├─ Lifetime Hours: 46577
       └─ Time Since: -46577 hours ago
    ............................................................
  ############################################################
```

Example Output NVME

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
