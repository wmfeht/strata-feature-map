---
proposed: {page: reference/themes.md, section: GTK CSS precedence}
nodes: [app/window]
reason: The window frame on client-decorating compositors changed in v1.1.1 with the same change that isolated Strata from desktop GTK styling, which "GTK CSS precedence" already describes; the frame is the visible result of that isolation, and its border uses the theme's border color. The only page naming app/window is the Keyboard navigation reference, whose sections cover keys and focus only. A person must add app/window to the Themes reference's nodes in site/pagemap.yaml before merging.
release: v1.1.1
---

Raw material for a paragraph after the list of desktop styling Strata ignores.
The border and no-compositing lines were inferred from code; check them on
GNOME before merging.

- On a compositor that expects applications to draw their own title bar, such
  as GNOME Mutter, Weston or WSLg, a Strata window shows only Strata's header,
  with no second GTK title bar above it. This holds for every browser window,
  after opening new tabs, and for the system file chooser.
- Drag Strata's header to move the window, and drag a window edge to resize it.
- With compositing, such a window has square corners and a 1 px hairline in the
  theme's border color at 60% opacity instead of a drop shadow. A maximized, fullscreen or tiled
  window draws no border.
- Without compositor transparency, the window draws no border, shadow or
  padding.
