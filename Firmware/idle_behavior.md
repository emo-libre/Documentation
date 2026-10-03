# Idle Behavior

What EMO does by himself when nobody is interacting with him: exploring, free play, staying vigilant, sleeping. How animations are played and interrupted is covered in [Animation system](animation_system.md). The behaviors EMO runs on cloud command (the `rec_behavior` values) are in [/Behaviors](/Behaviors).

Source: `ghidraExtracted-elfPartition1.c`. See the [evidence legend](README.md#evidence-legend). All animation names and addresses below are Confirmed strings. The decision logic in §7–8 is **Inferred**.

---

## 1. Behavior task

| Name | Address | Purpose |
| --- | --- | --- |
| `behavior_task` | `0x3f4288ac` | Main autonomous-behavior loop; function `FUN_401e116c` (at `0x401e11c4`) |
| `behavior_paras` | `0x3f40f632` | NVS: behavior configuration |
| `rec_behavior` | `0x3f40f715` | NVS: recorded behavior / history (also the field name in [intent responses](/Intents)) |
| `show_index` | | NVS: current show/mode index |

Idle state management: `FUN_401ffb14`, with fallback `"something wrong, goto idle\r"` (`0x3f4316ae`).

Mode strings: `explore` (`0x3f40f9d6`), `play_around` (`0x3f40f9de`), `anime_boy` (`0x3f40f9cc`), `tree_sleep_and_wake_up` (`0x3f40f9f4`), `tree_search_and_interact` (`0x3f40fa0b`), `wake_up` (`0x3f40fa03`).

---

## 2. Idle animations per music role

When EMO is in a [Bluetooth speaker](/Bluetooth) role:

- DJ: `DJ1_idle1` (`0x3f43151f`), `DJ1_idle2` (`0x3f431529`)
- Partygoer: `Partygoer_idle1` (`0x3f431533`)
- Singer: `Singer_idle1` (`0x3f431543`)

---

## 3. Exploration behaviors

### Look around

`look_around_1` (`0x3f42abec`), `look_around_2` (`0x3f42abfa`), `look_around_4` (`0x3f42ac08`), `look_around_5` (`0x3f42ac16`), `look_around_6` (`0x3f42ac24`), `look_around_7` (`0x3f42ac32`), `look_around_8` (`0x3f42ac40`), `turn_around_look_around_v05` (`0x3f42a4e8`)

No `look_around_3` was found.

### Explore play

`explore_play1` … `explore_play18` (18 variants, `0x3f42ac4e`–`0x3f42aca4`; e.g. `explore_play2` = `0x3f42b447`, `explore_play3` = `0x3f42b455`)

### Explore movement

| Movement | Animations |
| --- | --- |
| Turn left | `explore_turn_left1` (`0x3f42b525`), `explore_turn_left2` (`0x3f42b538`), `explore_turn_left3` (`0x3f42b54b`) |
| Turn right | `explore_turn_right1` (`0x3f42b55e`), `explore_turn_right2` (`0x3f42b572`), `explore_turn_right3` (`0x3f42b586`) |
| Forward | `explore_foward1` (`0x3f42b59a`), `explore_foward2` (`0x3f42b5aa`), `explore_foward3` (`0x3f42b5ba`) |
| Back away | `explore_back_away1` (`0x3f42b5ca`), `explore_back_away2` (`0x3f42b5dd`), `explore_back_away3` (`0x3f42b5f0`) |
| Up/down | `explore_updown1` (`0x3f42b603`), `explore_updown2` (`0x3f42b613`), `explore_updown3` (`0x3f42b623`), `explore_updown4` (`0x3f42b633`) |

(`foward` is spelled that way in the firmware.)

---

## 4. Free play

`free_play1` … `free_play17` (17 variants, `0x3f42b384`–`0x3f42b43b`; e.g. `free_play2` = `0x3f42b38f`, `free_play3` = `0x3f42b39a`)

---

## 5. Vigilant

`keep_vigilant1` (`0x3f42b84c`) has 20+ references in the code and looks like the default "watching" state.

---

## 6. Sleep and wake-up

| Phase | Animations |
| --- | --- |
| Getting in | `sleep_get_in` (`0x3f431871`), `sleep_get_in_slow` (`0x3f42b1b2`), `sleep_get_in_fast` (`0x3f42b1c4`), `sleep_get_in_Doze_off` (`0x3f42b1d6`) |
| Loop | `sleep_loop_1` (`0x3f42b105`), `sleep_loop_2` (`0x3f42b112`), `sleep_still` (`0x3f43188b`) |
| Breathing | `sleep_breath` (`0x3f43187e`), `sleep_breath_1` (`0x3f42b143`), `sleep_breath_2` (`0x3f42b152`), `sleep_yawn` (`0x3f42b161`) |
| Effects | `sleep_Fireflies_1` (`0x3f42b11f`), `sleep_Fireflies_2` (`0x3f42b131`), `sleep_bubble_1` (`0x3f42b1ec`), `sleep_bubble_2` (`0x3f42b1fb`), `sleep_bubble_burst` (`0x3f42b16c`), `sleep_bubble_burst_sleep` (`0x3f42b17f`), `sleep_bubble_burst_wakeup` (`0x3f42b198`) |
| Peeking | `sleep_peep1` (`0x3f42ca1e`), `sleep_peep2` (`0x3f42ca2a`) |
| Waking | `sleep_wake_up_slow` (`0x3f429e9e`), `sleep_wake_up_fast` (`0x3f429eb1`), `sleep_wake_up_angry` (`0x3f429e8a`), `sleep_wake_up_after_1` (`0x3f429ec4`), `sleep_wake_up_after_2` (`0x3f429eda`) |
| Wake and fall asleep again | `sleep_wake_up_and_sleep_1` (`0x3f429ef0`), `_2` (`0x3f429f0a`), `_3` (`0x3f429f24`) |
| Sudden wake | `sleep_awake_suddenly_grievance` (`0x3f429f3e`), `sleep_awake_suddenly_panic` (`0x3f429f5d`) |
| Reminder | `reminder_sleep` (`0x3f42b045`) |

The [2.0.0 changelog](README.md#200---emo-go-home) says sleep starts at 10 PM.

### Sleep cycle (Inferred)

```
1. Long inactivity or sleep time (optionally reminder_sleep)
2. sleep_get_in_X (slow / fast / Doze_off)
3. Loop: sleep_loop_X, sleep_breath_X, sleep_Fireflies_X, sleep_bubble_X, now and then sleep_peep_X
4. Wake trigger (touch, voice, movement):
     gentle → sleep_wake_up_slow     normal → sleep_wake_up_fast
     sudden → sleep_awake_suddenly_* annoyed → sleep_wake_up_angry
     brief  → sleep_wake_up_and_sleep_X (back to step 3)
5. Back to active
```

---

## 7. Decision making (Inferred)

The likely model is a state machine that picks randomly from a pool of animations for each state:

| State | Pool |
| --- | --- |
| Vigilant | `keep_vigilant1` |
| Explore | 18 `explore_play` + 8 look around + 16 movement |
| Free play | 17 `free_play` |
| Role idle | DJ / Partygoer / Singer idles |
| Sleep | entry, loop, effects, wake (§6) |

```c
while (1) {
    state = get_behavior_state();
    anim  = select_random_from_pool(pool[state]);   // vigilant → "keep_vigilant1"
    play_animation(anim);
    wait_animation_complete();
    if (user_interaction_detected()) exit_idle();
    check_state_transition();                       // timers, probabilities, battery
}
```

Things that probably feed into the choice: time since the last interaction, weighted randomness, the current music role, sensors (obstacles), battery level (low → go home/sleep), and `rec_behavior` history to avoid repeats.

## 8. Transitions (Inferred)

- **Timers**: animation finished, idle timeout, sleep timer.
- **Sensors**: touch, foot sensors (lifted/falling), ToF (obstacle), microphone.
- **Events**: user interaction, face recognized, Bluetooth connection, low battery.

The idle progression is believed to go vigilant → explore/free play → sleep. The thresholds are **not** in the strings. The 30 s / 2 min / 5 min values seen in earlier notes are guesses.

```
[Idle] → interaction? → exit idle
   ↓ no
short idle  → Vigilant
medium idle → Explore / Free play (random)
long idle   → Sleep → wake on sensor → [Idle]
```

---

## 9. Counts

| Category | Count |
| --- | --- |
| Role idles | 4 |
| Explore play | 18 |
| Look around | 8 |
| Explore movement | 16 |
| Free play | 17 |
| Vigilant | 1 |
| Sleep (all phases, excl. reminder) | 30 |

About 94 idle-related animation names in total.
