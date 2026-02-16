# Tutorial: Generating Shell Dataset Data on a Phylogeny

This tutorial demonstrates how to simulate shell morphospace parameters on a phylogenetic tree using R. This is a data preparation step that creates the CSV file you'll import into TraitBlender.

## Overview

We'll use the `phytools` and `ape` packages in R to:
1. Generate a random coalescent phylogeny
2. Simulate shell morphospace parameters on the tree
3. Export the data as CSV for use in TraitBlender

## Shell Morphospace Parameters

For reference, here are all the parameters available for the shell morphospace, along with their mathematical domains:

| Parameter | Domain | Description |
|-----------|--------|-------------|
| `b` | ℝ⁺ (positive reals) | Growth rate parameter controlling shell expansion: γ(t) = (d·sin(t), d·cos(t), z)·exp(b·t) |
| `d` | ℝ⁺ (positive reals) | Distance from the coiling axis, controls shell width |
| `z` | ℝ (all reals) | Vertical translation along the coiling axis |
| `a` | ℝ⁺ (positive reals) | Aperture shape parameter affecting the cross-sectional form |
| `phi` | [0, 2π] or ℝ (radians) | Rotation angle φ controlling aperture orientation |
| `psi` | [0, 2π] or ℝ (radians) | Rotation angle ψ used in rotation matrix R_b(ψ) |
| `c_depth` | [0, 1] or ℝ⁺ | Axial rib depth: ribs = 1 + c_depth·sin(c_n·t) |
| `c_n` | ℤ⁺ or ℝ⁺ | Axial rib frequency along the shell length |
| `n_depth` | [0, 1] or ℝ⁺ | Spiral rib depth: ribs = 1 + n_depth·sin(n·θ) |
| `n` | ℤ⁺ or ℝ⁺ | Spiral rib frequency around the aperture |
| `t` | ℝ⁺ (positive reals) | Time parameter defining shell length (upper bound of integration) |
| `time_step` | ℝ⁺ (small positive reals) | Time step for shell generation (Δt in numerical integration) |
| `points_in_circle` | ℤ⁺ (positive integers) | Number of points around each shell ring (aperture resolution) |
| `eps` | ℝ⁺ (positive reals) | Thickness parameter: thickness = (exp(b·t) - 1/(t+1))^eps · h_0 |
| `h_0` | ℝ⁺ (positive reals) | Base thickness parameter in the allometric thickness function |
| `length` | ℝ⁺ (positive reals, meters) | Desired final shell length in meters (applied as scaling factor) |

**Parameter Notes:**

- Parameters `b`, `d`, `z`, `a`, `phi`, `psi`, `c_depth`, `c_n`, `n_depth`, and `n` come from the Contreras paper and describe the overall shape of the outer surface of the shell.
- Parameters `eps`, `h_0`, and `length` come from Okabe and describe the thickness of the shell as an allometric function of its radius at any point.
- Parameter `t` describes the number of half spirals of the shell.
- Parameters `time_step` and `points_in_circle` are not biologically meaningful parameters, but describe how many vertices will be in the outer and inner surfaces as a function of `t` along the growth curve and as a raw count along the aperture.

## Setup

First, load the required packages and set up your working directory:

```r
library(phytools)
library(ape)
set.seed(789)

# Set your working directory to where you want to save the CSV file
# Replace the path below with your desired directory
setwd("/path/to/your/datasets/directory")
```

## Step 1: Generate a Phylogeny

Create a random coalescent phylogeny with 10 tips, scaled so the root age is 1 million years:

```r
tip_count <- 10
tree <- rcoal(tip_count, tip.label = paste0("t", 1:10))

# Get current root age
root_age <- max(node.depth.edgelength(tree))

# Rescale so root = 1 Myr
tree$edge.length <- tree$edge.length / root_age

# Visualize the tree
plot(tree)
axisPhylo()
```

## Step 2: Initialize the Data Frame

Set up a data frame to store the shell parameters for each species:

```r
snails <- data.frame(
  species = tree$tip.label,
  b = numeric(length = tip_count),
  z = numeric(length = tip_count),
  n = integer(length = tip_count),
  n_depth = rep(0.1, tip_count)
)
```

## Step 3: Simulate Traits on the Phylogeny

### Simulate `b` and `z` Parameters

Since `b` and `z` must be positive in the TraitBlender morphospace, we evolve these traits on a log scale on the phylogeny:

```r
# Simulate b (growth rate) on log scale
snails$b <- exp(ape::rTraitCont(
  phy = tree, 
  model = 'BM', 
  sigma = 0.1,
  root.value = -1
))

# Simulate z (vertical offset) on log scale
snails$z <- exp(ape::rTraitCont(
  phy = tree, 
  model = 'BM', 
  sigma = 1,
  root.value = 0
))
```

### Simulate `n` Parameter

The `n` parameter (spiral rib frequency) takes integer values ≥ 0. We'll allow this trait to take one of two possible values: 0 or 10:

```r
snails$n <- ape::rTraitDisc(tree, rate = 1, states = c(0, 10))
print(snails)
```

## Step 4: Set Constant Parameters

Since shells grow according to their spiral curve, the `t` parameter essentially corresponds to an ontogenic age. We'll keep this constant across species for simplicity. Additionally, we'll make `time_step` and `points_in_circle` constant across species, set high enough that the generated shells have a nice high-poly look:

```r
snails$t <- 30
snails$points_in_circle <- 80
snails$time_step <- 0.1
snails$d <- 1.5
```

## Step 5: Export the Dataset

Export the data frame to CSV format for import into TraitBlender:

```r
write.csv(snails, "snails.csv", row.names = FALSE)
```

## Next Steps

After generating your dataset:

1. Import the CSV file into TraitBlender using the **Datasets** panel
2. Select a morphospace (e.g., CO_Raup)
3. Generate specimens using the **Generate Sample** button
4. Configure your scene and render images

For more details on using TraitBlender with your dataset, see the [Basic Specimen Imaging Tutorial](./basic-imaging.md).
