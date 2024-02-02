from rest_framework.throttling import UserRateThrottle


class FriendRequestThrottleRate(UserRateThrottle):
    rate = '3/min'