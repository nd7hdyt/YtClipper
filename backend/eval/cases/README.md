Each case EN：

- `input.srt` — EN
- `timeline.json` — EN step2 LLM EN（EN）
- `expect.json` — EN：`clips_min/max`、`duration_min/max`、`must_not_zero`、`coverage_min`

```bash
python -m backend.eval
```
