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
import random
import math

def _sample_dirichlet(alphas):
    """
    Sample from a Dirichlet distribution.

    Args:
        alphas (list[float]): Concentration parameters (must all be > 0).
    Returns:
        tuple[float]: A tuple of samples summing to 1, each in (0,1).
    """
    gammas = [random.gammavariate(a, 1) for a in alphas]
    total = sum(gammas)
    return tuple(g / total for g in gammas)

def _sample_poisson(lam):
    """
    Sample from a Poisson distribution using Knuth's algorithm.

    Args:
        lam (float): Expected number of events (lambda, must be > 0).
    Returns:
        int: A non-negative integer sample from Poisson(lam).
    """
    # Knuth's algorithm
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.uniform(0, 1)
    return k - 1

def _sample_cauchy(x0, gamma):
    """
    Sample from a Cauchy (Lorentz) distribution using inverse transform sampling.

    Args:
        x0 (float): Location parameter (peak of the distribution).
        gamma (float): Scale parameter (half-width at half-maximum, must be > 0).
    Returns:
        float: A sample from Cauchy(x0, gamma).
    """
    # Inverse transform sampling
    u = random.uniform(0, 1)
    return x0 + gamma * math.tan(math.pi * (u - 0.5))

def _sample_multivariate_normal(mu, cov):
    """
    Sample from a multivariate normal distribution using Cholesky decomposition.
    
    Args:
        mu (list[float]): Mean vector.
        cov (list[list[float]]): Covariance matrix (must be positive definite).
    Returns:
        tuple[float]: A sample from the multivariate normal distribution.
    """
    # Simple implementation using Cholesky decomposition
    # For production, consider using numpy for better numerical stability
    n = len(mu)
    
    # Generate independent standard normal samples
    z = [random.gauss(0, 1) for _ in range(n)]
    
    # Cholesky decomposition of covariance matrix
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            if i == j:
                L[i][j] = math.sqrt(cov[i][j] - sum(L[i][k]**2 for k in range(j)))
            else:
                L[i][j] = (cov[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]
    
    # Transform: x = mu + L * z
    x = [mu[i] + sum(L[i][j] * z[j] for j in range(n)) for i in range(n)]
    return tuple(x)

def _uniform_sampler(low, high, number=None):
    """
    Sample from a uniform distribution.
    
    Args:
        low (float): Lower bound of the uniform distribution.
        high (float): Upper bound of the uniform distribution.
        number (int, optional): Number of samples to return. If None, returns a single value.
    Returns:
        float or list[float]: Single sample if number is None, otherwise list of samples.
    """
    if number is None:
        return random.uniform(low, high)
    return [random.uniform(low, high) for _ in range(number)]

def _normal_sampler(mu, sigma, number=None, cov=None):
    """
    Sample from a normal (Gaussian) distribution.
    
    Args:
        mu (float or list[float]): Mean(s) of the normal distribution.
        sigma (float or list[float]): Standard deviation(s) of the normal distribution.
        number (int, optional): Number of samples to return. If None, returns a single value.
        cov (list[list[float]], optional): Covariance matrix for multivariate sampling.
    Returns:
        float, list[float], tuple[float], or list[tuple[float]]: Single sample if number is None, otherwise list of samples.
    """
    if cov is not None:
        # Multivariate case
        if number is None:
            return _sample_multivariate_normal(mu, cov)
        return [_sample_multivariate_normal(mu, cov) for _ in range(number)]
    else:
        # Univariate case
        if number is None:
            return random.gauss(mu, sigma)
        return [random.gauss(mu, sigma) for _ in range(number)]

def _multivariate_normal_sampler(mu, cov, number=None):
    """
    Sample from a multivariate normal distribution.
    
    Args:
        mu (list[float]): Mean vector.
        cov (list[list[float]]): Covariance matrix (must be positive definite).
        number (int, optional): Number of samples to return. If None, returns a single tuple.
    Returns:
        tuple[float] or list[tuple[float]]: Single tuple if number is None, otherwise list of tuples.
    """
    if number is None:
        return _sample_multivariate_normal(mu, cov)
    return [_sample_multivariate_normal(mu, cov) for _ in range(number)]

def _dirichlet_sampler(alphas, number=None):
    """
    Sample from a Dirichlet distribution.
    
    Args:
        alphas (list[float]): Concentration parameters (must all be > 0).
        number (int, optional): Number of samples to return. If None, returns a single tuple.
    Returns:
        tuple[float] or list[tuple[float]]: Single tuple if number is None, otherwise list of tuples.
    """
    if number is None:
        return _sample_dirichlet(alphas)
    return [_sample_dirichlet(alphas) for _ in range(number)]

def _beta_sampler(a, b, number=None):
    """
    Sample from a Beta distribution.
    
    Args:
        a (float): First shape parameter (must be > 0).
        b (float): Second shape parameter (must be > 0).
        number (int, optional): Number of samples to return. If None, returns a single value.
    Returns:
        float or list[float]: Single sample if number is None, otherwise list of samples.
    """
    if number is None:
        return random.betavariate(a, b)
    return [random.betavariate(a, b) for _ in range(number)]

def _poisson_sampler(lam, number=None):
    """
    Sample from a Poisson distribution.
    
    Args:
        lam (float): Expected number of events (lambda, must be > 0).
        number (int, optional): Number of samples to return. If None, returns a single value.
    Returns:
        int or list[int]: Single sample if number is None, otherwise list of samples.
    """
    if number is None:
        return _sample_poisson(lam)
    return [_sample_poisson(lam) for _ in range(number)]

def _gamma_sampler(alpha, beta, number=None):
    """
    Sample from a Gamma distribution.
    
    Args:
        alpha (float): Shape parameter (must be > 0).
        beta (float): Scale parameter (must be > 0).
        number (int, optional): Number of samples to return. If None, returns a single value.
    Returns:
        float or list[float]: Single sample if number is None, otherwise list of samples.
    """
    if number is None:
        return random.gammavariate(alpha, beta)
    return [random.gammavariate(alpha, beta) for _ in range(number)]

def _exponential_sampler(lambd, number=None):
    """
    Sample from an Exponential distribution.
    
    Args:
        lambd (float): Rate parameter (must be > 0).
        number (int, optional): Number of samples to return. If None, returns a single value.
    Returns:
        float or list[float]: Single sample if number is None, otherwise list of samples.
    """
    if number is None:
        return random.expovariate(lambd)
    return [random.expovariate(lambd) for _ in range(number)]

def _cauchy_sampler(x0, gamma, number=None):
    """
    Sample from a Cauchy (Lorentz) distribution.
    
    Args:
        x0 (float): Location parameter (peak of the distribution).
        gamma (float): Scale parameter (half-width at half-maximum, must be > 0).
        number (int, optional): Number of samples to return. If None, returns a single value.
    Returns:
        float or list[float]: Single sample if number is None, otherwise list of samples.
    """
    if number is None:
        return _sample_cauchy(x0, gamma)
    return [_sample_cauchy(x0, gamma) for _ in range(number)]

def _discrete_uniform_sampler(low, high, number=None):
    """
    Sample from a discrete uniform distribution.
    
    Args:
        low (int): Lower bound (inclusive).
        high (int): Upper bound (inclusive).
        number (int, optional): Number of samples to return. If None, returns a single value.
    Returns:
        int or list[int]: Single sample if number is None, otherwise list of samples.
    """
    if number is None:
        return random.randint(low, high)
    return [random.randint(low, high) for _ in range(number)]

TRANSFORMS = {
    'uniform': _uniform_sampler,
    'normal': _normal_sampler,
    'multivariate_normal': _multivariate_normal_sampler,
    'dirichlet': _dirichlet_sampler,
    'beta': _beta_sampler,
    'poisson': _poisson_sampler,
    'gamma': _gamma_sampler,
    'exponential': _exponential_sampler,
    'cauchy': _cauchy_sampler,
    'discrete_uniform': _discrete_uniform_sampler,
    # Add more as needed
}

