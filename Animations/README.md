# Animations
This folder contains the known animations for Emo.

Animation docs were generated from:
- https://raw.githubusercontent.com/JoVe13/Emo-Scripts/refs/heads/main/all_animations.txt

## File naming
- Format: `<category>_<animation>.md`
- Examples:
	- `emotions_hug.md`
	- `daily_jump_up.md`
	- `v3_1_0_fried_chicken.md`

## Inside each file
Each animation file includes:
- `category`: normalized category name used in the filename prefix.
- `animation_name`: the actual animation key to use when calling `play_animation`.
- `description`: short behavior description from the source list.

You can use `animation_name` values together with [JoVe13's animation script](https://github.com/JoVe13/Emo-Scripts/tree/main?tab=readme-ov-file#runpy).
