# Learning workshop site

## Structure

The `docs` subdirectory is where the live version of the site lives.
The `raw` subdirectory is where you put the output of the Notion HTML export.
`build.py` converts the Notion export in `raw` to the cleaned-up site in `docs`.
`style.css` is a stylesheet that will be injected into every page.


## Updating the site with new content

To use it:
1. Export the root note from Notion as HTML. Include content "everything",
    include subpages, but do not create folders for subpages.
2. Unzip all the files from the Notion import into the `raw` subdirectory of
    this repo.
3. If you have added or renamed notes in the Notion, modify `HTML_PREFIX_MAPPING`
    in `build.py`: add a mapping from the start of the name of the new note
    to some unique name you'd like to have show up in a URL.
4. `python build.py`.
5. Commit the changes, push to GitHub, and make sure they show up on the site.
