baseline = finAvg
print(baseline)

i1 = int(0.20) * (baseline)
i2 = int(0.40) * (baseline)
i3 = int(0.60) * (baseline)
i4 = int(0.80) * (baseline)
i5 = baseline

import random

t1test = random.randrange(int(i1),int(i5))
print(t1test)
t1value = int(input("Scale Reading: "))
bfvalue = t1test - t1value
print("Biofeedback: ", bfvalue)

if i1 < t1test < i2 and i1 < t1value < i2:
  print("Match! Go to next test.")
elif i2 < t1test < i3 and i2 < t1value < i3:
  print("Match! Go to next test.")
elif i3 < t1test < i4 and i3 < t1value < i4:
  print("Match! Go to next test.")
elif i4 < t1test < i5 and i4 < t1value < i5:
  print("Match! Go to next test.")
else:
  print("No match! Try again!")
