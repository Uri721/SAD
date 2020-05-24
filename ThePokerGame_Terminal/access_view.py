
from system_tool import client_id_cmd as client_id


class Access_View(object):

    def execute(self):

        print("ACCESS VIEW")
        print("Username: ")
        nom = input()
        print("Password: ")
        contra = input()

        data = [nom, contra]

        return data
