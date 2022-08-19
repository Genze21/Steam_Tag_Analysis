import numpy as np
import statsmodels.api as sm

x=np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
blue_y = np.array([0.94732871, 0.85729212, 0.86039587, 0.89169027, 0.90817473, 0.93606619, 0.93890423, 1., 0.97783521, 0.93035495])
light_blue_y = np.array([0.81346023, 0.72248919, 0.72406021, 0.74823437, 0.77759055, 0.81167983,  0.84050726, 0.90357904, 0.97354455, 1. ])

y = blue_y-light_blue_y
x=np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([-126.09612296 ,-126.0698156  ,-126.04350825 ,-126.01720089 ,-125.99089354,
 -125.96458618 ,-125.93827883, -125.91197147, -125.88566412])
print(y)
# Let create a linear regression
mod = sm.OLS(y, sm.add_constant(x))
res = mod.fit()

print(res.summary())