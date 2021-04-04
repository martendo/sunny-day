# Sunny Day! Map Data Format
The .smd (**S**unny Day! **M**ap **D**ata) files contain data for the level map and enemy placements.

Tile type IDs are defined by the `TYPES` tuple in [block.py](/game/block.py) and the enemy type IDs are defined by the `TYPES` tuple in [enemy.py](/game/enemy.py).

All multi-byte numbers are little-endian.

---

The file is made up of the following:
<table>
  <thead>
    <tr>
      <th colspan="3">.smd File</th>
    </tr>
    <tr>
      <th>Name</th>
      <th>Size</th>
      <th>Content</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Width</td>
      <td>2 bytes</td>
      <td>Width of the map in number of tiles</td>
    </tr>
    <tr>
      <td>Height</td>
      <td>2 bytes</td>
      <td>Height of the map in number of tiles</td>
    </tr>
    <tr>
      <td>Tilemap</td>
      <td>Width × Height bytes</td>
      <td>Map of tile type IDs, representing the map</td>
    </tr>
    <tr>
      <td>Number of Enemies</td>
      <td>2 bytes</td>
      <td>Number of enemies on this map</td>
    </tr>
    <tr>
      <td>Enemy Entries</td>
      <td>Enemy Entry × Number of Enemies</td>
      <td>Data for the enemies to place on the map</td>
    </tr>
  </tbody>
</table>

An Enemy Entry looks like this:
<table>
  <thead>
    <tr>
      <th colspan="3">Enemy Entry</th>
    </tr>
    <tr>
      <th>Name</th>
      <th>Size</th>
      <th>Content</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Enemy Type</td>
      <td>1 byte</td>
      <td>The integer type ID of the enemy</td>
    </tr>
    <tr>
      <td>X Position</td>
      <td>2 bytes</td>
      <td>The X position of the enemy relative to the map, in tiles</td>
    </tr>
    <tr>
      <td>Y Position</td>
      <td>2 bytes</td>
      <td>The Y position of the enemy relative to the map, in tiles</td>
    </tr>
  </tbody>
</table>
