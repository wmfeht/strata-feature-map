---
title: Drive grouping in Devices
status: shipped
origin: {issue: lgse/strata#2071, pr: lgse/strata#2075}
branch: null
reviewed_at: 5738aad808ea4cc4671516bc569d85f862664809
review: draft
code: [src/ui/window/device_order.rs, src/ui/window/device_order/**]
tests: [src/ui/window/device_order/tests.rs]
related: [browser/sidebar, devices/volumes/drive-dialogs]
---

## Summary

The order of rows under DEVICES in the sidebar. Rows are grouped by physical drive in the system's drive order, with a divider between groups. Drive-less rows and then network shares follow the drives. It is for users with several disks or partitions who need to tell which volume sits on which disk.

## Behavior

### Groups

- Volumes on one drive sit together under DEVICES, even when the volume monitor reports them interleaved with another drive's volumes. lgse/strata#2075
- A divider line separates each group from the next, in the full sidebar and in the icon rail. lgse/strata#2075
- No divider shows above the first group or below the last. lgse/strata#2075 (unverified)
- A password-start drive with no listed volume, and a volume-less mount on a drive, join that drive's group. lgse/strata#2075 (unverified)
- Rows with no drive follow every drive's group, as one group of their own. lgse/strata#2075
- Mounted network shares come last, as one group after the rows with no drive. lgse/strata#2075
- A pending-release stand-in for a device no longer listed follows every group, with no divider before it. lgse/strata#2075 (unverified)

### Drive order

- Drives follow their system sort key, so a fixed disk keyed `00coldplug/00fixed/nvme0` comes before a removable one keyed `00coldplug/12removable/sd____b`. lgse/strata#2075
- Fixed disks come before removable and hot-plugged drives. lgse/strata#2075
- A drive with no sort key follows every drive that has one. lgse/strata#2075 (unverified)
- Two drives with the same name, such as two "External USB 3.0" disks, get separate groups. lgse/strata#2075 (unverified)

### Within a drive

- Rows in one group follow natural name order of their system names, such as `2TEUI`, `Guoxue`, `T2ERP`. lgse/strata#2075
- Two volumes named "129 GB Volume" on `/dev/nvme0n1p2` and `/dev/nvme0n1p10` list p2 first, whatever order the monitor reports, and keep that order across rebuilds. lgse/strata#2075
- A row renamed with Set label… keeps its place at the next rebuild, sorted by its system name. lgse/strata#2075

## Design

- Drive order is the backend's own ranking from `g_drive_get_sort_key`. udisks fills it so fixed disks rank ahead of removable and hot-plugged ones (lgse/strata#2075).
- A divider marks each group boundary because every drive uses the same icon, so adjacency alone would not show it (lgse/strata#2075).
- Rows sort by the system device name, not a Strata label. Labels update rows in place without a rebuild, so sorting by them would make rows jump at a later, unrelated refresh (lgse/strata#2075).
- The device path breaks ties between same-named volumes, so they do not swap places between rebuilds (lgse/strata#2075).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
