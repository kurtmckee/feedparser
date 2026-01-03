Project development
-------------------

*   Rename the ``develop`` branch to ``main``,
    and rename the ``master`` branch to ``releases``.

    To update local branches, run these commands
    (assuming that the upstream repository is named "origin"):

    ..  code-block:: bash

        # Update local repo knowledge of the upstream repo.
        git fetch origin

        # Rename and re-home the "develop" branch.
        git branch -m develop main
        git branch -u origin/main main

        # Rename and re-home the "master" branch.
        git branch -m master releases
        git branch -u origin/releases releases

        # Auto-detect the local repo's HEAD branch.
        git remote set-head origin -a
