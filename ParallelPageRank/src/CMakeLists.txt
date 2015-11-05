add_executable(ranker ranker.c)

# I think this makes it so the installer will also want to install
# needed system libraries
include (InstallRequiredSystemLibraries)
# Allows generating installers (!)
include (CPack)
