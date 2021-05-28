
# run setup
./dockertools/setup.sh

# run tests
python3 /autopi/tests/automated_tests/run_tests.py

# run CMD
if [ $# -ne 0 ]; then
	bash -c "$@"
fi
