---
proposed: {page: reference/keyboard-navigation.md, section: Refreshing a directory}
nodes: [browser/directory-monitoring/network-checks]
reason: '"Refreshing a directory" already names the Watch network folders switch and its default, and the SFTP locations reference gives the check cadence, but neither says what turning the switch off does. Add the node to the page''s nodes in site/pagemap.yaml and merge the sentence below.'
release: v1.1.1
---

With **Watch network folders** off, folders on network mounts are never checked,
so changes made on other computers show only after **F5**.
