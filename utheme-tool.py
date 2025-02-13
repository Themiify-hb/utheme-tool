is_running = True

theme_name = input("Please enter your theme's name: ")
theme_author = input("Please enter the name of the theme author: ")
theme_id = input("Please enter a theme ID for your theme (keep it clear for users so they can know what they're installing): ")
theme_region = input("Please enter your theme's region (Options: UNIVERAL, JPN, USA, EUR). If you have region specific text patches, you must set your theme's region to the region of the text patches (Defualts to UNIVERSAL): ")
if theme_region not in ('UNIVERSAL', 'JPN', 'USA', 'EUR'):
    theme_region = 'UNIVERSAL' # default just cuz

bps_files = []
og_files = []
menu_paths = []

while is_running == True:
    bps_path = input("Please enter the path to your bps file (e.g. /path/to/Men.bps). When you're done entering all your theme's bps files, just enter nothing to continue: ")
    if bps_path != '':
        og_path = input("Please input the path to your original file (e.g. /path/to/Men.pack): ")
        menu_path = input("Please input where this file should be installed to relative to /content (e.g. input: Common/Package/Men.pack): ")

        bps_files.append(bps_path)
        og_files.append(og_path)
        menu_paths.append(menu_path)
    else:
        is_running = False

print(theme_name, theme_author, theme_id, theme_region, bps_files, og_files, menu_paths)