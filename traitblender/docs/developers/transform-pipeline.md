# Transform Pipeline

For statistical distributions, see: [NumPy Random Sampling](https://numpy.org/doc/stable/reference/random/index.html) and [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)

---

## Overview

The Transform Pipeline system lets you randomize scene properties for data augmentation. Instead of manually creating variations of your scene (moving the camera slightly, changing lighting brightness, adjusting colors), you define statistical distributions and let the pipeline generate variations automatically.

**What it does:**

When training computer vision models, you need lots of varied data. The Transform Pipeline helps by randomizing:

- **Camera properties**: Position, angle, focal length jitter
- **Lighting**: Brightness variations, color temperature shifts, position wobble  
- **Colors**: Background color, specimen material color, mat color
- **Specimen positioning**: Small rotations, position offsets

**Why this matters:**

Training a neural network on images that are all identical except for the specimen leads to overfitting. The model learns to recognize the lighting/camera setup instead of the specimen features. Randomizing these scene properties creates robust models that generalize better.

**How it works:**

- Define transforms: "Randomize camera.location[2] using normal distribution (mean=5, std=0.2)"
- Run the pipeline: All transforms execute in sequence, randomizing your scene
- Render your image with the randomized scene
- Undo: Restore all original values to reset the scene
- Repeat for the next specimen

The pipeline includes 10 statistical distributions (uniform, normal, beta, gamma, etc.) and saves/loads with your configuration files for reproducibility.

---

## Transform Class

The `Transform` class (in `core/transforms/transforms.py`) represents a single property randomization. Each transform has:

- **Property path**: Which config property to randomize (e.g., `"world.color"`, `"camera.location[2]"`)
- **Sampler name**: Which statistical distribution to use (e.g., `"uniform"`, `"normal"`)
- **Parameters**: Distribution parameters (e.g., `{"low": 0, "high": 1}`)
- **Cache stack**: History of values for undo operations

**How it works:**

When you create a transform with `Transform("world.color", "uniform", {"low": 0, "high": 1})`, it validates that the property exists in the config and that the sampler is registered. The property path is internally converted to the full path: `"bpy.context.scene.traitblender_config.world.color"`.

**Execution:**

When you call `transform()`, it caches the current value, samples a new value from the distribution, and applies it to the property. The cache stack grows with each execution, allowing you to undo multiple times.

**Undo operations:**

- `transform.undo()` - Reverts to the previous value (pops one item from the cache stack)
- `transform.undo_all()` - Reverts to the original value (clears the entire cache stack)

**Internal methods:**

The Transform class uses `_get_property_value()` and `_set_property_value()` to read/write property values via `eval()` and `exec()`. The `_call_sampler()` method looks up the sampler factory in the registry, validates parameters using Python's `inspect` module, and calls the sampler function.

**Serialization:**

`to_dict()` exports the transform to a dictionary (property path, sampler name, and parameters). `from_dict()` creates a Transform from a dictionary. Note that the cache stack is **not** serialized by default - this is the source of the undo bug in `TransformPipelineConfig` (see below).

---

## TransformPipeline Class

The `TransformPipeline` class (in `core/transforms/transform_pipeline.py`) manages multiple transforms as a group. It maintains a list of `Transform` objects and an execution history.

**Core methods:**

- `add_transform(property_path, sampler_name, params)` - Adds a new transform to the pipeline. Returns self for method chaining.
- `run()` - Executes all transforms in order. Each transform caches its value before randomization. Failures don't stop execution.
- `undo()` - Reverts all transforms in reverse order (LIFO). Each transform resets to its original value and clears its cache stack.
- `clear()` - Removes all transforms from the pipeline.

**Example:**

```python
pipeline = TransformPipeline()
pipeline.add_transform("world.color", "uniform", {"low": 0, "high": 1})
pipeline.add_transform("camera.location[2]", "normal", {"mu": 5, "sigma": 0.2})
pipeline.run()  # Randomizes both properties
pipeline.undo()  # Restores both to original values
```

The class also implements standard Python protocols (`__len__`, `__getitem__`, `__iter__`, etc.) for convenient access to transforms.

### Serialization

#### `to_dict()` - Export

```python
def to_dict(self):
    """Serialize pipeline to list of transform dicts."""
    return [t.to_dict() for t in self._transforms]
```

**Output format:**

```python
[
    {
        'property_path': 'world.color',
        'sampler_name': 'uniform',
        'params': {'low': 0, 'high': 1}
    },
    {
        'property_path': 'camera.location',
        'sampler_name': 'normal',
        'params': {'mu': 0, 'sigma': 1, 'n': 3}
    }
]
```

#### `from_dict()` - Import

```python
@classmethod
def from_dict(cls, d, name="TransformPipeline"):
    """Create pipeline from list of transform dicts."""
    pipeline = cls(name=name)
    for t_dict in d:
        pipeline._transforms.append(Transform.from_dict(t_dict))
    return pipeline
```

---

## Transform Registry

Sampler functions are registered using the `@register_transform` decorator (defined in `core/transforms/transform_registry_decorator.py`). The decorator validates type hints, creates a factory pattern for flexible parameterization, and adds the sampler to the `TRANSFORMS` dictionary in `core/transforms/registry.py`.

**Sampler requirements:**

All custom samplers must have type hints on all parameters, support an optional `n` parameter for vector properties, and return either a single value (when `n=None`) or a list of values (when `n=int`).

**Example template:**

```python
@register_transform('my_sampler')
def my_sampler(param1: float, param2: int, n: int = None) -> float | list[float]:
    """My custom sampler."""
    samples = ...  # Generate samples using NumPy/SciPy
    if n is None:
        return float(samples[0])
    return [float(s) for s in samples]
```

---

## Available Samplers

All samplers are defined in `core/transforms/registry.py`. Each sampler supports an optional `n` parameter: when `n=None` (default), returns a single value; when `n=int`, returns a list of values.

<details>
<summary>Click to expand all 10 distributions</summary>


**`uniform(low, high, n=None)`** → `float | list[float]`

Uniform distribution between low and high. Use for random camera positions, focal lengths, unbiased variation.

**`normal(mu, sigma, n=None)`** → `float | list[float]`

Normal (Gaussian) distribution with mean `mu` and standard deviation `sigma`. Use for natural variation around a mean, measurement error simulation.

**`beta(a, b, n=None)`** → `float | list[float]`

Beta distribution with shape parameters `a` and `b`. Values bounded between 0 and 1. Use for roughness/metallic variation.

**`gamma(alpha, beta, n=None)`** → `float | list[float]`

Gamma distribution with shape `alpha` and scale `beta`. Positive values with right skew. Use for light intensity variation.

**`dirichlet(alphas, n=None)`** → `list[float] | list[list[float]]`

Dirichlet distribution (multivariate beta) for compositional data. Parameter `alphas` is a list of concentration parameters. Use for color variation (RGB/RGBA).

**`multivariate_normal(mu, cov, n=None)`** → `list[float] | list[list[float]]`

Multivariate normal with mean vector `mu` and covariance matrix `cov`. Use for correlated parameters (e.g., camera position with correlation between axes).

**`poisson(lam, n=None)`** → `int | list[int]`

Poisson distribution with rate `lam`. Use for count data, discrete events.

**`exponential(lambd, n=None)`** → `float | list[float]`

Exponential distribution with rate `lambd`. Use for time between events, decay rates.

**`cauchy(x0, gamma, n=None)`** → `float | list[float]`

Cauchy distribution with location `x0` and scale `gamma`. Heavy-tailed distribution for extreme outliers.

**`discrete_uniform(low, high, n=None)`** → `int | list[int]`

Discrete uniform distribution between `low` and `high` (inclusive). Use for random integer selections.

</details>

---

## Config Integration

The transform pipeline integrates with the configuration system via `TransformPipelineConfig` in `core/config/config_templates/transforms.py`. Unlike normal config sections that directly map to Blender objects, the transform config stores the entire pipeline state as a serialized YAML string. It uses a delegation pattern: deserialize the pipeline, call the method, re-serialize the pipeline.

**Known issue - Undo doesn't work through config:**

When you use `config.transforms.undo()`, it doesn't work because the `Transform._cache_stack` (undo history) isn't serialized. Each deserialization creates fresh Transform objects with empty cache stacks. 

**Workaround:** Use `TransformPipeline` directly instead of through the config system:

```python
# Undo works correctly
pipeline = TransformPipeline()
pipeline.add_transform("world.color", "uniform", {"low": 0, "high": 1})
pipeline.run()
pipeline.undo()  # ✓ Works
```

**To fix:** Modify `Transform.to_dict()` to include `'_cache_stack': self._cache_stack.copy()` and `Transform.from_dict()` to restore it.

---

## Creating a New Sampler

To add a custom sampler, define a function in `core/transforms/registry.py` with the `@register_transform` decorator:

```python
@register_transform('my_sampler')
def my_sampler(param1: float, param2: int, n: int = None) -> float | list[float]:
    """My custom sampler."""
    samples = ...  # Generate using NumPy/SciPy
    if n is None:
        return float(samples[0])
    return [float(s) for s in samples]
```

**Requirements:** All parameters must have type hints, function must support optional `n` parameter, and return either a single value or list of values.

