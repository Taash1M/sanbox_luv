# Netflix-scale streaming pipeline architecture

    This pipeline simulates a **high-throughput event streaming architecture** for near real-time analytics, using a producer, a streaming backbone, and a Spark streaming job.

    ```mermaid
    flowchart LR
        subgraph Producers
            ClientApps[Client Apps
(Web, Mobile, Devices)]
            ProducerSim[producer_sim.py]
        end

        subgraph Streaming_Backbone
            Kafka[(Kafka / Event Hub)]
            Topics[(Event Topics)]
        end

        subgraph Processing
            SparkJob[spark_streaming_job.py
(Spark Structured Streaming)]
            QoS[Quality & Schema Validation]
        end

        subgraph Storage
            Bronze[(Raw Events / Bronze)]
            Silver[(Validated Events / Silver)]
            Gold[(Aggregated KPIs / Gold)]
        end

        subgraph Consumers
            RealtimeDash[Real-time Dashboards]
            FeatureStore[Feature Store]
            BatchJobs[Downstream Batch Jobs]
        end

        ClientApps --> ProducerSim --> Kafka --> Topics
        Topics --> SparkJob --> QoS

        QoS --> Bronze
        Bronze --> Silver
        Silver --> Gold

        Gold --> RealtimeDash
        Gold --> FeatureStore
        Gold --> BatchJobs
    ```

    ## Architecture narrative

    **Volume & scale assumptions:**
    - Tens of thousands of events per second per region.
    - Ordering guarantees are best-effort within partition keys (e.g., account_id, device_id).
    - Latency target: **sub-minute** end-to-end from event to dashboard.

    **Key design decisions:**
    - **Schema-first events:** Event schemas are versioned and validated (`test_event_schema.py`) to prevent bad data from impacting consumers.
    - **Streaming backbone:** Kafka or Event Hubs provide durable, replayable logs supporting multiple independent consumers.
    - **Streaming compute:** Spark Structured Streaming (in `spark_streaming_job.py`) handles windowed aggregations, watermarking, and stateful operations.
    - **Layered storage:** Bronze retains raw events, Silver stores validated, partitioned data, and Gold holds pre-aggregated KPIs and session metrics.

    ## Operational considerations (Director-level)

    - **Multi-region strategy:** Topics are replicated or sharded by region; DR strategy is documented and tested.
    - **Backpressure and failure modes:** Clear runbooks for lag, schema evolution, and poison-pill messages.
    - **Cost management:** Tiered storage and compaction strategies balance retention with cost.
    - **SLOs:** SLOs defined for latency, data freshness, and schema validation success rates; on-call is aligned with these metrics.
