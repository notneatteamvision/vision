import visionMath, math

x, a = visionMath.triangulatePoint(math.radians(340.201), math.radians(329.03))
a = math.degrees(a)
print((x, a))