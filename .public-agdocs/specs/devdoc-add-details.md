### Main Task

Update docs/dev-docs/dev-summary-v2.md with contents for the Commit Message, Spec, and Patch. (replacing the existing "TBD" contents in the place.)

Use docs/dev-docs/v2.md as an example of how this should look.

Spec and Patch are inside the details tag for each item.

Wrap the contents of the spec and patch with <pre></pre> tags and leave a blank line between the h3 and pre tag for rendering.

### Spec contents
Add the contents from .public-agdocs/specs/<spec-name> where spec-name is listed under the "Spec" bullet.

If you can't find this, a match for the file, add "Spec file not found".

If the contents are > 100 lines long, truncate this at 100 lines.

### Patch + Commit Message contents
Generate the patch / code diff from the commit listed under "Patch Sha"

Use commands to generate this via "git show <patch-sha>".

This will produce a commit message, which you should add to the bullet point, and a full code diff which should be placed in pre tag inside the details tag for the item.

