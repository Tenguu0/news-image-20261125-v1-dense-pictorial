# The World in One Page — Wednesday 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Tenguu0/news-image-20261125-v1-dense-pictorial/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Tenguu0/news-image-20261125-v1-dense-pictorial/reward.svg)](https://make.fun/bounty/news-image-20261125)

An entry for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125): one 1024×1024 newspaper front page that squeezes the whole of Wednesday 25 November 2026 into a single dense, fully pictured sheet — a big illustrated lead, twelve illustrated stories in a grid, and a short strip of lighter items at the bottom.

## How to run

You need Python 3 and Pillow. Install the single dependency with:

```sh
pip install pillow
```

Then, from this directory, run:

```sh
python3 main.py
```

The script reads the pictures from `assets/`, draws the complete page with Pillow, and saves the finished image to `/output/entry.png`. To put the output somewhere else, set `OUTPUT_DIR` before running:

```sh
OUTPUT_DIR=/tmp/out python3 main.py
```

When it finishes it prints the path and the size of the file it wrote, for example `wrote /output/entry.png (1024, 1024)`. It needs no network access while it runs — every picture and every word is already in this repository — and it draws its text with the DejaVu fonts that ship with most Linux systems, falling back to Pillow's built-in font if those are missing.

## Content list

Sixteen stories from 25 November 2026, each one checked against same-day reporting before it went on the page.

**Lead story — Middle East.** A Houthi drone struck the PIF Tower in Riyadh, the city's tallest tower, wounding 11 people, among them two Indian and three Nepali nationals. Civil defence described it as the second attack on the tower in a matter of days.

**The grid — twelve stories, four columns by three rows:**

1. Ukraine — Kyiv says its forces hit a Russian ship in the Gulf of Finland, while Norway urges caution.
2. Climate — the COP31 talks in Antalya collapse with no deal, the fossil-fuel deadlock unbroken.
3. Tech — a Brooklyn jury finds Huawei guilty on 10 of 12 counts after a three-month trial.
4. USA — the CIA and the spy chief's office (ODNI) are hit by a hack of unclassified systems.
5. Indonesia — dozens of workers are feared trapped in the flooded Pongkor gold mine in Bogor, Java, about 100 metres underground.
6. Space — China launches the Shenzhou-24 crew to orbit from Jiuquan aboard a Long March 2F rocket.
7. Football — Real Madrid rout PSV 5–1, powered by a Bellingham stunner and a Mbappé brace.
8. Africa — Senegal get their AFCON crown back after CAS overturns CAF's decision.
9. Cricket — Vaibhav smashes 204 off 53 balls with 28 sixes, the fastest List A double century ever and a world record.
10. Markets — Asian stocks slide as the tariff threat returns, the Nikkei down 2.9% and Seoul down 5.3%.
11. France — Sarkozy and Bruni are ordered to trial over the Libya case.
12. Vietnam — a blast in Hanoi kills six and injures 10, with a gas leak suspected.

**Also today — three short items in the strip at the foot of the page:** Trump pardons the Thanksgiving turkeys Freedom and Feathers; Giuliani receives the Medal of Freedom; Gukesh draws his World Chess Championship opener.

## Design & method notes

The layout is deliberately dense: a broadsheet front page with almost no empty space, so a reader can take in the whole day at a glance. A wide illustrated lead takes the top of the page, its picture on the left and the headline and summary on the right; below it, twelve uniform picture cards fill a 4×3 grid; a single-line ALSO TODAY strip and a footer close the page. Headlines sit in a bold serif face, kickers and the strip in a small red sans, summaries in a quiet grey — the same visual grammar on every card, so the eye can scan the grid quickly.

Every pictured story carries its own illustration — thirteen pictures in total, stored in `assets/` as `lead.jpg` plus `g1.jpg` through `g12.jpg`, one per story, each 1920×1280. They are AI-generated pictures made to match what each story is about: a drone and a tower for Riyadh, a ship at sea for the Gulf of Finland, a rocket on the pad for Shenzhou-24, a flooded mine shaft for Pongkor, and so on. The footer states this honestly — "Pictures are AI-generated illustrations." — and nothing on the page pretends to be a photograph of the real event.

The build is deterministic. The script centre-crops every picture to its frame, draws the text with fixed DejaVu fonts, and writes the PNG with no timestamps or random elements, so running it twice on the same assets produces byte-identical output. You can check this yourself by running `python3 main.py` twice into two different output folders and comparing the two files' hashes. The headlines and summaries were verified against wire reports and same-day coverage published on 25 November 2026; the dates, casualty counts and scores on the page are the figures reported that day.

## Files

- `main.py` — the entry program. It builds the page end to end and exits 0 on success.
- `assets/` — the thirteen illustrations, one per pictured story.
- `LICENSE` — MIT.
