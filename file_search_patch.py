"""
Simplified patch for File_Search_v9.2.2_Beta.py to enable .doc file search 
and fix odfdo library issues - without pkg_resources dependency
"""
import os
import sys
import importlib
import subprocess

def check_library(library_name):
    """Check if a library is installed"""
    try:
        importlib.import_module(library_name)
        return True
    except ImportError:
        return False

def main():
    # Check required libraries
    print("Checking required libraries...")
    missing_libs = []
    
    # Check odfdo
    odfdo_installed = check_library("odfdo")
    if not odfdo_installed:
        missing_libs.append("odfdo")
    else:
        print("✓ odfdo is installed")
    
    # Check pywin32 (needed for .doc files)
    pywin32_installed = check_library("win32com.client")
    if not pywin32_installed:
        missing_libs.append("pywin32")
    else:
        print("✓ pywin32 is installed")
    
    # Install missing libraries
    if missing_libs:
        print(f"Missing libraries: {', '.join(missing_libs)}")
        try:
            for lib in missing_libs:
                print(f"Installing {lib}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                print(f"✓ {lib} installed successfully")
        except Exception as e:
            print(f"Error installing libraries: {str(e)}")
            print("Please install the missing libraries manually with:")
            for lib in missing_libs:
                print(f"pip install {lib}")
            return
    
    # Path to the original file
    original_file = "File_Search_v9.2.2_Beta.py"
    if not os.path.exists(original_file):
        print(f"Error: {original_file} not found in the current directory")
        return
    
    # Create backup
    backup_file = "File_Search_v9.2.2_Beta.py.bak"
    if not os.path.exists(backup_file):
        print(f"Creating backup at {backup_file}...")
        with open(original_file, 'r', encoding='utf-8') as f_in:
            with open(backup_file, 'w', encoding='utf-8') as f_out:
                f_out.write(f_in.read())
    
    print("Patching file to enable .doc search...")
    with open(original_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the block that prevents .doc files from being searched
    if "# Blocca specificamente i file .doc per evitare blocchi" in content:
        content = content.replace(
            "# Blocca specificamente i file .doc per evitare blocchi\n"
            "        if ext == '.doc':\n"
            "            self.log_debug(f\"File .doc temporaneamente escluso dall'analisi: {file_path}\")\n"
            "            return False",
            "# .doc files are now enabled for search\n"
            "        if ext == '.doc' and file_format_support[\"doc\"]:\n"
            "            self.log_debug(f\"Analisi abilitata per file .doc: {file_path}\")\n"
            "            return True\n"
            "        elif ext == '.doc' and not file_format_support[\"doc\"]:\n"
            "            self.log_debug(f\"File .doc non può essere analizzato: libreria win32com mancante\")\n"
            "            return False"
        )
        print("✓ Successfully removed .doc file analysis block")
    else:
        print("Warning: Couldn't find .doc blocking code. Is this the correct version?")
    
    # Fix odfdo import handling if needed
    if check_library("odfdo"):
        # No need to modify the import statement as it's already at the top level,
        # but we can add a specific debug line
        if "import odfdo" in content:
            content = content.replace(
                "import odfdo",
                "import odfdo  # Verified as installed by patch"
            )
            print("✓ odfdo import verified")
    
    # Write the modified content back
    with open(original_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\nPatch completed successfully!")
    print("You can now run the application with improved .doc file support.")
    print("Note: Searching .doc files may still be slow due to the COM interface.")

if __name__ == "__main__":
    main()