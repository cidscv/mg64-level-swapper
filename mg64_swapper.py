#!/usr/bin/env python3
"""
Mario Golf 64 Course Mapper & Randomizer
Interactive tool for creating custom courses and random hole selections
"""

import struct
import random
from typing import List, Dict, Tuple, Optional

class MarioGolf64CourseMapper:
    def __init__(self, rom_path: str):
        self.rom_path = rom_path
        self.rom_data = None
        
        # Resource table constants
        self.RESOURCE_TABLE_START = 0xE473F0
        self.RESOURCE_TABLE_END = 0xE493A8
        self.ENTRY_SIZE = 8
        
        # Hole mapping data
        self.hole_map = self._build_hole_map()
        self.course_holes = self._build_course_holes()
        
        # Load ROM
        self.load_rom()
    
    def _build_hole_map(self) -> Dict[int, str]:
        """Build the complete hole mapping from the provided data"""
        return {
            0: "Koopa Park Hole 1", 1: "Toad Highlands Hole 8", 2: "Toad Highlands Hole 5", 3: "Koopa Park Hole 4",
            4: "Koopa Park Hole 5", 5: "Koopa Park Hole 6", 6: "Koopa Park Hole 7", 7: "Koopa Park Hole 8",
            8: "Koopa Park Hole 9", 9: "Koopa Park Hole 10", 10: "Koopa Park Hole 11", 11: "Koopa Park Hole 12",
            12: "Koopa Park Hole 13", 13: "Koopa Park Hole 14", 14: "Koopa Park Hole 15", 15: "Koopa Park Hole 16",
            16: "Koopa Park Hole 17", 17: "Koopa Park Hole 18", 18: "Boo Valley Hole 1", 19: "Boo Valley Hole 2",
            20: "Boo Valley Hole 3", 21: "Boo Valley Hole 4", 22: "Boo Valley Hole 5", 23: "Boo Valley Hole 6",
            24: "Boo Valley Hole 7", 25: "Boo Valley Hole 8", 26: "Boo Valley Hole 9", 27: "Boo Valley Hole 10",
            28: "Boo Valley Hole 11", 29: "Boo Valley Hole 12", 30: "Boo Valley Hole 13", 31: "Boo Valley Hole 14",
            32: "Boo Valley Hole 15", 33: "Boo Valley Hole 16", 34: "Boo Valley Hole 17", 35: "Boo Valley Hole 18",
            36: "Toad Highlands Hole 1", 37: "Toad Highlands Hole 13", 38: "Toad Highlands Hole 3", 39: "Toad Highlands Hole 16",
            40: "Koopa Park Hole 3", 41: "Toad Highlands Hole 6", 42: "Toad Highlands Hole 7", 43: "Koopa Park Hole 2",
            44: "Toad Highlands Hole 9", 45: "Toad Highlands Hole 10", 46: "Toad Highlands Hole 11", 47: "Toad Highlands Hole 12",
            48: "Toad Highlands Hole 2", 49: "Toad Highlands Hole 14", 50: "Toad Highlands Hole 15", 51: "Toad Highlands Hole 4",
            52: "Toad Highlands Hole 17", 53: "Toad Highlands Hole 18", 54: "Shy Guy Desert Hole 18", 55: "Shy Guy Desert Hole 4",
            56: "Shy Guy Desert Hole 11", 57: "Shy Guy Desert Hole 16", 58: "Shy Guy Desert Hole 1", 59: "Shy Guy Desert Hole 10",
            60: "Shy Guy Desert Hole 6", 61: "Shy Guy Desert Hole 5", 62: "Shy Guy Desert Hole 2", 63: "Shy Guy Desert Hole 7",
            64: "Shy Guy Desert Hole 12", 65: "Shy Guy Desert Hole 15", 66: "Shy Guy Desert Hole 3", 67: "Shy Guy Desert Hole 14",
            68: "Shy Guy Desert Hole 17", 69: "Shy Guy Desert Hole 9", 70: "Shy Guy Desert Hole 13", 71: "Shy Guy Desert Hole 8",
            72: "Yoshi's Island Hole 1", 73: "Yoshi's Island Hole 2", 74: "Yoshi's Island Hole 3", 75: "Yoshi's Island Hole 4",
            76: "Yoshi's Island Hole 5", 77: "Yoshi's Island Hole 6", 78: "Yoshi's Island Hole 7", 79: "Yoshi's Island Hole 8",
            80: "Yoshi's Island Hole 9", 81: "Yoshi's Island Hole 10", 82: "Yoshi's Island Hole 11", 83: "Yoshi's Island Hole 12",
            84: "Yoshi's Island Hole 13", 85: "Yoshi's Island Hole 14", 86: "Yoshi's Island Hole 15", 87: "Yoshi's Island Hole 16",
            88: "Yoshi's Island Hole 17", 89: "Yoshi's Island Hole 18", 90: "Mario's Star Hole 11", 91: "Mario's Star Hole 9",
            92: "Mario's Star Hole 1", 93: "Mario's Star Hole 4", 94: "Mario's Star Hole 14", 95: "Mario's Star Hole 7",
            96: "Mario's Star Hole 13", 97: "Mario's Star Hole 5", 98: "Mario's Star Hole 15", 99: "Mario's Star Hole 8",
            100: "Mario's Star Hole 12", 101: "Mario's Star Hole 3", 102: "Mario's Star Hole 6", 103: "Mario's Star Hole 17",
            104: "Mario's Star Hole 16", 105: "Mario's Star Hole 10", 106: "Mario's Star Hole 2", 107: "Mario's Star Hole 18",
            108: "Luigi's Garden Hole 1", 109: "Luigi's Garden Hole 2", 110: "Luigi's Garden Hole 3", 111: "Luigi's Garden Hole 4",
            112: "Luigi's Garden Hole 5", 113: "Luigi's Garden Hole 6", 114: "Luigi's Garden Hole 7", 115: "Luigi's Garden Hole 8",
            116: "Luigi's Garden Hole 9", 117: "Luigi's Garden Hole 10", 118: "Luigi's Garden Hole 11", 119: "Luigi's Garden Hole 12",
            120: "Luigi's Garden Hole 13", 121: "Luigi's Garden Hole 14", 122: "Luigi's Garden Hole 15", 123: "Luigi's Garden Hole 16",
            124: "Luigi's Garden Hole 17", 125: "Luigi's Garden Hole 18", 126: "Peach's Castle Hole 1", 127: "Peach's Castle Hole 2",
            128: "Peach's Castle Hole 3", 129: "Peach's Castle Hole 4", 130: "Peach's Castle Hole 5", 131: "Peach's Castle Hole 6",
            132: "Peach's Castle Hole 7", 133: "Peach's Castle Hole 8", 134: "Peach's Castle Hole 9", 135: "Peach's Castle Hole 10",
            136: "Peach's Castle Hole 11", 137: "Peach's Castle Hole 12", 138: "Peach's Castle Hole 13", 139: "Peach's Castle Hole 14",
            140: "Peach's Castle Hole 15", 141: "Peach's Castle Hole 16", 142: "Peach's Castle Hole 17", 143: "Peach's Castle Hole 18",
            144: "Intro Preview Course"
        }
    
    def _build_course_holes(self) -> Dict[str, List[int]]:
        """Build a mapping of course names to their hole indices"""
        courses = {}
        for index, description in self.hole_map.items():
            course_name = description.split(" Hole ")[0]
            if course_name not in courses:
                courses[course_name] = []
            courses[course_name].append(index)
        
        # Sort holes by hole number for each course
        for course in courses:
            courses[course].sort(key=lambda x: self._get_hole_number(self.hole_map[x]))

        return courses
    
    def _get_hole_number(self, description: str) -> int:
        """Extract hole number from description"""
        try:
            return int(description.split(" Hole ")[1])
        except:
            return 999
    
    def _get_toad_highlands_indices(self) -> List[int]:
        """Get the original Toad Highlands hole indices in order 1-18"""
        toad_holes = []
        for hole_num in range(1, 19):
            for index, description in self.hole_map.items():
                if description == f"Toad Highlands Hole {hole_num}":
                    toad_holes.append(index)
                    break
        return toad_holes
    
    def load_rom(self):
        """Load the ROM file into memory"""
        try:
            with open(self.rom_path, 'rb') as f:
                self.rom_data = bytearray(f.read())
            print(f"Loaded ROM: {len(self.rom_data)} bytes")
            return True
        except FileNotFoundError:
            print(f"Error: ROM file not found: {self.rom_path}")
            return False
    
    def save_rom(self, output_path: str):
        """Save the modified ROM"""
        with open(output_path, 'wb') as f:
            f.write(self.rom_data)
        print(f"ROM saved to: {output_path}")
    
    def read_resource_entry(self, entry_index: int) -> Tuple[int, int]:
        """Read a resource table entry"""
        offset = self.RESOURCE_TABLE_START + (entry_index * self.ENTRY_SIZE)
        
        if offset >= self.RESOURCE_TABLE_END:
            raise ValueError(f"Entry index {entry_index} is outside the level data section")
        
        data_length = struct.unpack('>I', self.rom_data[offset:offset+4])[0]
        data_offset = struct.unpack('>I', self.rom_data[offset+4:offset+8])[0]
        
        return data_length, data_offset
    
    def write_resource_entry(self, entry_index: int, data_length: int, data_offset: int):
        """Write a resource table entry"""
        offset = self.RESOURCE_TABLE_START + (entry_index * self.ENTRY_SIZE)
        
        if offset >= self.RESOURCE_TABLE_END:
            raise ValueError(f"Entry index {entry_index} is outside the level data section")
        
        struct.pack_into('>I', self.rom_data, offset, data_length)
        struct.pack_into('>I', self.rom_data, offset + 4, data_offset)
    
    def swap_holes(self, hole1_index: int, hole2_index: int):
        """Swap two holes by swapping their resource table entries"""
        # Get entry ranges for both holes (7 components per hole)
        hole1_start = hole1_index * 7
        hole2_start = hole2_index * 7
        
        # Swap each component
        for component in range(7):
            entry1_idx = hole1_start + component
            entry2_idx = hole2_start + component
            
            # Read both entries
            length1, offset1 = self.read_resource_entry(entry1_idx)
            length2, offset2 = self.read_resource_entry(entry2_idx)
            
            # Swap them
            self.write_resource_entry(entry1_idx, length2, offset2)
            self.write_resource_entry(entry2_idx, length1, offset1)
        
        return True
    
    def display_courses(self):
        """Display available courses and their holes"""
        print("\n=== AVAILABLE COURSES ===")
        for i, (course_name, holes) in enumerate(self.course_holes.items(), 1):
            if course_name != "Intro Preview Course":
                print(f"{i:2d}. {course_name:<20} ({len(holes)} holes)")
    
    def display_course_holes(self, course_name: str):
        """Display holes for a specific course"""
        if course_name in self.course_holes:
            holes = self.course_holes[course_name]
            print(f"\n{course_name} holes:")
            for hole_index in holes:
                hole_desc = self.hole_map[hole_index]
                hole_num = self._get_hole_number(hole_desc)
                print(f"  {hole_num:2d}. Index {hole_index:3d} - {hole_desc}")
    
    def get_user_hole_selection(self) -> Optional[int]:
        """Get hole selection from user input"""
        return self._select_by_course_and_hole()
    
    def _select_by_course_and_hole(self) -> Optional[int]:
        """Select hole by course name and hole number"""
        print("\nAvailable courses:")
        course_list = [name for name in self.course_holes.keys() if name != "Intro Preview Course"]
        for i, course in enumerate(course_list, 1):
            print(f"{i}. {course}")
        
        try:
            course_choice = int(input("Select course number: ")) - 1
            if 0 <= course_choice < len(course_list):
                course_name = course_list[course_choice]
                hole_num = int(input(f"Select hole number (1-18) for {course_name}: "))
                
                # Find the index for this course and hole
                target_desc = f"{course_name} Hole {hole_num}"
                for index, desc in self.hole_map.items():
                    if desc == target_desc:
                        return index
                
                print(f"Hole {hole_num} not found for {course_name}")
            else:
                print("Invalid course selection")
        except ValueError:
            print("Please enter valid numbers")
        
        return None
    
    def _show_course_holes(self):
        """Show holes for a specific course"""
        course_name = input("Enter course name (e.g., 'Koopa Park'): ").strip()
        found_course = None
        
        for course in self.course_holes.keys():
            if course.lower() == course_name.lower():
                found_course = course
                break
        
        if found_course:
            self.display_course_holes(found_course)
        else:
            print(f"Course '{course_name}' not found")
            self.display_courses()
    
    def create_custom_course(self):
        """Interactive course creation"""
        print("\n" + "="*60)
        print("MARIO GOLF 64 CUSTOM COURSE CREATOR")
        print("="*60)
        print("\nThis will replace Toad Highlands holes with your selections.")
        print("You can select up to 18 holes, or type 'D' when done.")
        
        toad_indices = self._get_toad_highlands_indices()
        custom_holes = []
        
        for hole_num in range(1, 19):
            print(f"\n--- HOLE {hole_num} ---")
            
            user_input = input(f"Press Enter to replace hole {hole_num} or 'D' to finish: ").strip()
            
            if user_input.upper() == 'D':
                break
            
            # Get their hole selection
            selected_index = self.get_user_hole_selection()
            
            if selected_index is not None:
                custom_holes.append(selected_index)
                print(f"Hole {hole_num}: {self.hole_map[selected_index]}")
            else:
                # If selection failed, keep original
                custom_holes.append(toad_indices[hole_num-1])
                print(f"Selection failed, keeping original: {self.hole_map[toad_indices[hole_num-1]]}")
        
        return custom_holes, toad_indices[:len(custom_holes)]
    
    def create_random_course(self):
        """Create a random course"""
        print("\n" + "="*60)
        print("MARIO GOLF 64 RANDOM COURSE GENERATOR")
        print("="*60)
        
        # Ask for 9 or 18 holes
        while True:
            num_holes = input("Generate 9 or 18 holes? (9/18): ").strip()
            if num_holes in ["9", "18"]:
                num_holes = int(num_holes)
                break
            print("Please enter 9 or 18")
        
        # Get all available holes (excluding practice course)
        available_holes = [idx for idx, desc in self.hole_map.items() 
                          if "Intro Preview" not in desc and idx < 108]
        print(available_holes)
        # Generate random selection
        random_holes = random.sample(available_holes, num_holes)
        
        print(f"\nGenerated {num_holes} random holes:")
        for i, hole_idx in enumerate(random_holes, 1):
            print(f"  Hole {i:2d}: {self.hole_map[hole_idx]}")
        
        # Get corresponding Toad Highlands holes to replace
        toad_indices = self._get_toad_highlands_indices()[:num_holes]
        
        return random_holes, toad_indices
    
    def apply_course_changes(self, new_holes: List[int], target_holes: List[int]):
        """Apply the course changes to the ROM"""
        print(f"\nApplying {len(new_holes)} hole changes...")
        
        changes_made = []
        for i, (new_hole, target_hole) in enumerate(zip(new_holes, target_holes)):
            if new_hole != target_hole:  # Only swap if different
                self.swap_holes(target_hole, new_hole)
                changes_made.append((i+1, target_hole, new_hole))
                print(f"  Hole {i+1}: {self.hole_map[target_hole]} → {self.hole_map[new_hole]}")
            else:
                print(f"  Hole {i+1}: Keeping {self.hole_map[target_hole]}")
        
        return changes_made
    
    def main_menu(self):
        """Main interactive menu"""
        print("\n" + "="*60)
        print("MARIO GOLF 64 COURSE MAPPER & RANDOMIZER 🏌️")
        print("="*60)
        
        while True:
            print("\nWhat would you like to do?")
            print("1. Create custom course (manual selection)")
            print("2. Generate random course")
            print("3. View available courses")
            print("4. Exit")
            
            choice = input("\nChoice (1-4): ").strip()
            
            if choice == "1":
                new_holes, target_holes = self.create_custom_course()
                
                if new_holes:
                    print(f"\nCOURSE SUMMARY:")
                    for i, hole_idx in enumerate(new_holes, 1):
                        print(f"  Hole {i:2d}: {self.hole_map[hole_idx]}")
                    
                    confirm = input("\nApply these changes? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.apply_course_changes(new_holes, target_holes)
                        
                        filename = input("\nSave ROM as (e.g., 'my_custom_course.z64'): ").strip()
                        if filename:
                            self.save_rom(filename)
                            print(f"🎉 Custom course created! Load '{filename}' in your emulator.")
                        break
                    else:
                        print("Changes cancelled.")
                else:
                    print("No changes made.")
            
            elif choice == "2":
                new_holes, target_holes = self.create_random_course()
                
                confirm = input(f"\nApply this random {len(new_holes)}-hole course? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.apply_course_changes(new_holes, target_holes)
                    
                    filename = input("\nSave ROM as: ('random_course.z64') ").strip()
                    if filename:
                        self.save_rom(filename)
                        print(f"Random course created! Load '{filename}' in your emulator.")
                    else:
                        self.save_rom('random_course.z64')
                    break
                else:
                    print("Random course cancelled.")
            
            elif choice == "3":
                self.display_courses()
                
                course_name = input("\nView holes for which course? (or Enter to continue): ").strip()
                if course_name:
                    self._show_course_holes()
            
            elif choice == "4":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")

# Main execution
if __name__ == "__main__":
    print("Mario Golf 64 Course Mapper & Randomizer")
    print("=" * 50)
    
    rom_path = input("Enter ROM path (or 'baserom.z64'): ").strip()
    if not rom_path:
        rom_path = "baserom.z64"
    
    mapper = MarioGolf64CourseMapper(rom_path)
    
    if mapper.rom_data:
        mapper.main_menu()
    else:
        print("Failed to load ROM. Please check the file path.")