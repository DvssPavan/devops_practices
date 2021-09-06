# Memphis Bamboo Build Plans 1.0
# Author: ShubhamS
"""This module is responsible for triggering bamboo build plans for driver/adapter.

This triggers the bamboo build plan.

  Typical usage example:
  $ python BambooBuildPlans.py
  And follow the on-screen instructions.
"""
import json
import os
import time
from json import load

import requests
import getpass
import base64
import xml.etree.cElementTree as et
import webbrowser

from atlassian import Bamboo


class BambooBuildPlans:

    def __init__(self, input_args: dict):
        self.input_args = input_args
        self.project = input_args['inBambooConfigs']['inProjectKey']
        self.driver_label = input_args['inBambooConfigs']['inDriverLabel']
        self.core_label = input_args['inBambooConfigs']['inCoreLabel']
        self.sen_label = input_args['inBambooConfigs']['inSENLabel']
        self.driver_brand = input_args['inBambooConfigs']['inDriverBrand']
        self.windows_build_configs = input_args['inBambooConfigs']['inBuildConfigs']['Windows']['inPlatform'] + " " + \
                                     input_args['inBambooConfigs']['inBuildConfigs']['Windows']['inCompiler'] + " " + \
                                     input_args['inBambooConfigs']['inBuildConfigs']['Windows']['inConfiguration']
        self.linux_build_configs = input_args['inBambooConfigs']['inBuildConfigs']['Linux']['inPlatform'] + " " + \
                                   input_args['inBambooConfigs']['inBuildConfigs']['Linux']['inCompiler'] + " " + \
                                   input_args['inBambooConfigs']['inBuildConfigs']['Linux']['inConfiguration']
        self.osx_build_configs = input_args['inBambooConfigs']['inBuildConfigs']['OSX']['inPlatform'] + " " + \
                                 input_args['inBambooConfigs']['inBuildConfigs']['OSX']['inCompiler'] + " " + \
                                 input_args['inBambooConfigs']['inBuildConfigs']['OSX']['inConfiguration']
        self.branch_name = input_args['inBambooConfigs']['inBranchName']

    def build(self):
        # Ask user to login with Bigsight credentials and trigger the build plan
        atlassian_user = input("Enter user name :")
        atlassian_password = input("Enter password: ")

        user_pass = atlassian_user + ':' + atlassian_password
        base_64_val = base64.b64encode(user_pass.encode()).decode()
        bamboo_url = os.environ.get("http://bergamot3.lakes.ad:8085", "http://bergamot3.lakes.ad:8085")

        # Creates the bamboo object with user credentials for sending http requests
        bamboo = Bamboo(url=bamboo_url, username=atlassian_user, password=atlassian_password)
        url = self.get_project_url(base_64_val)
        if not url == None:
            if len(self.windows_build_configs) > 2:
                branch_info = bamboo.get_branch_info(self.get_plan_key(url, base_64_val, self.windows_build_configs),
                                                 self.branch_name)
                print(branch_info)
                branch_key = branch_info['key']
                print(branch_key)
                bamboo.execute_build(branch_key, **self.get_params())
                print('Bamboo build is started for ' + self.branch_name.split(' ')[0] + ' adapter in windows platform')
                self.open_browser_and_check_status(branch_info, branch_key, base_64_val)
                return True
            if len(self.linux_build_configs) > 2:
                branch_info = bamboo.get_branch_info(self.get_plan_key(url, base_64_val, self.linux_build_configs),
                                                 self.branch_name)
                branch_key = branch_info['key']
                bamboo.execute_build(branch_key, **self.get_params())
                print('Bamboo build is started for ' + self.branch_name.split(' ')[0] + ' adapter in linux platform')
                self.open_browser_and_check_status(branch_info, branch_key, base_64_val)
                return True
            if len(self.osx_build_configs) > 2:
                branch_info = bamboo.get_branch_info(self.get_plan_key(url, base_64_val, self.osx_build_configs),
                                                 self.branch_name)
                branch_key = branch_info['key']
                bamboo.execute_build(branch_key, **self.get_params())
                print('Bamboo build is started for ' + self.branch_name.split(' ')[0] + ' adapter in osx platform')
                self.open_browser_and_check_status(branch_info, branch_key, base_64_val)
                return True
        else:
            print(self.project + ' project not found. Please verify the project key.')
            return False

    def get_plan_key(self, url, base_64_user_pass, build_configs):
        url += '?expand=plans'
        payload = ""
        headers = {
            'Authorization': "Basic " + base_64_user_pass,
            'Accept': "application/json"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        tree = response.json()      # response format make as a json

        found_proj = False
        start_index, max_results, size = 0, int(tree['plans']['max-result']), int(tree['plans']['size'])

        # traverse all the plan for the project using pagination
        while start_index <= size:
            if 'plans' in tree and tree['plans'] is not None and tree['plans']['size'] > 0:
                for plan in tree['plans']['plan']:
                    if plan['shortName'] == build_configs:
                        found_proj = True
                        break
                if found_proj:
                    return plan['key']       # return key value of the plan
                else:
                    start_index = int(tree['plans']['start-index'])
                    start_index = start_index + max_results          # set start_index for the next page

            # update the url for new start-index
            response = requests.request("GET", f"{url}&start-index={start_index}", data=payload, headers=headers)
            tree = response.json()



    def get_project_url(self, base_64_user_pass):
        url = "http://bergamot3.lakes.ad:8085/rest/api/latest/project/"
        url += self.project       # append the project key behind the url
        payload = ""
        headers = {
            'Authorization': "Basic " + base_64_user_pass,
        }

        # checking the request is valid or not
        response = requests.request("GET", url, data=payload, headers=headers)
        if(response.status_code != 200):
            url = None
        return url

    def get_params(self):
        params = {
            "BOOSTER_LABEL": "__head__",
            "DRV_LABEL": self.driver_label,
            "CORE_LABEL": self.core_label,
            "SEN_LABEL": self.sen_label,
            "DYNAMIC_LINKING": 0,
            "RETAIL": 0,
            "PRODUCT_LABEL": "BAMBOO_DRV_LABEL",
            "DISBALE_PARENT_MATCH": 0,
            "TARGET": "release",
            "MEMORY_TEST": 0,
            "AFL": 0,
            "VERACODE": 0,
            "CODE_ANALYSIS": 0,
            "DRV_BRAND": self.driver_brand
        }
        return params

    def open_browser_and_check_status(self, branch_info, branch_key, base_64_val):
        if 'latestResult' not in branch_info:
            firstBuildPlan = 'http://bergamot3.lakes.ad:8085/rest/api/latest/result/' + branch_key + '-0'
            self.open_browser(firstBuildPlan)
            self.check_plan_status(firstBuildPlan.split("/")[-1], base_64_val)
        else:
            self.open_browser(branch_info['latestResult']['link']['href'])
            self.check_plan_status(branch_info['latestResult']['link']['href'].split("/")[-1],
                                   base_64_val)

    def open_browser(self, url: str):
        job_id = url.split("-")[-1]
        url = url[0: len(url) - len(job_id)] + str(int(job_id) + 1)
        url = url.replace('rest/api/latest/result', 'browse')
        webbrowser.open(url, new=2)

    def check_plan_status(self, build_key, base_64_user_pass):
        url = "http://bergamot3.lakes.ad:8085/rest/api/latest/result/" + build_key
        job_id = url.split("-")[-1]
        url = url[0: len(url) - len(job_id)] + str(int(job_id) + 1)
        payload = ""
        headers = {
            'Authorization': "Basic " + base_64_user_pass
        }
        signingPlanCodes = ['SGINOMEM', 'SOMID', 'SGPOOMEM']
        if build_key.split("-")[0] in signingPlanCodes:
            print("Code signing plan has started and it's in progress")
        else:
            print("OEM plan has started and it's in progress")
        status = ""
        while True:
            response = requests.request("GET", url, data=payload, headers=headers)
            root = et.fromstring(response.content)
            for buildState in root.iter('buildState'):
                status = buildState.text
            if status != "Unknown":
                break
            time.sleep(60)
        print("Bamboo Plan Execution Finished with result: "+ status)


def run_bamboo_adapter_build(input_args: dict):
    print("Building driver/adapter on bamboo...BEGIN")
    bamboo_build = BambooBuildPlans(input_args)
    # run_build_driver_as_server(input_args)
    if bamboo_build.build():
        print("Please go through the logs generated on bamboo for further reference.")
    else:
        print("Please check the input parameters and try again.")


def main():
    input_json_file = 'user_input.json'
    if not os.path.exists(input_json_file):
        print("IMPORTANT: Please ensure to modify user_input.json as per your "
              "needs prior to running this.")
        input_json_file = input("Please enter the full path to the input json "
                                "file (e.g., C:\\user_input.json): ")
    f = open(input_json_file)
    run_bamboo_adapter_build(load(f))


if __name__ == '__main__':
    main()
