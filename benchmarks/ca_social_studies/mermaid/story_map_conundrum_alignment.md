# Story Map and Conundrum Alignment

This workflow maps benchmark terrain into a UCC History Story Map and an evidence-producing campaign.

```mermaid
flowchart TD
  Benchmark["Social Studies Benchmark Node"]
  Topic["Historical Topic"]
  Places["Places / Map Coordinates"]
  Actors["Actors / Perspectives"]
  Pressures["Pressures"]
  Choices["Choices"]
  Consequences["Consequences"]
  Conundrum["Conundrum / Moral Tradeoff"]
  Receipt["Story Map Receipt"]
  Campaign["Learning Campaign"]
  Hermes["Hermes Brief"]
  Benchmark --> Topic
  Topic --> Places
  Topic --> Actors
  Actors --> Pressures
  Pressures --> Choices
  Choices --> Consequences
  Consequences --> Conundrum
  Receipt --> Benchmark
  Receipt --> Campaign
  Benchmark --> Hermes
  Campaign --> Hermes
```

**Legend:** Benchmark = terrain; Story Map receipt = evidence; campaign = active plan; parent = final judgment.
