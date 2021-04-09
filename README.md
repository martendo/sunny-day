# Sunny Day!
A pygame platformer game!

Made for the 2021 PETCS Game Jam.

See [this release](https://github.com/martendo7/sunny-day/releases/tag/v1.0.0) for the state the game was in at the time of submission.

## Running the Game
Requirements:
- Python 3
- Pygame

Run the following command in the root directory of the repository to run the game:
```bash
python -m sunny-day
```

## Controls
<table>
  <thead>
    <tr>
      <th>Key</th>
      <th>Function</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><kbd>A</kbd> <kbd>D</kbd></td>
      <td>Move left/right</td>
    </tr>
    <tr>
      <td><kbd>Space</kbd></td>
      <td>Jump</td>
    </tr>
    <tr>
      <td><kbd>Left Shift</kbd></td>
      <td>Run</td>
    </tr>
    <tr>
      <td><kbd>S</kbd></td>
      <td>Crouch</td>
    </tr>
    <tr>
      <td><kbd>Escape</kbd></td>
      <td>Exit level</td>
    </tr>
  </tbody>
</table>

## Save File Format
Save files (.sds files) are just a JSON-serialized dict in the following format. Knock yourself out.
```python
{
    "last_completed_level": <int in range(0, Game.LEVEL_COUNT + 1)>,
    "lives": <int>,
    "coins": <int>,
}
```
