# geolocation_waldrain

Python geolocation calculation for the [Waldrain](https://waldrain.github.io) plot of land.

To begin with, I had six unconfirmed latitude and longtitude coordinates for the six corner points for a plot of land.

I also had pretty precise edge length and area measurements in metres:

![Edge lengths](img/edge_lengths.png "Edge lengths")

That leads to the following data:

```
pts = [
  [47.61240287934088,7.668455564143808],
  [47.61238603493116,7.66886803694362],
  [47.61227235282722,7.668805013356426],
  [47.612081232450755,7.668710772100395],
  [47.61209766306042,7.668317607008359],
  [47.612263038360155,7.668392271613928]]

tags = ['NW','NO','OM','SO','SW','WM']

edge_length = [ # in metres
  31.10, # Nord
  13.34, 22.51, # Ost
  29.63, # Sued
  19.26, 16.24 ] # West

area = 1043 # square metres
```

## Task

Calculate the expected edge lengths and area from the given latitude and longtitude coordinates.

