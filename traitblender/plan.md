# TraitBlender Roadmap

This file is the current working plan for the repo.

## Next Priorities

- Update the documentation so it reflects the current workflow and UI.
- Restore the platform-specific extension zip builds for:
  - Windows
  - macOS
  - Linux
- Move the project structure and release workflow back into the main Imageomics repository.

## Documentation

- Review the existing docs for anything that is now outdated.
- Update the getting-started pages so they match the current extension layout and workflow.
- Refresh any references to:
  - old packaging paths
  - old build steps
  - old panel names
  - old simulation / imaging wording
- Make sure the docs describe the current user flow clearly:
  - choose morphospace
  - optionally edit dataset
  - simulate dataset
  - export meshes if enabled

## Zip Builds

- Re-enable the build process for separate platform zips.
- Keep the build outputs platform-specific:
  - Windows zip
  - macOS zip
  - Linux zip
- Make sure each zip includes the correct wheels for that platform.
- Make sure the manifest generated in each build points at the correct wheel set.
- Verify the build still works from the repo layout that is currently in use.
- Add or restore any CI steps needed to produce the zips automatically again.

## Main Imageomics Repo Move

- Move the current TraitBlender state into the main Imageomics repository.
- Make sure the folder layout in the main repo matches the current working structure.
- Bring over any docs and build automation needed for the move.
- Confirm that the extension still loads correctly after the move.
- Confirm that the platform zips are still buildable after the move.

## Suggested Order

1. Clean up and update documentation.
2. Restore the multi-platform zip build workflow.
3. Move the project into the main Imageomics repo.
4. Test the final result on at least Windows and one non-Windows platform.
