"""
Registry of available transform sampling functions for TraitBlender.
Each entry maps a string name to a callable or factory that returns a sample value.

- 'uniform': function taking (low, high, number=None) and returning a scalar or list of samples
- 'normal': function taking (mu, sigma, number=None, cov=None) and returning a scalar or list of samples
- 'multivariate_normal': function taking (mu, cov, number=None) and returning a tuple or list of tuples
- 'dirichlet': function taking (alphas: list, number=None) and returning a tuple or list of tuples
- 'beta': function taking (a, b, number=None) and returning a scalar or list of samples
- 'poisson': function taking (lam, number=None) and returning a scalar or list of samples
- 'gamma': function taking (alpha, beta, number=None) and returning a scalar or list of samples
- 'exponential': function taking (lambd, number=None) and returning a scalar or list of samples
- 'cauchy': function taking (x0, gamma, number=None) and returning a scalar or list of samples
- 'discrete_uniform': function taking (low, high, number=None) and returning a scalar or list of samples
"""
import numpy as np
import scipy.stats as stats

TRANSFORMS = {}
from .transform_registry_decorator import register_transform

@register_transform('dirichlet')
def dirichlet_sampler(alphas: list[float], n: int = None) -> list[float] | list[list[float]]:
    samples = np.random.dirichlet(alphas, n or 1)
    if n is None:
        return [float(x) for x in samples[0]]
    return [[float(x) for x in s] for s in samples]

@register_transform('poisson')
def poisson_sampler(lam: float, n: int = None) -> int | list[int]:
    samples = np.random.poisson(lam, n or 1)
    if n is None:
        return int(samples[0])
    return [int(s) for s in samples]

@register_transform('cauchy')
def cauchy_sampler(x0: float, gamma: float, n: int = None) -> float | list[float]:
    samples = stats.cauchy.rvs(loc=x0, scale=gamma, size=n or 1)
    if n is None:
        return float(samples[0])
    return [float(s) for s in samples]

@register_transform('multivariate_normal')
def multivariate_normal_sampler(mu: list[float], cov: list[list[float]], n: int = None) -> list[float] | list[list[float]]:
    samples = np.random.multivariate_normal(mu, cov, n or 1)
    if n is None:
        return [float(x) for x in samples[0]]
    return [[float(x) for x in s] for s in samples]

@register_transform('uniform')
def uniform_sampler(low: float, high: float, n: int = None) -> float | list[float]:
    samples = np.random.uniform(low, high, n or 1)
    if n is None:
        return float(samples[0])
    return [float(s) for s in samples]

@register_transform('normal')
def normal_sampler(mu: float, sigma: float, n: int = None, cov: list[list[float]] = None) -> float | list[float] | list[list[float]]:
    if cov is not None:
        samples = np.random.multivariate_normal(mu, cov, n or 1)
        if n is None:
            return [float(x) for x in samples[0]]
        return [[float(x) for x in s] for s in samples]
    else:
        samples = np.random.normal(mu, sigma, n or 1)
        if n is None:
            return float(samples[0])
        return [float(s) for s in samples]

@register_transform('beta')
def beta_sampler(a: float, b: float, n: int = None) -> float | list[float]:
    samples = np.random.beta(a, b, n or 1)
    if n is None:
        return float(samples[0])
    return [float(s) for s in samples]

@register_transform('gamma')
def gamma_sampler(alpha: float, beta: float, n: int = None) -> float | list[float]:
    samples = np.random.gamma(alpha, beta, n or 1)
    if n is None:
        return float(samples[0])
    return [float(s) for s in samples]

@register_transform('exponential')
def exponential_sampler(lambd: float, n: int = None) -> float | list[float]:
    samples = np.random.exponential(1.0 / lambd, n or 1)
    if n is None:
        return float(samples[0])
    return [float(s) for s in samples]

@register_transform('discrete_uniform')
def discrete_uniform_sampler(low: int, high: int, n: int = None) -> int | list[int]:
    samples = np.random.randint(low, high + 1, n or 1)
    if n is None:
        return int(samples[0])
    return [int(s) for s in samples]

# TRANSFORMS dict is now populated by the decorator

