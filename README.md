## Code to compute entropy
### Use (example)
```python
from compute_entropy import load_taxi_data, compute_entropy, pd_compute_entropy

# load sample taxi data
taxi_data = load_taxi_data()
# print resultant entropy calculations
print(compute_entropy(taxi_data.payment_type))
print(pd_compute_entropy(taxi_data, "dropoff_latitude", to_bucketise=True))
```