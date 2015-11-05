add_executable(ranker ranker.c)
add_library(hashtable hashtable.c)
target_link_libraries(ranker hashtable)

# I think this makes it so the installer will also want to install
# needed system libraries
include (InstallRequiredSystemLibraries)
# Allows generating installers (!)
include (CPack)
