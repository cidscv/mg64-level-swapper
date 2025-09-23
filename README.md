# Mario Golf 64 Course Playlist/Randomizer Creator

A Python tool for creating custom courses in Mario Golf 64 by swapping hole geometry and par values.

## Features

- **Custom course playlist creation**: Manually select each hole from any course
- **Random course generation**: Generate 9 or 18-hole random courses

## Requirements

- Python 3.6+
- Mario Golf 64 ROM (.z64 format)
- N64 emulator for testing

## Installation

1. Download the `mg64_swapper.py` file
2. Place your Mario Golf 64 ROM in the same directory
3. Run the tool:
   ```bash
   python mg64_swapper.py
   ```

## Usage

### Quick Start

1. Run the script and enter your ROM path when prompted
2. Choose between custom or random course creation
3. Follow the interactive prompts
4. Save your custom ROM and test in an emulator

### Custom Course Creation

- Select course numbers 0-5:
  - 0: Toad Highlands
  - 1: Koopa Park
  - 2: Shy Guy Desert
  - 3: Yoshi's Island
  - 4: Boo Valley
  - 5: Mario's Star
- Choose hole numbers 1-18 from each course
- Type 'D' when done (for courses shorter than 18 holes)
- Your selections replace Toad Highlands in the game

### Random Course Generation

- Choose 9 or 18 holes
- Tool randomly selects from all available holes
- Preview generated course before applying

## How It Works

The tool modifies two key data structures in the ROM:

1. **Resource Table** (0xE473F0): Contains pointers to hole geometry data

   - Each hole has 7 components: vtx, dtx, objects, conditions, pins, triangles, surface
   - Tool swaps these pointers between holes

2. **Runtime Par Table** (0x9C800): Contains par values used during gameplay
   - Uses formula: `HoleParTable + 20 + 200 * course + 10 * hole`
   - Updates actual par values that affect scoring

## Course Mapping

The game stores holes in a non-sequential order. The tool handles the complex mapping between:

- Hole indices (0-144)
- Course and hole numbers (Course 0-5, Holes 1-18)
- Internal data structures

## Technical Details

### File Structure

- `mg64_swapper.py`: Main program
- Input: Original Mario Golf 64 ROM
- Output: Modified ROM with custom course

- `rn64crc.exe`: Required to update checksum so the game will run in emulator

### Memory Layout

```
ROM Structure:
├── 0x9C800: Runtime Par Table
├── 0xE473F0: Resource Table Start
├── 0xE493A8: Level Data Section End
└── 0xE4C078: Full Resource Table End
```

## Limitations

- Only replaces Toad Highlands course
- Requires original Mario Golf 64 ROM

## Troubleshooting

**"ROM file not found"**

- Ensure ROM is in the same directory as the script
- Check ROM filename matches your input

**"Unknown hole index"**

- All main holes 0-107 are supported

## Example

```
Mario Golf 64 Interactive Course Creator
======================================

Enter ROM path: baserom.z64
Loaded ROM: 25165824 bytes

What would you like to create?
1. Custom course (choose each hole)
2. Random course (9 or 18 holes)

Choice: 1

--- Hole 1 ---
Enter course number (0-5) for hole 1, or 'D' to finish: 1
Selected: Koopa Park
Enter hole number (1-18) from Koopa Park: 5
Selected: Koopa Park Hole 5

--- Hole 2 ---
Enter course number (0-5) for hole 2, or 'D' to finish: 3
Selected: Yoshi's Island
Enter hole number (1-18) from Yoshi's Island: 12
Selected: Yoshi's Island Hole 12

...

Course Summary (18 holes):
  Hole  1: Koopa Park Hole 5
  Hole  2: Yoshi's Island Hole 12
  ...

Create this course? (y/n): y
Save ROM as: my_custom_course.z64
Custom course created! Load 'my_custom_course.z64' in your emulator.
```

## Credits

- Reverse engineering research from hack64.net wiki contributors
- Original level import/export tool by DeathBasket
- RN64CRC Tool found (https://www.smwcentral.net/?p=section&a=details&id=8799 **website not currently available as of 2025/09/22**)

## License

Educational/research purposes. Requires original Mario Golf 64 ROM.
See LICENSE for more details
