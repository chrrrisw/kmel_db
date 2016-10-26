"""Python's unittest main entry point, extended to include coverage"""

import sys
try:
    import coverage
    HAVE_COVERAGE = True
except ImportError:
    HAVE_COVERAGE = False

if sys.argv[0].endswith("__main__.py"):
    import os.path
    # We change sys.argv[0] to make help message more useful
    # use executable without path, unquoted
    # (it's just a hint anyway)
    # (if you have spaces in your executable you get what you deserve!)
    executable = os.path.basename(sys.executable)
    sys.argv[0] = executable + " -m unittest"
    del os

__unittest = True

from unittest.main import main

if HAVE_COVERAGE:
    html_dir = 'test_coverage'
    cov = coverage.Coverage(branch=True)
    cov._warn_no_data = False
    cov.exclude(r'\@abc\.abstract', 'partial')
    cov.start()

try:
    main(module=None, exit=False)
except:
    raise
finally:
    if HAVE_COVERAGE:
        cov.stop()
        cov.save()
        cov.html_report(
            directory=html_dir,
            title='DapGen test coverage')
