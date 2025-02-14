## running scrape
### test it out
1. `cd scrape`
2. `python run_scrap.py` to run the scraper
3. answer the prompt with `0` or `1` to mock or take live data once

### schedule scraping
1. open a new `tmux` session with `tmux new -s scrape`
- install tmux with homebrew if not already installed with `brew install tmux`, verify installation with `which tmux`
2. activate `venv` in this tmux session (`source venv/bin/activate`)
3. `cd scrape`
4. `python run_scrape.py` (enter 2 this time to schedule tasks)
5. hit `cntrl+b` then `d` to detach from tmux session (this allows it to keep running in the background while your computer is shut, asleep, etc.)
6. view tmux session with `tmux ls`
7. reattach to tmux session with `tmux attach -t scrape` to see scraping progress
8. kill tmux session with `tmux kill-session -t scrape`

### store data
store data generated in `out` to [google drive](https://drive.google.com/drive/folders/1XgHf5oBGeM3tbPtI-WzvOpNLY5MvlX3g?usp=sharing)