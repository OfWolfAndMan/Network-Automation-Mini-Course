from EVE_NG.test_provisioning import test_login, test_delete_lab
import sys

ProjectName = "{}".format("%20".join(sys.argv[1].split()))

cookies = test_login()
test_delete_lab(cookies, ProjectName)
