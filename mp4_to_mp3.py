#!/usr/bin/env python3
"""
MP4 to MP3 Converter
Compatible with: macOS Tahoe 26.5, Apple M4 Pro, Python 3.13.5
Usage: python mp4_to_mp3.py <input.mp4> [output.mp3]
       python mp4_to_mp3.py --batch <folder_path>
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
from tqdm import tqdm


class MP4toMP3Converter:
    """A lightweight converter using ffmpeg with quality presets for music."""

    # Bitrate presets (kbps) — 'music' optimized for iTunes/Apple Music
    PRESETS = {
        'standard': '192k',   # Good balance
        'music': '256k',      # Recommended for music libraries
        'archive': '320k',    # Maximum quality
        'voice': '128k'       # Podcasts / spoken word
    }

    def __init__(self, bitrate_preset: str = 'music'):
        self.bitrate = self.PRESETS.get(bitrate_preset, '256k')
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> None:
        """Verify ffmpeg is installed and accessible."""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                check=True
            )
            version_line = result.stdout.split('\n')[0]
            print(f"✓ Found: {version_line}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ Error: ffmpeg not found.")
            print("  Install it: brew install ffmpeg")
            sys.exit(1)

    def convert(self, input_path: str, output_path: str | None = None) -> str:
        """
        Convert a single MP4 file to MP3.

        Args:
            input_path: Path to the .mp4 file
            output_path: Optional destination path (defaults to same name, .mp3)

        Returns:
            Path to the generated .mp3 file
        """
        input_file = Path(input_path).resolve()

        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if input_file.suffix.lower() not in {'.mp4', '.m4a', '.m4v', '.mov'}:
            print(
                f"⚠ Warning: Unexpected extension '{input_file.suffix}'. Attempting anyway.")

        # Default output: same directory, same name, .mp3 extension
        if output_path is None:
            output_file = input_file.with_suffix('.mp3')
        else:
            output_file = Path(output_path).resolve()
            # If output is a directory, place file inside it
            if output_file.is_dir():
                output_file = output_file / input_file.with_suffix('.mp3').name

        # ffmpeg command optimized for music extraction
        # -vn: no video
        # -ar 44100: standard CD sample rate (iTunes compatible)
        # -ac 2: stereo
        # -q:a 0: highest VBR quality (or use -b:a for CBR)
        cmd = [
            'ffmpeg',
            '-i', str(input_file),           # Input
            '-vn',                           # No video
            '-ar', '44100',                  # Sample rate
            '-ac', '2',                      # Stereo channels
            '-b:a', self.bitrate,            # Audio bitrate
            '-map_metadata', '0',            # Preserve metadata
            '-id3v2_version', '3',           # iTunes-friendly ID3 tags
            '-y',                            # Overwrite if exists
            str(output_file)
        ]

        print(f"\n🎵 Converting: {input_file.name}")
        print(f"   → Output:   {output_file}")
        print(f"   → Bitrate:  {self.bitrate}")

        # Run conversion with progress indication
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise RuntimeError(f"ffmpeg failed:\n{stderr}")

            # Verify output
            if output_file.exists():
                size_mb = output_file.stat().st_size / (1024 * 1024)
                print(f"✓ Success! ({size_mb:.1f} MB)")
                return str(output_file)
            else:
                raise RuntimeError("Output file was not created.")

        except KeyboardInterrupt:
            print("\n⚠ Conversion cancelled by user.")
            # Clean up partial file
            if output_file.exists():
                output_file.unlink()
            sys.exit(0)

    def batch_convert(self, folder_path: str, recursive: bool = False) -> list[str]:
        """
        Convert all MP4 files in a directory.

        Args:
            folder_path: Directory containing .mp4 files
            recursive: Whether to search subdirectories

        Returns:
            List of paths to generated .mp3 files
        """
        folder = Path(folder_path).resolve()

        if not folder.is_dir():
            raise NotADirectoryError(f"Not a directory: {folder_path}")

        # Find all MP4 files
        pattern = '**/*.mp4' if recursive else '*.mp4'
        mp4_files = list(folder.glob(pattern))

        if not mp4_files:
            print(f"No .mp4 files found in: {folder}")
            return []

        print(f"\n📁 Batch mode: {len(mp4_files)} file(s) found")
        print(f"   Directory: {folder}")
        print("-" * 50)

        results = []
        for mp4_file in tqdm(mp4_files, desc="Converting", unit="file"):
            try:
                output = self.convert(str(mp4_file))
                results.append(output)
            except Exception as e:
                print(f"✗ Failed: {mp4_file.name} — {e}")
                continue

        print(f"\n{'=' * 50}")
        print(
            f"Complete: {len(results)}/{len(mp4_files)} files converted successfully")
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Convert MP4 video files to MP3 audio for iTunes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mp4_to_mp3.py song.mp4                    # → song.mp3
  python mp4_to_mp3.py concert.mp4 ~/Music/        # → ~/Music/concert.mp3
  python mp4_to_mp3.py --batch ~/Downloads/rips/   # Convert all MP4s in folder
  python mp4_to_mp3.py --batch ~/Music/ --recursive # Include subfolders
  python mp4_to_mp3.py --preset archive symphony.mp4 # 320kbps quality
        """
    )

    parser.add_argument(
        'input', help='Input .mp4 file or folder (with --batch)')
    parser.add_argument('output', nargs='?',
                        help='Output .mp3 path or directory (optional)')

    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='Batch mode: convert all MP4 files in the specified directory'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='When using --batch, include subdirectories'
    )
    parser.add_argument(
        '--preset', '-p',
        choices=['standard', 'music', 'archive', 'voice'],
        default='music',
        help='Audio quality preset (default: music = 256kbps)'
    )

    args = parser.parse_args()

    # Initialize converter
    converter = MP4toMP3Converter(bitrate_preset=args.preset)

    try:
        if args.batch:
            # Batch mode: input is a folder
            results = converter.batch_convert(
                args.input, recursive=args.recursive)
            if not results:
                sys.exit(1)
        else:
            # Single file mode
            output = converter.convert(args.input, args.output)

            # iTunes tip
            print(f"\n💡 iTunes tip: File → Add to Library (or drag into Music app)")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
