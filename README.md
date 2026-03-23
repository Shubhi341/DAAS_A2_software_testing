PART-1 (whitebox testing)
Step 1:
Enter into whitebox
Then run:
PYTHONPATH=moneypoly pytest tests/

PART-2 (Integration testing)
run:
pytest integration/tests/test_integration.py (from
2024101038)

PART - 3 (blackbox testing)
Prerequisites:
– QuickCart API running at http://localhost:8080
– Python and pytest installed

For Running all tests:
python3 -m pytest blackbox/tests/ -v

For Running single file:
python3 -m pytest blackbox/tests/test_additional.py -v

For Running single test:python3 -m pytest
blackbox/tests/test_additional.py::test_add_and_get_cart_item -q -s

I am usually running my file mostly as :
Step 1.
Run:
sudo docker run -p 8080:8080 quickcart
Step 2.
python3 -m pytest blackbox/tests/ -v

my Github link:
https://github.com/Shubhi341/DAAS_A2_software_testing

