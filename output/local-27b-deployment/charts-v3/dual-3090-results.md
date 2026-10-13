# Benchmark Results

All numbers measured on the hardware described in the [README](../README.md) — vLLM running directly under systemd inside a **Proxmox unprivileged LXC** with 2× RTX 3090 passed through. No Docker, no Compose. Benchmarks were run from a separate machine on the same LAN hitting the LXC's IP via the OpenAI-compatible HTTP endpoint.

Model: `cyankiwi/Qwen3.6-27B-AWQ-BF16-INT4`
Date: 2026-05-26
vLLM: 0.21.0
Workload: structured JSON generation, ~25 prompt tokens, ~1024 max_tokens, `enable_thinking: false`

## Headline numbers (v1 = the config shipped in this repo)

```
=== summary (v1) ===
  c=1   agg=  97.3 t/s   per-stream-avg= 97.3 t/s   wall=10.52s
  c=2   agg= 163.6 t/s   per-stream-avg= 82.4 t/s   wall=11.62s
  c=4   agg= 255.9 t/s   per-stream-avg= 65.6 t/s   wall=15.38s
```

| Concurrency | Wall (s) | Aggregate t/s | Avg per-stream t/s |
|---|---|---|---|
| 1 | 10.52 | 97.3 | 97.3 |
| 2 | 11.62 | 163.6 | 82.4 |
| 4 | 15.38 | 255.9 | 65.6 |

These match noonghunna's published `qwen36-dual-3090` numbers (257 t/s at c=4) to within 0.5%. We are at the practical ceiling for stock vLLM 0.21.0 on this hardware + this quant.

From the vLLM startup logs on this config:

```
GPU KV cache size: 375,342 tokens
Maximum concurrency for 262,144 tokens per request: 1.43x
```

So four concurrent agents at full 256K each is mathematically impossible — vLLM will preempt as needed. In practice this matters less than it sounds because most workloads aren't at peak context constantly and prefix-cache reuse cushions the recompute.

## Reproducing

Inside any environment that can reach the vLLM endpoint:

```bash
# Point at your endpoint
export VLLM_URL=http://<your-lxc-ip>:8000
export VLLM_MODEL=cyankiwi/Qwen3.6-27B-AWQ-BF16-INT4

# Run the benchmark
python3 bench.py v1 v1_results.json
```

The script runs a warmup call, then concurrent test runs at c=1, c=2, c=4. Numbers should land within ±3% of the table above on identical hardware.

## What we also tried (v2 ablation that didn't win)

Before locking in v1 we tested a "safer for 24/7" variant with three changes from Dzombak's baseline:

| Change | v1 | v2 |
|---|---|---|
| `--kv-cache-dtype` | `fp8` | `fp8_e5m2` (explicit Ampere variant) |
| `--gpu-memory-utilization` | `0.98` | `0.93` |
| `--max-num-batched-tokens` | `4096` | `8192` |
| `--performance-mode` | `interactivity` | (removed; balanced default) |

### Why v2 lost on every dimension

**`fp8_e5m2` is hard-rejected by this quant.** vLLM errored on engine init with:

```
ValueError: fp8_e5m2 kv-cache is not supported with fp8 checkpoints.
```

The cyankiwi AWQ-BF16-INT4 weights carry fp8 E4M3 scale factors. vLLM forces the KV-cache dtype to match the checkpoint's. The bare `fp8` alias was already doing the right thing on v1 — it was not a "silent fallback to BF16" as some Ampere-generic advice suggests.

Once `fp8_e5m2` was reverted to `fp8`, v2 booted. Results:

```
=== summary (v2) ===
  c=1   agg=  95.0 t/s   per-stream-avg= 95.0 t/s   wall=10.78s
  c=2   agg= 155.5 t/s   per-stream-avg= 79.1 t/s   wall=12.21s
  c=4   agg= 238.0 t/s   per-stream-avg= 61.2 t/s   wall=16.53s
```

| Metric | v1 | v2 | Δ |
|---|---|---|---|
| c=1 agg | 97.3 | 95.0 | −2.4% |
| c=2 agg | 163.6 | 155.5 | −5.0% |
| c=4 agg | 255.9 | 238.0 | −7.0% |
| KV pool | 375K tok | 326K tok | −13% |
| Max conc @ 262K | 1.43× | 1.24× | −13% |

v2 lost on every dimension. The "safer headroom" from GMU 0.93 came at a real cost in throughput AND KV pool, with no observable stability gain in any of our testing. The `balanced` cudagraph capture set `[1,2,4,8,16,24]` pads up to the nearest captured size at odd batch counts; `interactivity` captures each size 1-24 individually and avoids that penalty for our bounded N=2-4 workload.

The full ablation rationale (and why specifically-on-Ampere generic advice doesn't apply to this quant) lives in [`../GOTCHAS.md`](../GOTCHAS.md).

## Output correctness

Every benchmark response across c=1/2/4 was clean valid JSON. No character-substitution corruption (`<!!!`, `wcodebergtorg`-style garbling) — vLLM issue [#35288](https://github.com/vllm-project/vllm/issues/35288) did not reproduce on this stack at c=4.

If you do see corruption on your run, the cheapest mitigation is dropping `num_speculative_tokens` from 2 to 1 in the speculative-config flag. Trades ~10-15% throughput for output safety.
