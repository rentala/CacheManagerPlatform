# CacheManager
-Cache Manager A cache manager to support multiple readers/writers. Think of a service to manage in-memory cache which can support such clients. Writers/readers are random and can make requests at any time 
-Strong consistency guarantees: 
-A reader should never read stale data (data written to already) 
-Readers should get notified if the data they have has gone stale. 
-Readers get preference over writers, multiple readers-one writer at a time. 
-No starvation. 
-Bonus: Design the system so that it can be distributed. 
-No need to consider high availability for this exercise.
