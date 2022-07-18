from rest_framework.throttling import UserRateThrottle


class GetBurstRateThrottle(UserRateThrottle):
    scope = 'get-burst'


class GetSustainedRateThrottle(UserRateThrottle):
    scope = 'get-sustained'


class PostBurstRateThrottle(UserRateThrottle):
    scope = 'post-burst'


class PostSustainedRateThrottle(UserRateThrottle):
    scope = 'post-sustained'
