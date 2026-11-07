# HackerTok

The YouTube videos Hacker News keeps recommending, as a vertical scroll feed. Every video drops you in at a random minute, and the comments are the real HN comments that recommended it.

- Scroll (or `j`/`k`) for the next video, double-tap or `l` to save, `c` for comments, `r` to jump to another random minute, `f` to switch between fill-screen and the whole video.
- No accounts. Saved videos live only in your browser.

## Run it

It's a static site with no build step:

```bash
python3 -m http.server 8417 --directory site
```

Then open http://localhost:8417.

## Data

`site/data/` is generated from the [HackerTube](https://hackertube.org) dataset:

1. Download `hackertube-data.zip` from https://hackertube.org/data and unzip it into `data/raw/`.
2. Run `python3 scripts/build_data.py`.

## Credits

Data from [HackerTube](https://hackertube.org) (ODC-By 1.0), built on the [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news) archive. Hacker News comments remain the work of their authors; videos belong to their creators and play through YouTube's embedded player.

Not affiliated with YouTube, Google, TikTok, Hacker News or Y Combinator.
