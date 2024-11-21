from rest_framework.throttling import AnonRateThrottle

class BurstRateThrottle(AnonRateThrottle):
    scope = 'x'

    