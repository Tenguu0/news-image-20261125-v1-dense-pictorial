# The World in One Page — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Tenguu0/news-image-20261125-v1-dense-pictorial/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Tenguu0/news-image-20261125-v1-dense-pictorial/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page newspaper image summing up the world news of **Wednesday 25 November 2026** — an entry for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125) on make.fun.

## The page

Dense broadsheet layout: one big pictured lead story, a 4×3 grid of pictured stories, and an ALSO TODAY strip — 13 pictured stories plus 3 short items, 16 stories in total.

- **Lead:** Houthi drone hits Riyadh's tallest tower — 11 wounded.
- **Grid:** Ukraine confirms a drone strike on a Russian ship in the Gulf of Finland · COP31 talks collapse with no deal · Huawei guilty on 10 of 12 counts in a US trial · CIA and ODNI hit by hack · Dozens feared trapped in a flooded Java gold mine · China launches Shenzhou-24 · Real Madrid rout PSV 5–1 · Senegal get their AFCON crown back · Vaibhav's 204 off 53 balls, a world record · Asia stocks slide as the tariff threat returns · Sarkozy and Bruni ordered to trial · Hanoi blast kills six.
- **Also today:** Trump pardons the Thanksgiving turkeys Freedom and Feathers · Giuliani gets the Medal of Freedom · Gukesh draws his World Chess opener.

Every story is a real reported story from 25 November 2026. Pictures are AI-generated illustrations matched to each story.

## How to run

```sh
python3 main.py
```

Requires Python 3 and Pillow (`pip install pillow`). The program reads the illustrations in `assets/` and writes a deterministic 1024×1024 PNG to `/output/entry.png` (override with `OUTPUT_DIR`). No network access at runtime; two runs produce identical bytes.

## Files

- `main.py` — the entry program (composes the page with Pillow).
- `assets/` — 13 AI-generated pictorial illustrations, one per pictured story.
- `LICENSE` — MIT.

## Sources

Headlines verified against Reuters, BBC-style wire summaries and same-day news reports published 25 November 2026.
