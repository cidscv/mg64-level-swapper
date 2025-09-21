#!/usr/bin/env python3
"""
Mario Golf 64 Interactive Course Creator
Complete tool for creating custom courses with geometry and par swapping
"""

import struct
import random
from typing import List, Dict, Tuple, Optional

class MarioGolf64InteractiveCourseCreator:
    def __init__(self, rom_path: str):
        self.rom_path = rom_path
        self.rom_data = None
        
        # Resource table constants
        self.RESOURCE_TABLE_START = 0xE473F0
        self.RESOURCE_TABLE_END = 0xE493A8
        self.ENTRY_SIZE = 8
        
        # Par table constants
        self.HOLE_PAR_TABLE = 641056  # 0x9C800
        
        # Course mapping (0-5 for user selection)
        self.course_names = {
            0: "Toad Highlands",
            1: "Koopa Park", 
            2: "Shy Guy Desert",
            3: "Yoshi's Island",
            4: "Boo Valley",
            5: "Mario's Star"
        }
        
        # Complete hole mapping from your data
        self.hole_map = self._build_hole_map()
        self.course_to_indices = self._build_course_to_indices()
        
        # Load ROM
        self.load_rom()
    
    def _build_hole_map(self) -> Dict[int, str]:
        """Build the complete hole mapping"""
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
            104: "Mario's Star Hole 16", 105: "Mario's Star Hole 10", 106: "Mario's Star Hole 2", 107: "Mario's Star Hole 18"
        }
    
    def _build_course_to_indices(self) -> Dict[int, Dict[int, int]]:
        """Build mapping from course number and hole number to hole index"""
        course_mapping = {}
        
        # Initialize courses
        for course_id in range(6):
            course_mapping[course_id] = {}
        
        # Map each hole index to its course and hole number
        for hole_index, description in self.hole_map.items():
            if "Toad Highlands" in description:
                course_id = 0
            elif "Koopa Park" in description:
                course_id = 1
            elif "Shy Guy Desert" in description:
                course_id = 2
            elif "Yoshi's Island" in description:
                course_id = 3
            elif "Boo Valley" in description:
                course_id = 4
            elif "Mario's Star" in description:
                course_id = 5
            else:
                continue  # Skip practice course
            
            # Extract hole number
            hole_num = int(description.split(" Hole ")[1])
            course_mapping[course_id][hole_num] = hole_index
        
        return course_mapping
    
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
    
    def get_par_address(self, course: int, hole: int) -> int:
        """Calculate the ROM address for a hole's par value"""
        return self.HOLE_PAR_TABLE + 20 + 200 * course + 10 * hole
    
    def read_par_value(self, course: int, hole: int) -> int:
        """Read the par value for a specific course and hole"""
        address = self.get_par_address(course, hole)
        if address < len(self.rom_data):
            return self.rom_data[address]
        else:
            raise ValueError(f"Par address 0x{address:06X} is outside ROM bounds")
    
    def write_par_value(self, course: int, hole: int, par_value: int):
        """Write a par value for a specific course and hole"""
        if par_value not in [3, 4, 5]:
            raise ValueError(f"Invalid par value: {par_value}. Must be 3, 4, or 5")
        
        address = self.get_par_address(course, hole)
        if address < len(self.rom_data):
            self.rom_data[address] = par_value
        else:
            raise ValueError(f"Par address 0x{address:06X} is outside ROM bounds")
    
    def hole_index_to_course_hole(self, hole_index: int) -> tuple:
        """Convert hole index to (course, hole) for par table access"""
        hole_mapping = {
            0: (1, 0), 3: (1, 3), 4: (1, 4), 5: (1, 5), 6: (1, 6), 7: (1, 7), 8: (1, 8), 9: (1, 9),
            10: (1, 10), 11: (1, 11), 12: (1, 12), 13: (1, 13), 14: (1, 14), 15: (1, 15), 16: (1, 16), 17: (1, 17),
            40: (1, 2), 43: (1, 1), 1: (0, 7), 2: (0, 4), 36: (0, 0), 37: (0, 12), 38: (0, 2), 39: (0, 15),
            41: (0, 5), 42: (0, 6), 44: (0, 8), 45: (0, 9), 46: (0, 10), 47: (0, 11), 48: (0, 1), 49: (0, 13),
            50: (0, 14), 51: (0, 3), 52: (0, 16), 53: (0, 17), 18: (4, 0), 19: (4, 1), 20: (4, 2), 21: (4, 3),
            22: (4, 4), 23: (4, 5), 24: (4, 6), 25: (4, 7), 26: (4, 8), 27: (4, 9), 28: (4, 10), 29: (4, 11),
            30: (4, 12), 31: (4, 13), 32: (4, 14), 33: (4, 15), 34: (4, 16), 35: (4, 17), 54: (2, 17), 55: (2, 3),
            56: (2, 10), 57: (2, 15), 58: (2, 0), 59: (2, 9), 60: (2, 5), 61: (2, 4), 62: (2, 1), 63: (2, 6),
            64: (2, 11), 65: (2, 14), 66: (2, 2), 67: (2, 13), 68: (2, 16), 69: (2, 8), 70: (2, 12), 71: (2, 7),
            72: (3, 0), 73: (3, 1), 74: (3, 2), 75: (3, 3), 76: (3, 4), 77: (3, 5), 78: (3, 6), 79: (3, 7),
            80: (3, 8), 81: (3, 9), 82: (3, 10), 83: (3, 11), 84: (3, 12), 85: (3, 13), 86: (3, 14), 87: (3, 15),
            88: (3, 16), 89: (3, 17), 90: (5, 10), 91: (5, 8), 92: (5, 0), 93: (5, 3), 94: (5, 13), 95: (5, 6),
            96: (5, 12), 97: (5, 4), 98: (5, 14), 99: (5, 7), 100: (5, 11), 101: (5, 2), 102: (5, 5), 103: (5, 16),
            104: (5, 15), 105: (5, 9), 106: (5, 1), 107: (5, 17)
        }
        
        if hole_index in hole_mapping:
            return hole_mapping[hole_index]
        else:
            raise ValueError(f"Unknown hole index: {hole_index}")
    
    def swap_holes_complete(self, hole1_index: int, hole2_index: int):
        """Swap two holes completely (geometry + par)"""
        # Swap geometry (7 components per hole)
        hole1_start = hole1_index * 7
        hole2_start = hole2_index * 7
        
        for component in range(7):
            entry1_idx = hole1_start + component
            entry2_idx = hole2_start + component
            
            # Read both entries
            offset = self.RESOURCE_TABLE_START + (entry1_idx * self.ENTRY_SIZE)
            length1 = struct.unpack('>I', self.rom_data[offset:offset+4])[0]
            offset1 = struct.unpack('>I', self.rom_data[offset+4:offset+8])[0]
            
            offset = self.RESOURCE_TABLE_START + (entry2_idx * self.ENTRY_SIZE)
            length2 = struct.unpack('>I', self.rom_data[offset:offset+4])[0]
            offset2 = struct.unpack('>I', self.rom_data[offset+4:offset+8])[0]
            
            # Swap them
            offset = self.RESOURCE_TABLE_START + (entry1_idx * self.ENTRY_SIZE)
            struct.pack_into('>I', self.rom_data, offset, length2)
            struct.pack_into('>I', self.rom_data, offset + 4, offset2)
            
            offset = self.RESOURCE_TABLE_START + (entry2_idx * self.ENTRY_SIZE)
            struct.pack_into('>I', self.rom_data, offset, length1)
            struct.pack_into('>I', self.rom_data, offset + 4, offset1)
        
        # Swap par values
        try:
            course1, hole_num1 = self.hole_index_to_course_hole(hole1_index)
            course2, hole_num2 = self.hole_index_to_course_hole(hole2_index)
            
            par1 = self.read_par_value(course1, hole_num1)
            par2 = self.read_par_value(course2, hole_num2)
            
            self.write_par_value(course1, hole_num1, par2)
            self.write_par_value(course2, hole_num2, par1)
            
        except ValueError as e:
            print(f"Par swap failed: {e}")
    
    def get_toad_highlands_indices(self) -> List[int]:
        """Get Toad Highlands hole indices in order 1-18"""
        toad_holes = []
        for hole_num in range(1, 19):
            if hole_num in self.course_to_indices[0]:
                toad_holes.append(self.course_to_indices[0][hole_num])
        return toad_holes
    
    def display_courses(self):
        """Display available courses"""
        print("\nAvailable courses:")
        for course_id, course_name in self.course_names.items():
            print(f"{course_id}. {course_name}")
    
    def get_hole_selection(self, hole_number: int) -> Optional[int]:
        """Get user selection for a specific hole"""
        while True:
            print(f"\n--- Hole {hole_number} ---")
            course_input = input(f"Enter course number (0-5) for hole {hole_number}, or 'D' to finish: ").strip()
            
            if course_input.upper() == 'D':
                return None
            
            try:
                course_id = int(course_input)
                if course_id not in self.course_names:
                    print("Invalid course number. Please enter 0-5.")
                    continue
                
                print(f"Selected: {self.course_names[course_id]}")
                
                hole_input = input(f"Enter hole number (1-18) from {self.course_names[course_id]}: ").strip()
                hole_num = int(hole_input)
                
                if hole_num < 1 or hole_num > 18:
                    print("Invalid hole number. Please enter 1-18.")
                    continue
                
                if hole_num not in self.course_to_indices[course_id]:
                    print(f"Hole {hole_num} not found in {self.course_names[course_id]}")
                    continue
                
                hole_index = self.course_to_indices[course_id][hole_num]
                hole_description = self.hole_map[hole_index]
                print(f"Selected: {hole_description}")
                
                return hole_index
                
            except ValueError:
                print("Please enter valid numbers.")
    
    def create_custom_course(self):
        """Interactive custom course creation"""
        print("\n" + "="*60)
        print("CUSTOM COURSE CREATOR")
        print("="*60)
        print("This will replace Toad Highlands with your custom selection.")
        print("Enter course and hole for each position, or 'D' when done.")
        
        toad_indices = self.get_toad_highlands_indices()
        custom_holes = []
        
        for hole_position in range(1, 19):
            selected_index = self.get_hole_selection(hole_position)
            
            if selected_index is None:
                break
            
            custom_holes.append(selected_index)
        
        return custom_holes, toad_indices[:len(custom_holes)]
    
    def create_random_course(self):
        """Create a random course"""
        print("\n" + "="*60)
        print("RANDOM COURSE GENERATOR")
        print("="*60)
        
        while True:
            num_holes = input("Generate 9 or 18 holes? (9/18): ").strip()
            if num_holes in ["9", "18"]:
                num_holes = int(num_holes)
                break
            print("Please enter 9 or 18")
        
        # Get all available holes (excluding practice)
        available_holes = [idx for idx in self.hole_map.keys() if idx <= 107]
        
        # Generate random selection
        random_holes = random.sample(available_holes, num_holes)
        
        print(f"\nGenerated {num_holes} random holes:")
        for i, hole_idx in enumerate(random_holes, 1):
            print(f"  Hole {i:2d}: {self.hole_map[hole_idx]}")
        
        toad_indices = self.get_toad_highlands_indices()[:num_holes]
        
        return random_holes, toad_indices
    
    def apply_course_changes(self, new_holes: List[int], target_holes: List[int]):
        """Apply course changes to the ROM"""
        print(f"\nApplying {len(new_holes)} hole changes...")
        
        for i, (new_hole, target_hole) in enumerate(zip(new_holes, target_holes)):
            if new_hole != target_hole:
                self.swap_holes_complete(target_hole, new_hole)
                print(f"  Hole {i+1}: {self.hole_map[target_hole]} -> {self.hole_map[new_hole]}")
            else:
                print(f"  Hole {i+1}: Keeping {self.hole_map[target_hole]}")
    
    def main_menu(self):
        """Main interactive menu"""
        print("\n" + "="*60)
        print("MARIO GOLF 64 COURSE CREATOR")
        print("="*60)
        
        while True:
            print("\nWhat would you like to create?")
            print("1. Custom course (choose each hole)")
            print("2. Random course (9 or 18 holes)")
            print("3. Exit")
            
            choice = input("\nChoice (1-3): ").strip()
            
            if choice == "1":
                new_holes, target_holes = self.create_custom_course()
                
                if new_holes:
                    print(f"\nCourse Summary ({len(new_holes)} holes):")
                    for i, hole_idx in enumerate(new_holes, 1):
                        print(f"  Hole {i:2d}: {self.hole_map[hole_idx]}")
                    
                    confirm = input("\nCreate this course? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.apply_course_changes(new_holes, target_holes)
                        
                        filename = input("\nSave ROM as: ").strip()
                        if filename:
                            self.save_rom(filename)
                            print(f"Custom course created! Load '{filename}' in your emulator.")
                        break
                    else:
                        print("Course creation cancelled.")
                else:
                    print("No holes selected.")
            
            elif choice == "2":
                new_holes, target_holes = self.create_random_course()
                
                confirm = input(f"\nCreate this random {len(new_holes)}-hole course? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.apply_course_changes(new_holes, target_holes)
                    
                    filename = input("\nSave ROM as: ").strip()
                    if filename:
                        self.save_rom(filename)
                        print(f"Random course created! Load '{filename}' in your emulator.")
                    break
                else:
                    print("Random course cancelled.")
            
            elif choice == "3":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")

# Main execution
if __name__ == "__main__":
    print("Mario Golf 64 Interactive Course Creator")
    print("=" * 50)
    
    rom_path = input("Enter ROM path (or press Enter for 'baserom.z64'): ").strip()
    if not rom_path:
        rom_path = "baserom.z64"
    
    creator = MarioGolf64InteractiveCourseCreator(rom_path)
    
    if creator.rom_data:
        creator.main_menu()
    else:
        print("Failed to load ROM. Please check the file path.")