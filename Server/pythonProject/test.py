import torch

# Parameters of the Beta distribution
alpha = 0.1  # shape parameter
beta = 0.1  # shape parameter

# Create a Beta distribution object
beta_distribution = torch.distributions.Beta(alpha, beta)

# Sample a single value from the Beta distribution
sample = beta_distribution.sample()

print("Sampled value from Beta distribution:", sample.item())

lmda = torch.full((64,1,1,1),sample)
print(float(lmda[0]))
#
#
# indices = torch.randperm(64)
# print(indices)
#
# print(torch.arange(1,65))