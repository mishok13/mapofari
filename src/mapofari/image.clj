(ns mapofari.image)

(defprotocol ImageSurface
  "Image rendering surface"

  (line [_] "Draw a line")

  (multiline [_] "Draw a line")

  (point [_] "Draw a point")

  (multipoint [_] "Draw a point")

  (polygon [_])

  (to-bytes []
    "Render the surface and return the rendered image"))

(defrecord RasterSurface
    "Raster image surface"

  ImageSurface

  (line [] "")

    )

(defrecord SVGSurface)

(defrecord PDFSurface)
