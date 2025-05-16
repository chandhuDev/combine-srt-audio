import os
import re
import shutil

def parse_srt(srt_filepath):
    """Parses an SRT file and returns a list of timeline entries."""
    entries = []
    with open(srt_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_entries = re.split(r'\n\s*\n', content.strip())

    for entry_text in raw_entries:
        lines = entry_text.strip().split('\n')
        if len(lines) >= 3:
            sequence = int(lines[0])
            time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', lines[1])
            if time_match:
                start_time = time_match.group(1)
                end_time = time_match.group(2)
                subtitle_text = '\n'.join(lines[2:]) 
                entries.append({
                    'sequence': sequence,
                    'start_time': start_time,
                    'end_time': end_time,
                    'text': subtitle_text
                })
    return entries

def create_sequence_folders(srt_filepath, audio_folder_path, output_folder):
    """
    Creates a folder structure where each subtitle sequence gets its own folder
    containing both the individual subtitle file and the corresponding audio file.
    
    Folder structure:
    output/[sequence_number]/[sequence_number].srt
    output/[sequence_number]/[sequence_number].mp3
    """
    srt_entries = parse_srt(srt_filepath)
    
    os.makedirs(output_folder, exist_ok=True)
    
    processed_count = 0
    missing_audio_count = 0
    
    for entry in srt_entries:
        sequence = entry['sequence']
        
        sequence_folder = os.path.join(output_folder, str(sequence))
        os.makedirs(sequence_folder, exist_ok=True)
        
        srt_output_path = os.path.join(sequence_folder, f"{sequence}.srt")
        with open(srt_output_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(f"{sequence}\n")
            srt_file.write(f"{entry['start_time']} --> {entry['end_time']}\n")
            srt_file.write(f"{entry['text']}\n")
        
        audio_filename = f"{sequence}.mp3"
        audio_filepath = os.path.join(audio_folder_path, audio_filename)
        
        if os.path.exists(audio_filepath):
            audio_output_path = os.path.join(sequence_folder, audio_filename)
            shutil.copy2(audio_filepath, audio_output_path)
            processed_count += 1
        else:
            print(f"Warning: Audio file for sequence {sequence} not found at {audio_filepath}")
            missing_audio_count += 1
    
    print(f"Processing complete!")
    print(f"Total sequences processed: {len(srt_entries)}")
    print(f"Sequences with audio: {processed_count}")
    print(f"Sequences missing audio: {missing_audio_count}")
    print(f"Output folder: {output_folder}")

if __name__ == "__main__":
    srt_file = "/Users/kishorekumaravulakonda/Downloads/es.srt"
    audio_folder = "/Users/kishorekumaravulakonda/Downloads/es"
    output_folder = "/Users/kishorekumaravulakonda/Downloads/output"

    create_sequence_folders(srt_file, audio_folder, output_folder)
