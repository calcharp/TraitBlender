library(ape)

# Read and clean labels
tree <- read.tree("C:/Users/caleb/Downloads/subset.tre")
tree$tip.label <- gsub("'", "", tree$tip.label)
tree$tip.label <- sapply(tree$tip.label, function(lbl) {
  parts <- strsplit(lbl, " ")[[1]]
  parts[1] <- paste0(toupper(substring(parts[1],1,1)), substring(parts[1],2))
  paste(parts, collapse=" ")
})

# Save old par and expand margins
oldpar <- par(mar = c(1,1,1,6) + 0.1, xpd = NA)

# 1. Draw tree skeleton (no labels/axes)
plot(
  tree,
  direction      = "upwards",
  type           = "phylogram",
  show.tip.label = FALSE,
  root.edge      = TRUE,
  no.margin      = TRUE
)

# 2. Draw horizontal green bands every 10 units
usr <- par("usr")  # c(xleft, xright, ybottom, ytop)
for (y in seq(0, usr[4], by = 10)) {
  segments(
    x0 = usr[1], y0 = y,
    x1 = usr[2], y1 = y,
    col = adjustcolor("darkgreen", alpha.f = 0.2),
    lwd = 6
  )
}

# 3. Redraw tree with 90° tip labels correctly centered
plot(
  tree,
  direction      = "downwards",
  type           = "phylogram",
  show.tip.label = TRUE,
  srt            = 45,
  adj            = .5,    
  label.offset   = -250,    # tiny nudge off the branch
  cex            = 3.5,
  no.margin      = TRUE,
  root.edge      = TRUE,
  edge.width = 5
)

# Restore par
par(oldpar)
