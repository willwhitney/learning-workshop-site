"""
This is a pretty hacky script that cleans up the output of Notion's HTML export
to make it into a better web page. It has a couple of goals:

1. Rename all the other HTML pages to something more reasonable, while also
    updating all references to those pages so that links still works.
2. Modify each page to inject a stylesheet with additional styling.

To use this:
1. Export the root note from Notion as HTML. Include content "everything",
    include subpages, but do not create folders for subpages.
2. Unzip all the files from the Notion import into the `raw` subdirectory of
    this repo.
3. If you have added or renamed notes in the Notion, modify HTML_PREFIX_MAPPING:
    add the start of the new note name mapping to some unique name you'd like to
    have show up in a URL.
4. `python build.py`.
5. Commit the changes, push to GitHub, and make sure they show up on the site.
"""

import glob
import os
import shutil
import urllib.parse


LANDING_PAGE_PREFIX = 'The Learning Workshop'
RAW_EXPORT_DIR = 'raw'
OUTPUT_DIR = 'docs'
STYLESHEET_FILE = 'style.css'

HTML_PREFIX_MAPPING = {
    'The Learning Workshop': 'index',
    'March 2020': '2020',
    'March 2022': '2022',
}


def move_by_prefix(html_filename_prefix, output_filename):
    candidate_paths = glob.glob(f'{RAW_EXPORT_DIR}/{html_filename_prefix}*.html')
    if len(candidate_paths) > 1:
        raise ValueError((
            f"Multiple pages that start with the name '{html_filename_prefix}'. "
            f"Either rename the ones that shouldn't be `{output_filename}.html` "
            "or modify the build script."
        ))
    elif len(candidate_paths) == 0:
        raise ValueError((
            f"No pages start with the name '{html_filename_prefix}'. "
            f"Either rename whichever one should be `{output_filename}.html` to "
            "start with that string or modify the build script."
        ))
    old_path = candidate_paths[0]
    new_path = f'{OUTPUT_DIR}/{output_filename}.html'
    os.rename(old_path, new_path)

    old_name = old_path.split('/')[-1]
    new_name = f'{output_filename}.html'
    return {old_name: new_name}


def move_all_files():
    # Move all the HTML files. Should have specified names to avoid ugly URLs.
    html_rename_mapping = {}
    for old_prefix, new_name in HTML_PREFIX_MAPPING.items():
        single_rename_mapping = move_by_prefix(old_prefix, new_name)
        html_rename_mapping.update(single_rename_mapping)

    # Move all the other files.
    for path in glob.glob(f'{RAW_EXPORT_DIR}/*'):
        file_name = path.split('/')[-1]
        if path.endswith('.html'):
            continue
        os.rename(path, f'{OUTPUT_DIR}/{file_name}')

    unmoved_html_files = glob.glob(f'{RAW_EXPORT_DIR}/*.html')
    if len(unmoved_html_files) > 0:
        raise ValueError((
            "Failed to move the following HTML files. Edit HTML_PREFIX_MAPPING "
            "in build.py to give nice URLs to any new files.\n"
        ) + '\n'.join(unmoved_html_files))
    return html_rename_mapping


def replace_string_inplace(path, old_str, new_str):
    with open(path, "r") as input_file:
        newText = input_file.read().replace(old_str, new_str)

    with open(path, "w") as output_file:
        output_file.write(newText)


def update_references(html_rename_mapping):
    for old_name, new_name in html_rename_mapping.items():
        escaped_old_name = urllib.parse.quote(old_name, safe='/,')
        escaped_new_name = urllib.parse.quote(new_name, safe='/,')
        print(f"Renaming '{escaped_old_name}' to '{escaped_new_name}'.")
        for html_file in glob.glob(f'{OUTPUT_DIR}/*.html'):
            replace_string_inplace(html_file, escaped_old_name, escaped_new_name)


def inject_stylesheet():
    shutil.copy(STYLESHEET_FILE, f'{OUTPUT_DIR}/{STYLESHEET_FILE}')
    stylesheet_html = f'<link rel="stylesheet" type="text/css" href="{STYLESHEET_FILE}">'
    for html_file in glob.glob(f'{OUTPUT_DIR}/*.html'):
        replace_string_inplace(html_file, '</head>', f'{stylesheet_html}</head>')


if __name__ == '__main__':
    html_rename_mapping = move_all_files()
    update_references(html_rename_mapping)
    inject_stylesheet()
