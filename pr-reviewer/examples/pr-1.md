### Summary of Changes
This pull request introduces a new caching layer for the `UserAPI` endpoints to reduce database load. It adds a Redis dependency, implements caching logic in `user_service.py`, and updates the corresponding unit tests to verify cache hits and misses.

### Identified Risks
- The Redis connection timeout is set to a high value (10 seconds), which might cause application hangs if the cache server becomes unresponsive.
- There is no fallback mechanism to the database if the cache cluster is down, leading to a hard failure on the endpoints.

### Improvement Suggestions
- Consider lowering the Redis connection timeout to 1-2 seconds.
- Implement a graceful fallback to query the database directly and log a warning if the cache is unreachable.
- Use an environment variable for the Redis URI instead of hardcoding the default localhost address.

### Confidence Score
High
