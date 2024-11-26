from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class TenPerDayUserThrottle(UserRateThrottle):
    rate = '10/day'

class ThreePerDayAnonThrottle(AnonRateThrottle):
    rate = '3/day'



